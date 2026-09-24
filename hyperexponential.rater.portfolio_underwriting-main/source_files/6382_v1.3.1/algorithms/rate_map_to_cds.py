import algorithms.rate_utilities                                    as utils
import algorithms.rate_constants                                    as constants

def rate_map_to_cds(hxd, is_bbt):
    
    # paths
    layers_path     = hxd.cds.layers[0]                                 # Get the first layer in the layers collection
    risk_inf_path   = hxd.cds.risk_information                          # Access the risk information section of the CDS
    summary_path    = hxd.cds.rating_summary                            # Access the rating summary section
    metrics_path    = hxd.cds.rating_summary.pricing_adequacy_metrics
    metrics_bbt_path= hxd.cds.rating_summary.pricing_outputs
    kpis_path       = hxd.cds.standard_kpis
    p_l_path        = hxd.cds.prem_limit_profile
    sf_path         = hxd.cds.standard_fields
    case_path       = hxd.cds.rating_summary.case_pricing

    # calculate term
    incept = hxd.hx_core.inception_date
    expiry = hxd.hx_core.expiry_date
    term   = utils.year_diff(incept,expiry,True)

    is_case_priced = sf_path.rating_methodology != "Rater"

    ###################################
    # STEP 1 gather loss ratios and financial ratios
    ###################################

    if is_case_priced:                              # Case Priced scenario
        # Extract values
        deductions          = case_path.brokerage           or 0
        quoted_premium_100  = case_path.quoted_premium_100  or 0
        line                = case_path.written_line        or 0
        tracker_class       = case_path.tracker_class       or ''
        section_ref         = '' # TODO: Day 2 SECTION REF consider
        quoted_premium      = quoted_premium_100 * line
        brk                 = deductions

        # calc attr_pct for later
        cat_gnulr           = 0
        tot_gnulr           = case_path.gn_ulr
        attr_pct            = 1 - utils.ratio(cat_gnulr, tot_gnulr, 0)


    elif is_bbt:                                    # BBT scenario
        # Extract values
        deductions_5623     = metrics_bbt_path.deductions_5623   or 0
        afb_api             = metrics_bbt_path.afb_api           or 0
        line                = metrics_bbt_path.line_size         or 0
        tracker_class       = metrics_bbt_path.tracker_class     or ''
        section_ref         = metrics_bbt_path.section_ref_5623  or '' # TODO: Day 2 SECTION REF consider
        quoted_premium      = utils.ratio(afb_api, (1 - deductions_5623))
        brk                 = deductions_5623

        # calc attr_pct for later
        cat_gnulr           = metrics_bbt_path.bbt_gn_cat_ulr.selected  or 0 
        tot_gnulr           = metrics_bbt_path.bbt_gn_ulr.selected      or 0
        attr_pct            = 1 - utils.ratio(cat_gnulr, tot_gnulr, 0)
    
    else:                                           # MAIN MODEL (not bbt) scenario
        # Extract values
        bst_net_premium     = p_l_path.summary.bst_net_premium                                       or 0 
        bst_gross_premium   = p_l_path.summary.bst_share_ultimate_gross_premium                      or 0
        line                = p_l_path.summary.bst_share_line_size                                   or 0 
        tracker_class       = summary_path.model_gn_ulr.projected_gn_ulr.table[0].tracker_class      or ''
        section_ref         = summary_path.model_gn_ulr.projected_gn_ulr.table[0].policy_ref_by_lob  or '' # TODO: Day 2 SECTION REF consider
        quoted_premium      = bst_gross_premium
        brk                 = 1 - utils.ratio(bst_net_premium, bst_gross_premium, 1)

        # calc attr_pct for later
        attr_pct_helper     = summary_path.cat_loadings.summary.attr_and_lrg                         or 0
        base_gnulr          = summary_path.model_gn_ulr.model_weights.summary.model_estimate         or 0
        attr_gnulr          = (attr_pct_helper * base_gnulr)                                         or 0 
        tot_gnulr           = metrics_path.pricing_adequacy_pre_adj.summary.best_estimate_pre_pc_adj or 0
        attr_pct            = utils.ratio(attr_gnulr, tot_gnulr, 1)


    ###################################
    # STEP 2 gather performance metrics and associated financials
    ###################################

    if is_case_priced:
        tpi                           = case_path.tpi      or 0 
        bpi                           = case_path.bpi      or 0
        pflr                          = case_path.gn_ulr   or 0
        roc                           = case_path.roc      or 0
        tpi_pre_uw_adj                = case_path.tpi      or 0
        bpi_pre_uw_adj                = case_path.bpi      or 0
        pflr_pre_uw_adj               = case_path.gn_ulr   or 0
        benchmark_premium             = utils.ratio(quoted_premium, bpi)
        technical_premium             = utils.ratio(quoted_premium, tpi)
        technical_premium_net         = technical_premium * (1 - brk)
        expected_loss_cost            = benchmark_premium * (1 - brk) * constants.benchmark_lr
        expected_loss_cost_pre_uw_adj = expected_loss_cost
    else:
        tpi                           = metrics_path.pricing_adequacy_final_pricing.summary.tpi               or 0 
        bpi                           = metrics_path.pricing_adequacy_final_pricing.summary.bpi               or 0
        pflr                          = metrics_path.pricing_adequacy_final_pricing.summary.best_estimate_gn  or 0
        roc                           = metrics_path.pricing_adequacy_final_pricing.summary.roc               or 0
        tpi_pre_uw_adj                = metrics_path.pricing_adequacy_actuarial_basis.summary.tpi             or 0
        bpi_pre_uw_adj                = metrics_path.pricing_adequacy_actuarial_basis.summary.bpi             or 0
        pflr_pre_uw_adj               = metrics_path.pricing_adequacy_actuarial_basis.summary.best_estimate   or 0
        benchmark_premium             = summary_path.technical_premium_build_up.summary.gg_bm_final           or 0
        technical_premium             = summary_path.technical_premium_build_up.summary.gg_tp_final           or 0 
        technical_premium_net         = summary_path.technical_premium_build_up.summary.tp_final              or 0 
        expected_loss_cost            = summary_path.technical_premium_build_up.summary.el_final              or 0
        expected_loss_cost_pre_uw_adj = summary_path.technical_premium_build_up.summary.el_actuarial          or 0


    ###################################
    # STEP 3 Assign to dictionary
    ###################################

    # Initialize a dictionary to store standard KPIs
    std_layer_dict                                   = {}

    # assign basic values limit, xs etc.
    std_layer_dict['status']                         = risk_inf_path.deal_status
    std_layer_dict['brokerage']                      = brk
    std_layer_dict['written_line']                   = line
    std_layer_dict['quoted_premium']                 = quoted_premium
    std_layer_dict['limit']                          = hxd.cds.prem_limit_profile.summary.avg_limit_at_100_per               or 0
    std_layer_dict['excess']                         = hxd.cds.prem_limit_profile.summary.avg_attachment_point               or 0
    std_layer_dict['currency']                       = hxd.cds.currencies.source_currency                                    
    std_layer_dict['section_reference']              = section_ref
    std_layer_dict['trifocus']                       = tracker_class

    # Assign TPI, BPI, PFLR from final pricing summary, default 0 if None
    std_layer_dict['tpi']                            = tpi
    std_layer_dict['bpi']                            = bpi
    std_layer_dict['pflr']                           = pflr
    std_layer_dict['roc']                            = roc
    std_layer_dict['tpi_pre_uw_adj']                 = tpi_pre_uw_adj
    std_layer_dict['bpi_pre_uw_adj']                 = bpi_pre_uw_adj
    std_layer_dict['pflr_pre_uw_adj']                = pflr_pre_uw_adj
    std_layer_dict['uw_adj_impact']                  = utils.ratio( std_layer_dict['pflr'], std_layer_dict['pflr_pre_uw_adj'] , 1)
    std_layer_dict['pflr_att']                       = std_layer_dict['pflr'] *      attr_pct
    std_layer_dict['pflr_cat']                       = std_layer_dict['pflr'] * (1 - attr_pct)

    # assign remaining quoted premiums to dictionary
    std_layer_dict['quoted_premium_100']             = utils.ratio( std_layer_dict['quoted_premium'], line)
    std_layer_dict['quoted_premium_annual']          = utils.ratio( std_layer_dict['quoted_premium'], term)
    std_layer_dict['quoted_premium_annual_100']      = utils.ratio( std_layer_dict['quoted_premium'], line * term)
    std_layer_dict['quoted_premium_net']             = (1 - brk) *  std_layer_dict['quoted_premium']
    std_layer_dict['quoted_premium_net_100']         = utils.ratio( std_layer_dict['quoted_premium_net'], line)

    # assign benchmark premiums to dictionary
    std_layer_dict['benchmark_premium']              = benchmark_premium
    std_layer_dict['benchmark_premium_100']          = utils.ratio( std_layer_dict['benchmark_premium'], line)
    std_layer_dict['benchmark_premium_annual']       = utils.ratio( std_layer_dict['benchmark_premium'], term)
    std_layer_dict['benchmark_premium_annual_100']   = utils.ratio( std_layer_dict['benchmark_premium'], line * term)
    std_layer_dict['benchmark_premium_net']          = (1 - brk) *  std_layer_dict['benchmark_premium']
    std_layer_dict['benchmark_premium_net_100']      = utils.ratio( std_layer_dict['benchmark_premium_net'], line)
    std_layer_dict['benchmark_premium_pre_uw_adj']   = utils.ratio( std_layer_dict['quoted_premium'], std_layer_dict['bpi_pre_uw_adj'])
    
    # assign technical premiums to dictionary
    std_layer_dict['technical_premium']              = technical_premium
    std_layer_dict['technical_premium_100']          = utils.ratio( std_layer_dict['technical_premium'], line)
    std_layer_dict['technical_premium_net']          = technical_premium_net
    std_layer_dict['technical_premium_net_100']      = utils.ratio( std_layer_dict['technical_premium_net'], line)
    std_layer_dict['technical_premium_pre_uw_adj']   = utils.ratio( std_layer_dict['quoted_premium'], std_layer_dict['tpi_pre_uw_adj'])

    # assign loss costs to dictionary
    std_layer_dict['expected_loss_cost']             = expected_loss_cost
    std_layer_dict['expected_loss_cost_pre_uw_adj']  = expected_loss_cost_pre_uw_adj
    std_layer_dict['expected_loss_cost_100']         = utils.ratio( std_layer_dict['expected_loss_cost'], line)

    # Set all KPI values as attributes on the first layer
    for k, v in std_layer_dict.items():
        setattr(layers_path, k, v)

    # standard fields
    sf_path.uw_rationale        = build_rationale_str(hxd)
    sf_path.facility_reference  = sf_path.policy_reference
    sf_path.benchmark_class     = tracker_class
    sf_path.trifocus            = tracker_class
    sf_path.is_case_priced      = is_case_priced
    sf_path.is_rater_priced     = is_case_priced==False

    # Store needed values to kpis path
    kpis_path.policy_reference      = sf_path.policy_reference
    kpis_path.pflr_pre_uw_adj       = std_layer_dict['pflr_pre_uw_adj'] 


def build_rationale_str(hxd):
    rationale_path = hxd.cds.rationale

    rationale_str = ""
    
    rationale_str += "Key Information about Account:"
    rationale_str += rationale_path.key_information or ""
    rationale_str += "\nRationale behind Assumption Selection:"
    rationale_str += rationale_path.rationale_assumptions or ""
    rationale_str += "\nRationale behind Methodology Selection and Overrides:"
    rationale_str += rationale_path.rationale_methodology or ""
    rationale_str += "\nKey Uncertainties:"
    rationale_str += rationale_path.key_uncertainties or ""
    
    return rationale_str