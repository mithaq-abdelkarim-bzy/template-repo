import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format, create_node
from algorithms import rate_constants as constants


def core_ids():
    as_o = []
    return {

            'lob_number':               hx.Int(  mode='output',   async_output = as_o, view={'label': 'Number of Line of Business'}),
            'risk_code':                hx.Str(  mode='output',   async_output = as_o, view={'label': 'Risk Code'}),
            'selected_lob':             hx.Str(  mode='output',   async_output = as_o, view={'label': 'Selected\nLine of\nBusiness'}),
            'lookup_lob':               hx.Str(  mode='output',   async_output = as_o, view={'label': 'Lookup LOB'}),
    }


def generate_risk_detail_row(is_total):
    as_o  = []
    nodes = {
        'yoa':                              hx.Str(  mode='output',     async_output = as_o, view={'label': 'YoA'}),
        'latest_gpi':                       hx.Float(mode='output',     async_output = as_o, view={'label': 'Latest\nGPI',                'format': thousands_format(0),    'group': 'Current Position'}),
        'latest_gnpi':                      hx.Float(mode='output',     async_output = as_o, view={'label': 'Latest\nGNPI',               'format': thousands_format(0),    'group': 'Current Position'}),
        'latest_paid':                      hx.Float(mode='output',     async_output = as_o, view={'label': 'Latest\nPaid',               'format': thousands_format(0),    'group': 'Current Position'}),
        'latest_incurred':                  hx.Float(mode='output',     async_output = as_o, view={'label': 'Latest\nIncurred',           'format': thousands_format(0),    'group': 'Current Position'}),
        'acquisition_ratio':                hx.Float(mode='output',     async_output = as_o, view={'label': 'Acquisition\ncosts %',       'format': percent_format(2),      'group': 'Current Position'}),
        'incurred_loss_ratio':              hx.Float(mode='output',     async_output = as_o, view={'label': 'Incurred\nLoss ratio',       'format': percent_format(2),      'group': 'Current Position'}),

        'ultimate_gnpi':                    hx.Float(mode='output',     async_output = as_o, view={'label': 'Ultimate\nGNPI',             'format': thousands_format(0),    'group': 'Premiums'}),
        'ultimate_gnpi_ol_model':           hx.Float(mode='output',     async_output = as_o, view={'label': 'Ultimate\nGNPI\nOn-level\nDefault',    'format': thousands_format(0),    'group': 'Premiums'}),
        'ultimate_gnpi_ol_selected':        hx.Float(mode='output',     async_output = as_o, view={'label': 'Ultimate\nGNPI\nOn-level\nSelected',   'format': thousands_format(0),    'group': 'Premiums'}),

        'ultimate_cl_paid':                 hx.Float(mode='output',     async_output = as_o, view={'label': 'CL Ultimate\nPaid',          'format': thousands_format(0),    'group': 'Ultimate - CL'}),
        'ultimate_cl_paid_ulr':             hx.Float(mode='output',     async_output = as_o, view={'label': 'CL ULR\nPaid',               'format': percent_format(2),      'group': 'Ultimate - CL'}),
        'ultimate_cl_incurred':             hx.Float(mode='output',     async_output = as_o, view={'label': 'CL Ultimate\nIncurred',      'format': thousands_format(0),    'group': 'Ultimate - CL'}),
        'ultimate_cl_incurred_ulr':         hx.Float(mode='output',     async_output = as_o, view={'label': 'CL ULR\nIncurred',           'format': percent_format(2),      'group': 'Ultimate - CL'}),

        'ultimate_ielr_model':              hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nIncurred',            'format': thousands_format(0),    'group': 'Ultimate - IELR'}),
        'ultimate_ielr_model_ulr':          hx.Float(mode='output',     async_output = as_o, view={'label': 'IELR \nModel',               'format': percent_format(2),      'group': 'Ultimate - IELR'}),
        'ultimate_ielr_selected':           hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected\nIncurred',         'format': thousands_format(0),    'group': 'Ultimate - IELR'}),
        'ultimate_ielr_selected_ulr':       hx.Float(mode='output',     async_output = as_o, view={'label': 'IELR\nSelected',             'format': percent_format(2),      'group': 'Ultimate - IELR'}),

        'ultimate_bf_model_paid':           hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nPaid',                'format': thousands_format(0),    'group': 'Ultimate - BF'}),
        'ultimate_bf_model_incurred':       hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nIncurred',            'format': thousands_format(0),    'group': 'Ultimate - BF'}),
        'ultimate_bf_selected_paid':        hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected\nPaid',             'format': thousands_format(0),    'group': 'Ultimate - BF'}),
        'ultimate_bf_selected_incurred':    hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected\nIncurred',         'format': thousands_format(0),    'group': 'Ultimate - BF'}),

        'ultimate_model':                   hx.Float(mode='output',     async_output = as_o, view={'label': 'Model Ult.\nIncurred',       'format': thousands_format(0),    'group': 'Ultimate - Method Blend'}),
        'ultimate_model_ulr':               hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nUlt. ULR',            'format': percent_format(2),      'group': 'Ultimate - Method Blend'}),
        'ultimate_selected':                hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected Ult.\nIncurred',    'format': thousands_format(0),    'group': 'Ultimate - Method Blend'}),
        'ultimate_selected_ulr':            hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected\nUlt. ULR',         'format': percent_format(2),      'group': 'Ultimate - Method Blend'}),

        'on_levelled_model_ulr':            hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nULR',                 'format': percent_format(2),      'group': 'On Levelled'}),
        'on_levelled_selected_ulr':         hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected\nULR',              'format': percent_format(2),      'group': 'On Levelled'}),
    }

    nodes_without_totals = {
        
        **core_ids(),
 
        'dev_patterns_gnpi':                hx.Float(mode='override',   async_output = as_o, view={'label': 'GNPI',                       'format': percent_format(2),      'group': 'Development Patterns'}),
        'dev_patterns_paid':                hx.Float(mode='override',   async_output = as_o, view={'label': 'Paid',                       'format': percent_format(2),      'group': 'Development Patterns'}),
        'dev_patterns_incurred':            hx.Float(mode='override',   async_output = as_o, view={'label': 'Incurred',                   'format': percent_format(2),      'group': 'Development Patterns'}),

        'weighting_ielr':                   hx.Float(mode='override',   async_output = as_o, view={'label': 'IELR\nWeighting',            'format': percent_format(1)}),
        'method_paid':                      hx.Str(  mode='override',   async_output = as_o, view={'label': 'Method\nPaid'}),
        'method_incurred':                  hx.Str  (mode='override',   async_output = as_o, view={'label': 'Method\nIncurred'}),

        'inflation_model':                  hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nInflation',           'format': percent_format(2)}),
        'rate_change_model':                hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nRate Change',         'format': percent_format(2)}),
        'rate_change_selected':             hx.Float(mode='override',   async_output = as_o, view={'label': 'Selected\nRate Change',      'format': percent_format(2)}),

        'inflation_model_index':            hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nInflation\nIndex',     'format': percent_format(2)}),
        'rate_change_model_index':          hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nRate Change\nIndex',   'format': percent_format(2)}),
        'rate_change_selected_index':       hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected\nRate Change\nIndex','format': percent_format(2)}),
        'loss_ratio_model_index':           hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nLoss Ratio\nIndex',    'format': percent_format(2)}),
        'loss_ratio_selected_index':        hx.Float(mode='output',     async_output = as_o, view={'label': 'Selected\nLoss Ratio\nIndex', 'format': percent_format(2)}),

        'weighting_model':                  hx.Float(mode='output',     async_output = as_o, view={'label': 'Model\nWeighting',           'format': percent_format(1)}),
        'weighting_selected':               hx.Float(mode='override',   async_output = as_o, view={'label': 'Selected\nWeighting',        'format': percent_format(1)}),

        'weighting_1_exposure_onlevel':     hx.Float(mode='output',     async_output = as_o, view={'label': 'Exposure -\nweighting 1',    'format': percent_format(1),      'group': 'Weighting\nOn-level'}),
        'weighting_2_decay_ratio':          hx.Float(mode='output',     async_output = as_o, view={'label': 'Decay Ratio -\nweighting 2', 'format': percent_format(1),      'group': 'Weighting\nOn-level'}),
        'weighting_3_developed':            hx.Float(mode='output',     async_output = as_o, view={'label': '% Develop -\nWeighting 3',   'format': percent_format(1),      'group': 'Weighting\nOn-level'}),
        'weighting_onlevel':                hx.Float(mode='output',     async_output = as_o, view={'label': 'Onlevel \nWeighting',   'format': percent_format(1),      'group': 'Weighting\nOn-level'}),

        'weighting_1_exposure_nominal':     hx.Float(mode='output',     async_output = as_o, view={'label': 'Exposure -\nweighting 1',    'format': percent_format(1),      'group': 'Weighting\nNominal'}),
        'weighting_nominal':                hx.Float(mode='output',     async_output = as_o, view={'label': 'Nominal \nWeighting',   'format': percent_format(1),      'group': 'Weighting\nNominal'}),
        
        # to control views
        'is_row_visible':           hx.Bool (mode='output',   async_output = as_o, view={'label': 'is_row_visible'}),
        'lob_visible_1':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_1'}),
        'lob_visible_2':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_2'}),
        'lob_visible_3':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_3'}),
        'lob_visible_4':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_4'}),
        'lob_visible_5':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_5'}),


    }

    if not is_total:
        nodes.update(nodes_without_totals)

    return nodes




