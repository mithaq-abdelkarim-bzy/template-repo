import hx_data_schema as hx
from algorithms.data_schema.sch_utilities import thousands_format, percent_format

### --- DEFINING THE NODES HERE SO THAT THEIR PROPERTIES ARE DYNAMICALLY ACCESSIBLE BY THE RATING ALGORITHM --- ###

coverages_dict = {
    "cargo_transit": {"label": "Cargo"},
    "cargo_storage": {"label": "Cargo"},
    "specie_transit": {"label": "Specie"},
    "specie_storage": {"label": "Specie"},
    "conloss_transit": {"label": "Con Loss"},
    "conloss": {"label": "Con Loss"},
    "cargo_cyber_transit": {"label": "Cargo Cyber"},
    "cargo_cyber_storage": {"label": "Cargo Cyber"},
    "cargo_cyber_addon":{"label": "Cargo Cyber Add On"},
}

cover_selection_dict = {
    "cover_selection": hx.Structure(children={
        "select_message": hx.Str(mode="input", default="Please select the relevant cover to price", view={"label": " ", "read_only": True}),
        "cover": hx.Str(mode="input", default=None, optionality="optional", options=["Cargo", "Cargo Cyber", "Specie", "Con Loss"], view={"label": "Cover"}),
        "is_selected": hx.Bool(mode="output"),
        "is_cargo": hx.Bool(mode="output", async_input=["rarc_task", "policy_to_excel_task"]),
        "is_cargo_cyber": hx.Bool(mode="input", default = False, view = {"label": "Cargo Cyber"}, async_input=["rarc_task", "policy_to_excel_task", "pass_pas_reference"]),
        "is_cargo_cyber_dropdown": hx.Bool(mode="output", async_input=["rarc_task", "policy_to_excel_task"]),
        "is_cargo_cyber_combined": hx.Bool(mode="output", async_input=["rarc_task", "policy_to_excel_task"]),
        "is_specie": hx.Bool(mode="output", async_input=["rarc_task", "policy_to_excel_task"]),
        "is_conloss": hx.Bool(mode="output", async_input=["rarc_task", "policy_to_excel_task"]),
        "show_cargo_cyber": hx.Bool(mode="output", async_input=["rarc_task", "policy_to_excel_task"]),
    }),
}

policy_info_dict = {
    "term": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Term (Years)"})
}

layers_dict = {
    "benchmark_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)"}),
    "benchmark_premium_att": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Att)"}),
    "benchmark_premium_cat": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Cat)"}),
    "expected_loss_cost_att": hx.Float(mode="output", view={"label": "Expected Loss Cost (Att)"}),
    "expected_loss_cost_cat": hx.Float(mode="output", view={"label": "Expected Loss Cost (Cat)"}),
    "quoted_premium_view": hx.Float(mode = "output", view={ "label": "Gross Quoted Premium", "format":thousands_format(0)}),
    "pflr_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"output": "percent", "mantissa": 1}}),
    "brokerage_view": hx.Float(mode="output", optionality="optional", view={"label": "Brokerage (excl. PC's)", "format": {"output": "percent", "mantissa": 1}}),
    "written_line_view": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}}),
    "status_view": hx.Str(mode="output", optionality="optional", view={"label": "Status"}),
    "section_reference_view": hx.Str(mode="output", optionality="optional", view={"label": "Section Reference"}),
    # "brokerage_cargo_cyber": hx.Float(mode="input", default=0, async_input=["rarc_task"], optionality="required", view={"label": "Deductions", "format": {"output": "percent", "mantissa": 1}}),
    # "written_line_cargo_cyber": hx.Float(mode="input", default=0, optionality="required", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}}),
}

