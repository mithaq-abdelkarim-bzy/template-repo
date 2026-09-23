import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_rationale(cds):
    # Rationale
    cds.extend_node_rater_defined(f"cds", {
        "rationale": hx.Structure(children={
            # CURRENT YEAR -----------------------------------------------------------------------------
            # INSURED OVERVIEW
            "insured_name" : hx.Str(mode="output", view={"label": "Insured Name"}, async_input=["generate_rationale_doc_task"]),
            "inception_date" : hx.Date(mode="output", view={"label": "Inception Date"}, async_input=["generate_rationale_doc_task"]),
            "policy_ref" : hx.Str(mode="output", view={"label": "Policy Reference"}, async_input=["generate_rationale_doc_task"]),
            "coverholder_background" : hx.Str(mode="input", optionality = "optional", default = None, async_input=["generate_rationale_doc_task"], view={"label": "Coverholder Background"}),

            # RISK DETAILS
            "risk_type" : hx.Str(mode="input", default = None, optionality = "optional", view={"label": "Risk Type"}, async_input=["generate_rationale_doc_task"]),
            "construction" : hx.Str(mode="input", default = None, optionality = "optional", view={"label": "Construction"}, async_input=["generate_rationale_doc_task"]),
            "signed_line" : hx.Float(mode="output", view={"label": "Written / Signed Line", "format": percent_format(2)}, async_input=["generate_rationale_doc_task"]),
            "written_line" : hx.Float(mode="output", view={"label": "Written", "format": percent_format(2)}, async_input=["generate_rationale_doc_task"]),
            "limit" : hx.Float(mode="output", view={"label": "Risk Limit", "format": thousands_format()}, async_input=["generate_rationale_doc_task"]),
            "deductions" : hx.Float(mode="output", view={"label": "Deductions", "format": percent_format(2)}, async_input=["generate_rationale_doc_task"]),
            "avg_limit" : hx.Float(mode="input", default = None, optionality = "optional", view = {"label": "Average Limit", "format": thousands_format()}, async_input=["generate_rationale_doc_task"]),
            "top_country" : hx.Str(mode="input", default = None, optionality = "optional", view = {"label" : "Top Country"}, async_input=["generate_rationale_doc_task"]),

            "avg_model_rate" : hx.Float(mode="output", view = {"label": "Average GG Technical Rate", "format":percent_format(2)}, async_input=["generate_rationale_doc_task"]),
            "avg_uw_rate" : hx.Float(mode="output", view = {"label": "Average GG Achieved Rate", "format": percent_format(2)}, async_input=["generate_rationale_doc_task"]),
            "epi" :hx.Float(mode = "output", view={"label": "EPI", "format": thousands_format()}, async_input=["generate_rationale_doc_task"]),
            "rate_change" :hx.Float(mode = "output", view={"label": "Rate Change", "format": percent_format()}, async_input=["generate_rationale_doc_task"]),
            "attr_lr" :hx.Float(mode = "output", view={"label": "Attritional Loss Ratio", "format": percent_format()}, async_input=["generate_rationale_doc_task"]),
            "cat_load" :hx.Float(mode = "output", view={"label": "Cat Load (if applicable)", "format": percent_format()}, async_input=["generate_rationale_doc_task"]),

            "bpi" :hx.Float(mode = "output", view={"label": "BPI (Post UW Adj)", "format": percent_format()}, async_input=["generate_rationale_doc_task"]),
            "tpi" :hx.Float(mode = "output", view={"label": "TPI (Post UW Adj)", "format": percent_format()}, async_input=["generate_rationale_doc_task"]),
            "roc" :hx.Float(mode = "output", view={"label": "RoC (Post UW Adj)", "format": percent_format()}, async_input=["generate_rationale_doc_task"]),

            # FURTHER RATIONALE
            "uw_comments" : hx.Str(mode="input", optionality = "optional", default = None, view={"label": "Underwriter Commentary"}, async_input=["generate_rationale_doc_task"]),
            "rate_change_rationale" : hx.Str(mode="input", optionality = "optional", default = None, view={"label": "Terms and Conditions change"}, async_input=["generate_rationale_doc_task"]),
            "tnc_change" : hx.Str(mode="input", optionality = "optional", default = None, view={"label": "Terms and Conditions change"}, async_input=["generate_rationale_doc_task"]),
            "risk_profile" : hx.Str(mode="input", optionality = "optional", default = None, view={"label": "Risk Profile"}, async_input=["generate_rationale_doc_task"]),
            "territory_and_agg_dist" : hx.Str(mode="input", optionality = "optional", default = None, view={"label": "Territory Profile and Agg Distribution"}, async_input=["generate_rationale_doc_task"]),
            "exposure_change" : hx.Str(mode="input", optionality = "optional", default = None, view={"label": "Exposure Change / Management"}, async_input=["generate_rationale_doc_task"]),
            "large_losses" : hx.Str(mode="input", optionality = "optional", default = None, view={"label": "Exposure Change / Management"}, async_input=["generate_rationale_doc_task"]),

            # EXPIRING YEAR -----------------------------------------------------------------------------
            # INSURED OVERVIEW
            "insured_name_expiry" : hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Insured Name (Expiring)"}),
            "inception_date_expiry" : hx.Date(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Inception Date"}),
            "pol_ref_expiry" : hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Policy Reference"}),
            "coverholder_background_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Coverholder Background"}),

            # RISK DETAILS
            "risk_type_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Risk Type"}),
            "construction_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Construction"}),
            "signed_line_expiry" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Written / Signed Line", "format": percent_format(2)}),
            "limit_expiry" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Risk Limit", "format": thousands_format()}),
            "deductions_expiry" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Deductions", "format": percent_format(2)}),
            "avg_limit_expiry" : hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view = {"label": "Average Limit", "format": thousands_format()}),
            "top_country_expiry" : hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view = {"label": "Top Country"}),

            "avg_model_rate_expiry" : hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view = {"label": "Average Rate (Model View)", "format": percent_format(2)}),
            "avg_uw_rate_expiry" : hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view = {"label": "Average Rate (UW View)", "format": percent_format(2)}),
            "epi_expiry" :hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "EPI", "format": thousands_format()}),
            "rate_change_expiry" :hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Rate Change", "format": percent_format()}),
            "attr_lr_expiry" :hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Attritional Loss Ratio", "format": percent_format()}),
            "cat_load_expiry" :hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Cat Load (if applicable)", "format": percent_format()}),

            "bpi_expiry" :hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "BPI (Post UW Adj)", "format": percent_format()}),
            "tpi_expiry" :hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "TPI (Post UW Adj)", "format": percent_format()}),
            "roc_expiry" :hx.Float(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "RoC (Post UW Adj)", "format": percent_format()}),

            # FURTHER RATIONALE
            "uw_comments_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Underwriter Commentary"}),
            "rate_change_expiry_rationale" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Terms and Conditions change"}),
            "tnc_change_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Terms and Conditions change"}),
            "risk_profile_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Risk Profile"}),
            "territory_and_agg_dist_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Territory Profile and Agg Distribution"}),
            "exposure_change_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Exposure Change / Management"}),
            "large_losses_expiry" : hx.Str(mode = "output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Exposure Change / Management"}),

            "test_list": hx.List(mode = "output", children = {
                "country" : hx.Str(mode = "output", view = {"label": "Country"}),
                "premium" : hx.Float(mode = "output", view = {"label": "Premium"}),
                "premium_usd" : hx.Float(mode = "output", view = {"label": "Premium usd"}),
                "conv" : hx.Float(mode = "output", view = {"label": "FX rate"}),
            })    
        })
    })

    # cds.override_node_properties(f"cds/layers/uw_adj_impact", {
        # "mode": "input", 
        # "default": 0,
        # "view": {"options": {"read_only": {"label": "Impact of Underwriting Adjustments", "read_only": True}}},
    # })


