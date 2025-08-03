import numpy as np
import polars as pl
import matplotlib.pyplot as plt


def app():
    df = pl.read_csv("2_min_stress_timestamp.csv")
    df = df.with_columns(
        pl.col('sensor_ts_us').diff().alias("sensor_timestamp_diff_us"),
        pl.col('system_ts_us').diff().alias("system_timestamp_diff_us"),
    )

    print(df.describe())
    arr = df.to_numpy()

    fig, ax = plt.subplots(3,1)

    ndiffs = np.arange(arr[1:, 2].size)
    
    sys_mean = np.mean(arr[1:,3])
    sys_std_dev = np.std(arr[1:,3])

    filtered_sys = (arr[1:,3])[((sys_mean - 3*sys_std_dev)<= arr[1:,3])
        &((sys_mean + 3*sys_std_dev)>= arr[1:,3]) ]

    ylims = [sys_mean - 3*sys_std_dev, sys_mean + 3*sys_std_dev]
    # SensorTimestamp
    ax[0].scatter(ndiffs, arr[1:,2], color='tab:orange')
    ax[0].set_ylim(ylims)
    ax[0].set_title("SensorTimestamp Diff (microseconds) Compared to Frame Index")
    ax[0].grid()

    # System Timestamp
    ax[1].scatter(ndiffs, arr[1:,3], color='tab:blue')
    ax[1].set_ylim(ylims)
    ax[1].set_title("SystemTimestamp Diff (microseconds) Compared to Frame Index")
    ax[1].grid()



    h, edges = np.histogram(filtered_sys, bins=100)
    ax[2].stairs(h,edges, fill=True, label="SystemTimestamp (us) Diff", color='tab:blue')

    h, edges = np.histogram(arr[1:,2], bins=100)
    ax[2].stairs(h,edges, fill=True, label="SensorTimestamp (us) Diff", color='tab:orange') 

    ax[2].set_xlim(ylims)
    ax[2].set_ylim([0,500])
    ax[2].legend()
    ax[2].grid()
    ax[2].set_title("Distribution of timestamp First Differences (us)")
    plt.show()


if __name__ == "__main__":
    app()