layers_dict_cargo_cyber = {
    "benchmark_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Cargo Cyber- Gross Benchmark Premium (Pre-UW Adjustment)"}),
    "benchmark_premium_att": hx.Float(mode="output", view={"label": "Cargo Cyber -  Gross Benchmark Premium (Att)"}),
    "benchmark_premium_cat": hx.Float(mode="output", view={"label": "Cargo Cyber -  Gross Benchmark Premium (Cat)"}),
    "expected_loss_cost": hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost", "format": {"thousandSeparated": True, "mantissa": 0}}),
    "expected_loss_cost_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (Pre-UW Ajustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
    "expected_loss_cost_att": hx.Float(mode="output", view={"label": "Cargo Cyber - Expected Loss Cost (Att)"}),
    "expected_loss_cost_cat": hx.Float(mode="output", view={"label": "Cargo Cyber -  Expected Loss Cost (Cat)"}),
    "quoted_premium_view": hx.Float(mode = "output", view={ "label": "Cargo Cyber - Gross Quoted Premium", "format":thousands_format(0)}),
    "pflr_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Cargo Cyber - Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"output": "percent", "mantissa": 1}}),
    "brokerage_view": hx.Float(mode="output", optionality="optional", view={"label": "Cargo Cyber - Brokerage (excl. PC's)", "format": {"output": "percent", "mantissa": 1}}),
    "written_line_view": hx.Float(mode="output", optionality="optional", view={"label": "Cargo Cyber - Written Line", "format": {"output": "percent", "mantissa": 1}}),
    "status_view": hx.Str(mode="output", optionality="optional", view={"label": "Cargo Cyber - Status"}),
    "section_reference_view": hx.Str(mode="output", optionality="optional", view={"label": "Cargo Cyber - Section Reference"}),
    "single_section_reference": hx.Structure(children={
        "ref": hx.Str(mode="input", default="", view={"label": "Cargo Cyber Section Reference"}, async_input=["pass_pas_reference"]),
        "type": hx.Str(mode="input", default="Cargo Cyber: All", view={"label": "Region", "read_only": True}),
        "is_shown": hx.Bool(mode = "output")
    }),
    "eea_section_reference": hx.Structure(children={
        "ref": hx.Str(mode="input", default="", view={"label": "Cargo Cyber Section Reference"}, async_input=["pass_pas_reference"]),
        "type": hx.Str(mode="input", default="Cargo Cyber: EEA", view={"label": "Region", "read_only": True}),
        "is_shown": hx.Bool(mode = "output")
    }),
    "non_eea_section_reference": hx.Structure(children={
        "ref": hx.Str(mode="input", default="", view={"label": "Cargo Cyber Section Reference"}, async_input=["pass_pas_reference"]),
        "type": hx.Str(mode="input", default="Cargo Cyber: Non-EEA", view={"label": "Region", "read_only": True}),
        "is_shown": hx.Bool(mode = "output")
    }),

}



# def create_cargo_transit_dict():
#     return{    
#     "transit_flag": hx.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Transit"}),
#     "wh_to_port_flag": hx.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Initial Warehouse to Port"}),
#     "loading_flag": hx.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Loading"}),
#     "voyage_flag": hx.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Voyage"}),
#     "unloading_flag": hx.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Unloading"}),
#     "port_to_wh_flag": hx.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Port to Final Warehouse"}),
#     "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
#     "commodity": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", options_table="ca_commodity", options_column="commodity", view={"label": "Commodity"}),
#     "commodity_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "trans_vals": hx.Float(mode="input", default=0, async_input=["rarc_task"], validation={"min_value": 0, "max_value": 1000000000000}, view={"label": "Est Ann Transit Vals", "format": thousands_format()}),
#     "trans_vals_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "deductible_level": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_deductible_level", options_column="deductible_level", view={"label": "Deductible Level"}),
#     "deductible_level_factor": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Overridable Factor"}),
#     "excess_factor": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Overridable Factor"}),
#     "packaging": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_packaging", options_column="packaging", view={"label": "Packaging"}),
#     "packaging_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "conv_air": hx.Str(mode="input", async_input=["rarc_task"], default="AIR", view={"label": " ", "read_only": True}),
#     "conv_land": hx.Str(mode="input", async_input=["rarc_task"], default="LAND", view={"label": " ", "read_only": True}),
#     "conv_sea": hx.Str(mode="input", async_input=["rarc_task"], default="SEA", view={"label": " ", "read_only": True}),
#     "conv_air_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Splits", "format": percent_format(0)}),
#     "conv_land_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": " ", "format": percent_format(0)}),
#     "conv_sea_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": " ", "format": percent_format(0)}),
#     "conv_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "conv_check": hx.Str(mode="output", view={"label": "Check"}),
#     "conv_check_show": hx.Bool(mode="output", view={"label": "Check"}),
#     "voyage": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_voyage", options_column="voyage", view={"label": "Voyage"}),
#     "voyage_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "surveyor": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_surveyor", options_column="surveyor", view={"label": "Surveyor Present"}),
#     "surveyor_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "vessel": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_vessel", options_column="vessel", view={"label": "Vessel"}),
#     "vessel_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "uw_discretion": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "UW Discretion"}),
#     "uw_discretion_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
#     "type_of_cover": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_type_of_cover", options_column="type_of_cover", view={"label": "Type of Cover"}),
#     "type_of_cover_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "technical_deductions": hx.Float(mode="output", view={"label": "Transit Rate (Base Deductions)", "format": thousands_format(3)}),
#     "technical_rate": hx.Float(mode="output", view={"label": "Transit Rate (Annual)", "format": thousands_format(3)}),
#     "actual_rate": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Transit Rate (Annual)", "format": thousands_format(3)}),
#     "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage of Model", "format": percent_format(2)}),
#     "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
#     "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"}),
#     "are_fields_full": hx.Bool(mode="output")
#     }




