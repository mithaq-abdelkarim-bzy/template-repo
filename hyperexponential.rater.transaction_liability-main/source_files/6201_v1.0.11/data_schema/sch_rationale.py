import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_rationale(cds):
    
    cds.extend_node_rater_defined("cds", {
        "rationale": hx.Structure(children={
            "transaction_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Transaction Description and Summary of Target"},  async_input= ["generate_uw_doc"]),
            "knowledge_of_insured": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Knowledge of the Insured - List of DD Reports"},  async_input= ["generate_uw_doc"]),
            "reasons_for_writing_risk": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Reasons for writing the Risk"},  async_input= ["generate_uw_doc"]),
            "complex_considerations": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Unusual Or Complex Aspects of the Risk"},  async_input= ["generate_uw_doc"]),
            "exclusions_and_carve_outs": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Exclusions and Carve Outs"},  async_input= ["generate_uw_doc"]),
        }),
    })