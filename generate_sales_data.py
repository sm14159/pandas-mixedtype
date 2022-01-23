# Generates random sales data
import logging

import numpy as np
import pandas as pd


def generate_random_dates(start, end, n=10):
    # Thanks to https://stackoverflow.com/questions/50559078/generating-random-dates-within-a-given-range-in-pandas
    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')


def generate_sales_data(file_path):
    """Generates random sales data from address file and current data

    Parameters
    ----------
    file_path : str
        File path to save csv sales data to, including filename

    Outputs
    -------
    sales_data : DataFrame
        Random sales data with date, units_sold, addres
    """
    random_addresses = pd.read_json("generate_address/addresses.json")
    n_rows = len(random_addresses)
    random_dates = generate_random_dates(pd.Timestamp.today() + pd.DateOffset(years=-3), pd.Timestamp.today(), n_rows)
    sales_data = pd.DataFrame({"date": random_dates,
                            "units_sold": np.random.randint(-3, 20, n_rows)})
    sales_data[random_addresses.columns] = random_addresses

    # Randomly remove some entries
    sales_data.loc[np.random.randint(0, len(sales_data), 82), "zip_code"] = None                

    sales_data.to_csv(file_path, index=False)