def create_cargo_transit_dict_02(async_in = None, async_out = None):
    #Default value if None provided
    async_in = async_in or ["rarc_task"]
    async_out = async_out or []
    return{    
    "transit_flag": hx.Bool(mode="input", default=False, async_input=async_in, async_output=async_out, view={"label": "Transit"}),
    "wh_to_port_flag": hx.Bool(mode="input", default=False, async_input=async_in, async_output=async_out, view={"label": "Initial Warehouse to Port"}),
    "loading_flag": hx.Bool(mode="input", default=False, async_input=async_in, async_output=async_out, view={"label": "Loading"}),
    "voyage_flag": hx.Bool(mode="input", default=False, async_input=async_in, async_output=async_out, view={"label": "Voyage"}),
    "unloading_flag": hx.Bool(mode="input", default=False, async_input=async_in, async_output=async_out, view={"label": "Unloading"}),
    "port_to_wh_flag": hx.Bool(mode="input", default=False, async_input=async_in, async_output=async_out, view={"label": "Port to Final Warehouse"}),
    "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
    "commodity": hx.Str(mode="input", default=None, async_input=async_in, async_output=async_out, optionality="optional", options_table="ca_commodity", options_column="commodity", view={"label": "Commodity"}),
    "commodity_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "trans_vals": hx.Float(mode="input", default=0, async_input=async_in, async_output=async_out, validation={"min_value": 0, "max_value": 1000000000000}, view={"label": "Est Ann Transit Vals", "format": thousands_format()}),
    "trans_vals_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "deductible_level": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_deductible_level", options_column="deductible_level", view={"label": "Deductible Level"}),
    "deductible_level_factor": hx.Float(mode="override", async_input=async_in, view={"label": "Overridable Factor"}),
    "excess_factor": hx.Float(mode="override", async_input=async_in, view={"label": "Overridable Factor"}),
    "packaging": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_packaging", options_column="packaging", view={"label": "Packaging"}),
    "packaging_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "conv_air": hx.Str(mode="input", async_input=async_in, async_output=async_out, default="AIR", view={"label": " ", "read_only": True}),
    "conv_land": hx.Str(mode="input", async_input=async_in, async_output=async_out, default="LAND", view={"label": " ", "read_only": True}),
    "conv_sea": hx.Str(mode="input", async_input=async_in, async_output=async_out, default="SEA", view={"label": " ", "read_only": True}),
    "conv_air_factor": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": "Splits", "format": percent_format(0)}),
    "conv_land_factor": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": " ", "format": percent_format(0)}),
    "conv_sea_factor": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": " ", "format": percent_format(0)}),
    "conv_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "conv_check": hx.Str(mode="output", view={"label": "Check"}),
    "conv_check_show": hx.Bool(mode="output", view={"label": "Check"}),
    "voyage": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_voyage", options_column="voyage", view={"label": "Voyage"}),
    "voyage_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "surveyor": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_surveyor", options_column="surveyor", view={"label": "Surveyor Present"}),
    "surveyor_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "vessel": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_vessel", options_column="vessel", view={"label": "Vessel"}),
    "vessel_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "uw_discretion": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", view={"label": "UW Discretion"}),
    "uw_discretion_factor": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=1, view={"label": "Factor"}),
    "type_of_cover": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_type_of_cover", options_column="type_of_cover", view={"label": "Type of Cover"}),
    "type_of_cover_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "technical_deductions": hx.Float(mode="output", view={"label": "Transit Rate (Base Deductions)", "format": thousands_format(3)}),
    "technical_rate": hx.Float(mode="output", view={"label": "Transit Rate (Annual)", "format": thousands_format(3)}),
    "actual_rate": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", view={"label": "Transit Rate (Annual)", "format": thousands_format(3)}),
    "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage of Model", "format": percent_format(2)}),
    "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
    "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"}),
    "are_fields_full": hx.Bool(mode="output")
    }


