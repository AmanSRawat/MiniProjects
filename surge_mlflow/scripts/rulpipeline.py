
# surge_mlflow/scripts/runpipeline.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from datetime import datetime

def load_data(csv_path=None):
    """
    Load data from CSV file or database.
    If csv_path is provided, loads from CSV.
    Otherwise, attempts to load from database using environment variables.
    """
    if csv_path and os.path.exists(csv_path):
        print(f"Loading data from CSV: {csv_path}")
        return pd.read_csv(csv_path)

    # Try to load from database using environment variables
    try:
        from sqlalchemy import create_engine
        db_host = os.getenv('DB_HOST', 'localhost')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', 'amanrawat')
        db_name = os.getenv('DB_NAME', 'weatherdata')
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

        engine = create_engine(db_url)
        query = "SELECT * FROM weather"
        print(f"Loading data from database: {db_url}")
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error loading data from database: {e}")
        raise

def validate_data(df):
    """
    Validate the data for expected columns and basic constraints.
    Returns True if validation passes, False otherwise.
    """
    required_columns = ['temperature', 'condition', 'timestamp', 'surge']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"Validation failed: Missing columns: {missing_columns}")
        return False

    # Check for null values in critical columns
    null_counts = df[required_columns].isnull().sum()
    if null_counts.any():
        print(f"Validation failed: Null values found:\n{null_counts[null_counts > 0]}")
        return False

    # Validate surge range
    if df['surge'].min() < 0 or df['surge'].max() > 3.0:
        print(f"Validation failed: Surge values out of expected range [0, 3.0]. "
              f"Min: {df['surge'].min()}, Max: {df['surge'].max()}")
        return False

    # Validate condition values
    valid_conditions = ['sunny', 'rainy', 'cloudy', 'snowy', 'windy']
    invalid_conditions = df[~df['condition'].isin(valid_conditions)]['condition'].unique()
    if len(invalid_conditions) > 0:
        print(f"Validation failed: Invalid condition values found: {invalid_conditions}")
        return False

    print("Data validation passed successfully.")
    return True

def preprocess_data(df):
    """
    Preprocess the data:
    - Convert timestamp to datetime and extract cyclical features
    - One-hot encode categorical features
    - Return processed features and target separately
    """
    # Make a copy to avoid modifying original data
    df_processed = df.copy()

    # Convert timestamp to datetime
    df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp'])

    # Extract hour and apply cyclical encoding (24-hour cycle)
    hour = df_processed['timestamp'].dt.hour
    df_processed['hour_sin'] = np.sin(2 * np.pi * hour / 24)
    df_processed['hour_cos'] = np.cos(2 * np.pi * hour / 24)

    # Extract day of week (0-6, Monday=0) and apply cyclical encoding (7-day cycle)
    day_of_week = df_processed['timestamp'].dt.dayofweek
    df_processed['day_sin'] = np.sin(2 * np.pi * day_of_week / 7)
    df_processed['day_cos'] = np.cos(2 * np.pi * day_of_week / 7)

    # Extract month (1-12) and apply cyclical encoding (12-month cycle)
    month = df_processed['timestamp'].dt.month
    df_processed['month_sin'] = np.sin(2 * np.pi * month / 12)
    df_processed['month_cos'] = np.cos(2 * np.pi * month / 12)

    # Drop original timestamp column
    df_processed.drop(columns=['timestamp'], inplace=True)

    # One-hot encode categorical features
    categorical_cols = ['condition']
    df_processed = pd.get_dummies(df_processed, columns=categorical_cols, drop_first=True)

    # Separate features and target
    target_col = 'surge'
    if target_col not in df_processed.columns:
        raise ValueError(f"Target column '{target_col}' not found in processed data")

    X = df_processed.drop(columns=[target_col])
    y = df_processed[target_col]

    return X, y