def generate_risk_summary_row():
    as_o = []
    return {

            **core_ids(),

            'bp_class':                 hx.Str(  mode='output',   async_output = as_o, view={'label': 'Beazley\nBusiness\nPlan class'}),
            'tracker_class':            hx.Str(  mode='output',   async_output = as_o, view={'label': 'Tracker\nClass'}),
            'projection_type':          hx.Str(  mode='input',    async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'Projection\nType', "options": {"read_only_option": {"read_only": True}}},       default_index=0, options=['Incurred',     'Paid']),
            'ielr_approach':            hx.Str(  mode='input',    async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'IELR Method\n& Weights'}, default_index=1, options=['Nominal',      'On-level']),

            # the next 3 nodes are needed for beazley projection but given we do together with lloyds they are included for both
            'ielr_source':              hx.Str(  mode='input',    async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'Selected\nIELR Source'},  default_index=0, options=['Beazley Data', 'Lloyds Data']),
            'cat_lr_source':            hx.Str(  mode='input',    async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'GN Cat\nULR Source'},     default_index=0, options=['Experience',   'Business Plan']),
            'lloyds_ielr':              hx.Float(mode='output',   async_output = as_o, view={'label': 'Lloyds IELR',                    'format': percent_format(2)}),

            'composition':              hx.Float(mode='output',   async_output = as_o, view={'label': 'Composition',                    'format': percent_format(2)}),

            'model_ielr_nominal':       hx.Float(mode='output',   async_output = as_o, view={'label': 'Model Default IELR - Nominal',   'format': percent_format(2), 'group': 'Model Default'}),
            'model_ielr_onlevel':       hx.Float(mode='output',   async_output = as_o, view={'label': 'Model Default IELR - On-Level',  'format': percent_format(2), 'group': 'Model Default'}),
            'model_ielr_ol_allyr':      hx.Float(mode='output',   async_output = as_o, view={'label': 'Model Default IELR - On-level All yr', 'format': percent_format(2), 'group': 'Model Default'}),

            'model_ielr':               hx.Float(mode='output',   async_output = as_o, view={'label': 'Model Default\nIELR - Incurred',  'format': percent_format(2), 'group': 'Model Default'}),
            'model_gn_ulr':             hx.Float(mode='output',   async_output = as_o, view={'label': 'GN ULR',                          'format': percent_format(2), 'group': 'Model Default'}),
            'model_base_aqn':           hx.Float(mode='output',   async_output = as_o, view={'label': 'Base Aqn',                        'format': percent_format(2), 'group': 'Model Default'}),
            'model_acc_aqn':            hx.Float(mode='output',   async_output = as_o, view={'label': 'Account Aqn',                     'format': percent_format(2)}),
            'model_adj_gn_ulr':         hx.Float(mode='output',   async_output = as_o, view={'label': 'GN ULR Acc Aqn',                  'format': percent_format(2), 'group': 'Model Default'}),
            'model_final_gn_ulr':       hx.Float(mode='output',   async_output = as_o, view={'label': 'Final GN ULR',                    'format': percent_format(2), 'group': 'Model Default'}),

            'selected_ielr':            hx.Float(mode='override', async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'Selected\nIELR - Incurred',       'format': percent_format(2), 'group': 'Selected'}),
            'selected_gn_ulr':          hx.Float(mode='output',   async_output = as_o, view={'label': 'GN ULR',                          'format': percent_format(2), 'group': 'Selected'}),
            'selected_base_aqn':        hx.Float(mode='output',   async_output = as_o, view={'label': 'Base Aqn',                        'format': percent_format(2), 'group': 'Selected'}),
            'selected_acc_aqn':         hx.Float(mode='output',   async_output = as_o, view={'label': 'Account Aqn',                     'format': percent_format(2), 'group': 'Selected'}),
            'selected_adj_gn_ulr':      hx.Float(mode='output',   async_output = as_o, view={'label': 'GN ULR Acc Aqn',                  'format': percent_format(2), 'group': 'Selected'}),
            'selected_final_gn_ulr':    hx.Float(mode='output',   async_output = as_o, view={'label': 'Final GN ULR',                    'format': percent_format(2), 'group': 'Selected'}),

            'bp_cat':                   hx.Bool( mode='input',    async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'Apply BP \nCat ULR?', 'group': 'Selected'},   default=False),
            'bp_cat_load':              hx.Float(mode='override', async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'BP Cat Load',                   "format":percent_format(2), 'group': 'Selected'}),


            'actuarial_notes':          hx.Str(  mode='input',    async_output = as_o, async_input = ["sync_lob_lists_task"], view={'label': 'Actuarial Notes'},       default=None, optionality='optional',),

        # to control views
            'is_row_visible':           hx.Bool (mode='output',   async_output = as_o, view={'label': 'is_row_visible'}),
            'lob_visible_1':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_1'}),
            'lob_visible_2':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_2'}),
            'lob_visible_3':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_3'}),
            'lob_visible_4':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_4'}),
            'lob_visible_5':            hx.Bool( mode='output',   async_output = as_o, view={'label': 'lob_visible_5'}),

            'comments':                 hx.Str(  mode='input',    async_output = as_o, view={'label': 'Comments'},              default=None, optionality='optional'),
            'checked':                  hx.Bool( mode='input',    async_output = as_o, view={'label': 'Checked'},               default=False),

            # we want the totals stored here
            **generate_risk_detail_row(True)

        }


