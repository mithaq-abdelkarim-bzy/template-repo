import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers, experience_rating_max_years, max_data_layout, reinstatement_max_number, raw_data_max_column
import data_schema.sch_utilities as utils
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict
from data_schema.sch_rate_change import rarc_task_name

from data_schema.steer.sch_steer_risk_information import _steer_risk_info
from data_schema.steer.sch_steer_exposure import _steer_cd_all_curves, _steer_cd_commercial_auto_state, _steer_cd_cyber, _steer_cd_healthcare, _steer_cd_private_d_and_o


from data_schema.steer.sch_steer_exposure import _steer_exposure
from data_schema.steer.sch_steer_experience import (
    _steer_experience_on_levelling,
    _steer_experience_years,
    _steer_raw_data,
    _steer_data_format,
    _steer_data_format_other_field_children_nodes,
    _steer_raw_data_error,
    _steer_processed_claims,
    _steer_claims_movements,
    _steer_experience_rating_layers,
    _steer_data_format_column_display
)

def sch_steer(cds):
    return {
        cds.extend_node_rater_defined("cds", { 
            "steer": hx.Structure(children={
                "risk_information": hx.Structure(view={"label": "Risk Information"}, children={
                    ** _steer_risk_info(),
                }),
                "experience_rating": hx.Structure(view={"label": "Experience Rating"}, children={
                    ** _steer_experience_on_levelling(),
                    ** _steer_raw_data(),
                    ** _steer_data_format(),
                    ** _steer_raw_data_error(),
                    ** _steer_processed_claims(),
                    ** _steer_claims_movements(),
                    ** _steer_experience_rating_layers(), # includes triangles, claims count, burning cost
                }),
                "exposure_rating": hx.Structure(view={"label": "Exposure Rating"}, children={
                    ** _steer_exposure(),
                }),
                
            }),   
        })
    }

def sch_non_cds_steer():
    '''
    Non CDS nodes for display only
    '''
    return {
        "steer": hx.Structure(children={
            "experience_rating": hx.Structure(view={"label": "Experience Rating"}, children={
                # Display column - show and hide
                "column_display": hx.Structure(view={"label": "Column Name"}, children={
                    **_steer_data_format_column_display()
                }),
                "raw_data_column_names": hx.Structure(view={"label": "Raw Data Column Names"}, children={
                    f"column_{i:02d}": hx.Str(mode="output", view={"label": f"Column\n{i}"})
                    for i in range(1, raw_data_max_column+1)
                }),                
                
            }),
            "exposure_rating": hx.Structure(view={"label": "Exposure Rating"}, children={
                "curve_descriptions": hx.Structure(view={"label": "Curve Descriptions"}, children={
                    "all_curves":hx.List(mode="output", view={"label": "All Curves"}, children={
                        ** _steer_cd_all_curves(),
                    }),
                    "commercial_auto_state":hx.List(mode="output", view={"label": "Commercial Auto State"}, children={
                        ** _steer_cd_commercial_auto_state(),
                    }),
                    "cyber":hx.List(mode="output", view={"label": "ACyber"}, children={
                        ** _steer_cd_cyber(),
                    }),
                    "healthcare":hx.List(mode="output", view={"label": "Healthcare"}, children={
                        ** _steer_cd_healthcare(),
                    }),
                    "private_d_o":hx.List(mode="output", view={"label": "Private D&O"}, children={
                        ** _steer_cd_private_d_and_o(),
                    }),
                }),
            }),
        }),
    }



        


