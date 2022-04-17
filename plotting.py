import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set(rc={"figure.figsize": (11, 4)})


def plot_CTR(ctr: pd.DataFrame):
    """
    This function will plot CTR per hour.
    :param ctr: Dataframe that contain "ctr_per_hour" field
    :return: None
    """
    fig, ax, index_min, index_max = _plotting_guide(ctr)
    ax.plot(
        ctr.loc[index_min:index_max, "ctr_per_hour"],
        marker="o",
        linestyle="-",
        label="ctr_per_hour",
    )
    ax.set_title("Click Through Rate Per Hour")
    plt.legend()
    plt.savefig("ctr_per_hour.png")


def plot_outliers(outliers: pd.DataFrame, window_size: int):
    """
    This function will plot outliers
    :param outliers: dataframe that contains Outliers
    :param window_size: size of the moving average window
    :return: None
    """
    fig, ax, index_min, index_max = _plotting_guide(outliers)
    ax.plot(outliers["ctr_per_hour"], marker="o", label="CTR")
    ax.plot(
        outliers[f"moving_avg_window_{window_size}"],
        label=f"Moving Average  {window_size}  hours",
    )
    ax.plot(outliers["outlier_values"], "ro", label="Outliers")
    ax.set_title("Outlier Detection Using Simple Moving Average")
    plt.legend()
    plt.savefig(f"outlier_detection_moving_average_{window_size}.png")


def _plotting_guide(data: pd.DataFrame):
    fig, ax = plt.subplots()
    index_max = str(data.index.values.max())
    index_min = str(data.index.values.min())
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%y-%b-%d"))
    ax.set_ylabel("CTR_per_hour")
    ax.set_xlabel("Date")

    return fig, ax, index_min, index_max
