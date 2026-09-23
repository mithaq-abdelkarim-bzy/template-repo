import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_rate_change(cds):
    for cob in ["jb", "fa", "gs", "cit"]:
        for rc_type in ["tech", "uwadj"]:
            cds.extend_node_rater_defined(f"cds/layers", {
                f"{cob}_rc_{rc_type}": hx.Structure(children={
                    "prem_ly": hx.Float(mode="output", view={"label": "Quote\nPremium\nLY", "format": thousands_format()}),

                    "prem_exp_ly": hx.Float(mode="output", view={"label": "Exposure\nPremium\nLY", "format": thousands_format()}),
                    "uwinput_exp": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                    "prem_exp_ty": hx.Float(mode="output", view={"label": "Exposure\nPremium\nTY", "format": thousands_format()}),
                    "chg_exp": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                    "prem_adj_exp": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                    "prem_ded_ly": hx.Float(mode="output", view={"label": "Deductibles\nLY", "format": percent_format()}),
                    "uwinput_ded": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                    "prem_ded_ty": hx.Float(mode="output", view={"label": "Deductibles\nTY", "format": percent_format()}),
                    "chg_ded": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                    "prem_adj_ded": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                    "prem_lim_ly": hx.Float(mode="output", view={"label": "Limits\nLY", "format": thousands_format()}),
                    "uwinput_lim": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                    "prem_lim_ty": hx.Float(mode="output", view={"label": "Limits\nTY", "format": thousands_format()}),
                    "chg_lim": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                    "prem_adj_lim": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                    "prem_risk_ly": hx.Float(mode="output", view={"label": "Risk\nLY", "format": thousands_format()}),
                    "uwinput_risk": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                    "prem_risk_ty": hx.Float(mode="output", view={"label": "Risk\nTY", "format": thousands_format()}),
                    "chg_risk": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                    "prem_adj_risk": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                    "prem_tc_ly": hx.Float(mode="output", view={"label": "T&C's\nLY", "format": thousands_format()}),
                    "uwinput_tc": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                    "prem_tc_ty": hx.Float(mode="output", view={"label": "T&C's\nTY", "format": thousands_format()}),
                    "chg_tc": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                    "prem_adj_tc": hx.Float(mode="output", view={"label": "LY's Risk \nAdj Premium\nTY", "format": thousands_format()}),

                    "prem_ty": hx.Float(mode="output", view={"label": "Quote\nPremium\nTY", "format": thousands_format()}),
                    "rarc": hx.Float(mode="output", view={"label": "RARC", "format": percent_format()})
                })
            })
            
            
            for sub_group in [1, 2, 3]:
                cds.extend_node_rater_defined(f"cds/layers", {
                    f"{cob}_{sub_group}_rc_{rc_type}": hx.Structure(children={
                        "subcategory": hx.Str(mode="output", view={"label": "Sub-Category"}),
                        "prem_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Quote\nPremium\nLY", "format": thousands_format()}),

                        "prem_exp_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Exposure\nPremium\nLY", "format": thousands_format()}),
                        "uwinput_exp": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                        "prem_exp_ty": hx.Float(mode="output", view={"label": "Exposure\nPremium\nTY", "format": thousands_format()}),
                        "chg_exp": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                        "prem_adj_exp": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                        "prem_ded_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Deductibles\nLY", "format": percent_format()}),
                        "uwinput_ded": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                        "prem_ded_ty": hx.Float(mode="output", view={"label": "Deductibles\nTY", "format": percent_format()}),
                        "chg_ded": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                        "prem_adj_ded": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                        "prem_lim_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Limits\nLY", "format": thousands_format()}),
                        "uwinput_lim": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                        "prem_lim_ty": hx.Float(mode="output", view={"label": "Limits\nTY", "format": thousands_format()}),
                        "chg_lim": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                        "prem_adj_lim": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                        "prem_risk_ly": hx.Float(mode="output", view={"label": "Risk\nLY", "format": thousands_format()}),
                        "uwinput_risk": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                        "prem_risk_ty": hx.Float(mode="output", view={"label": "Risk\nTY", "format": thousands_format()}),
                        "chg_risk": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                        "prem_adj_risk": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                        "prem_tc_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "T&C's\nLY", "format": thousands_format()}),
                        "uwinput_tc": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                        "prem_tc_ty": hx.Float(mode="output", view={"label": "T&C's\nTY", "format": thousands_format()}),
                        "chg_tc": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                        "prem_adj_tc": hx.Float(mode="output", view={"label": "LY's Risk \nAdj Premium\nTY", "format": thousands_format()}),

                        "prem_ty": hx.Float(mode="output", view={"label": "Quote\nPremium\nTY", "format": thousands_format()}),
                        "rarc": hx.Float(mode="output", view={"label": "RARC", "format": percent_format()})
                    })
                })

    
        # Waterfall (Technical Rate Change) ~~~
        for sub_group in [1, 2, 3]:
            cds.extend_node_rater_defined(f"cds/layers", {
                f"{cob}_{sub_group}_rc_waterfall": hx.Structure(children={
                    "exp_prem" : hx.Float(mode="output",view={"label":"Expiring Premium"}),
                    "exposure" : hx.Float(mode="output",view={"label":"Exposure"}),
                    "deduct" : hx.Float(mode="output",view={"label":"Deductibles"}),
                    "risk" : hx.Float(mode="output",view={"label":"Risk"}),
                    "t_and_cs" : hx.Float(mode="output",view={"label":"T&Cs"}),
                    "risk_adj_premium" : hx.Float(mode="output",view={"label":"Risk Adj Prem"}),
                    "limit" : hx.Float(mode="output",view={"label":"Limit"}),
                    "quoted_premium" : hx.Float(mode="output",view={"label":"Quoted Premium"}),
                })
            })

    # GS additional
    for rc_type in ["tech", "uwadj"]:
        cds.extend_node_rater_defined(f"cds/layers", {
            f"gs_4_rc_{rc_type}": hx.Structure(children={
                "subcategory": hx.Str(mode="output", view={"label": "Sub-Category"}),
                "prem_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Quote\nPremium\nLY", "format": thousands_format()}),

                "prem_exp_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Exposure\nPremium\nLY", "format": thousands_format()}),
                "uwinput_exp": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                "prem_exp_ty": hx.Float(mode="output", view={"label": "Exposure\nPremium\nTY", "format": thousands_format()}),
                "chg_exp": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                "prem_adj_exp": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                "prem_ded_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Deductibles\nLY", "format": percent_format()}),
                "uwinput_ded": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                "prem_ded_ty": hx.Float(mode="output", view={"label": "Deductibles\nTY", "format": percent_format()}),
                "chg_ded": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                "prem_adj_ded": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                "prem_lim_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Limits\nLY", "format": thousands_format()}),
                "uwinput_lim": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                "prem_lim_ty": hx.Float(mode="output", view={"label": "Limits\nTY", "format": thousands_format()}),
                "chg_lim": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                "prem_adj_lim": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                "prem_risk_ly": hx.Float(mode="output", view={"label": "Risk\nLY", "format": thousands_format()}),
                "uwinput_risk": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                "prem_risk_ty": hx.Float(mode="output", view={"label": "Risk\nTY", "format": thousands_format()}),
                "chg_risk": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                "prem_adj_risk": hx.Float(mode="output", view={"label": "Adj Prem", "format": thousands_format()}),

                "prem_tc_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "T&C's\nLY", "format": thousands_format()}),
                "uwinput_tc": hx.Float(mode="output", view={"label": "UW Input", "format": percent_format()}),
                "prem_tc_ty": hx.Float(mode="output", view={"label": "T&C's\nTY", "format": thousands_format()}),
                "chg_tc": hx.Float(mode="output", view={"label": "Change", "format": percent_format()}),
                "prem_adj_tc": hx.Float(mode="output", view={"label": "LY's Risk \nAdj Premium\nTY", "format": thousands_format()}),

                "prem_ty": hx.Float(mode="output", view={"label": "Quote\nPremium\nTY", "format": thousands_format()}),
                "rarc": hx.Float(mode="output", view={"label": "RARC", "format": percent_format()})
            })
        })
    cds.extend_node_rater_defined(f"cds/layers", {
                f"gs_4_rc_waterfall": hx.Structure(children={
                    "exp_prem" : hx.Float(mode="output",view={"label":"Expiring Premium"}),
                    "exposure" : hx.Float(mode="output",view={"label":"Exposure"}),
                    "deduct" : hx.Float(mode="output",view={"label":"Deductibles"}),
                    "risk" : hx.Float(mode="output",view={"label":"Risk"}),
                    "t_and_cs" : hx.Float(mode="output",view={"label":"T&Cs"}),
                    "risk_adj_premium" : hx.Float(mode="output",view={"label":"Risk Adj Prem"}),
                    "limit" : hx.Float(mode="output",view={"label":"Limit"}),
                    "quoted_premium" : hx.Float(mode="output",view={"label":"Quoted Premium"}),
                })
            })

    cds.override_node_properties(f"cds/layers/rate_change/exposure_change/uw_selected", {"view": {"label": "Exposure", "format": percent_format(2)}})
    cds.override_node_properties(f"cds/layers/rate_change/deductible_change/uw_selected", {"view": {"label": "Deductibles", "format": percent_format(2)}})
    cds.override_node_properties(f"cds/layers/rate_change/limit_change/uw_selected", {"view": {"label": "Limit", "format": percent_format(2)}})
    cds.override_node_properties(f"cds/layers/rate_change/risk_characteristics_change/uw_selected", {"view": {"label": "Risk", "format": percent_format(2)}})
    cds.override_node_properties(f"cds/layers/rate_change/terms_conditions_change/uw_selected", {"view": {"label": "T&Cs", "format": percent_format(2)}})


