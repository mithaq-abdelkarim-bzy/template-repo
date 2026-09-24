import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, create_node
from algorithms import parameter_tables_schema as params
import algorithms.rate_constants as constants


def generate_common_nodes(mode='input', format=thousands_format(0), type='float', default=None):
    nodes = {}
    # additional_tasks = []
    # additional_tasks = []
    # async_input_tasks = ["calculate_profit_commission_task"]
    # async_output_tasks = []

    # if mode == 'input':
    #     async_input_tasks += additional_tasks
    # else:
    #     async_output_tasks += additional_tasks

    for i in range(1, constants.NUM_CURVES_IN_CAT + 1):
        nodes[f'curve_{i}'] = create_node(f"Curve {i}", mode=mode, format=format, type=type, async_input=["calculate_profit_commission_task"], default=default)
        nodes[f'curve_{i}_cnv'] = create_node(
            f"Curve {i} CNV", 
            'output', 
            format=format, 
            type=type
        )
    return nodes


def generate_dropdown_nodes(format=thousands_format(0)):
    nodes = {}
    for i in range(1, constants.NUM_CURVES_IN_CAT + 1):
        nodes[f'curve_{i}'] = hx.Str(
            mode='input',
            default=None,
            optionality='optional',
            options_data=f"../selected_class_drop_down_{i}",
            options_field="selected_lob",
            view={"label": f"Curve {i}", "format": format},
            async_input=['calculate_profit_commission_task']
        )
        nodes[f'selected_class_drop_down_{i}'] = hx.List(
            mode="output",
            children={"selected_lob": hx.Str(mode="output")}
        )
        nodes[f'curve_{i}_cnv'] = hx.Str(
            mode='output',
            view={"label": f"Curve {i} CNV", "format": format}
        )
    return nodes

def generate_probability_structures():
    probabilities = [
        10000, 5000, 1000, 500, 250, 200, 100, 50, 30, 10, 5, 2
    ]

    return {
        f'one_in_{prob}': hx.Structure(children={
            'critical_prob': create_node(
                "Critical Prob", 
                mode='output', 
                format=percent_format(2), 
                async_input=['calculate_profit_commission_task']
            ),
            'return_period': create_node(
                "Return Period", 
                mode='input', 
                async_input=[]
            ),
            **generate_common_nodes("input")
        })
        for prob in probabilities
    }


def sch_cat(cds):
    
    note1 = (
        """Inflation and Rate Change Roll-forward
            - This functionality for the rater will roll-forward the implied CAT ULR to the pricing year. If the modelling provided and the premium against this already reflects the latest view of inflation and rate change, then this should be set to No. Otherwise inflation and rate change needs to apply to roll the CAT ULR to be on the same basis as all other projections.
        """)
    note2 = (
        """EP Curves
            - If an "All Perils" curve is available from the CAT modelling, please ONLY enter the All Perils curve and exclude individual peril curves. 
            - If ONLY individual peril curves are available then please enter them in the order of the EP curve's severity from left to write. In the In-Force premium field please enter the TOTAL in-force premium for the class of business against each Peril curve.
        """)


    cds.extend_node_rater_defined(
        "cds",
        {
            "cat": hx.Structure(
                children={
                    'modelling_as_at_date': hx.Date(mode='input', view={'label': 'Modelling As At Date'},               default=None, optionality='optional',                                  async_input=[]),
                    'currency':             hx.Str( mode='input', view={'label': 'Currency'},                           default='USD', options_column="ccy", options_table="table_currency", async_input=[]),
                    'note_1':               hx.Str( mode='input', view={"options": {"read_only": {"read_only": True}}}, default=note1),
                    'note_2':               hx.Str( mode='input', view={"options": {"read_only": {"read_only": True}}}, default=note2),
                    
                    'curve_label':          hx.Structure(view={'label': 'Curve Label'},             children=generate_common_nodes(type='str'                               )),
                    'model':                hx.Structure(view={'label': 'Model'},                   children=generate_common_nodes(type='str'                               )),
                    'aal':                  hx.Structure(view={'label': 'AAL'},                     children=generate_common_nodes(                                         )),
                    'standard_deviation':   hx.Structure(view={'label': 'Standard Deviation'},      children=generate_common_nodes(                                         )),
                    'cov':                  hx.Structure(view={'label': 'CoV'},                     children=generate_common_nodes(mode="output", format=percent_format(1)  )),
                    'gn_in_force_premium':  hx.Structure(view={'label': 'GN In-Force Premium'},     children=generate_common_nodes(                                         )),
                    'unadjusted_gn_cat_ulr':hx.Structure(view={'label': 'Unadjusted GN CAT ULR %'}, children=generate_common_nodes(mode="output", format=percent_format(1)  )),
                    'roll_forward':         hx.Structure(view={'label': 'Roll-Forward?'},           children=generate_common_nodes(type='bool', mode='input', default=True  )),
                    'inflation_factor':     hx.Structure(view={'label': 'Inflation Factor'},        children=generate_common_nodes(mode="override", format=percent_format(1))),
                    'rate_change_factor':   hx.Structure(view={'label': 'Rate Change Factor'},      children=generate_common_nodes(mode="override", format=percent_format(1))),
                    'selected_gn_cat_ulr':  hx.Structure(view={'label': 'Selected GN CAT ULR %'},   children=generate_common_nodes(mode="override", format=percent_format(1))),
                    'selected_class':       hx.Structure(view={'label': 'Selected Class'},          children=generate_dropdown_nodes(                                       )),

                    **generate_probability_structures()

                }
            )
        }
    )