cargo_transit_dict = create_cargo_transit_dict_02(async_in= ["rarc_task", "load_cargo_input"])
cargo_cyber_transit_dict = create_cargo_transit_dict_02(async_in= ["rarc_task"], async_out = [{"task":"load_cargo_input", "reset": False}] )


# def create_cargo_storage_dict():
#     return{
#     "storage_flag": hx.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Storage"}),
#     "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
#     "stock_vals": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Expo'd Stock Vals", "format": thousands_format()}),
#     "deductible_level": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_deductible_level", options_column="deductible_level", view={"label": "Deductible Level"}),
#     "deductible_level_factor": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Overridable Factor"}),
#     "excess_factor": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Overridable Factor"}),
#     "survey": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Satis. Survey Report"}),
#     "survey_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "risk_mgmt": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Risk Management"}),
#     "risk_mgmt_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
#     "type_of_cover": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_type_of_cover", options_column="type_of_cover", view={"label": "Type of Cover"}),
#     "type_of_cover_factor": hx.Float(mode="output", view={"label": "Factor"}),
#     "uw_discretion": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "UW Discretion"}),
#     "uw_discretion_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
#     "rate": hx.Float(mode="output", view={"label": "Storage Rate", "format": thousands_format(3)}),
#     "avg_val_pcm": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Avg Val Expo'd PCM", "format": thousands_format()}),
#     "cat_expo": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Exposure", "format": thousands_format()}),
#     "cat_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
#     "combined_cat_load": hx.Float(mode="output", view={"label": "Combined Cat Load"}),
#     "cat_expo_tp": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Model Premium", "format": thousands_format()}),
#     "countries": hx.List(mode="input", async_input=["rarc_task"], default_element_count=5, children={
#         "country": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_cat_load", options_column="country", view={"label": "Country", "format": thousands_format()}),
#         "cat_expo": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Cat Exposure Amount", "format": thousands_format()}),
#         "cat_load": hx.Float(mode="output", view={"label": "Load Applied"}),
#         "pct_of_cat": hx.Float(mode="output", view={"label": "% of CAT", "format": percent_format(2)}),
#     }),
#     "cat_expo_check": hx.Str(mode="output", view={"label": "Check"}),
#     "cat_expo_check_show": hx.Bool(mode="output"),
#     "retail_expo": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Exposure", "format": thousands_format()}),
#     "retail_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
#     "retail_load": hx.Float(mode="input", async_input=["rarc_task"], default= 1.5, view={"label": "Retail Load", "read_only": True}),
#     "retail_expo_tp": hx.Float(mode="output", view={"label": "Model Premium", "format": thousands_format()}),
#     "all_else_expo": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Exposure", "format": thousands_format()}),
#     "all_else_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
#     "all_else_load": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Everything Else Load", "read_only": True}),
#     "all_else_expo_tp": hx.Float(mode="output", view={"label": "Model Premium", "format": thousands_format()}),
#     "technical_deductions": hx.Float(mode="output", view={"label": "Storage Rate (Base Deductions)", "format": thousands_format(3)}),
#     "technical_rate": hx.Float(mode="output", view={"label": "Storage Rate (Annual)", "format": thousands_format(3)}),
#     "actual_rate": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Storage Rate (Annual)", "format": thousands_format(3)}),
#     "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage of Model", "format": percent_format(2)}),
#     "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
#     "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"}),
#     "are_fields_full": hx.Bool(mode="output")
#     }

