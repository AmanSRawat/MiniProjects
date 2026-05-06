import mlflow
import mlflow.xgboost
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

def train_model(df:pd.DataFrame,target_col:str):
    X = df.drop(columns = [target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    
    with mlflow.start_run(nested=True):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("learning_rate", 0.1)
        mlflow.log_param("max_depth", 5)
        mlflow.log_metric("r2_score", r2)
        mlflow.log_metric("mean_absolute_error", mae)
        mlflow.xgboost.log_model(model, "xgboost_model")
        
        # Create training DataFrame for logging (optional, can be omitted if mlflow.data.log_dataset is not available)
        # train_df = X_train.copy()
        # train_df[target_col] = y_train
        # train_ds = mlflow.data.from_pandas(train_df, source='train_data')
        # mlflow.data.log_dataset(train_ds, "train_data")
        
        print(f"Model trained with R2 Score: {r2:.4f} and MAE: {mae:.4f}")
        return model