import hx
import pandas as pd
import math

def spatialkey_rating_col_save(hxd):
    if hxd.policy_information.small_schedule_model:
        columns = ["latitude", "longitude"]
        save_cols = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.schedule.schedule_table])
        
        try:
            save_cols.to_csv("spatialkey_saved_cols.csv", index=False)
            hxd.spatialkey.csv_status = "Ready"
        except OSError:
            hxd.spatialkey.csv_status = "OSError while writing to spatialkey_saved_cols.csv"