def chart_list():
    as_i = ['calculate_profit_commission_task']
    as_o = []
    return {
        "chart_data"             : hx.List( mode="output", async_output=as_o, async_input=as_i, children={
            'yoa':                          create_node('YoA',           mode='output', type='str',                   async_output=as_o, async_input=as_i),
            'incurred_loss_ratio':          create_node('Total ILR',     mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i),
            'ultimate_selected_ulr':        create_node('Total ULR',     mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i),
            'on_levelled_selected_ulr':     create_node('Total ULR - OL',mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i),        
            'pricing_basis':                create_node('Total LR - Sel',mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i)
        })}

 
def sch_projections_lloyds(cds):
    as_o                = []
    as_i                = []
    row                 = {"row": hx.Int(mode="output")}
    detail_table_rows   = constants.DEFAULT_NUM_RISK_CODES * constants.YEARS_TO_CONSIDER_IN_LLOYDS_PROJECTIONS
    summary_table_rows  = constants.DEFAULT_NUM_RISK_CODES
    
    cds.extend_node_rater_defined(
        'cds',
        {'projections_lloyds': hx.Structure(
                children={
                    'error_msg':        hx.Str(  mode='output'),
                    'show_all_yrs':     hx.Bool( mode='input', default=False,                        view={"label": 'Show All Years'}, async_output=as_o, async_input=as_i),   
                    'show_all_lobs':    hx.Bool( mode='input', default=False,                        view={"label": 'Show All LOBs'},  async_output=as_o, async_input=as_i), #JB: consider deleting not used
                    'lookup_lob_1':     hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected Line (1)"},   options_data=f"../drop_down_lobs",   options_field="lookup_lob", async_output=as_o, async_input=as_i),
                    'lookup_lob_2':     hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected Line (2)"},   options_data=f"../drop_down_lobs",   options_field="lookup_lob", async_output=as_o, async_input=as_i),
                    'lookup_lob_3':     hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected Line (3)"},   options_data=f"../drop_down_lobs",   options_field="lookup_lob", async_output=as_o, async_input=as_i),
                    'drop_down_lobs':   hx.List( mode="output",        children={ 'lookup_lob': hx.Str(mode="output")}),             ### notice children

                    'summary_table': hx.List(   mode='input',      
                                                default_element_count= summary_table_rows, 
                                                async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                children={**generate_risk_summary_row()}),
                    'detail_table':  hx.List(   mode='input',      
                                                default_element_count= detail_table_rows,
                                                async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                children={**generate_risk_detail_row(False)}),

                    'selected_lob_totals_1':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_2':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_3':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_4':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_5':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),

                }
            )
        }
    )