def create_cargo_storage_dict_02(async_in = None, async_out = None):
    #Default value if None provided
    async_in = async_in or ["rarc_task"]
    async_out = async_out or []    
    return{
    "storage_flag": hx.Bool(mode="input", default=False, async_input=async_in, async_output=async_out, view={"label": "Storage"}),
    "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
    "stock_vals": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": "Expo'd Stock Vals", "format": thousands_format()}),
    "deductible_level": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_deductible_level", options_column="deductible_level", view={"label": "Deductible Level"}),
    "deductible_level_factor": hx.Float(mode="override", async_input=async_in, view={"label": "Overridable Factor"}),
    "excess_factor": hx.Float(mode="override", async_input=async_in, view={"label": "Overridable Factor"}),
    "survey": hx.Bool(mode="input", async_input=async_in, async_output=async_out, default=False, view={"label": "Satis. Survey Report"}),
    "survey_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "risk_mgmt": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", view={"label": "Risk Management"}),
    "risk_mgmt_factor": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=1, view={"label": "Factor"}),
    "type_of_cover": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_type_of_cover", options_column="type_of_cover", view={"label": "Type of Cover"}),
    "type_of_cover_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "uw_discretion": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", view={"label": "UW Discretion"}),
    "uw_discretion_factor": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=1, view={"label": "Factor"}),
    "rate": hx.Float(mode="output", view={"label": "Storage Rate", "format": thousands_format(3)}),
    "avg_val_pcm": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": "Avg Val Expo'd PCM", "format": thousands_format()}),
    "cat_expo": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": "Exposure", "format": thousands_format()}),
    "cat_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
    "combined_cat_load": hx.Float(mode="output", view={"label": "Combined Cat Load"}),
    "cat_expo_tp": hx.Float(mode="override", async_input=async_in, view={"label": "Model Premium", "format": thousands_format()}),
    "countries": hx.List(mode="input", async_input=async_in, async_output=async_out, default_element_count=5, children={
        "country": hx.Str(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", options_table="ca_cat_load", options_column="country", view={"label": "Country", "format": thousands_format()}),
        "cat_expo": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": "Cat Exposure Amount", "format": thousands_format()}),
        "cat_load": hx.Float(mode="output", view={"label": "Load Applied"}),
        "pct_of_cat": hx.Float(mode="output", view={"label": "% of CAT", "format": percent_format(2)}),
    }),
    "cat_expo_check": hx.Str(mode="output", view={"label": "Check"}),
    "cat_expo_check_show": hx.Bool(mode="output"),
    "retail_expo": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=0, view={"label": "Exposure", "format": thousands_format()}),
    "retail_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
    "retail_load": hx.Float(mode="input", async_input=async_in, async_output=async_out, default= 1.5, view={"label": "Retail Load", "read_only": True}),
    "retail_expo_tp": hx.Float(mode="output", view={"label": "Model Premium", "format": thousands_format()}),
    "all_else_expo": hx.Float(mode="override", async_input=async_in, view={"label": "Exposure", "format": thousands_format()}),
    "all_else_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
    "all_else_load": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=1, view={"label": "Everything Else Load", "read_only": True}),
    "all_else_expo_tp": hx.Float(mode="output", view={"label": "Model Premium", "format": thousands_format()}),
    "technical_deductions": hx.Float(mode="output", view={"label": "Storage Rate (Base Deductions)", "format": thousands_format(3)}),
    "technical_rate": hx.Float(mode="output", view={"label": "Storage Rate (Annual)", "format": thousands_format(3)}),
    "actual_rate": hx.Float(mode="input", async_input=async_in, async_output=async_out, default=None, optionality="optional", view={"label": "Storage Rate (Annual)", "format": thousands_format(3)}),
    "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage of Model", "format": percent_format(2)}),
    "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
    "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"}),
    "are_fields_full": hx.Bool(mode="output")
    }


cargo_storage_dict = create_cargo_storage_dict_02(async_in= ["rarc_task", "load_cargo_input"])
cargo_cyber_storage_dict = create_cargo_storage_dict_02(async_in= ["rarc_task"], async_out = [{"task":"load_cargo_input", "reset": False}] )


