import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_check_async(cds):
        
    # Extending cds nodes for RMS
    cds.extend_node_rater_defined("cds", {
        "sch_check_async": hx.Structure(children={

            "experience_premium"     : hx.Float(mode="output", view={"label": "experience_premium"},                                            async_output=["bi_clm_and_mvmt_exc_triangles_fetch_task"]),
            "experience_signed_line"    : hx.Float(mode="output", view={"label": "experience_signed_line"},                                     async_output=["bi_clm_and_mvmt_exc_triangles_fetch_task"]),
            "experience_deductions"     : hx.Float(mode="output",   view={"label": "experience_deductions"},                                      async_output=["bi_clm_and_mvmt_exc_triangles_fetch_task"]),

            "exposure_premium"     : hx.Float(mode="output",     view={"label": "exposure_premium"},                                            async_output=["run_bordereau_rater_task"]),
            "exposure_signed_line"    : hx.Float(mode="output",  view={"label": "exposure_signed_line"},                                        async_output=["run_bordereau_rater_task"]),
            "exposure_deductions"     : hx.Float(mode="output",  view={"label": "exposure_deductions"},                                         async_output=["run_bordereau_rater_task"]),

            "pc_premium"     : hx.Float(mode="output", view={"label": "pc_premium"},                      async_output=["simulate_pc_task"]),
            "pc_signed_line"    : hx.Float(mode="output",   view={"label": "pc_signed_line"},             async_output=["simulate_pc_task"]),
            "pc_deductions"     : hx.Float(mode="output",   view={"label": "pc_deduction"},               async_output=["simulate_pc_task"]),
            "pc_pc"     : hx.Float(mode="output",   view={"label": "pc_pc"},                              async_output=["simulate_pc_task"]),
            "pc_uw_expense"     : hx.Float(mode="output", view={"label": "pc_uw_expense"},                async_output=["simulate_pc_task"]),

   
        })
    })
