import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import algorithms.rate_constants as constants


def generate_years_array(num_years):
    return [{'field': f"year_{i}", 'group': f"Pricing Year - {i}"} for i in range(1, num_years + 1)]


def sch_expiring(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            'expiring': hx.Structure(children=
                {
                    'rate_change': hx.List(
                        mode='input',
                        default_element_count=constants.DEFAULT_NUM_LOB,
                        async_input=["map_expiring_rate_change_task"],
                        async_output=["start_renewal_task"],
                        children={
                            'selected_lob': hx.Str(      mode='input', default=None, optionality='optional', view={'label': 'Selected Line\n of Business'}, async_input=["map_expiring_rate_change_task"], async_output=["start_renewal_task"]),
                            'year_0': hx.Structure(
                                children={
                                    'yoa':      hx.Str(  mode='input', default=None, optionality='optional', view={'label': 'YOA',                                      'group': 'Pricing Year'}, async_input=["map_expiring_rate_change_task"], async_output=["start_renewal_task"]),
                                    'facility': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'Facility', 'format': percent_format(2),    'group': 'Pricing Year'}, async_input=["map_expiring_rate_change_task"], async_output=["start_renewal_task"]),
                                    'source':   hx.Str(  mode='input', default_index=0, options=['Business Plan', 'Facility', 'Blend', 'None'], view={'label': 'Source','group': 'Pricing Year'}, async_input=["map_expiring_rate_change_task"], async_output=["start_renewal_task"]),
                                }
                            ),
                            **{
                                year['field']: hx.Structure(
                                    children={
                                        'yoa':      hx.Str(  mode='input', default=None, optionality='optional', view={'label': 'YOA',                                   'group': year['group']}, async_input=["map_expiring_rate_change_task"], async_output=["start_renewal_task"]),
                                        'facility': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'Facility', 'format': percent_format(2), 'group': year['group']}, async_input=["map_expiring_rate_change_task"], async_output=["start_renewal_task"]),
                                    }
                                ) for year in generate_years_array(constants.YEARS_TO_CONSIDER_IN_RATE_CHANGE-1)
                            }
                        }
                    )
                }
            )        
        }
    )
