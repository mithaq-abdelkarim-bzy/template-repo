import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, create_node
from algorithms import rate_constants as constants

def generate_common_nodes(is_summary):
    
    # define the async inputs and outputs
    as_i = ['calculate_profit_commission_task']
    as_o = []

    # define the group names
    grp_prem_lat            = "Premium Current Position"
    grp_inc_cy_op           = "Open Incurred Claims (undeveloped)"
    grp_inc_cy_cl           = "Closed Incurred Claims (undeveloped)"
    grp_inc_cy_all          = "Total Incurred Claims (undeveloped)"
    grp_inc_py_all          = "Last Year's\nPosition"
    grp_inc_mvmt            = "Movement"
    grp_gn_ilr              = "GN ILR %"
    grp_dev_pat             = "Development Pattern"
    grp_prem_ult            = "Ultimate Premium - Selected"
    grp_ult_inc_mthd_ielr   = "IELR - Ultimate Incurred"
    grp_ult_inc_mthd_bf     = "BF - Ultimate Incurred"
    grp_ult_inc_mthd_cl     = "CL - Ultimate Incurred"
    grp_ult_inc_ielr_wgt    = "IELR Weighting"
    grp_ibnr_add            = "Additional IBNR \n(Additive to Ultimate Incurred - Selected)"
    grp_ult_inc_sel         = "Selected Ultimate"
    grp_ult_ulr_sel         = "Selected ULR"
    grp_ult_inc_sel_wgt     = "Selected Model Weighting"
    grp_ult_ulr_sel_ol      = "On-Levelled"
    grp_adj                 = "Adjustments"
    grp_view                = "Booleans for view control"
    grp_inc_ind             = "Incremental Indices"
    grp_cum_ind             = "Cumulative Indices"
    grp_wgt_nominal         = "Weighting Nominal"
    grp_wgt_ol              = "Weighting On-level"

    # nested function to calculate correct mode allowing for provided mode and whether it is summary or detail
    def computed_mode(inner_mode):
        return 'output' if is_summary else inner_mode


    # nested function to calculate all the nodes for a given split - attritional/large/cat/total
    def alct_nodes(k,v):
        k = str(k)
        v = str(v)
        return{
            f'latest_incurred_open_claims_{k}':     create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_inc_cy_op,         async_output=as_o, async_input=as_i),
            f'latest_incurred_closed_claims_{k}':   create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_inc_cy_cl,         async_output=as_o, async_input=as_i),
            f'latest_incurred_total_claims_{k}':    create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_inc_cy_all,        async_output=as_o, async_input=as_i),
            f'last_year_position_{k}':              create_node(v,  mode=computed_mode('input'),    format=thousands_format(0), default=0, group=grp_inc_py_all,        async_output=as_o, async_input=as_i),
            f'movement_{k}':                        create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_inc_mvmt,          async_output=as_o, async_input=as_i),
            f'gn_ilr_{k}':                          create_node(v,  mode=computed_mode('output'),   format=percent_format(1),   default=0, group=grp_gn_ilr,            async_output=as_o, async_input=as_i),
            f'ultimate_incurred_ielr_{k}':          create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_ult_inc_mthd_ielr, async_output=as_o, async_input=as_i),        
            f'ultimate_incurred_bf_{k}':            create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_ult_inc_mthd_bf,   async_output=as_o, async_input=as_i),
            f'ultimate_incurred_cl_{k}':            create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_ult_inc_mthd_cl,   async_output=as_o, async_input=as_i),       
            f'ielr_weighting_cl_{k}':               create_node(v,  mode=computed_mode('override'), format=percent_format(2),   default=0, group=grp_ult_inc_ielr_wgt,  async_output=as_o, async_input=as_i),
            f'ultimate_incurred_selected_{k}':      create_node(v,  mode=computed_mode('override'), format=thousands_format(0), default=0, group=grp_ult_inc_sel,       async_output=as_o, async_input=as_i),
            f'ultimate_ulr_selected_{k}':           create_node(v,  mode=computed_mode('output'),   format=percent_format(1),   default=0, group=grp_ult_ulr_sel,       async_output=as_o, async_input=as_i),
            f'ultimate_ulr_on_levelled_{k}':        create_node(v,  mode=computed_mode('output'),   format=percent_format(1),   default=0, group=grp_ult_ulr_sel_ol,    async_output=as_o, async_input=as_i),
            f'ielr_weighting_sel_{k}':              create_node(v,  mode=computed_mode('override'), format=percent_format(2),   default=0, group=grp_ult_inc_sel_wgt,   async_output=as_o, async_input=as_i)
        }
    
    def xcat_nodes(k,v):
        k = str(k)
        v = str(v)
        return{
            f'ultimate_incurred_selected_{k}':      create_node(v,  mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_ult_inc_sel,       async_output=as_o, async_input=as_i),
            f'ultimate_ulr_selected_{k}':           create_node(v,  mode=computed_mode('output'),   format=percent_format(1),   default=0, group=grp_ult_ulr_sel,       async_output=as_o, async_input=as_i),
            f'ultimate_ulr_on_levelled_{k}':        create_node(v,  mode=computed_mode('output'),   format=percent_format(1),   default=0, group=grp_ult_ulr_sel_ol,    async_output=as_o, async_input=as_i)
        }


    nodes = {
        'lob_number':                                       create_node('Number of Line of Business', mode='output', type='int', async_output=as_o, async_input=as_i),
        'selected_lob':                                     create_node('Selected Line of Business',  mode='output', type='str', async_output=as_o, async_input=as_i),
        'yoa':                                              create_node('YoA',                                                    mode=computed_mode('output'), type='str',                                     async_output=as_o, async_input=as_i),
        'latest_gpi':                                       create_node('Latest\nGPI',                                            mode=computed_mode('output'), format=thousands_format(0), group=grp_prem_lat, async_output=as_o, async_input=as_i),
        'latest_gnpi':                                      create_node('Latest\nGNPI',                                           mode=computed_mode('output'), format=thousands_format(0), group=grp_prem_lat, async_output=as_o, async_input=as_i),
        'acquisition_costs':                                create_node('Acquisition\nCosts %',                                   mode=computed_mode('output'), format=percent_format(1),   group=grp_prem_lat, async_output=as_o, async_input=as_i),

        'ultimate_premium_selected_gnpi_cl':                create_node("Ultimate\nGNPI -\nCL",              mode=computed_mode('output'),                            group=grp_prem_ult, async_output=as_o, async_input=as_i),
        'ultimate_premium_selected_gnpi_override':          create_node("Ultimate\nGNPI -\nOverride",        mode=computed_mode('input'), format=thousands_format(0), group=grp_prem_ult, async_output=as_o, async_input=as_i),
        'ultimate_premium_selected_gnpi_selected':          create_node("Ultimate\nGNPI -\nSelected",        mode=computed_mode('output'),                            group=grp_prem_ult, async_output=as_o, async_input=as_i),
        'ultimate_premium_selected_gnpi_selected_ol':       create_node("Ultimate\nGNPI\nOn-level\nSelected",mode=computed_mode('output'), format=thousands_format(0),group=grp_prem_ult, async_output=as_o, async_input=as_i),


        'ultimate_incurred_cl_ielr':                        create_node('CL - IELR',                    mode=computed_mode('output'),   format=percent_format(2), default=0, group=grp_ult_inc_mthd_cl, async_output=as_o, async_input=as_i),

        # these are handled separately as the mode changes for total
        'additional_ibnr_attr':                             create_node('Attritional',                  mode=computed_mode('input'),    format=thousands_format(0), default=0, group=grp_ibnr_add,          async_output=as_o, async_input=as_i),   
        'additional_ibnr_large':                            create_node('Large',                        mode=computed_mode('input'),    format=thousands_format(0), default=0, group=grp_ibnr_add,          async_output=as_o, async_input=as_i),   
        'additional_ibnr_cat':                              create_node('Cat',                          mode=computed_mode('input'),    format=thousands_format(0), default=0, group=grp_ibnr_add,          async_output=as_o, async_input=as_i),   
        'additional_ibnr_total':                            create_node('Total',                        mode=computed_mode('output'),   format=thousands_format(0), default=0, group=grp_ibnr_add,          async_output=as_o, async_input=as_i),   
        
        # to control views
        'is_row_visible':                                   create_node('is_row_visible',               mode='output',  type='bool', group=grp_view,          async_output=as_o, async_input=as_i),   
        'lob_visible_1':                                    create_node('lob_visible_1',                mode='output',  type='bool', group=grp_view,          async_output=as_o, async_input=as_i),   
        'lob_visible_2':                                    create_node('lob_visible_2',                mode='output',  type='bool', group=grp_view,          async_output=as_o, async_input=as_i),   
        'lob_visible_3':                                    create_node('lob_visible_3',                mode='output',  type='bool', group=grp_view,          async_output=as_o, async_input=as_i),   
        'lob_visible_4':                                    create_node('lob_visible_4',                mode='output',  type='bool', group=grp_view,          async_output=as_o, async_input=as_i),   
        'lob_visible_5':                                    create_node('lob_visible_5',                mode='output',  type='bool', group=grp_view,          async_output=as_o, async_input=as_i),  

        **alct_nodes("attr", "Attritional"),
        **alct_nodes("large","Large"      ),
        **alct_nodes("cat",  "Cat"        ),
        **alct_nodes("total","Total"      ),
        **xcat_nodes("total_x_cat","Total\n(excl. Cat)")
        }

    if not is_summary:
        nodes.update({
            'development_pattern_premium_lloyds_unadjusted':    create_node("Premium\nDevelopment\n Pattern -\nLloyds\n - Unadjusted",  mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
            'development_pattern_paid_lloyds_unadjusted':       create_node("Paid\nDevelopment\n Pattern -\nLloyds\n - Unadjusted",     mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
            'development_pattern_incurred_lloyds_unadjusted':   create_node("Incurred\nDevelopment\n Pattern -\nLloyds\n - Unadjusted", mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
            'development_pattern_premium_lloyds':               create_node("Premium\nDevelopment\n Pattern -\nLloyds",                 mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
            'development_pattern_paid_lloyds':                  create_node("Paid\nDevelopment\n Pattern -\nLloyds",                    mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
            'development_pattern_incurred_lloyds':              create_node("Incurred\nDevelopment\n Pattern -\nLloyds",                mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
            'development_pattern_premium_override':             create_node("Premium\nDevelopment\n Pattern -\nOverride",               mode=computed_mode('input'),  format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i, is_read_only=True),
            'development_pattern_incurred_override':            create_node("Incurred\nDevelopment\n Pattern -\nOverride",              mode=computed_mode('input'),  format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i, is_read_only=True),
            'development_pattern_premium_selected':             create_node("Premium\nDevelopment\n Pattern -\nSelected",               mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
            'development_pattern_incurred_selected':            create_node("Incurred\nDevelopment\n Pattern -\nSelected",              mode=computed_mode('output'), format=percent_format(1), group=grp_dev_pat, async_output=as_o, async_input=as_i),
    
            'method_incurred':                                  create_node('Method\nIncurred',                mode=computed_mode('override'),   type='str',   options=['CL', 'BF', 'IELR'],    async_output=as_o, async_input=as_i),
            'applied_rate_change':                              create_node('Applied\n  Rate Change',          mode=computed_mode('override'), format=percent_format(1),    group=grp_inc_ind,  async_output=as_o, async_input=as_i, is_read_only=True),
            'applied_inflation':                                create_node('Applied\n  Inflation',            mode=computed_mode('override'), format=percent_format(1),    group=grp_inc_ind,  async_output=as_o, async_input=as_i, is_read_only=True),
            'modelled_weighting':                               create_node('Modelled\n Weighting',            mode=computed_mode('output'),   format=percent_format(1),                        async_output=as_o, async_input=as_i),

            'applied_rate_change_cumulative':                   create_node('Applied\n  Rate Change\n  Cumulative',mode=computed_mode('output'),  format=percent_format(1), group=grp_cum_ind,  async_output=as_o, async_input=as_i),
            'applied_inflation_cumulative':                     create_node('Applied\n  Inflation\n  Cumulative', mode=computed_mode('output'),   format=percent_format(1), group=grp_cum_ind,  async_output=as_o, async_input=as_i),
            'onlevel_factor_cumulative':                        create_node('Selected\n  On-Level\n  Factor',     mode=computed_mode('output'),   format=percent_format(1), group=grp_cum_ind,  async_output=as_o, async_input=as_i),

            'exposure_weighting_onlevel_1':                     create_node('Exposure -\nweighting 1',      mode=computed_mode('output'),   format=percent_format(1),  group=grp_wgt_ol,        async_output=as_o, async_input=as_i),
            'decay_ratio_weighting_2':                          create_node('Decay Ratio -\nweighting 2',   mode=computed_mode('output'),   format=percent_format(1),  group=grp_wgt_ol,        async_output=as_o, async_input=as_i),
            'developed_weighting_3':                            create_node('Developed -\nweighting 3',     mode=computed_mode('output'),   format=percent_format(1),  group=grp_wgt_ol,        async_output=as_o, async_input=as_i),
            'overall_weighting_onlevel' :                       create_node('Modelled\n Weighting',         mode=computed_mode('output'),   format=percent_format(1),   group=grp_wgt_ol,       async_output=as_o, async_input=as_i),

            'exposure_weighting_nominal_1':                     create_node('Exposure -\nweighting\nNominal',mode=computed_mode('output'),   format=percent_format(1),  group=grp_wgt_nominal,async_output=as_o, async_input=as_i),
            'overall_weighting_nominal' :                       create_node('Modelled\n Weighting\nNominal', mode=computed_mode('output'),   format=percent_format(1),  group=grp_wgt_nominal,async_output=as_o, async_input=as_i),

            'adjustments_actual' :                              create_node('Actual',                       mode=computed_mode('output'),   format=thousands_format(2),group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_lower' :                               create_node('Lower',                        mode=computed_mode('output'),                              group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_upper' :                               create_node('Upper',                        mode=computed_mode('output'),                              group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_prem_lloyds_lower' :                   create_node('Premium \nLloyds\n Lower',     mode=computed_mode('output'),   format=percent_format(1),  group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_prem_lloyds_upper' :                   create_node('Premium \nLloyds\n Upper',     mode=computed_mode('output'),   format=percent_format(1),  group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_prem_lloyds_actual' :                  create_node('Premium \nLloyds\n Actual',    mode=computed_mode('output'),   format=percent_format(1),  group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_incurred_lloyds_lower' :               create_node('Incurred \nLloyds \nLower',    mode=computed_mode('output'),   format=percent_format(1),  group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_incurred_lloyds_upper' :               create_node('Incurred \nLloyds \nUpper',    mode=computed_mode('output'),   format=percent_format(1),  group=grp_adj,        async_output=as_o, async_input=as_i),
            'adjustments_incurred_lloyds_actual' :              create_node('Incurred \nLloyds \nActual',   mode=computed_mode('output'),   format=percent_format(1),  group=grp_adj,        async_output=as_o, async_input=as_i),
            'pricing_basis':                                    create_node(                                mode=computed_mode('output'),                                                    async_output=as_o, async_input=as_i),
        })

    return nodes


def chart_list():
    as_i = ['calculate_profit_commission_task']
    as_o = []
    return {
        "chart_data"             : hx.List( mode="output", async_output=as_o, async_input=as_i, children={
            'yoa':                                 create_node('YoA',           mode='output', type='str',                   async_output=as_o, async_input=as_i),
            'gn_ilr_total':                        create_node('Total ILR',     mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i),
            'ultimate_ulr_selected_total':         create_node('Total ULR',     mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i),
            'ultimate_ulr_on_levelled_total':      create_node('Total ULR - OL',mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i),        
            'pricing_basis':                       create_node('Total LR - Sel',mode='output',   format=percent_format(1),   async_output=as_o, async_input=as_i)
        })}


def ielr_approaches():
    as_i = ['calculate_profit_commission_task']
    as_o = []
    return {
        "ielr_approaches"             : hx.Structure( children={
            "nominal"             : hx.Structure(view={"label": 'Nominal'}, children={
                'ielr_attr':            create_node('Attritional IELR',                 mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_large':           create_node('Large IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_cat':             create_node('CAT IELR',                         mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_total':           create_node('Total IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_total_excl_cat':  create_node('Total (Excl. CAT) IELR',           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                }),
            "ol_all_yr"             : hx.Structure( view={"label": 'On-level\nAll Yr'}, children={
                'ielr_attr':            create_node('Attritional IELR',                 mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_large':           create_node('Large IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_cat':             create_node('CAT IELR',                         mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_total':           create_node('Total IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_total_excl_cat':  create_node('Total (Excl. CAT) IELR',           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                }),
            "ol_cl_yr"              : hx.Structure( view={"label":  'On-level\nCL Yr'}, children={
                'ielr_attr':            create_node('Attritional IELR',                 mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_large':           create_node('Large IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_cat':             create_node('CAT IELR',                         mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_total':           create_node('Total IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                'ielr_total_excl_cat':  create_node('Total (Excl. CAT) IELR',           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                }),
        })}





def sch_projections_own_experience(cds):
    as_i = ['calculate_profit_commission_task']
    as_o = []
    detail_table_rows   = constants.DEFAULT_NUM_LOB * constants.YEARS_TO_CONSIDER_IN_OWN_EXPERIENCE
    summary_table_rows  = constants.DEFAULT_NUM_LOB
    row                 = {"row": hx.Int(mode="output")}
    show                = {"show_alc": hx.Bool(mode="output")}

    cds.extend_node_rater_defined(
        'cds',
        { 'projections_own_experience': hx.Structure( children={
                    
                    'error_msg':        hx.Str(  mode='output'),
                    'show_all_yrs':     hx.Bool( mode='input', default=False,                        view={"label": 'Show All Years'},   async_output=as_o, async_input=as_i),   
                    'show_detail':      hx.Bool( mode='input', default=False,                        view={"label": 'Show Detail View'}, async_output=as_o, async_input=as_i),
                    'show_compact':     hx.Bool( mode='output',                                                                          async_output=as_o, async_input=as_i),   
                    'show_all_lobs':    hx.Bool( mode='input', default=False,                        view={"label": 'Show All LOBs'},    async_output=as_o, async_input=as_i), # not used
                    'selected_lob_1':   hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected LOB (1)"},   options_data=f"../drop_down_lobs",   options_field="selected_lob", async_output=as_o, async_input=as_i),
                    'selected_lob_2':   hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected LOB (2)"},   options_data=f"../drop_down_lobs",   options_field="selected_lob", async_output=as_o, async_input=as_i),
                    'selected_lob_3':   hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected LOB (3)"},   options_data=f"../drop_down_lobs",   options_field="selected_lob", async_output=as_o, async_input=as_i),
                    'selected_lob_4':   hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected LOB (4)"},   options_data=f"../drop_down_lobs",   options_field="selected_lob", async_output=as_o, async_input=as_i),
                    'selected_lob_5':   hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Selected LOB (5)"},   options_data=f"../drop_down_lobs",   options_field="selected_lob", async_output=as_o, async_input=as_i),
                    'drop_down_lobs':   hx.List( mode="output",        children={ 'selected_lob': hx.Str(mode="output")}),             ### notice children

                    'summary_table': hx.List(  mode='input',      default_element_count= summary_table_rows, async_input=as_i, async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                        children={
                            'claim_source':                 create_node("Claim Source",                     mode='input', type='str',                                    async_output=as_o, async_input=as_i + ["sync_lob_lists_task"],  options=['Policy Level Data', 'Claim Level Data']),
                            'claim_basis':                  create_node("Claim Basis",                      mode='input', type='str',                                    async_output=as_o, async_input=as_i + ["sync_lob_lists_task"],  options=['Total', 'Attr / Lrg / Cat']),
                            'claim_to_develop_to_ultimate': create_node("Claim to Develop\n to Ultimate",   mode='input', type='str',                                    async_output=as_o, async_input=as_i + ["sync_lob_lists_task"],  options=['Open + Closed', 'Open']),
                            'cat_basis':                    create_node("Cat Basis",                        mode='input', type='str',                                    async_output=as_o, async_input=as_i + ["sync_lob_lists_task"],  options=['Experience', 'BP', 'RMS', 'None']),
                            'ielr_approach':                create_node("IELR Method\n& Weights",           mode='input', type='str',    default='On-level',             async_output=as_o, async_input=as_i + ["sync_lob_lists_task"],  options=['Nominal', 'On-level'], is_read_only=True),
                           
                            'ielr_attr':                    create_node('Attritional IELR',                 mode='override', format=percent_format(2),                   async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'ielr_large':                   create_node('Large IELR',                       mode='override', format=percent_format(2),                   async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'ielr_cat':                     create_node('CAT IELR',                         mode='override', format=percent_format(2),                   async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'ielr_total':                   create_node('Total IELR',                       mode='override', format=percent_format(2),                   async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'ielr_total_excl_cat':          create_node('Total (Excl. CAT) IELR',           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),

                            'lloyds_model_ielr':            create_node("Lloyds Model IELR",                mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'lloyds_model_final_gn_ulr':    create_node("Lloyds Model GNULR",               mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'lloyds_selected_ielr':         create_node("Lloyds Selected IELR",             mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'lloyds_selected_final_gn_ulr': create_node("Lloyds Selected GNULR",            mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),

                            'beazley_model_ielr':            create_node("Beazley Model IELR",              mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'beazley_model_final_gn_ulr':    create_node("Beazley Model GNULR",             mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'beazley_selected_ielr':         create_node("Beazley Selected IELR",           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'beazley_selected_final_gn_ulr': create_node("Beazley Selected GNULR",          mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),

                            'ielr_nominal_attr':            create_node('Attritional IELR',                 mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_nominal_large':           create_node('Large IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_nominal_cat':             create_node('CAT IELR',                         mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_nominal_total':           create_node('Total IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_nominal_total_excl_cat':  create_node('Total (Excl. CAT) IELR',           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),

                            'ielr_ol_all_yr_attr':          create_node('Attritional IELR',                 mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_all_yr_large':         create_node('Large IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_all_yr_cat':           create_node('CAT IELR',                         mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_all_yr_total':         create_node('Total IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_all_yr_total_excl_cat':create_node('Total (Excl. CAT) IELR',           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),

                            'ielr_ol_cl_yr_attr':           create_node('Attritional IELR',                 mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_cl_yr_large':          create_node('Large IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_cl_yr_cat':            create_node('CAT IELR',                         mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_cl_yr_total':          create_node('Total IELR',                       mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'ielr_ol_cl_yr_total_excl_cat': create_node('Total (Excl. CAT) IELR',           mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),


                            'selected_attr':                create_node('Attritional',                      mode='override', format=percent_format(2), group='Selected', async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'selected_large':               create_node('Large',                            mode='override', format=percent_format(2), group='Selected', async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'selected_cat':                 create_node('Cat (on\nSelected\nBasis)',        mode='override', format=percent_format(2), group='Selected', async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'selected_total':               create_node('Total',                            mode='output',   format=percent_format(2), group='Selected', async_output=as_o, async_input=as_i),
                            'selected_total_excl_cat':      create_node('Total\n(Excl. CAT)',               mode='output',   format=percent_format(2), group='Selected', async_output=as_o, async_input=as_i),
                            'selected_cat_exp':             create_node("Cat (Experience)",                 mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'selected_cat_bp':              create_node("Cat (BP)",                         mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'selected_cat_rms':             create_node("Cat (RMS)",                        mode='output',   format=percent_format(2),                   async_output=as_o, async_input=as_i),
                            'selected_cat_basis':           create_node("Cat Basis",                        mode='output', type='str',                                   async_output=as_o, async_input=as_i),
 
                            'model_default_attr':           create_node('Attritional',                      mode='override', format=percent_format(2), group='Model Default', async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'model_default_large':          create_node('Large',                            mode='override', format=percent_format(2), group='Model Default', async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'model_default_cat':            create_node('Cat (on\nSelected\nBasis)',        mode='override', format=percent_format(2), group='Model Default', async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            'model_default_total':          create_node('Total',                            mode='output',   format=percent_format(2), group='Model Default', async_output=as_o, async_input=as_i),
                            'model_default_total_excl_cat': create_node('Total\n(Excl. CAT)',               mode='output',   format=percent_format(2), group='Model Default', async_output=as_o, async_input=as_i),
                            'model_default_cat_exp':        create_node("Cat (Experience)",                 mode='output',   format=percent_format(2),                        async_output=as_o, async_input=as_i),
                            'model_default_cat_bp':         create_node("Cat (BP)",                         mode='output',   format=percent_format(2),                        async_output=as_o, async_input=as_i),
                            'model_default_cat_rms':        create_node("Cat (RMS)",                        mode='output',   format=percent_format(2),                        async_output=as_o, async_input=as_i),
                            'model_default_cat_basis':      create_node("Cat Basis",                        mode='output', type='str',                                        async_output=as_o, async_input=as_i),

                            'ovd_dev':                      create_node('Devt',                             mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_index':                    create_node('Indices',                          mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_premium':                  create_node('Premium',                          mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_ielr_weights':             create_node('IELR Wgt',                         mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_ielr':                     create_node('IELR',                             mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_ibnr':                     create_node('IBNR add',                         mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_ultimate_method':          create_node('Ult Mtd',                          mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_ultimate':                 create_node('Ult',                              mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_ulr_weights':              create_node('ULR Wgt',                          mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),
                            'ovd_ulr':                      create_node('ULR',                              mode='output',  type='str',               group='Overrides Used?', async_output=as_o, async_input=as_i, hx_calc=True),

                            # superfluous as handled in pc algo directly JB 08/01/2026
                            # 'percent_attr':                 create_node("% ATT",                            mode='output', format=percent_format(0),                          async_output=as_o, async_input=as_i),
                            # 'percent_large':                create_node("% LRG",                            mode='output', format=percent_format(0),                          async_output=as_o, async_input=as_i),
                            # 'percent_cat':                  create_node("% CAT",                            mode='output', format=percent_format(0),                          async_output=as_o, async_input=as_i),
                            
                            'cov_attr':                     create_node("ATT COV",                          mode='output', format=percent_format(0),                          async_output=as_o, async_input=as_i),
                            'cov_large':                    create_node("LRG COV",                          mode='output', format=percent_format(0),                          async_output=as_o, async_input=as_i),
                            'cov_cat':                      create_node("CAT COV",                          mode='output', format=percent_format(0),                          async_output=as_o, async_input=as_i),
                            'cov_total':                    create_node("TOTAL COV",                        mode='output', format=percent_format(0),                          async_output=as_o, async_input=as_i),

                            'actuarial_notes':              create_node("Actuarial Notes",                  mode='input', type='str',                                         async_output=as_o, async_input=as_i + ["sync_lob_lists_task"]),
                            
                            ** generate_common_nodes(True)
                       }),

                    'detail_table':                         hx.List(        mode='input',      
                                                                            default_element_count=detail_table_rows, 
                                                                            async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                                            async_input=as_i,   
                                                                            children={ ** generate_common_nodes(False)                          }),
                    'selected_lob_totals_1':                hx.Structure(   children={ ** generate_common_nodes(True), **chart_list(), **ielr_approaches(), **row, **show    }),
                    'selected_lob_totals_2':                hx.Structure(   children={ ** generate_common_nodes(True), **chart_list(), **ielr_approaches(), **row, **show    }),
                    'selected_lob_totals_3':                hx.Structure(   children={ ** generate_common_nodes(True), **chart_list(), **ielr_approaches(), **row, **show    }),
                    'selected_lob_totals_4':                hx.Structure(   children={ ** generate_common_nodes(True), **chart_list(), **ielr_approaches(), **row, **show    }),
                    'selected_lob_totals_5':                hx.Structure(   children={ ** generate_common_nodes(True), **chart_list(), **ielr_approaches(), **row, **show    }),
                }
            )
        }
    )
