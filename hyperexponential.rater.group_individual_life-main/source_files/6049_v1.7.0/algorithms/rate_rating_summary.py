import hx
import pandas as pd
import numpy as np
import math as math
from functools import reduce
from algorithms.rate_utilities import one_layer, ratio, pd_df_from_hx_list, look_up, tp_components
from algorithms.rate_constants import benchmark_lr
from algorithms import parameter_tables_schema as params


# Update Simulation results:
def calculate_pc_ncb_on_benchmark(hxd, lives_df, covered_benefits):
    layer, cvg = one_layer(hxd)
    brokerage = layer.brokerage or 0

    pi = hxd.cds.policy_info
    has_pc = pi.has_profit_commission
    pc = pi.profit_commission
    pc_exp = pi.pc_expenses
    pc_def = pi.pc_deficit
    ncb = pi.ncb_pct
    has_ncb = pi.has_no_claims_bonus

    tot = layer.totals
    tot_ex = tot.total_ex_pc_ncb
   # benchmark_lr = tot_ex.benchmark_lr

    pc_g = layer.pc.model.gross
    pc_n = layer.pc.model.net
    ncb_g = layer.ncb.model.gross
    ncb_n = layer.ncb.model.net

    # E(L)
    layer.expected_loss_cost_pre_uw_adj = tot_ex.el_cost_pre_uw_pre_exp
    el = layer.expected_loss_cost = tot_ex.expected_loss_cost  # This includes the post-experience adjustment

    # P(No claims)
    layer.no_claim_prob = lives_df["no_claim_prob"].prod()
    no_claim_prob = layer.no_claim_prob

    # # Benchmark premium (ex PC/NCB)
    benchmark_premium = tot_ex.benchmark_premium
    benchmark_premium_net = benchmark_premium * (1 - brokerage)

    # Simulated result PC/ NCB payments

    temp = layer.temp
    exp_pc_pay_g = getattr(temp, "exp_pc_payment_gross_sim", None)
    exp_pc_pay_n = getattr(temp, "exp_pc_payment_net_sim", None)
    exp_ncb_pay_g = getattr(temp, "exp_ncb_payment_gross_sim", None)
    exp_ncb_pay_n = getattr(temp, "exp_ncb_payment_net_sim", None)

    sim_pc_available = has_pc and (exp_pc_pay_g is not None) and (exp_pc_pay_n is not None)
    sim_ncb_available = has_ncb and (exp_ncb_pay_g is not None) and (exp_ncb_pay_n is not None)

    #PC
    pc_struct = [pc_g, pc_n]
    for struct in pc_struct:

        premium = benchmark_premium if struct == pc_g else benchmark_premium_net
        struct.premium = premium

        premium_gross = benchmark_premium
        premium_net   = benchmark_premium_net


        # Expected PC
        if sim_pc_available:
            exp_pc_payment_net = float(exp_pc_pay_n)
            exp_pc_payment_gross = float(exp_pc_pay_g)
        else:
            exp_pc_payment_net = 0
            exp_pc_payment_gross = 0           
    
        net_premium_after_pc = premium_net - exp_pc_payment_net
        # Why we have this condition to choose a value not lwer than 1e-9?
        net_premium_after_pc = max(net_premium_after_pc, 1e-9)

        adjusted_lr = ratio(el, net_premium_after_pc)

        adjusted_expected_loss = benchmark_premium_net * adjusted_lr

        adjusted_premium_net = ratio(adjusted_expected_loss, benchmark_lr)

        adjusted_premium_gross = adjusted_premium_net / (1 - brokerage)

        adjusted_premium = adjusted_premium_gross if struct == pc_g else adjusted_premium_net

        struct.pc_cost = exp_pc_payment_gross if struct == pc_g else exp_pc_payment_net
        struct.pc_load = max(adjusted_premium - struct.premium, 0)


       # struct.adjusted_premium = adjusted_premium

    # NCB 
    ncb_struct = [ncb_g, ncb_n]

    for struct in ncb_struct:

        premium = benchmark_premium if struct == ncb_g else benchmark_premium_net
        struct.premium = premium

        if sim_ncb_available:
            exp_ncb_payment = float(exp_ncb_pay_g) if struct == ncb_g else float(exp_ncb_pay_n)
        else:
            exp_ncb_payment = 0

        # Convert payment to premium load
        # why we have the 1e-9. Remove the 1-brokerage part because the exp_ncb_payment has already include the scenario including/excluding the brokerage
        struct.ncb_load = ratio(
            exp_ncb_payment,
            benchmark_lr or 1e-9
        ) if has_ncb else 0
        


