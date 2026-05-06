# surge_mlflow/scripts/runpipeline.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
from datetime import datetime

# Import existing modules from src
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.load import load_data
from data.preprocess import preprocess_data
from models.train import train_model
from models.evaluate import evaluate_model
from utils.validate_data import validate_data

def main():
    """
    Main pipeline execution function that orchestrates the ML workflow
    using existing modular code from the src directory.
    """
    # Set up MLflow experiment
    mlflow.set_experiment("surge_prediction")

    with mlflow.start_run(run_name=f"surge_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        try:
            # Log pipeline parameters
            mlflow.log_param("pipeline_version", "1.0")
            mlflow.log_param("execution_time", datetime.now().isoformat())

            # 1. Load data
            print("=== Loading Data ===")
            # Try to load from database using environment variables (matches existing load_data function)
            df = load_data()  # Uses default parameters from load_data function
            mlflow.log_param("data_source", "database")
            mlflow.log_param("num_samples", len(df))
            mlflow.log_param("num_features", len(df.columns))

            # 2. Validate data
            print("\n=== Validating Data ===")
            # Note: validate_data function expects lowercase condition values
            # and specific column names. We'll need to prepare data accordingly
            validation_passed = validate_data(df)
            if not validation_passed:
                raise ValueError("Data validation failed. Pipeline aborted.")

            # 3. Preprocess data
            print("\n=== Preprocessing Data ===")
            # Note: preprocess_data function expects 'weather_condition' column
            # but our data has 'condition' column. We'll rename it temporarily
            df_for_preprocessing = df.copy()
            if 'condition' in df_for_preprocessing.columns and 'weather_condition' not in df_for_preprocessing.columns:
                df_for_preprocessing = df_for_preprocessing.rename(columns={'condition': 'weather_condition'})

            # Also need to handle case sensitivity for condition values
            # Convert to lowercase for validation compatibility
            if 'weather_condition' in df_for_preprocessing.columns:
                df_for_preprocessing['weather_condition'] = df_for_preprocessing['weather_condition'].str.lower()

            # Preprocess the data
            processed_df = preprocess_data(df_for_preprocessing)

            # Select only the features we want to use for modeling
            # Based on the problem statement: features are temperature, condition, timestamp
            # After preprocessing: temperature remains, condition becomes one-hot encoded,
            # timestamp becomes cyclical features (hour_sin, hour_cos, day_sin, day_cos, month_sin, month_cos)

            # Identify feature columns to keep
            feature_cols = []

            # Always keep temperature
            if 'temperature' in processed_df.columns:
                feature_cols.append('temperature')

            # Keep cyclical timestamp features (these are created by preprocess_data)
            timestamp_features = [col for col in processed_df.columns if any(x in col for x in ['_sin', '_cos']) and
                                any(t in col for t in ['hour', 'day', 'month'])]
            feature_cols.extend(timestamp_features)

            # Keep one-hot encoded condition columns
            condition_features = [col for col in processed_df.columns if col.startswith('weather_condition_')]
            feature_cols.extend(condition_features)

            # Create feature dataframe and target series
            if not feature_cols:
                raise ValueError("No feature columns identified after preprocessing")

            X = processed_df[feature_cols]
            y = processed_df['surge']

            mlflow.log_param("selected_features", feature_cols)
            mlflow.log_param("selected_num_features", len(feature_cols))
            mlflow.log_param("processed_features", list(processed_df.columns))
            mlflow.log_param("processed_num_features", len(processed_df.columns))

            # 4. Train-test split
            print("\n=== Splitting Data ===")
            test_size = 0.2
            random_state = 42
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            mlflow.log_param("test_size", test_size)
            mlflow.log_param("random_state", random_state)
            mlflow.log_param("train_samples", len(X_train))
            mlflow.log_param("test_samples", len(X_test))

            # 5. Model training
            print("\n=== Training Model ===")
            # Use the existing train_model function which handles MLflow logging internally
            # Note: train_model expects target_col as string parameter
            target_col_name = 'surge'

            # We need to pass a dataframe with the target column to train_model
            # Recreate df with processed features for training
            train_df = X_train.copy()
            train_df[target_col_name] = y_train

            model = train_model(train_df, target_col_name)

            # 6. Model evaluation
            print("\n=== Evaluating Model ===")
            metrics, y_pred = evaluate_model(model, X_test, y_test)

            # Log metrics (evaluate_model prints but doesn't return, so we calculate again for logging)
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)

            mlflow.log_metric("mae", mae)
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)

            # 7. Log model
            print("\n=== Logging Model ===")
            mlflow.sklearn.log_model(model, "surge_prediction_model")

            # Log feature importance if available
            if hasattr(model, 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)

                # Log top 10 features as parameters
                top_features = feature_importance.head(10)
                for idx, row in top_features.iterrows():
                    mlflow.log_param(f"top_feature_{idx+1}_{row['feature']}",
                                   float(row['importance']))

                # Save feature importance as artifact
                feature_importance_csv = "feature_importance.csv"
                feature_importance.to_csv(feature_importance_csv, index=False)
                mlflow.log_artifact(feature_importance_csv)
                # Clean up temp file
                if os.path.exists(feature_importance_csv):
                    os.remove(feature_importance_csv)

            print("\n=== Pipeline Completed Successfully ===")
            print(f"MLflow Run ID: {mlflow.active_run().info.run_id}")

        except Exception as e:
            print(f"\n=== Pipeline Failed ===")
            print(f"Error: {e}")
            mlflow.log_param("pipeline_status", "failed")
            mlflow.log_param("error_message", str(e))
            raise

if __name__ == "__main__":
    main()