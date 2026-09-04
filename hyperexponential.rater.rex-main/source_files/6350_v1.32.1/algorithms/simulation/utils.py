import pandas as pd
import polars as pl
import numpy as np


def is_df_empty(df) -> bool:
    """
    Check if a DataFrame or LazyFrame is empty.
    Supports Pandas DataFrame, Polars DataFrame, and Polars LazyFrame.
    """
    if isinstance(df, pd.DataFrame):
        return df.empty
    elif isinstance(df, pl.DataFrame):
        return df.height == 0
    elif isinstance(df, pl.LazyFrame):
        # LazyFrames need to be collected to evaluate
        return df.collect().height == 0
    else:
        raise TypeError("Unsupported type. Expected Pandas DataFrame, Polars DataFrame, or Polars LazyFrame.")


class SimulationProgress:
    def __init__(self, hxd, progress, num_layers, has_us, has_intl):
        self.hxd = hxd
        self.progress = progress
        self.num_layers = num_layers
        self.has_us = has_us
        self.has_intl = has_intl
        self.us_stages = 4
        self.intl_stages = 10
        self.current_stage = 0
        self.total = self._total_stages()
        self.update()

    
    def _total_stages(self):
        us = self.num_layers * self.us_stages if self.has_us else 0
        intl = self.num_layers * self.intl_stages if self.has_intl else 0
        return us + intl + 1

    
    def _get_label(self):
        self.percent = int(self.current_stage / self.total * 100)
        label = "⏳ Simulating....."
        return f"{label} {self.percent}%"

    def update(self):
        self.hxd.exposure_management_api.simulation_fetch_status = self._get_label()
        self.progress.update(self.percent/100)
        self.current_stage += 1

    def finish(self):
        self.hxd.exposure_management_api.simulation_fetch_status = "✅ Simulation Complete!"

    def skip_us(self):
        self.current_stage += self.us_stages
    
    def skip_intl(self):
        self.current_stage += self.intl_stages



def compare_dataframes(df1, df2) -> bool:
    # Convert to pandas if either is a Polars DataFrame
    if isinstance(df1, pl.DataFrame):
        df1 = df1.to_pandas()
    if isinstance(df2, pl.DataFrame):
        df2 = df2.to_pandas()
    
    # Reset index
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)
    
    # Remove any index columns accidentally preserved as normal columns
    if 'index' in df1.columns and 'index' in df2.columns:
        df1 = df1.drop(columns=['index'])
        df2 = df2.drop(columns=['index'])
    
    return df1.equals(df2)


def has_intl_or_us_tiv(df):
    df = df.copy()
    df['us_intl'] = np.where(
        df['country'].str.lower() == 'united states',
        'US', 
        'INTL'
    )
    df = df.groupby('us_intl')['TIV'].sum()
    d = df.to_dict()

    has_us = d.get('US', 0) > 0
    has_intl = d.get('INTL', 0) > 0

    return has_us, has_intl


def has_intl_or_us_elt(hxd, sql_loader):

    accgrpid = hxd.policy_information.accgrpid
    perspcode = hxd.layers[0].elt_for_sim
    elt = sql_loader.get_elt(accgrpid=accgrpid, perspcode=perspcode)
    
    region_lst = (
        elt.select("region")
        .unique()
        .to_series()
        .to_list()
    )

    has_us = 'NA' in region_lst
    has_intl = 'EU' in region_lst

    return has_us, has_intl



def conv_col_lowercase(df: pl.DataFrame, column_name: str) -> pl.DataFrame:
    """
    Converts all string values in the specified column to lowercase.
    """
    return df.with_columns(
        pl.col(column_name).str.to_lowercase().alias(column_name)
    )