#Update using simulation results:
def calculate_pc_ncb_on_quoted(hxd, pc_load_attr, ncb_load_attr):
    from functools import reduce

    layer, cvg = one_layer(hxd)
    brokerage = layer.brokerage or 0

    pi = hxd.cds.policy_info
    has_pc = pi.has_profit_commission
    pc = pi.profit_commission
    pc_exp = pi.pc_expenses
    pc_def = pi.pc_deficit
    ncb = pi.ncb_pct
    has_ncb = pi.has_no_claims_bonus

    el = layer.expected_loss_cost
    no_claim_prob = layer.no_claim_prob

    tot = layer.totals
    tot_tot = tot.total
    tot_ex = tot.total_ex_pc_ncb
    
    pc_g = layer.pc.quoted.gross
    pc_n = layer.pc.quoted.net
    ncb_g = layer.ncb.quoted.gross
    ncb_n = layer.ncb.quoted.net

    # Premiums
    quoted_premium = tot_ex.quoted_premium
    quoted_premium_net = quoted_premium * (1 - brokerage)

    if quoted_premium_net == 0 :
        priced_for_lr = benchmark_lr
    else:
        priced_for_lr = el / quoted_premium_net

    #den_pc = 1 - (1 - pc_exp) * ratio(pc, benchmark_lr)  
    temp = layer.temp
    exp_pc_pay_q_g = getattr(temp, "exp_pc_payment_quoted_gross_sim", None)
    exp_pc_pay_q_n = getattr(temp, "exp_pc_payment_quoted_net_sim", None)
    exp_ncb_pay_q_g = getattr(temp, "exp_ncb_payment_quoted_gross_sim", None)
    exp_ncb_pay_q_n = getattr(temp, "exp_ncb_payment_quoted_net_sim", None)

    sim_pc_available = has_pc and (exp_pc_pay_q_g is not None) and (exp_pc_pay_q_n is not None)
    sim_ncb_available = has_ncb and (exp_ncb_pay_q_g is not None) and (exp_ncb_pay_q_n is not None)

    # PC with achieved premium for gross and net
    pc_struct = [pc_g, pc_n]
    for struct in pc_struct:
        
        premium = quoted_premium if struct == pc_g else quoted_premium_net
        struct.premium = premium

        premium_gross = quoted_premium 
        premium_net = quoted_premium_net


        if sim_pc_available:
            exp_pc_payment_net = float(exp_pc_pay_q_n)
            exp_pc_payment_gross = float(exp_pc_pay_q_g)
        else:
            exp_pc_payment_net = 0
            exp_pc_payment_gross = 0


        net_premium_after_pc = premium_net - exp_pc_payment_net
        net_premium_after_pc = max(net_premium_after_pc, 1e-9)


        adjusted_lr = ratio(el, net_premium_after_pc)

        adjusted_expected_loss = premium_net * adjusted_lr

        adjusted_premium_net = ratio(adjusted_expected_loss, priced_for_lr)

        adjusted_premium_gross = adjusted_premium_net / (1 - brokerage)

        adjusted_premium = adjusted_premium_gross if struct == pc_g else adjusted_premium_net

        struct.pc_cost = exp_pc_payment_gross if struct == pc_g else exp_pc_payment_net
        struct.pc_load = max(adjusted_premium - struct.premium, 0)


    # NCB with achieved premium for gross and net
    ncb_struct = [ncb_g, ncb_n]
    for struct in ncb_struct:
        # Gross premium if pc_g, else net premium
        premium = quoted_premium if struct == ncb_g else quoted_premium_net
        struct.premium = premium

        if sim_ncb_available:
            exp_ncb_payment = float(exp_ncb_pay_q_g) if struct == ncb_g else float(exp_ncb_pay_q_n)
        else:
            exp_ncb_payment =  0

        struct.ncb_load = ratio(
            exp_ncb_payment,
            benchmark_lr or 1e-9
        ) if has_ncb else 0


    pc_load = reduce(getattr, pc_load_attr, layer.pc.quoted)
    ncb_load = reduce(getattr, ncb_load_attr, layer.ncb.quoted)

    return pc_load, ncb_load