def sch_projections_beazley(cds):
    as_o                = []
    as_i                = []
    row                 = {"row": hx.Int(mode="output")}
    detail_table_rows   = constants.DEFAULT_NUM_RISK_CODES * constants.YEARS_TO_CONSIDER_IN_LLOYDS_PROJECTIONS
    summary_table_rows  = constants.DEFAULT_NUM_RISK_CODES
    
    cds.extend_node_rater_defined(
        'cds',
        {'projections_beazley': hx.Structure(
                children={
                    'error_msg':        hx.Str(  mode='output'),
                    'show_all_yrs':     hx.Bool( mode='input', default=False,                        view={"label": 'Show All Years'}, async_output=as_o, async_input=as_i),   
                    'show_all_lobs':    hx.Bool( mode='input', default=False,                        view={"label": 'Show All LOBs'},  async_output=as_o, async_input=as_i), #JB: consider deleting not used
                    'lookup_lob_1':     hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected Line (1)"},   options_data=f"../drop_down_lobs",   options_field="lookup_lob", async_output=as_o, async_input=as_i),
                    'lookup_lob_2':     hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected Line (2)"},   options_data=f"../drop_down_lobs",   options_field="lookup_lob", async_output=as_o, async_input=as_i),
                    'lookup_lob_3':     hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected Line (3)"},   options_data=f"../drop_down_lobs",   options_field="lookup_lob", async_output=as_o, async_input=as_i),
                    'drop_down_lobs':   hx.List( mode="output",        children={ 'lookup_lob': hx.Str(mode="output")}),             ### notice children

                    'summary_table': hx.List(   mode='input',      
                                                default_element_count= summary_table_rows, 
                                                async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                children={**generate_risk_summary_row()}),
                    'detail_table':  hx.List(   mode='input',      
                                                default_element_count= detail_table_rows,
                                                async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                children={**generate_risk_detail_row(False)}),

                    'selected_lob_totals_1':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_2':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_3':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_4':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),
                    'selected_lob_totals_5':                hx.Structure(   children={ **core_ids(), **generate_risk_detail_row(True), **chart_list(), **row    }),

                }
            )
        }
    )