def train_model(X_train, y_train, model_type='random_forest', **kwargs):
    """
    Train a regression model.
    Supported model types: 'random_forest', 'xgboost'
    """
    if model_type == 'random_forest':
        model = RandomForestRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            max_depth=kwargs.get('max_depth', 10),
            random_state=kwargs.get('random_state', 42),
            n_jobs=kwargs.get('n_jobs', -1)
        )
    elif model_type == 'xgboost':
        try:
            from xgboost import XGBRegressor
            model = XGBRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                learning_rate=kwargs.get('learning_rate', 0.1),
                max_depth=kwargs.get('max_depth', 5),
                random_state=kwargs.get('random_state', 42),
                n_jobs=kwargs.get('n_jobs', -1)
            )
        except ImportError:
            print("XGBoost not installed. Falling back to RandomForestRegressor.")
            model = RandomForestRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 10),
                random_state=kwargs.get('random_state', 42),
                n_jobs=kwargs.get('n_jobs', -1)
            )
    else:
        raise ValueError(f"Unsupported model type: {model_type}. "
                         "Supported types: 'random_forest', 'xgboost'")

    print(f"Training {model_type} model...")
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model and return metrics.
    """
    print("Evaluating model...")
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "mae": mae,
        "mse": mse,
        "rmse": rmse,
        "r2": r2
    }

    print(f"Evaluation Metrics:")
    print(f"  MAE: {mae:.4f}")
    print(f"  MSE: {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R2:  {r2:.4f}")

    return metrics, y_pred

def main():
    """
    Main pipeline execution function.
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
            # Try to load from CSV first, fallback to database
            csv_path = os.getenv('CSV_PATH', None)
            df = load_data(csv_path=csv_path)
            mlflow.log_param("data_source", "csv" if csv_path else "database")
            mlflow.log_param("num_samples", len(df))
            mlflow.log_param("num_features", len(df.columns))

            # 2. Validate data
            print("\n=== Validating Data ===")
            if not validate_data(df):
                raise ValueError("Data validation failed. Pipeline aborted.")

            # 3. Preprocess data
            print("\n=== Preprocessing Data ===")
            X, y = preprocess_data(df)
            mlflow.log_param("processed_features", list(X.columns))
            mlflow.log_param("processed_num_features", len(X.columns))

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
            model_type = os.getenv('MODEL_TYPE', 'random_forest')
            mlflow.log_param("model_type", model_type)

            # Model hyperparameters
            if model_type == 'random_forest':
                n_estimators = int(os.getenv('RF_N_ESTIMATORS', '100'))
                max_depth = int(os.getenv('RF_MAX_DEPTH', '10'))
                mlflow.log_param("rf_n_estimators", n_estimators)
                mlflow.log_param("rf_max_depth", max_depth)
                model = train_model(
                    X_train, y_train,
                    model_type=model_type,
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    random_state=random_state
                )
            elif model_type == 'xgboost':
                n_estimators = int(os.getenv('XGB_N_ESTIMATORS', '100'))
                learning_rate = float(os.getenv('XGB_LEARNING_RATE', '0.1'))
                max_depth = int(os.getenv('XGB_MAX_DEPTH', '5'))
                mlflow.log_param("xgb_n_estimators", n_estimators)
                mlflow.log_param("xgb_learning_rate", learning_rate)
                mlflow.log_param("xgb_max_depth", max_depth)
                model = train_model(
                    X_train, y_train,
                    model_type=model_type,
                    n_estimators=n_estimators,
                    learning_rate=learning_rate,
                    max_depth=max_depth,
                    random_state=random_state
                )

            # 6. Model evaluation
            print("\n=== Evaluating Model ===")
            metrics, y_pred = evaluate_model(model, X_test, y_test)

            # Log metrics
            for metric_name, value in metrics.items():
                mlflow.log_metric(metric_name, value)

            # 7. Log model
            print("\n=== Logging Model ===")
            if model_type == 'random_forest':
                mlflow.sklearn.log_model(model, "random_forest_model")
            elif model_type == 'xgboost':
                try:
                    import mlflow.xgboost
                    mlflow.xgboost.log_model(model, "xgboost_model")
                except ImportError:
                    # Fallback to sklearn if xgboost mlflow integration not available
                    mlflow.sklearn.log_model(model, "xgboost_model")

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
                os.remove(feature_importance_csv)  # Clean up

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