def calculate_technical_premium(hxd, expected_loss_cost, total_expected_loss_cost=None):
    layer, cvg = one_layer(hxd)
    brokerage = layer.brokerage or 0
    tp = tp_components(hxd)

    # Set key TP params
    che = tp["che"]
    fixed_exp = tp["fixed_exp"]
    technical_lr = tp["technical_lr"]

    if total_expected_loss_cost:  # Allow for allocation of fixed expenses to different coverages based on EL
        fixed_exp = fixed_exp * ratio(expected_loss_cost, total_expected_loss_cost)

    # Calculate premium
    share_expected_loss = expected_loss_cost * layer.written_line
    technical_premium_net = ratio(
        ratio((share_expected_loss * (1 + che) + fixed_exp), technical_lr),
        layer.written_line
    )
    technical_premium = ratio(technical_premium_net, (1 - brokerage))

    return technical_premium


def sync_technical_summary(hxd, pc_load_attr, ncb_load_attr, discount):
    layer, cvg = one_layer(hxd)
    tp = tp_components(hxd)

    brokerage = layer.brokerage or 0
    tot = layer.totals
    tot_ex = tot.total_ex_pc_ncb
    tot_pc = tot.pc
    tot_ncb = tot.ncb
    tot_tot = tot.total
    nmp_load = tp["nmp_load"]

    ### --- RATER PRICED
    if hxd.cds.standard_fields.is_rater_priced:
        # Calculate layer totals
        layer.quoted_premium = tot_tot.quoted_premium
        #YZ 17/02/2025: The uw_adj_impact for layer should call total uw_adj because this is what UW adjustment. total uw_adj_impact is for commercial adjustment.
        layer.uw_adj_impact = tot_tot.uw_adj

        # PC and NCB
        pc_load, ncb_load = calculate_pc_ncb_on_quoted(hxd, pc_load_attr, ncb_load_attr)
        layer.expected_pc = pc_load
        layer.expected_ncb = ncb_load

        # BPI
        layer.benchmark_premium = tot_tot.benchmark_premium
        quoted_premium_net_net = layer.quoted_premium - layer.expected_pc - layer.expected_ncb
        bpi_den = ratio(ratio(layer.expected_loss_cost_pre_uw_adj * discount, benchmark_lr), 1 - brokerage)
        layer.bpi_pre_uw_adj = ratio(quoted_premium_net_net, bpi_den)
        layer.bpi = ratio(quoted_premium_net_net, tot_ex.benchmark_premium)

        # TPI
        layer.technical_premium = tot_tot.technical_premium
        layer.technical_premium_net = tot_tot.technical_premium * (1 - brokerage)
        layer.technical_premium_pre_uw_adj = ratio(tot_tot.technical_premium, tot_tot.uw_adj_impact)
        tpi_den = calculate_technical_premium(hxd, layer.expected_loss_cost_pre_uw_adj * discount)
        layer.tpi_pre_uw_adj = ratio(quoted_premium_net_net, tpi_den)
        layer.tpi = ratio(quoted_premium_net_net, tot_ex.technical_premium)

        # Additional metrics for CDS
        quoted_premium_net = layer.quoted_premium * (1 - brokerage)
        layer.pflr_pre_uw_adj = ratio(layer.expected_loss_cost_pre_uw_adj * discount, (quoted_premium_net or 1))
        layer.pflr = ratio(layer.expected_loss_cost, (quoted_premium_net or 1))
        layer.pflr_cat = ratio(layer.expected_loss_cost*nmp_load, (quoted_premium_net or 1))
        layer.pflr_att = layer.pflr - layer.pflr_cat
        layer.roc = ratio(
            1 - layer.pflr - tp["var_exp"] + tp["inv_inc"] - (tp["cost_of_ri"] - tp["ri_rec"]) - ratio(tp["fixed_exp"] + layer.expected_loss_cost * tp["che"], quoted_premium_net),
            tp["capital_req"]
        )

    # --- CASE PRICED
    elif hxd.cds.standard_fields.is_case_priced and layer.quoted_premium_case_priced:                
        layer.bpi = layer.bpi_case_priced
        layer.benchmark_premium = ratio(layer.quoted_premium_case_priced, layer.bpi)
        
        layer.expected_loss_cost = layer.benchmark_premium * benchmark_lr * (1 - brokerage)
        
        layer.technical_premium = calculate_technical_premium(hxd, layer.expected_loss_cost)
        layer.technical_premium_net = layer.technical_premium * (1 - brokerage)  
        layer.tpi = ratio(layer.quoted_premium_case_priced, layer.technical_premium)
        layer.tpi_pre_uw_adj = layer.tpi
        layer.technical_premium_pre_uw_adj = layer.technical_premium
        
        # Additional metrics for CDS
        layer.pflr = ratio(benchmark_lr, layer.bpi)
        layer.pflr_pre_uw_adj = layer.pflr
        layer.pflr_cat = ratio(layer.expected_loss_cost*nmp_load, layer.benchmark_premium*(1-brokerage) )
        layer.pflr_att = layer.pflr - layer.pflr_cat
    
        quoted_premium_net = layer.quoted_premium_case_priced * (1 - brokerage)
        layer.roc = ratio(
            1 - layer.pflr - tp["var_exp"] + tp["inv_inc"] - (tp["cost_of_ri"] - tp["ri_rec"]) - ratio(tp["fixed_exp"] + layer.expected_loss_cost * tp["che"], quoted_premium_net),
            tp["capital_req"]
        )
        
        layer.quoted_premium_case_priced_view = layer.quoted_premium_case_priced
        layer.bpi_case_priced_view = layer.bpi_case_priced
        

