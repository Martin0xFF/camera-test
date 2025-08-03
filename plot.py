import numpy as np
import polars as pl
import matplotlib.pyplot as plt


def app():
    df = pl.read_csv("10_min_timestamp.csv")
    df = df.with_columns(
        pl.col('sensor_ts').diff().alias("sensor_timestamp_diff"),
        pl.col('system_ts').diff().alias("system_timestamp_diff"),
    )

    print(df.describe())
    arr = df.to_numpy()

    fig, ax = plt.subplots(3,1)

    # SensorTimestamp
    ax[0].scatter(np.arange(18000), arr[1:,2], color='tab:orange')
    ax[0].set_ylim([33318.26 - 724*4, 33318 + 724*4])
    ax[0].set_title("SensorTimestamp Diff Compared to Frame Index")

    # System Timestamp
    ax[1].scatter(np.arange(18000), arr[1:,3], color='tab:blue')
    ax[1].set_ylim([33318.26 - 724*4, 33318 + 724*4])
    ax[1].set_title("SystemTimestamp Diff Compared to Frame Index")

    sys_mean = np.mean(arr[1:,3])
    sys_std_dev = np.std(arr[1:,3])

    filtered_sys = (arr[1:,3])[((sys_mean - 3*sys_std_dev)<= arr[1:,3])
        &((sys_mean + 3*sys_std_dev)>= arr[1:,3]) ]

    h, edges = np.histogram(filtered_sys, bins=100)
    ax[2].stairs(h,edges, fill=True, label="SystemTimestamp Diff", color='tab:blue')

    h, edges = np.histogram(arr[1:,2], bins=3)
    ax[2].stairs(h,edges, fill=True, label="SensorTimestamp Diff", color='tab:orange') 

    ax[2].set_xlim([33318.26 - 724*4, 33318 + 724*4])
    ax[2].legend()
    ax[2].set_title("Distribution of timestamp First Differences")
    plt.show()


if __name__ == "__main__":
    app()
