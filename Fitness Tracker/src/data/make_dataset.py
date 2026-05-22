import pandas as pd
from glob import glob

## Reading the data
files = glob("../../data/raw/MetaMotion/*.csv")
len(files)

def read_meta_motion_data(files):
    acc_df = pd.DataFrame()
    gyro_df = pd.DataFrame()

    acc_set = 1
    gyro_set = 1

    for f in files:
        participant = f.split("-")[0].replace(data_path, "")
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("12345").rstrip("_MetaWear_2019")
        
        df = pd.read_csv(f)
        df["participant"] = participant
        df["label"] = label
        df["category"] = category
        
        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df], ignore_index=True)
        elif "Gyroscope" in f:
            df["set"] = gyro_set
            gyro_set += 1
            gyro_df = pd.concat([gyro_df, df], ignore_index=True)
    
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyro_df.index = pd.to_datetime(gyro_df["epoch (ms)"], unit="ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyro_df["epoch (ms)"]
    del gyro_df["time (01:00)"]
    del gyro_df["elapsed (s)"]
    
    return acc_df, gyro_df

acc_df, gyro_df = read_meta_motion_data(files)

# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
data_merged = pd.concat([acc_df.iloc[:, :3], gyro_df], axis=1)

#Rename the column names
data_merged.columns =[
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_x",
    "gyro_y",  
    "gyro_z",
    "participant",
    "label",
    "category",
    "set"
]

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz
sampling = {
    "acc_x":"mean",
    "acc_y":"mean",
    "acc_z":"mean",
    "gyro_x":"mean",
    "gyro_y":"mean",  
    "gyro_z":"mean",
    "participant":"last",
    "label":"last",
    "category":"last",
    "set":"last"
}

data_merged[:1000].resample("200ms").apply(sampling)

days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]
days[1]

data_resampled = pd.concat([df.resample("200ms").apply(sampling).dropna() for df in days], ignore_index=True)

data_resampled["set"] = data_resampled["set"].astype(int)

data_resampled.info()

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
data_resampled.to_pickle("../../data/interim/meta_motion_data.pkl")