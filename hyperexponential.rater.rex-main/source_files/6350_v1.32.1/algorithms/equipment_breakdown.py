import hx
import polars as pl

def equipment_breakdown_calc(hxd, df, other_data):
    '''
    Calculate Equipment Breakdown Premium
    '''

    non_cat_base_rates_df = hx.params.non_cat_base_rates
    eb_rate_df = hx.params.eb_rate
    eb_deductible_df = hx.params.eb_deductible
    eb_sublimits_df = hx.params.eb_sublimits

    non_cat_base_rates_pl = pl.from_pandas(non_cat_base_rates_df[["Key", "EB Code", "Bpro risk class"]])
    non_layer_eb_structure = hxd.non_layer_perils.equipment_breakdown 

    # Assign EB industry and occupancy
    eb_df = df[["industry", "occupancy", "tiv_total_usd"]].sort("tiv_total_usd", descending=True)

    if len(eb_df) != 0:
        largest = eb_df.row(0, named=True)
        non_layer_eb_structure.industry.calculated = largest['industry']
        non_layer_eb_structure.occupancy.calculated = largest['occupancy']



    # Base Rate Calculation
    industry_occupancy = f"{non_layer_eb_structure.industry.selected or ''}{non_layer_eb_structure.occupancy.selected or ''}"

    filtered_code_pl = (non_cat_base_rates_pl.filter(pl.col("Key") == industry_occupancy))
    eb_breakdown_class = filtered_code_pl["EB Code"][0] if len(filtered_code_pl) else "No Occupancy Selected"
    risk_class = filtered_code_pl["Bpro risk class"][0] if len(filtered_code_pl) else ""

    hxd.quote_documents.bpro_outputs.risk_class = risk_class

    eb_rate_pl = pl.from_pandas(eb_rate_df[["EB Code", "Rate", "Min Ded", "Max Loc Total TIV", "Max Loc BI TIV"]])
    filtered_rate_pl = (eb_rate_pl.filter(pl.col("EB Code") == eb_breakdown_class))
    eb_base_rate = filtered_rate_pl["Rate"][0] if len(filtered_rate_pl) else 0
    min_ded = filtered_rate_pl["Min Ded"][0] if len(filtered_rate_pl) else 0
    max_total_tiv_lookup = filtered_rate_pl["Max Loc Total TIV"][0] if len(filtered_rate_pl) else "N/A"
    max_bi_tiv_lookup = filtered_rate_pl["Max Loc BI TIV"][0] if len(filtered_rate_pl) else "N/A"

    # Deductible load calculation
    eb_deductible_pl = pl.from_pandas(eb_deductible_df)
    ded_lower_pl = eb_deductible_pl.filter(pl.col("Deductible") <= (hxd.non_layer_perils.equipment_breakdown.deductible or 0))
    ded_upper_pl = eb_deductible_pl.filter(pl.col("Deductible") >= (hxd.non_layer_perils.equipment_breakdown.deductible or 0))

    if len(ded_lower_pl) == 0 or len(ded_upper_pl) == 0:
        deductible_load = 1
    else:
        ded_lower, load_lower = ded_lower_pl["Deductible"][-1], ded_lower_pl["Load"][-1]
        ded_upper, load_upper = ded_upper_pl["Deductible"][0], ded_upper_pl["Load"][0]

        if ded_lower == ded_upper:
            deductible_load = 1 + load_upper
        else:
            deductible_load = 1 + (load_lower + 
                                    (load_upper - load_lower) * (hxd.non_layer_perils.equipment_breakdown.deductible - ded_lower) / (ded_upper - ded_lower)
                                )

    # Coverage Load calculation
    eb_sublimits_pl = pl.from_pandas(eb_sublimits_df)

    perishable_goods_load =  get_eb_load(hxd, "perishable_goods", "Perishable Goods", eb_sublimits_pl)
    expediting_expense_load =  get_eb_load(hxd, "expediting_expense", "Expediting Expense", eb_sublimits_pl)
    pollution_load =  get_eb_load(hxd, "pollution", "Pollution Cleanup and removal", eb_sublimits_pl)
    data_media_load =  get_eb_load(hxd, "data_media", "Data Media", eb_sublimits_pl)
    demolition_load =  get_eb_load(hxd, "demolition", "Demolition and Increased cost of Construction", eb_sublimits_pl)
    water_damage_load =  get_eb_load(hxd, "water_damage", "Water Damage", eb_sublimits_pl)

    # Equipment Breakdown Premium
    ex_rate = hxd.policy_information.exchange_rate or 1
    for index, layer in enumerate(hxd.layers, start=1):
        layer.perils.equipment_breakdown.eb_premium = (other_data["total_tiv_total_usd"] * ex_rate * eb_base_rate * deductible_load * 
                (1 + perishable_goods_load + expediting_expense_load + pollution_load + data_media_load + demolition_load + water_damage_load) /
                (1 - 0.175) * layer.perils.equipment_breakdown.include * hxd.policy_information.policy_length.selected)


    # Referral Calculation
    eb_ded = hxd.non_layer_perils.equipment_breakdown.deductible
    deductible_validation = eb_ded < min_ded if eb_ded and min_ded else False

    max_bi_tiv = df["tiv_bi_usd"].max()
    max_total_tiv = df["tiv_total_usd"].max()

    max_total_tiv_validation = max_total_tiv_lookup != "N/A" and (max_total_tiv > float(max_total_tiv_lookup))
    max_bi_tiv_validation = max_bi_tiv_lookup != "N/A" and (max_bi_tiv > float(max_bi_tiv_lookup))

    if risk_class == "ERR":
        hxd.non_layer_perils.equipment_breakdown.referral = "Travelers will not offer EB on this class"
    elif (deductible_validation or max_total_tiv_validation or max_bi_tiv_validation or eb_breakdown_class == "D" 
            or perishable_goods_load == "Refer" or expediting_expense_load == "Refer" or pollution_load == "Refer"
            or data_media_load == "Refer" or demolition_load == "Refer" or water_damage_load == "Refer"):
        hxd.non_layer_perils.equipment_breakdown.referral = "Yes, refer to Travelers"
    else:
        hxd.non_layer_perils.equipment_breakdown.referral = "No"


def get_eb_load(hxd, table, column, eb_sublimits_pl):
    hxd_table = getattr(getattr(hxd.non_layer_perils.equipment_breakdown, table), "pd_sublimit")
    table_pl = eb_sublimits_pl.filter(pl.col("PD Sublimits") == hxd_table)
    if len(table_pl):
        load = float(table_pl[column][0]) if table_pl[column][0] != "Refer" else 0
    else:
        load = 0

    return load