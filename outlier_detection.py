import numpy as np
import pandas as pd


def moving_average(data: pd.DataFrame, window_size: int) -> pd.DataFrame:

    data = _calculate_moving_average_and_std(data, window_size)
    data["outlier"] = np.where(
        data["ctr_per_hour"]
        > (data[f"moving_avg_window_{window_size}"] + (1.5 * data["std"])),
        1,
        (
            np.where(
                data["ctr_per_hour"]
                < (data[f"moving_avg_window_{window_size}"] - (1.5 * data["std"])),
                1,
                0,
            )
        ),
    )
    data["outlier_values"] = np.where(
        data["outlier"] == 1, data["ctr_per_hour"], np.nan
    )

    return data


def _calculate_moving_average_and_std(
    data: pd.DataFrame, window_size: int
) -> pd.DataFrame:
    data[f"moving_avg_window_{window_size}"] = (
        data["ctr_per_hour"].rolling(window=window_size).mean()
    )
    data["std"] = np.std(data["ctr_per_hour"])
    return data
