import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/meta_motion_data.pkl")
df.head()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (12, 6)
mpl.rcParams["figure.dpi"] = 100

#Plot the exercise
for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig,ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop = True), label = label)
    plt.legend()
    plt.show()

for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig,ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop = True), label = label)
    plt.legend()
    plt.show()



# plot all combinations per sensor
labels = df["label"].unique()
participants = df["participant"].unique()

for label in labels:
    for participant in participants:
        all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()
        
        if len(all_axis_df) == 0:
            continue
        fig,ax = plt.subplots()
        all_axis_df[["acc_x", "acc_y", "acc_z"]].plot(ax = ax)
        ax.set_ylabel("acceleration")
        ax.set_xlabel("samples")
        ax.set_title(f"{label} - {participant}")
        plt.legend()

for label in labels:
    for participant in participants:
        all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()
        
        if len(all_axis_df) == 0:
            continue
        fig,ax = plt.subplots()
        all_axis_df[["gyro_x", "gyro_y", "gyro_z"]].plot(ax = ax)
        ax.set_ylabel("gyroscope")
        ax.set_xlabel("samples")
        ax.set_title(f"{label} - {participant}")
        plt.legend()

# --------------------------------------------------------------
# combinations and export for both sensors
# --------------------------------------------------------------
labels = df["label"].unique()
participants = df["participant"].unique()

for label in labels:
    for participant in participants:
        all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()
        if len(all_axis_df) == 0:
            continue
        fig,ax = plt.subplots(nrows=2, sharex=True, figsize=(20,10))
        all_axis_df[["acc_x", "acc_y", "acc_z"]].plot(ax = ax[0])
        all_axis_df[["gyro_x", "gyro_y", "gyro_z"]].plot(ax = ax[1])

        ax[0].legend(loc = "upper center",bbox_to_anchor=(0.5, 1.15), ncol=3,fancybox=True, shadow=True)
        ax[1].legend(loc = "upper center",bbox_to_anchor=(0.5, 1.15), ncol=3,fancybox=True, shadow=True)
        ax[1].set_xlabel("samples")
        
        plt.savefig(f"../../reports/figures/{label}_{participant}.png")
        plt.show()