specie_transit_dict = {
    "transit_flag": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Transit"}),
    "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
    "commodity": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="sp_commodity", options_column="commodity", view={"label": "Commodity"}),
    "commodity_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "trans_vals": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0, "max_value": 1000000000000}, view={"label": "Est Ann Transit Vals", "format": thousands_format()}),
    "trans_vals_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "deductible_level": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="sp_deductible", options_column="deductible", view={"label": "Deductible Level"}),
    "deductible_level_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "excess_factor": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Overridable Factor"}),
    "type_of_cover": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="sp_type_of_cover", options_column="type_of_cover", view={"label": "Type of Cover"}),
    "type_of_cover_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "uw_discretion": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "UW Discretion"}),
    "uw_discretion_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
    "technical_deductions": hx.Float(mode="output", view={"label": "Transit Rate (Base Deductions)", "format": thousands_format(3)}),
    "technical_rate": hx.Float(mode="output", view={"label": "Transit Rate (Annual)", "format": thousands_format(3)}),
    "actual_rate": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Transit Rate (Annual)", "format": thousands_format(3)}),
    "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage of Model", "format": percent_format(2)}),
    "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
    "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"})
}

specie_storage_dict = {
    "storage_flag": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Storage"}),
    "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
    "commodity": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="sp_commodity", options_column="commodity", view={"label": "Commodity"}),
    "commodity_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "stock_vals": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0, "max_value": 1000000000000}, view={"label": "Expo'D Stock Vals", "format": thousands_format()}),
    "stock_vals_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "deductible_level": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="sp_deductible", options_column="deductible", view={"label": "Deductible Level"}),
    "deductible_level_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "excess_factor": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Overridable Factor"}),
    "survey": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Satis. Survey Report"}),
    "survey_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "risk_mgmt": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Risk Management"}),
    "risk_mgmt_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
    "type_of_cover": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="sp_type_of_cover", options_column="type_of_cover", view={"label": "Type of Cover"}),
    "type_of_cover_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "uw_discretion": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "UW Discretion"}),
    "uw_discretion_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
    "rate": hx.Float(mode="output", view={"label": "Storage Rate", "format": thousands_format(3)}),
    "avg_val_pcm": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Avg Val Expo'd PCM", "format": thousands_format()}),
    "cat_expo": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Exposure", "format": thousands_format()}),
    "cat_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
    "combined_cat_load": hx.Float(mode="output", view={"label": "Combined Cat Load"}),
    "cat_expo_tp": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Model Premium", "format": thousands_format()}),
    "countries": hx.List(mode="input", async_input=["rarc_task"], default_element_count=5, children={
        "country": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_cat_load", options_column="country", view={"label": "Country", "format": thousands_format()}),
        "cat_expo": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Cat Exposure Amount", "format": thousands_format()}),
        "cat_load": hx.Float(mode="output", view={"label": "Load Applied"}),
        "pct_of_cat": hx.Float(mode="output", view={"label": "% of CAT", "format": percent_format(2)}),
    }),
    "cat_expo_check": hx.Str(mode="output", view={"label": "Check"}),
    "cat_expo_check_show": hx.Bool(mode="output"),
    "non_cat_expo": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Exposure", "format": thousands_format()}),
    "non_cat_pct_of_total": hx.Float(mode="output", view={"label": "% of Total", "format": percent_format(2)}),
    "non_cat_load": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Non-CAT Load", "read_only": True}),
    "non_cat_expo_tp": hx.Float(mode="output", view={"label": "Model Premium", "format": thousands_format()}),
    "technical_deductions": hx.Float(mode="output", view={"label": "Storage Rate (Base Deductions)", "format": thousands_format(3)}),
    "technical_rate": hx.Float(mode="output", view={"label": "Storage Rate (Annual)", "format": thousands_format(3)}),
    "actual_rate": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Storage Rate (Annual)", "format": thousands_format(3)}),
    "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage of Model", "format": percent_format(2)}),
    "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
    "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"})
}

