import hx_data_schema as hx
from data_schema.sch_utilities import *
from algorithms.rate_constants import *

# Replace / remove examples with your models exposures

def sch_freq_inputs():
    return{
        "jurisdiction": hx.Str(
            mode="input", options_table="table_country_factor", options_column="location", default=None, optionality="optional", async_input= ["generate_uw_doc"], 
            view={"label": "Jurisdiction", "multiline": True}),
        "industry": hx.Str(
            mode="input", options_table="table_industry", options_column="industry list", default=None, optionality="optional", async_input= ["generate_uw_doc"],
            view={"label": "Industry", "multiline": True}),
        "business_nature": hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Nature of Business"}),
        "ihs_enforcement": hx.Str(mode="output", view={"label": "IHS Contract Enforcement"}),
    }

def sch_sev_inputs_no_term():
    return{
        "coverage_flag": hx.Bool(mode="input", default=True, async_input= ["generate_uw_doc"], view={"label": "Covered?"}),
        "severity_assessment": hx.Str(mode="input", options_table="table_severity_parameters", options_column="severity", default="Medium", optionality="required", async_input= ["generate_uw_doc"], view={"label": "Severity assessment"}),
        "adjustment": hx.Float(mode="input", default=0, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Adjustment", "format": percent_format(2)}),
        "comment": hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Comment"}),
    }

def sch_sev_inputs():
    return{
        **sch_sev_inputs_no_term(),
        "term": hx.Float(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Term (years)"}),
        "term_modifier": hx.Float(mode="input", default=0, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Term modifier"}),
    }

def sch_exposure_details(cds):
    
    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds", {
        "term":                     hx.Float(   mode="output", async_input= ["generate_uw_doc"], 
                                                view={
                                                    "label": "Policy Period (years)", 
                                                    "format": integer_format(2),
                                                    "options": {"read_only": {"label": " "}}
                                                    }),
        "policy_info":              hx.Structure(children={
            "fundamental_top_up_flag":    hx.Bool(mode="input", default=False, async_input= ["generate_uw_doc"], view={"label": "Does this polciy include Fundamental Top Up Coverage?"}),
            "project_name":               hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Project Name"}),
            "target_name":                hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Target Company (Name)"}),
            "transaction_value":          hx.Float(mode="input", default=0, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Transaction Value"}),
            "total_limit":                hx.Float(mode="input", default=0, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Total Limit Purchased Source Currency"}),
            "total_limit_percentage":     hx.Float(mode="output", async_input= ["generate_uw_doc"], view={"label": "Total limit purchased %", "format": percent_format(2), "options": {"read_only": {"label": " "}}}),
            "brokerage":                  hx.Float(mode="input", default=0.15, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Brokerage", "format": percent_format(1)}),
            "policyholder":               hx.Str(mode="input", options=lst_policyholder, default=lst_policyholder[0], optionality="required", async_input= ["generate_uw_doc"], view={"label": "Policy Purchased by"}),
            "buyer_name":                 hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Buyer (name)"}),
            "buyer_lawyer":               hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Lawyer (buyer)"}),
            "seller_name":                hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Seller (name)"}),
            "seller_lawyer":              hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Lawyer (seller)"}),
            "uw_expenses_flag":           hx.Bool(mode="input", default=False, async_input= ["generate_uw_doc"], view={"label": "Include UW Expenses"}),
            "uw_expenses":                hx.Float(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Underwriting Expenses"}),
            "distressed_business_flag":   hx.Bool(mode="input", default=False, async_input= ["generate_uw_doc"], view={"label": "Distressed Business"}),


        }),

        "rating_factors":           hx.Structure(children={
            "freq":                     hx.Structure(children={
                "target":                   hx.Structure(view={"label": "Target"}, children={**sch_freq_inputs()}),
                "buyer":                    hx.Structure(view={"label": "Buyer"}, children={**sch_freq_inputs()}),                    
                "default_score":            hx.Float(mode="output", async_input= ["generate_uw_doc"], view={"label": "Default Score", "format": percent_format(2)}),
                "freq_adjustment":          hx.Float(mode="input", default=0, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Adjustment", "format": percent_format(2)}),
                "freq_adjusted":            hx.Float(mode="output", async_input= ["generate_uw_doc"], view={"label": "Adjusted frequency", "format": percent_format(2)}),
                "freq_adjusted_pre_uw":     hx.Float(mode="output", async_input= ["generate_uw_doc"], view={"label": "Adjusted frequency (Pre-UW Adj)", "format": percent_format(2)}),
            }),

            "sev":                      hx.Structure(children={
                "due_diligence":            hx.Structure(view={"label": "Due Diligence"}, children={**sch_sev_inputs_no_term()}),
                "disclosure":               hx.Structure(view={"label": "Disclosure"}, children={**sch_sev_inputs_no_term()}),
                "general_warranties":       hx.Structure(view={"label": "General Warranties"}, children={**sch_sev_inputs()}),
                "tax_warranties":           hx.Structure(view={"label": "Tax Warranties/Deed"}, children={**sch_sev_inputs()}),
                "modified_score":           hx.Float(mode="output", async_input= ["generate_uw_doc"], view={"label": "Modified Score"}),
                "modified_score_pre_uw":    hx.Float(mode="output", async_input= ["generate_uw_doc"], view={"label": "Modified Score (Pre-UW Adj)"}),
                "div_flag":                 hx.Bool(mode="input", default=False, async_input= ["generate_uw_doc"], view={"label": "Include DIV"}),
                "volatility":               hx.Str(mode="input", default="Medium", options_table="table_volatility", options_column="volatility", async_input= ["generate_uw_doc"], view={"label": "Volatility"}),
                "multiple":                 hx.Float(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Multiple"}),
            }),
            "fun_top_up":               hx.Structure(view={"label": "Fundamental Top Up"}, children={
                "base_rate":                hx.Float(mode="output", async_input= ["generate_uw_doc"],  view={"label": "Base Rate",  "format": percent_format(2)}),
                "adjustment":               hx.Float(mode="input", default=0, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Adjustment", "format": percent_format(2)}),
                "term":                     hx.Float(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Term (years)"}),
                "comment":                  hx.Str(mode="input", default=None, optionality="optional", async_input= ["generate_uw_doc"], view={"label": "Comment"}),
            })
        }),
    })