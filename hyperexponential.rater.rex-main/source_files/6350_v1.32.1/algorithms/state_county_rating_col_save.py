import hx
import pandas as pd
import math

def state_county_rating_col_save(hxd):
    if hxd.policy_information.small_schedule_model:
        columns = ["state", "county"]
        save_cols = pd.DataFrame([{column: getattr(getattr(row, "address_dropdown"), column) for column in columns} for row in hxd.schedule.schedule_table])

        if not (save_cols=="").all().all():
            try:
                save_cols.to_csv("state_county_saved_cols.csv", index=False)
                hxd.spatialkey.csv_status = "Ready"
            except OSError:
                hxd.spatialkey.csv_status = "OSError while writing to state_county_saved_cols.csv"
