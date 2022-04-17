from pathlib import Path
import datetime as dt

import pandas as pd


def read_csv_file_and_get_required_cols(
    file_path: str, required_cols: list
) -> pd.DataFrame:
    """

    This function will return the dataframe with required number of columns. By default it will return all the columns.

    :param file_path: path to the csv file,
    :param required_cols:
    :return: pandas dataframe with required columns
    """
    _validate_file_path_exists(file_path)
    data = pd.read_csv(filepath_or_buffer=file_path)
    if required_cols:
        _validate_columns_exists(
            cols_available=data.columns.tolist(), required_cols=required_cols
        )
        data = data[required_cols]
    return data


def _validate_file_path_exists(file_path: str):
    if not Path(file_path).is_file():
        raise FileNotFoundError(f" The File ({file_path}) is not be found.")


def _validate_columns_exists(cols_available: list, required_cols: list):
    for col in required_cols:
        if col not in cols_available:
            raise ValueError(f'Column "{col}" is not found in the dataframe.')


def convert_format_to_utc_and_add_to_dataframe(
    data: pd.DataFrame, date_col: str, date_format: str
) -> pd.DataFrame:
    """
    This function will convert the date and time to UTC format and add to dataframe.

    :param date_col:
    :param data: pandas dataframe with all columns
    :param date_col: columns that are considered to be date
    :param date_format: format of the date
    :return: dataframe with dates utc format
   """

    parse_date = lambda val: dt.datetime.strptime(str(val), date_format)
    data[f"{date_col}_utc"] = data[date_col].map(parse_date)

    return data
