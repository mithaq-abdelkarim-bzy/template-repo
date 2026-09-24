import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import algorithms.rate_constants as constants


def generate_years_array(num_years):
    return [{'field': f"year_{i}", 'group': f"Pricing Year - {i}"} for i in range(1, num_years + 1)]


def sch_rate_change(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            'rate_change': hx.List(
                mode='input',
                default_element_count=constants.DEFAULT_NUM_LOB,
                async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                async_input=["start_renewal_task"],
                children={
                    'selected_lob': hx.Str(mode='output', view={'label': 'Selected Line\n of Business'}, async_input=["map_expiring_rate_change_task"]),
                    'dominant_risk_code': hx.Str(mode='output', view={'label': 'Dominant Risk\n Code'}, async_input=[]),
                    'bp_class': hx.Str(mode='output', view={'label': 'BP Class'}, async_input=[]),
                    'is_row_visible': hx.Bool(mode='output', async_input=[]),
                    'year_0': hx.Structure(
                        children={
                            'yoa': hx.Str(mode='output', view={'label': 'YOA', 'group': 'Pricing Year'}, async_input=[]),
                            'facility': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'Facility', 'format': percent_format(2), 'group': 'Pricing Year'}, async_input=["sync_lob_lists_task", "start_renewal_task"], async_output=[{"task": "map_expiring_rate_change_task", "reset": False}]),
                            'bp_rate_change': hx.Float(mode='output', view={'label': 'Business Plan\n Rate Change', 'format': percent_format(2), 'group': 'Pricing Year'}, async_input=[]),
                            'bp_rarc_margin': hx.Float(mode='output', view={'label': 'Business Plan\n RARC Margin', 'format': percent_format(2), 'group': 'Pricing Year'}, async_input=[]),
                            'source': hx.Str(mode='input', options=['Business Plan', 'Facility', 'Blend', 'None'], default_index=0, view={'label': 'Source', 'group': 'Pricing Year'}, async_input=["sync_lob_lists_task", "start_renewal_task"]),
                            'selected': hx.Float(mode='output', view={'label': 'Selected', 'format': percent_format(2), 'group': 'Pricing Year'}, async_input=[]),
                            'blend_effective_rate_change': hx.Float(mode='output', async_input=[]),
                        }
                    ),
                    **{
                        year['field']: hx.Structure(
                            children={
                                'yoa': hx.Str(mode='output', view={'label': 'YOA', 'group': year['group']}, async_input=[]),
                                'facility': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'Facility', 'format': percent_format(2), 'group': year['group']}, async_input=["sync_lob_lists_task", "start_renewal_task"], async_output=[{"task": "map_expiring_rate_change_task", "reset": False}]),
                                'beazley_group_achieved': hx.Float(mode='output', view={'label': 'Beazley Group\n Achieved', 'format': percent_format(2), 'group': year['group']}, async_input=[]),
                                'selected': hx.Float(mode='output', view={'label': 'Selected', 'format': percent_format(2), 'group': year['group']}, async_input=[]),
                            }
                        ) for year in generate_years_array(constants.YEARS_TO_CONSIDER_IN_RATE_CHANGE-1)
                    }
                }
            ),

            'rate_change_summary': hx.Structure(
                view={"label": "Total"},
                children={
                    'year_0': hx.Structure(
                        children={
                            'facility': hx.Float(mode='output', view={'label': 'Facility', 'format': percent_format(2), 'group': 'Pricing Year'}),
                            'bp_rate_change': hx.Float(mode='output', view={'label': 'Business Plan\n Rate Change', 'format': percent_format(2), 'group': 'Pricing Year'}, async_input=[]),
                            'bp_rarc_margin': hx.Float(mode='output', view={'label': 'Business Plan\n Rate Change', 'format': percent_format(2), 'group': 'Pricing Year'}, async_input=[]),
                            'selected': hx.Float(mode='output', view={'label': 'Selected', 'format': percent_format(2), 'group': 'Pricing Year'}, async_input=[]),
                            'bp_rarc_margin_info': hx.Str(mode='output'),
                        }
                    ),
                    **{
                        year['field']: hx.Structure(
                            children={
                                'facility': hx.Float(mode='output', view={'label': 'Facility', 'format': percent_format(2), 'group': year['group']}),
                                'beazley_group_achieved': hx.Float(mode='output', view={'label': 'Beazley Group\n Achieved', 'format': percent_format(2), 'group': year['group']}, async_input=[]),
                                'selected': hx.Float(mode='output', view={'label': 'Selected', 'format': percent_format(2), 'group': year['group']}, async_input=[]),
                            }
                        ) for year in generate_years_array(constants.YEARS_TO_CONSIDER_IN_RATE_CHANGE-1)
                    }
                }
            )
        }
    )