conloss_transit_dict = {
    "transit_flag": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Transit"}),
    "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
    "trans_vals": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0, "max_value": 1000000000000}, view={"label": "Est Ann Transit Vals", "format": thousands_format()}),
    "trans_vals_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "deductible_level": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_deductible_level", options_column="deductible_level", view={"label": "Deductible"}),
    "deductible_level_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "packaging_1": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="cl_packaging", options_column="packaging", view={"label": " "}),
    "packaging_2": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="cl_packaging", options_column="packaging", view={"label": " "}),
    "packaging_1_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Splits", "format": percent_format(0)}),
    "packaging_2_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": " ", "format": percent_format(0)}),
    "packaging_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "packaging_check": hx.Str(mode="output", view={"label": "Check"}),
    "packaging_check_show": hx.Bool(mode="output"),
    "conv_air": hx.Str(mode="input", async_input=["rarc_task"], default="AIR", view={"label": " ", "read_only": True}),
    "conv_land": hx.Str(mode="input", async_input=["rarc_task"], default="LAND", view={"label": " ", "read_only": True}),
    "conv_sea": hx.Str(mode="input", async_input=["rarc_task"], default="SEA", view={"label": " ", "read_only": True}),
    "conv_air_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Splits", "format": percent_format(0)}),
    "conv_land_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": " ", "format": percent_format(0)}),
    "conv_sea_factor": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": " ", "format": percent_format(0)}),
    "conv_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "conv_check": hx.Str(mode="output", view={"label": "Check"}),
    "conv_check_show": hx.Bool(mode="output"),
    "voyage": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_voyage", options_column="voyage", view={"label": "Voyage"}),
    "voyage_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "surveyor": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_surveyor", options_column="surveyor", view={"label": "Surveyor Present"}),
    "surveyor_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "vessel": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_vessel", options_column="vessel", view={"label": "Vessel"}),
    "vessel_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "uw_discretion": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "UW Discretion"}),
    "uw_discretion_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
    "type_of_cover": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="ca_type_of_cover", options_column="type_of_cover", view={"label": "Type Of Cover"}),
    "type_of_cover_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "technical_deductions": hx.Float(mode="output", view={"label": "Transit Rate (Base Deductions)", "format": thousands_format(3)}),
    "technical_rate": hx.Float(mode="output", view={"label": "Transit Rate", "format": thousands_format(3)}),
    "actual_rate": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Transit Rate", "format": thousands_format(3)}),
    "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage of Model", "format": percent_format(2)}),
    "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
    "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"})
}

conloss_dict = {
    "conloss_flag": hx.Bool(mode="input", async_input=["rarc_task"], default=False, view={"label": "Con Loss"}),
    "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": thousands_format(3)}),
    "limit_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "exposure": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="cl_exposure", options_column="exposure", view={"label": "Exposure"}),
    "exposure_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "indemnity_period": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="cl_indemnity_period", options_column="period", view={"label": "Indemnity Period"}),
    "indemnity_message": hx.Str(mode="input", async_input=["rarc_task"], default="Please enter both the indemnity period and deductible", view={"label": "Check", "read_only": True}),
    "indemnity_message_show": hx.Bool(mode="output"),
    "deductible_level": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", options_table="cl_deductible", options_column="deductible", view={"label": "Deductible"}),
    "deductible_level_factor": hx.Float(mode="output", view={"label": "Factor"}),
    "uw_discretion": hx.Str(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "UW Discretion"}),
    "uw_discretion_factor": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Factor"}),
    "technical_deductions": hx.Float(mode="output", view={"label": "Con Loss Rate (Base Deductions)", "format": thousands_format(3)}),
    "technical_rate": hx.Float(mode="output", view={"label": "Con Loss Rate", "format": thousands_format(3)}),
    "actual_rate": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "Con Loss Rate", "format": thousands_format(3)}),
    "pct_of_technical": hx.Float(mode="output", view={"label": "Percentage Of Model", "format": percent_format(2)}),
    "technical_premium_att": hx.Float(mode="output", view={"label": "Gross Technical Premium (Att)"}),
    "technical_premium_cat": hx.Float(mode="output", view={"label": "Gross Technical Premium (Cat)"})
}

# add Cargo Cyber into dictionary. They are exactly the same as the main cargo


# Using the following dictionary as a subset of the data schema that is accessible in rating
all_coverages_dict = {
    "cargo_transit": cargo_transit_dict,
    "cargo_storage": cargo_storage_dict,
    "specie_transit": specie_transit_dict,
    "specie_storage": specie_storage_dict,
    "conloss_transit": conloss_transit_dict,
    "conloss": conloss_dict,
    "cargo_cyber_transit": cargo_cyber_transit_dict,
    "cargo_cyber_storage": cargo_cyber_storage_dict
}