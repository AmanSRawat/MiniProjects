import pandas as pd
import numpy as np

def validate_data(df) -> bool:
    errors = []
    
    # 1. Check for Required Columns
    required_columns = ['timestamp', 'temperature', 'condition', 'surge']
    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing column: '{col}'")

    if errors:
        # If columns are missing, we can't perform further checks safely
        print("Data validation failed with the following issues:")
        for err in errors:
            print(f"- {err}")
        return False

    # 2. Check Data Types
    # Check if 'timestamp' is a datetime type
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        errors.append(f"Column 'timestamp' is not datetime64[ns] (found {df['timestamp'].dtype})")

    # 3. Check Value Sets (Categorical)
    valid_conditions = {'Sunny', 'Rainy', 'Windy', 'Snowy', 'Cloudy'}
    invalid_rows = df[~df['condition'].isin(valid_conditions)]
    if not invalid_rows.empty:
        unique_invalid = invalid_rows['condition'].unique()
        errors.append(f"Column 'condition' contains invalid values: {unique_invalid}")

    # 4. Check Range (Numerical)
    # Check if 'surge' is between 0 and 3.0
    out_of_range = df[(df['surge'] < 0) | (df['surge'] > 3.0)]
    if not out_of_range.empty:
        errors.append(f"Column 'surge' has {len(out_of_range)} values outside range [0, 3.0]")

    # 5. Report Results
    if errors:
        print("Data validation failed with the following issues:")
        for err in errors:
            print(f"- {err}")
        return False
    else:
        print("Data validation passed successfully.")
        return True