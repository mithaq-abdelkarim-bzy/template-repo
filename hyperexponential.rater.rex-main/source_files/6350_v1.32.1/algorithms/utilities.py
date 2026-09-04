import hx
from operator import itemgetter
import pandas as pd
import time
from algorithms.constant import MAX_OPTIONS
RATER_PROGRESS_MAP = {
    "started": 0,
    "map_layers_usd": 20,
    "earthquake_windstorm_simulation": 40,
    "premium_summary": 60,
    "create_required_summary_tables": 80,
    "finished": 100 
}

def convert_hx_list_to_df(hx_list):
    df = pd.DataFrame(hx_list)
    desired_columns = df.iloc[0].str[0]
    
    for col in df.columns:
        df[col] = df[col].apply(itemgetter(1))
    df.columns = desired_columns

    return df

# Fastest way to convert a hx_list into a pandas dataframe
def pd_df_from_hx_list(hx_list):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way, without having to specify or loop through the keys/column names in the hx.List().
    '''

    col_designation = {x[0]: getattr(x[1], "is_overridden", None) is not None for x in hx_list[0]}
    override_cols = [k for k, v in col_designation.items() if v]
    normal_cols = [x for x in col_designation if x not in override_cols]

    list_representation = [
        {column: getattr(row, column) for column in normal_cols}
        | 
        {f"{column}_calculated": getattr(row, column).calculated for column in override_cols} 
        | 
        {f"{column}_override": getattr(row, column).override for column in override_cols} 
        for row in hx_list
    ]

    df = pd.DataFrame(list_representation)

    return df

# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write = []):
    dictionary = df.to_dict()
    
    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            setattr(list_node[i], col, dictionary[col][i])
        for col in override_cols_to_write:
            #only need to bring back calculated column as overrides will work as normal
            setattr(getattr(list_node[i], col),"calculated",dictionary[col + "_calculated"][i])


def generate_layer_location_ded_options(peril):
    '''
    Generates the US Location Deductibles dict when copying the primary layer.
    '''
    if not hasattr(peril, "location_ded"):
        return

    location_ded = dict()
    for item in peril.location_ded:
        if len(item) == 2:
            option_label = item[0]
            option = item[1]
            location_ded[option_label] = {
                "location_min_max": option.location_min_max,
                "percent": option.percent,
                "region_dropdown": {},
                "sublimit": option.sublimit,
                "type": option.type
            }

            location_ded[option_label]["region_dropdown"] = {key:val for key, val in option.region_dropdown}
            if hasattr(option, "named_storm_ded"):
                location_ded[option_label]["named_storm_ded"] = option.named_storm_ded
    
    return location_ded



class TimerTracker:
    """ Times different sections of code, for example:
        tracker = TimerTracker()
        ... your code ...
        tracker.checkpoint("after step 1")
        ... more code ...
        tracker.checkpoint("after step 2")
        df = tracker.to_dataframe()
        print(df)   """
    def __init__(self, disable=False):
        self.timestamps = []
        self.deltas = []
        self.start_time = time.perf_counter()
        self.last_time = self.start_time
        self.disable = disable

    def checkpoint(self, label=None):
        if not self.disable:
            now = time.perf_counter()
            delta = now - self.last_time
            self.deltas.append({
                'label': label or f'Checkpoint {len(self.deltas) + 1}',
                'elapsed': delta
            })
            self.last_time = now

    def to_dataframe(self):
        return pd.DataFrame(self.deltas)
    
    def stop(self, label=None):
        if not self.disable:
            self.checkpoint(label)
            print(self.to_dataframe())

    def fatal_stop(self, label=None):
        if not self.disable:
            self.checkpoint(label)
            df = self.to_dataframe().to_string()
            hx.errors.fatal(str(df))

class RunAsyncRaterProgress:
    def __init__(self, hxd, progress):
        """
        progress_map: dict {label: cumulative_percent}
        Example: {"schedule_load_and_calc": 1, "get_currency_exchange": 4, ...}
        """
        self.tracker = TimerTracker()
        self.hxd = hxd
        self.progress = progress
        self.progress_map = RATER_PROGRESS_MAP
        self.current = 0
        # self._set_percent(0) # start label
        self.update("started") # start label

    def update(self, step_label):
        """
        Called: status.update("schedule_load_and_calc")
        """
        pct = self.progress_map.get(step_label, self.current)
        self._set_percent(pct)

    def update_percent(self, pct):
        """
        You can manually update percent: status.update_percent(40)
        """
        self._set_percent(pct)

    def _set_percent(self, pct):
        self.hxd.schedule.run_rater_progress_information = f"⏳ Rating..... {pct}%"
        self.current = pct
        self.progress.update(pct / 100)
        # self._set_label(f"⏳ Rating..... {int(pct)}%")
        self.tracker.checkpoint()

    def finish(self):
        self.tracker.checkpoint()
        exec_time = 0.0
        for delta in self.tracker.deltas:
            exec_time += delta['elapsed']

        self.hxd.schedule.run_rater_progress_information = f"✅ Rating Complete! Elapsed time: {exec_time:,.2f}"