# For View 
def sch_rate_change_non_cds():
    return {
        # SA: uw_selected is to match the cds ones for the view, not a reflection of what it actually is
        "final_rc_total_summary_view_only" : hx.Structure(view = {"label":"Total"}, children = {
            "expiry_premium" : hx.Structure(children={"uw_selected": hx.Float(mode="override",view={"label":"Expiring Premium", "format":thousands_format()})}),
            "exposure_change" : hx.Structure(children={"uw_selected": hx.Float(mode="output",view={"label":"Exposure","format":percent_format(2)})}),
            "deductible_change" : hx.Structure(children={"uw_selected": hx.Float(mode="output",view={"label":"Deductibles","format":percent_format(2)})}),
            "limit_change" : hx.Structure(children={"uw_selected": hx.Float(mode="output",view={"label":"Limits","format":percent_format(2)})}),
            "risk_characteristics_change" : hx.Structure(children={"uw_selected": hx.Float(mode="output",view={"label":"Risk","format":percent_format(2)})}),
            "terms_conditions_change" : hx.Structure(children={"uw_selected": hx.Float(mode="output",view={"label":"T&Cs","format":percent_format(2)})}),
            "risk_adj_premium" : hx.Structure(children={"uw_selected": hx.Float(mode="output",view={"label":"Risk Adj Prem", "format":thousands_format()})}),
            "quoted_premium" : hx.Float(mode="output",view={"label":"Quoted Prem", "format":thousands_format()}),

            "pure_rc" : hx.Float(mode="output",view={"label":"Pure RC","format":percent_format(2)}),
            "rate_change" : hx.Structure(children={"uw_selected": hx.Float(mode="output",view={"label":"RARC","format":percent_format(2)})}),
            "business" : hx.Float(mode="output",view={"label":"Business","format":percent_format(2)}),
            "rate_change_calculated_pryr" : hx.Float(mode="output", view={"label":"RARC Last Year","format":percent_format(2)})
        }),
    }    