def calculate_statistics(lives_df, field, weight_col="no_lives", weighted_avg_only=False):
    weighted_avg = 0
    maximum = 0
    minimum = 0

    if field in lives_df.columns:
        df_field = lives_df[[field]].dropna()
        if not df_field.empty:
            maximum = df_field[field].max()
            minimum = df_field[field].min()
        
        if weight_col in lives_df.columns:
            df_weight = lives_df[[field, weight_col]].dropna()
            total_weight = df_weight[weight_col].sum()
            if total_weight > 0:
                weighted_avg = (df_weight[field] * df_weight[weight_col]).sum() / total_weight

    if weighted_avg_only:
        return weighted_avg
    else:
        return weighted_avg, maximum, minimum


def rate_rating_summary(hxd):
    cover = hxd.cds.cover_selection
    layer, cvg = one_layer(hxd)
    temp = layer.temp
    brokerage = layer.brokerage or 0
    tp = tp_components(hxd)

    pi = hxd.cds.policy_info
    has_pc = pi.has_profit_commission
    has_ncb = pi.has_no_claims_bonus

    tot = layer.totals
    tot_ex = tot.total_ex_pc_ncb
    tot_pc = tot.pc
    tot_ncb = tot.ncb
    tot_tot = tot.total

    db = cvg.death
    adb = cvg.additional_death
    ti = cvg.terminal_illness
    ci = cvg.critical_illness
    re = cvg.repat_exp

    expo = hxd.cds.exposure.granular
    expe = hxd.cds.experience_rating

    # Set rating methodology
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"

    # Get DataFrame with exposures
    lives = expo.lives
    lives_df = pd_df_from_hx_list(lives)

    if lives_df.empty or not hxd.cds.cover_selection.are_db_fields_full:
        return

    # Define coverage-related variables
    total_exposed_si = sum(lives_df["sum_insured"])
    db.label = "Death Benefit\n" + db.cover_type

    if not expe.claims_available:
        discount = 1
    elif expe.death_or_all_risks == "Death only":
        discount = expe.death_only_discount or 1  # Avoid None errors
    elif expe.death_or_all_risks == "All risk":
        discount = expe.all_risk_discount or 1  # Avoid None errors
    else:
        discount = 1

    hxd_cvg = {"db": db, "adb": adb, "ti": ti, "ci": ci, "re": re}
    cvg_keys = list(hxd_cvg.keys())
    cvg_values = list(hxd_cvg.values())
    cvg_bools = [True] + [cvg.is_covered for cvg in cvg_values[1:]]  # DB always covered
    covered_benefits = [cvg for cvg, flag in zip(cvg_keys, cvg_bools) if flag]
    
    # Loop through covered benefits to calculate totals
    total_expected_loss_cost = 0
    
    for cvg in covered_benefits:
        # --- Pre-experience adj (includes new NMP adjustment)
        if cvg == "db" and cover.are_agg_limits_full and temp.is_agg_priced and db.el_cost_post_sim.selected:  # Allow for replacement of deterministic EL with stochastic EL
            db.el_cost_pre_uw_pre_exp = db.el_cost_no_sim * (1+db.agg_impact_on_el) *  (1 + tp["nmp_load"])
        else:
            # Replaced `setattr` with direct assignment
            hxd_cvg[cvg].el_cost_pre_uw_pre_exp = sum(lives_df[lives_df[f"{cvg}_expected_loss_cost_pre_uw_adj"] > 0][f"{cvg}_expected_loss_cost_pre_uw_adj"]) * (1 + tp["nmp_load"])

        hxd_cvg[cvg].el_rate_pre_uw_pre_exp = ratio(hxd_cvg[cvg].el_cost_pre_uw_pre_exp, total_exposed_si) * 1000
        uw_adj = hxd_cvg[cvg].uw_adj
        hxd_cvg[cvg].el_cost_post_uw_pre_exp = hxd_cvg[cvg].el_cost_pre_uw_pre_exp * uw_adj
        hxd_cvg[cvg].el_rate_post_uw_pre_exp = ratio(hxd_cvg[cvg].el_cost_post_uw_pre_exp, total_exposed_si) * 1000
        
        # --- Post-experience adj
        hxd_cvg[cvg].expected_loss_cost = hxd_cvg[cvg].el_cost_post_uw_pre_exp * discount
        total_expected_loss_cost += hxd_cvg[cvg].expected_loss_cost  # For allocation of fixed expenses in TP

        benchmark_premium = ratio(ratio(hxd_cvg[cvg].expected_loss_cost, benchmark_lr), (1 - brokerage))
        hxd_cvg[cvg].benchmark_premium = benchmark_premium
        hxd_cvg[cvg].benchmark_rate = ratio(hxd_cvg[cvg].benchmark_premium, total_exposed_si) * 1000
    
    # Exit and re-enter loop to allow calc of total EL
    for cvg in covered_benefits:
        technical_premium = calculate_technical_premium(hxd, hxd_cvg[cvg].expected_loss_cost, total_expected_loss_cost)
        hxd_cvg[cvg].technical_premium = technical_premium
        hxd_cvg[cvg].technical_rate = ratio(hxd_cvg[cvg].technical_premium, total_exposed_si) * 1000

        # hxd_cvg[cvg].uw_adj_impact = ratio(hxd_cvg[cvg].quoted_rate, hxd_cvg[cvg].technical_rate)
        hxd_cvg[cvg].uw_adj_impact = ratio(hxd_cvg[cvg].quoted_rate, hxd_cvg[cvg].benchmark_rate)
        hxd_cvg[cvg].quoted_premium = hxd_cvg[cvg].quoted_rate * total_exposed_si / 1000

    # Total (ex PC & NCB)
    hxd_structures = [db, adb, ti, ci, re]
    tot_ex.el_cost_pre_uw_pre_exp = 0
    tot_ex.el_cost_post_uw_pre_exp = 0
    tot_ex.expected_loss_cost = 0
    tot_ex.benchmark_premium = 0
    tot_ex.technical_premium = 0
    tot_ex.quoted_premium = 0
    
    for cover in hxd_structures:
        tot_ex.el_cost_pre_uw_pre_exp += cover.el_cost_pre_uw_pre_exp or 0  # Replaced `getattr` with direct attribute access
        tot_ex.el_cost_post_uw_pre_exp += cover.el_cost_post_uw_pre_exp or 0
        tot_ex.expected_loss_cost += cover.expected_loss_cost or 0
        tot_ex.benchmark_premium += cover.benchmark_premium or 0
        tot_ex.technical_premium += cover.technical_premium or 0
        tot_ex.quoted_premium += cover.quoted_premium or 0

    tot_ex.el_rate_pre_uw_pre_exp = ratio(tot_ex.el_cost_pre_uw_pre_exp, total_exposed_si) * 1000
    tot_ex.el_rate_post_uw_pre_exp = ratio(tot_ex.el_cost_post_uw_pre_exp, total_exposed_si) * 1000
    tot_ex.uw_adj = ratio(tot_ex.el_cost_post_uw_pre_exp, tot_ex.el_cost_pre_uw_pre_exp)
    tot_ex.benchmark_rate = ratio(tot_ex.benchmark_premium, total_exposed_si) * 1000
    tot_ex.technical_rate = ratio(tot_ex.technical_premium, total_exposed_si) * 1000
    tot_ex.quoted_rate = ratio(tot_ex.quoted_premium, total_exposed_si) * 1000
    # tot_ex.uw_adj_impact = ratio(tot_ex.quoted_rate, tot_ex.technical_rate)
    tot_ex.uw_adj_impact = ratio(tot_ex.quoted_rate, tot_ex.benchmark_rate)

    # Calculate estimated payment values for PC and NCB on benchmark premium
    calculate_pc_ncb_on_benchmark(hxd, lives_df, covered_benefits)

    # Total for PC and NCB
    pc_g_or_n = pi.pc_to_gross.lower()
    ncb_g_or_n = pi.ncb_to_gross.lower()
    pc_load_attr = [pc_g_or_n, "pc_load"] #Changed from pc_load to pc_cost. YZ: Why? I changed back to the pc_load as this is the premium
    ncb_load_attr = [ncb_g_or_n, "ncb_load"]

    tot_pc.benchmark_premium = reduce(getattr, pc_load_attr, layer.pc.model)
    tot_pc.benchmark_rate = round(ratio(tot_pc.benchmark_premium, total_exposed_si) * 1000,2)
    tot_pc.technical_premium = tot_pc.benchmark_premium * ratio(tot_ex.technical_premium, tot_ex.benchmark_premium)
    tot_pc.technical_rate = ratio(tot_pc.technical_premium, total_exposed_si) * 1000

    tot_ncb.benchmark_premium = reduce(getattr, ncb_load_attr, layer.ncb.model)
    tot_ncb.benchmark_rate = round(ratio(tot_ncb.benchmark_premium, total_exposed_si) * 1000,2)
    tot_ncb.technical_premium = tot_ncb.benchmark_premium * ratio(tot_ex.technical_premium, tot_ex.benchmark_premium)
    tot_ncb.technical_rate = ratio(tot_ncb.technical_premium, total_exposed_si) * 1000

    # Calculate estimated payment values for PC and NCB on benchmark premium
    # For quoted premium for PC and NCB, assume that 1t is 100% benchmark premium. Why? BPI and TPI are derived from quoted premium
    tot_pc.quoted_premium = tot_pc.benchmark_premium 
    tot_pc.quoted_rate = round(ratio(tot_pc.quoted_premium, total_exposed_si) * 1000,2)
    # tot_pc.uw_adj_impact = ratio(tot_pc.quoted_rate, tot_pc.technical_rate)
    tot_pc.uw_adj_impact = ratio(tot_pc.quoted_rate, tot_pc.benchmark_rate)
    
    # Why here quoted premium = benchmark premium? Why? BPI and TPI are derived from quoted premium
    tot_ncb.quoted_premium = tot_ncb.benchmark_premium
    tot_ncb.quoted_rate = round(ratio(tot_ncb.quoted_premium, total_exposed_si) * 1000,2)
    # tot_ncb.uw_adj_impact = ratio(tot_ncb.quoted_rate, tot_ncb.technical_rate)
    tot_ncb.uw_adj_impact = ratio(tot_ncb.quoted_rate, tot_ncb.benchmark_rate)

    # Total totals    
    tot_tot.el_cost_pre_uw_pre_exp = 0
    tot_tot.el_cost_post_uw_pre_exp = 0
    tot_tot.expected_loss_cost = 0
    tot_tot.benchmark_premium = tot_pc.benchmark_premium + tot_ncb.benchmark_premium
    tot_tot.technical_premium = tot_pc.technical_premium + tot_ncb.technical_premium
    tot_tot.quoted_premium = tot_pc.quoted_premium + tot_ncb.quoted_premium
    
    for cover in hxd_structures:
        tot_tot.el_cost_pre_uw_pre_exp += cover.el_cost_pre_uw_pre_exp or 0  # Replaced `getattr` with direct attribute access
        tot_tot.el_cost_post_uw_pre_exp += cover.el_cost_post_uw_pre_exp or 0
        tot_tot.expected_loss_cost += cover.expected_loss_cost or 0
        tot_tot.benchmark_premium += cover.benchmark_premium or 0
        tot_tot.technical_premium += cover.technical_premium or 0
        tot_tot.quoted_premium += cover.quoted_premium or 0

    tot_tot.el_rate_pre_uw_pre_exp = ratio(tot_tot.el_cost_pre_uw_pre_exp, total_exposed_si) * 1000
    tot_tot.uw_adj = ratio(tot_tot.el_cost_post_uw_pre_exp, tot_tot.el_cost_pre_uw_pre_exp)
    tot_tot.el_rate_post_uw_pre_exp = ratio(tot_tot.el_cost_post_uw_pre_exp, total_exposed_si) * 1000
    #tot_tot.benchmark_rate = round(ratio(tot_tot.benchmark_premium, total_exposed_si) * 1000,2)
    tot_tot.benchmark_rate = tot_ex.benchmark_rate + tot_pc.benchmark_rate + tot_ncb.benchmark_rate
    tot_tot.technical_rate = ratio(tot_tot.technical_premium, total_exposed_si) * 1000
    #tot_tot.quoted_rate = round(ratio(tot_tot.quoted_premium, total_exposed_si) * 1000,2)
    tot_tot.quoted_rate = tot_ex.quoted_rate + tot_ncb.quoted_rate + tot_pc.quoted_rate
    tot_tot.quoted_premium = round(tot_tot.quoted_rate * total_exposed_si / 1000,2)
    # tot_tot.uw_adj_impact = ratio(tot_tot.quoted_rate, tot_tot.technical_rate)
    tot_tot.uw_adj_impact = ratio(tot_tot.quoted_rate, tot_tot.benchmark_rate)

    # Assign to layer totals for Rating Summary and calculate TPI
    sync_technical_summary(hxd, pc_load_attr, ncb_load_attr, discount)

    # Validate fields
    if tot_tot.el_cost_pre_uw_pre_exp > 0 and tot_ex.quoted_premium <= 0:
        hx.errors.validation("Commercially Achieved Premium in Rating Summary must be greater than 0. Please check the Commercial RPM.")

    # Add summary statistics
    layer.lives_wtd_avg_age, layer.max_age, layer.min_age = calculate_statistics(lives_df, "age_attained")
    layer.si_wtd_avg_age = calculate_statistics(lives_df, "age_attained", weight_col="sum_insured", weighted_avg_only=True)
    layer.lives_wtd_avg_salary, layer.max_salary, layer.min_salary = calculate_statistics(lives_df, "salary")
    layer.lives_wtd_avg_si, layer.max_si, layer.min_si = calculate_statistics(lives_df, "sum_insured")

    layer.total_no_lives = lives_df["no_lives"].sum()
    lives_df["db_qx_cleaned"] = lives_df["db_qx"].fillna(0) # Avoid None errors
    layer.exp_no_deaths_per_thousand = ratio(np.dot(lives_df["no_lives"], lives_df["db_qx_cleaned"]), layer.total_no_lives)
    layer.exp_no_deaths = layer.exp_no_deaths_per_thousand * layer.total_no_lives / 1000
    
    layer.avg_cost = layer.lives_wtd_avg_si
    lives_df["variance"] = lives_df["no_lives"] * (lives_df["sum_insured"] - layer.lives_wtd_avg_si)**2
    layer.sd_cost = np.sqrt(ratio(lives_df["variance"].sum(), layer.total_no_lives))

    layer.brokerage_view = layer.brokerage
    layer.status_view = layer.status
    layer.section_reference_view = hxd.cds.standard_fields.policy_reference

    if hxd.cds.standard_fields.is_rater_priced:
        layer.written_line_view = layer.written_line_input
    else:
        layer.written_line_view = layer.written_line



