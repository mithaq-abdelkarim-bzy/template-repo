import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers

def sch_risk_information(cds):

    cds.extend_node_rater_defined("cds", {                                
        # Do not remove
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "case_pricing_analysis_location": hx.Str(mode="input",  default=None, optionality="optional", view={"label": "Case Pricing Analysis Filepath"}),
        # ~~~~~

        # Risk Details

        # from old application sheet
        "deadline_date": hx.Date(mode="input",default = None, optionality="optional", view={"label": "Deadline Date"}),
        "short_description": hx.Str(mode="input", default="", view={"label": "Short Description", "options": {"read_only_option": {"read_only": True}}}),
        "deal_status": hx.Str(mode="input", default="Submission", options_table = "table_deal_status", options_column="status", view={"label": "Deal Status", "options": {"read_only_option": {"read_only": True}}}),
        "declinature_reason": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_reason_for_declinature", options_column="reason", view={"label": "Reason for Declinature"}),
        "declinature_comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Additional UW Comments"}),
        "quotation": hx.Str(mode="input", default=None, optionality="optional", options=["Quote Required", "Quote Not Required"], view={"label": "Quotation"}),
        "quoted": hx.Str(mode="input", default="No", options = ["No", "Yes"], view={"label": "Quoted"}),
        "programme": hx.Str(mode="input", default="Cat XL", optionality="optional", options=["Agg XL", "Cat XL", "QS", "Risk XL", "Workers Comp"], view={"label": "Programme", "options": {"read_only_option": {"read_only": True}}}),
        "territory": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_territory", options_column="territory", view={"label": "Territory"}),
        "multi_year": hx.Str(mode="input", default="No", options=["Yes", "No"], view={"label": "Multi-year?"}),
        "calc_type": hx.Str(mode="input", default="US", options=["US", "Non-US"], view={"label": "Calculation Type"}),
        "currency": hx.Str(mode="input", default=None, optionality="optional", options_table="table_currency", options_column="currency", view={"label": "Application Currency"}),
        "market_share": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Market Share", "format": utils.percent_format(0)}),
        "personal_commercial": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_personal_commercial", options_column="type", view={"label": "Personal/Commercial"}),
        "carrier_type": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_carrier_type", options_column="type", view={"label": "Carrier Type"}),
        "sanctions_clause": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_sanctions_clause", options_column="clause", view={"label": "Sanctions Clause"}),
        "non_pd_bi": hx.Str(mode="input", default=None, optionality="optional", options=["Yes","No"], view={"label": "Non PD BI?"}),
        "tax": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "Tax", "format": {"output": "percent", "mantissa": 1}}),
        "ceding_commission": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "Ceding Commission", "format": {"output": "percent", "mantissa": 1}}),
        "other_acq_costs": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "Other Acq. Costs", "format": {"output": "percent", "mantissa": 1}}),
        "brokerage": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
        "second_loss_brokerage": hx.Float(mode="input", default=0.05, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "2nd Loss Brokerage", "format": {"output": "percent", "mantissa": 1}}),
        "adj_base": hx.Str(mode="input", default=None, optionality="optional", options=["Income", "TIV", "PML", "Modelled Expected Loss", "Flat Premium", "Other"], view={"label": "Adj. Base"}),
        "core_account": hx.Str(mode="input", default=None, optionality="optional", options=["A", "B", "C"], view={"label": "Core Account"}),
        "hours_clause": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Hours Clause"}),
        "terrorism_code": hx.Str(mode="input", default=None, optionality="optional", options_table="table_terrorism_code",options_column="code", view={"label": "Terrorism Code"}),
        "com_disease": hx.Str(mode="input", default=None, optionality="optional", options_table="table_com_disease",options_column="code", view={"label": "Com Disease"}),
        "cyber_code": hx.Str(mode="input", default=None, optionality="optional", options_table="table_cyber_code",options_column="code", view={"label": "Cyber Code"}),
        "named_perils": hx.Str(mode="input", default=None, optionality="optional", options=["Yes","No"], view={"label": "Named Perils"}),
        "am_best_rating": hx.Str(mode="input", default=None, optionality="optional", options_table="table_am_best_rating",options_column="rating", view={"label": "AM Best Rating"}),
        "territorial_focus_group": hx.Str(mode="input", default=None, optionality="optional", options_table="table_territorial_focus_group",options_column="group", view={"label": "Territorial Focus Group"}),
        "risk_carrier": hx.Str(mode="input", default=None, optionality="optional", options_table="table_risk_carrier",options_column="risk_carrier", view={"label": "Risk Carrier"}),
        "met_client_last_12_months": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No"], view={"label": "Met client in last 12 months?"}),
        "application_comments": hx.Str(mode="input", default="", view={"label": "Comments"}),
        "includes_us_exposure": hx.Bool(mode="input", default=False, view = {"label": "Includes US Exposure"}),
        
        "underwriter_location": hx.Str(mode="input", default=None, optionality="optional", options = ["Bermuda", "London"], view = {"label": "Location of Underwriter"}),
        "technical_underwriter": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_input_underwriters", options_column="underwriter", view = {"label": "Technical Underwriter", "options": {"read_only_option": {"read_only": True}}}),
        "discussed_london": hx.Bool(mode="input", default=False, view = {"label": "Discussed with London office?", "options": {"read_only_option": {"read_only": True}}}),

        "treaty_basis": hx.Str(mode="input", default=None, optionality="optional", options = ["LOD", "RAD"], view = {"label": "Treaty Basis"}),

        "risk_xl_risk_definition": hx.Str(mode="input", default=None, optionality="optional", options = ["Location", "Policy"], view = {"label": "Risk Definition"}),
        "risk_xl_profile": hx.Str(mode="input", default=None, optionality="optional", options = ["Gross of FAC", "Net of FAC"], view = {"label": "Profile"}),
        "risk_xl_sublimit_wind": hx.Float(mode="input", default=None, optionality="optional", view = {"label": "Sub Limit (Wind)"}),
        "risk_xl_sublimit_quake": hx.Float(mode="input", default=None, optionality="optional", view = {"label": "Sub Limit (Quake)"}),
        "risk_xl_sublimit_flood": hx.Float(mode="input", default=None, optionality="optional", view = {"label": "Sub Limit (Flood)"}),
        "risk_xl_non_cat_lr": hx.Float(mode="input", default=None, optionality="optional", view = {"label": "Non-Cat LR (over last 5 years)"}),

        "limit_application_ccy_label": hx.Str(mode="output"),
        "excess_application_ccy_label": hx.Str(mode="output"),
        "aggregate_deductible_application_ccy_label": hx.Str(mode="output"),
        "total_label": hx.Str(mode="input", default="Total"),
        "burn_ol_ccy_label": hx.Str(mode="output"),

        # layer total
        "layer_totals": hx.Structure(view = {"label": "Total"}, children = {
            "limit": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
            "limit_ly": hx.Float(mode="input", default=None, optionality="optional",  async_output=["start_renewal_task", "populate_model_task"], view={"format": utils.thousands_format(0), "read_only": True}),
        }),


        # show hides
        "show_intl_fields": hx.Bool(mode="output"),
        "show_us_fields": hx.Bool(mode="output"),
        "show_us_exposure_fields": hx.Bool(mode="output"),
        "show_perc_us_el": hx.Bool(mode="output"),
        "show_agg_qs_input": hx.Bool(mode="output"),
        "show_cat_work_comp_input": hx.Bool(mode="output"),
        "show_cat_rate_change": hx.Bool(mode="output"),
        "show_other_programme_rate_change": hx.Bool(mode="output"),
        "show_case_priced": hx.Bool(mode="output"),
        "show_multi_year": hx.Bool(mode="output"),
        "show_declined_reasons": hx.Bool(mode="output"),
        "show_aad_cnv_field": hx.Bool(mode="output"),
        "show_ceding_commission": hx.Bool(mode="output"),
        "show_bermuda": hx.Bool(mode="output"),

        "show_non_risk_xl": hx.Bool(mode="output"),
        "show_risk_xl": hx.Bool(mode="output"),

        "generate_tags_run": hx.Bool(mode="input", default=False),

        # info fields
        "tp_calc_1_info": hx.Str(mode="input", default="""Capital intensive. \n EL + Expenses + Capital Cost + RI Cost - Inv. Income.""", view={"read_only": True}),
        "tp_calc_2_info": hx.Str(mode="input", default="""Volatile but low capital. \n EL + Expenses + SD Load (12% US, 7.5% Intl.).""", view={"read_only": True}),
        "tp_calc_3_info": hx.Str(mode="input", default="""Max LR acceptable. \n (EL + LAE) / Max LR (0.8).""", view={"read_only": True}),

        "number_reins_factor_info": hx.Str(mode="input", default="""Discount factor for number of (Free) reinstatements and AAD.""", view={"read_only": True}),
        "paid_reins_factor_info": hx.Str(mode="input", default="""Discount factor for paid reinstatements.""", view={"read_only": True}),

    })

    cds.extend_node_rater_defined("cds/layers", {
        "loss_affected": hx.Str(mode="input", default="No", options=["Yes", "No"], view={"label": "Loss Affected?"}),
        "renewal_layer": hx.Bool(mode="input", default=True, view={"label": "Renewal\nLayer", "options": {"read_only_option": {"read_only": True}}}),
        "leader": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Leader"}),
        "layer_description": hx.Str(mode="input", default="", view={"label": "Description"}),
        "layer_structure": hx.Str(mode="output", optionality="optional", view={"label": "Layer Structure"}),
        "layer_index": hx.Int(mode="output", optionality="optional"),

        "inner_type": hx.Str(mode="input", default=None, optionality="optional", options=["Conventional", "Franchise"], view={"label": "Inner Type"}),
        "number_reins": hx.Int(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Number of\nReinstatements"}),
        "perc_reins_1": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "% Reins. 1", "format": {"output": "percent", "mantissa": 0}}),
        "perc_reins_2": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "% Reins. 2", "format": {"output": "percent", "mantissa": 0}}),
        "perc_reins_3": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "% Reins. 3", "format": {"output": "percent", "mantissa": 0}}),
        "limit_cnv": hx.Float(mode="output", optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0)}),
        "excess_cnv": hx.Float(mode="output", optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0)}),
        "aggregate_deductible_cnv": hx.Float(mode="output", optionality="optional", view={"label": "AAD", "format": utils.thousands_format(0)}),
        "is_facility": hx.Bool(mode="input", default=False, view={"label": "Is Facility?"}),
        "effective_brokerage": hx.Float(mode="output", optionality="optional", view={"label": "Effective Brokerage", "format": utils.percent_format(1)}),
        "risk_xl_occurrence_limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Occurrence Limit", "format": utils.thousands_format(0)}),
        "risk_xl_occurrence_limit_cnv": hx.Float(mode="output", optionality="optional", view={"label": "Occurrence Limit", "format": utils.thousands_format(0)}),
        "risk_xl_us_pml_code": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_risk_xl_us_pml_code", options_column="code", view={"label": "US PML Code"}),
        "risk_xl_intl_pml_code": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_risk_xl_intl_pml_code", options_column="code", view={"label": "Intl PML Code"}),

        "section_reference_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Section Reference", "read_only": True}),
        "loss_affected_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Loss Affected?", "read_only": True}),
        "renewal_layer_ly": hx.Bool(mode="input", default=True, view={"label": "Renewal\nLayer", "read_only": True}),
        "currency_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Layer Currency", "read_only": True}),
        "leader_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Leader", "read_only": True}),
        "layer_description_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Description", "read_only": True}),
        "limit_ly": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0), "read_only": True}),
        "excess_ly": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0), "read_only": True}),
        "limit_cnv_ly": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0), "read_only": True}),
        "excess_cnv_ly": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0), "read_only": True}),
        "inner_type_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Inner Type", "format": utils.thousands_format(0), "read_only": True}),
        "aggregate_deductible_ly": hx.Float(mode="input", default=None,  optionality="optional", view={"label": "AAD", "format": utils.thousands_format(0), "read_only": True}),
        "aggregate_deductible_cnv_ly": hx.Float(mode="input", default=None,  optionality="optional", view={"label": "AAD", "format": utils.thousands_format(0), "read_only": True}),
        "number_reins_ly": hx.Int(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Number of\nReinstatements", "read_only": True}),
        "perc_reins_1_ly": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "% Reins. 1", "format": {"output": "percent", "mantissa": 0}, "read_only": True}),
        "perc_reins_2_ly": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "% Reins. 2", "format": {"output": "percent", "mantissa": 0}, "read_only": True}),
        "perc_reins_3_ly": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "% Reins. 3", "format": {"output": "percent", "mantissa": 0}, "read_only": True}),
        "risk_xl_occurrence_limit_ly": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Occurrence Limit", "format": utils.thousands_format(0), "read_only": True}),
        "risk_xl_occurrence_limit_cnv_ly": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Occurrence Limit", "format": utils.thousands_format(0), "read_only": True}),
        "risk_xl_us_pml_code_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "US PML Code", "read_only": True}),
        "risk_xl_intl_pml_code_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Intl PML Code", "read_only": True}),

        "layer_structure_ly": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Layer Structure", "read_only": True}),

        "is_facility_ly": hx.Bool(mode="input", default=None, optionality="optional", view={"label": "Is Facility?", "read_only": True}),
        "effective_brokerage_ly": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Effective Brokerage", "format": utils.percent_format(1), "read_only": True}),
    })                       