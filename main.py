import configs
import preprocessing
import outlier_detection
import plotting
import pandas as pd


def calculate_CTR_per_hour_and_add_to_dataframe(
    data: pd.DataFrame, date_col: str
) -> pd.DataFrame:
    """
    This function will calculate the CTR per hour and will it as dataframe.
    :param date_col:
    :param data: Dataframe
    :return: dataframe with ctr_per_hour
    """
    data_aggregated = pd.DataFrame()
    total_clicks_per_hour = data.groupby(f"{date_col}_utc")["click"].sum()
    # total impression are how many time ads are shown i.e. "sum of clicked and not-clicked adds"
    total_impressions_per_hour = data.groupby(f"{date_col}_utc")["click"].count()
    data_aggregated["ctr_per_hour"] = total_clicks_per_hour / total_impressions_per_hour

    return data_aggregated


if __name__ == "__main__":
    df = preprocessing.read_csv_file_and_get_required_cols(
        file_path=configs.FILE_PATH, required_cols=configs.COLS_REQUIRED
    )
    df_utc = preprocessing.convert_format_to_utc_and_add_to_dataframe(
        data=df, date_col=configs.DATE_COL, date_format=configs.DATE_FORMAT
    )
    ctr_per_hour = calculate_CTR_per_hour_and_add_to_dataframe(df_utc, configs.DATE_COL)
    outlier_df = outlier_detection.moving_average(ctr_per_hour, configs.WINDOW_SIZE)
    plotting.plot_CTR(ctr_per_hour)
    plotting.plot_outliers(outlier_df, configs.WINDOW_SIZE)
