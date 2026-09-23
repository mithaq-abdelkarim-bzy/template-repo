import hx
import pandas as pd
import numpy as np
from operator import itemgetter

def rate_exposure_input(hxd):
    cds = hxd.cds
    
    # Set dynamic dropdowns
    type_table = hx.params.table_input_classes_type
    cds.risk_info.risk_class_dropdown = sorted(set(type_table["classes"]))
    filtered_type = type_table[type_table["classes"] == cds.standard_fields.benchmark_class]
    cds.risk_info.type_dropdown = filtered_type["mapping"]
    # hxd.type_dropdown = hx.params.type[hx.params.type["tag"] == cds.standard_fields.benchmark_class["mapping"] # Why does this not work? Both elements of the dynamic dropdown have to be in the same parameter table?

    # Convert schedule into a DataFrame
    df = pd.DataFrame(cds.schedule)
    desired_columns = df.iloc[0].str[0]
    df.columns = desired_columns
    for col in df.columns:
        df[col] = df[col].apply(itemgetter(1))
    
    # # Currency default for override
    # df["currency"] = cds.currencies.source_currency
    # for schedule_row, df_row in zip(cds.schedule, df.iloc):
    #     schedule_row.currency.calculated = df_row["currency"]
    
    # Convert TSI to USD
    df = df.merge(hx.params.table_input_currency, how="left", left_on="currency", right_on="ccy")
    df.tsi_cnv = df.tsi / df.fx_rate  # SA: I'd suggest using df["tsi"] to access the columns so that it's visually distinct from how the hxd is accessed
    del df["fx_rate"]  # SA: While this'll work, it's more conventional to use df.drop('fx_rate', axis=1, inplace=True) 

    # Calculate TSI in each band
    band_thresholds = (0, 5e5, 1e6, 2e6, 3e6, 5e6, 1e7, 2e7, 5e7, 1e8, float('inf')) # Tuple or list? Does it matter? # Create parameter table, transpose  
                                                                                    # SA: It doesn't really matter tuple vs list. I'd go with list just to match the line below
    band_fields = ["tsi_band_" + str(x) for x in range(1,11)] # Is this the best way to do this?  # SA: Of forming that list, yes
    for i in range(len(band_fields)):        
        df[band_fields[i]] = np.maximum(np.minimum(df.tsi_cnv - band_thresholds[i], band_thresholds[i+1]-band_thresholds[i]),0) # Is this the best way to reference fields while looping?  
                                                                                                                                # SA: Yeah, I'd probably do it this way

    # Determine sanctioned countries
    df.loc[df["country"].isin(hx.params.table_lookup_country_sanctioned["sanctioned_territories"]), "sanctioned_country"] = "Yes"
    df.loc[~df["country"].isin(hx.params.table_lookup_country_sanctioned["sanctioned_territories"]), "sanctioned_country"] = "No"

    # Class
    if len(hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]) > 0:
        df["risk_class"] = hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]["tag"].iloc[0]
    else:
        df["risk_class"] = ""

    # Region
    del df["region"]
    df = df.merge(hx.params.table_input_country_region, how="left", left_on="country", right_on="countries")
    df.region = df.region.fillna('')

    # Write DataFrame back to Schedule hxd object
    for schedule_row, df_row in zip(cds.schedule, df.iloc):        
        schedule_row.tsi_cnv = df_row["tsi_cnv"] # How to iterate through this object? There must be a way to bulk assign values # Convert dataframe into dict todictrecord df.to_dict("records")
        schedule_row.tsi_band_1 = df_row["tsi_band_1"]  # SA: you can use setattr to assign in a loop. You can also use df_row.index or dir(schedule_row) to get all the columns to loop through
                                                        # although bare in mind this will loop through all columns in df_row or all children in schedule_row so may require some manual parts if 
                                                        # these things aren't identical. You could even first calculate all the similar fields by using [x for x in df_row.index if x in dir(schedule_row)].
                                                        # This list will be the same every time however so it might even be better outside the loop so you're not recalculating it every row!
                                                        # e.g. [x for x in df.columns if x in dir(cds.schedule[0])]
        schedule_row.tsi_band_2 = df_row["tsi_band_2"]
        schedule_row.tsi_band_3 = df_row["tsi_band_3"]
        schedule_row.tsi_band_4 = df_row["tsi_band_4"]
        schedule_row.tsi_band_5 = df_row["tsi_band_5"]
        schedule_row.tsi_band_6 = df_row["tsi_band_6"]
        schedule_row.tsi_band_7 = df_row["tsi_band_7"]
        schedule_row.tsi_band_8 = df_row["tsi_band_8"]
        schedule_row.tsi_band_9 = df_row["tsi_band_9"]
        schedule_row.tsi_band_10 = df_row["tsi_band_10"]
        schedule_row.sanctioned_country = df_row["sanctioned_country"]
        schedule_row.risk_class = df_row["risk_class"]
        schedule_row.region = df_row["region"]
    return df
