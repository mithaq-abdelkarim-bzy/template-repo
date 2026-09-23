import hx
import pandas as pd
import numpy as np
from algorithms.rate_utilities import ratio, one_layer, pd_df_from_hx_list, write_pd_to_hxd, usd, validate_empty_fields
from algorithms.rate_utilities import find_closest, look_up_closest, look_up, tp_components
from algorithms.rate_constants import benchmark_lr

def rate_life(hxd):
    # Only run when Individual selected
    if hxd.cds.is_group:
        return

    # Initialise param tables
    NonSmokerF = hx.params.NonSmokerF
    NonSmokerM = hx.params.NonSmokerM
    NatLocCode = hx.params.NatLocCode
    calcNaturalNationalityWeight = hx.params.calcNaturalNationalityWeight
    OccAdj = hx.params.OccAdj
    RiProgramme = hx.params.RiProgramme
    NatCauseNonSmoker = hx.params.NatCauseNonSmoker
    NatCauseSmoker = hx.params.NatCauseSmoker
    AnyCauseNonSmoker = hx.params.AnyCauseNonSmoker
    AnyCauseSmoker = hx.params.AnyCauseSmoker
    AccidentalDeathNonSmoker = hx.params.AccidentalDeathNonSmoker
    AccidentalDeathSmoker = hx.params.AccidentalDeathSmoker
    RGAcountries = hx.params.RGAcountries
    CountryClassLoadRates = hx.params.CountryClassLoadRates

    # Initialise useful variables
    layer, cvg = one_layer(hxd)
    expo = hxd.cds.exposure.granular
    ccy = hxd.cds.currencies.source_currency

    brokerage_direct = layer.brokerage
    brokerage_ri = layer.brokerage_ri
    rga_load_mult = layer.rga_load_mult
    rga_load_add = layer.rga_load_add

    # Get DataFrame with exposures
    life = expo.life
    life_df = pd_df_from_hx_list(life)
    input_cols = [
        "age_next_bday",
        "sum_insured",
        "coverage",
        "nationality",
        "location",
        "smoker_status",
        "term"
        ]
    life_df = life_df[input_cols]

    # Calculate age attained
    if life_df["age_next_bday"].iloc[0] < 1:
        return

    life_df["age_attained"] = life_df["age_next_bday"] - 1

    # Define lists for possible terms
    terms_str = ["0", "1", "2", "3", "4"]
    terms_int = [0, 1, 2, 3, 4]

    # Define mapping of inputs to col names in df
    input_mapping = {
        "Death natural causes" : "nat",
        "Death any cause": "any",
        "Smoker": "s",
        "Non-smoker": "ns"
    }
    
    # Get factors needed from tables
    nat_nation_weight = calcNaturalNationalityWeight["Weight to nationality"].iloc[0]
    occ_1_adj = OccAdj["Occ 1 Adj"].iloc[0]
    occ_4_adj = OccAdj["Occ 4 Adj"].iloc[0]

    # Calculate RGA discount factor
    rga_discount = look_up("RGA discount", "RI programme", "Val", RiProgramme, lookup_type="single")
    si_threshold = look_up("for SI greater than ($)", "RI programme", "Val", RiProgramme, lookup_type="single")
    sum_insured = life_df["sum_insured"].iloc[0]
    # sum_insured_usd = sum_insured #* ccy - NOTE: looks like sum_insured is supposed to be input in USD
    discount_factor = 1 - rga_discount if sum_insured > si_threshold else 1

    # Calculate country modifier
    country_code = look_up(life_df["nationality"], "Country", "Code", RGAcountries).iloc[0]
    country_mod = look_up(country_code, "Country Class", "Load to Rates Provided", CountryClassLoadRates, lookup_type="single")

    # Calculate surplus-related numbers
    lower_limit = look_up("Up to ($)", "RI programme", "Val", RiProgramme, lookup_type="single")
    ppn_ceded_below = look_up("ppn ceded", "RI programme", "Val", RiProgramme, lookup_type="single")
    ppn_ceded_above = look_up("ppn ceded", "RI programme", "Val1", RiProgramme, lookup_type="single")
    bzl_payout_no_surplus = sum_insured * ppn_ceded_below
    rga_payout_no_surplus = sum_insured - bzl_payout_no_surplus
    bzl_payout_w_surplus = min(sum_insured, lower_limit) * (1-ppn_ceded_below) + max(0, sum_insured - lower_limit) * (1-ppn_ceded_above)
    rga_payout_w_surplus = sum_insured - bzl_payout_w_surplus

    # Calculate all rates
    for t_str, t_int in zip(terms_str, terms_int):
        life_df[f"x_x_cmi_M_rate_{t_str}"] = look_up(life_df["age_attained"] + t_int, "Age", t_str, NonSmokerM)
        life_df[f"x_x_cmi_F_rate_{t_str}"] = look_up(life_df["age_attained"] + t_int, "Age", t_str, NonSmokerF)
    for t_str, t_int in zip(terms_str[:-1], terms_int[:-1]):    
        life_df[f"x_x_cmi_M_rel_{t_str}"] = ratio(life_df[f"x_x_cmi_M_rate_{str(t_int+1)}"], life_df[f"x_x_cmi_M_rate_{t_str}"])
        life_df[f"x_x_cmi_F_rel_{t_str}"] = ratio(life_df[f"x_x_cmi_F_rate_{str(t_int+1)}"], life_df[f"x_x_cmi_F_rate_{t_str}"])

    life_df["loc_M_age"] = life_df["location"] + "M" + life_df["age_attained"].astype(str)
    life_df["loc_F_age"] = life_df["location"] + "F" + life_df["age_attained"].astype(str)
    life_df["nation_M_age"] = life_df["nationality"] + "M" + life_df["age_attained"].astype(str)
    life_df["nation_F_age"] = life_df["nationality"] + "F" + life_df["age_attained"].astype(str)
    life_df["x_amr_nat_M_term_0"] = (look_up(life_df["loc_M_age"], "Code", "q(Natural only)", NatLocCode) * (1-nat_nation_weight) + look_up(life_df["nation_M_age"], "Code", "q(Natural only)", NatLocCode) * nat_nation_weight) / 1000
    life_df["x_amr_nat_F_term_0"] = (look_up(life_df["loc_F_age"], "Code", "q(Natural only)", NatLocCode) * (1-nat_nation_weight) + look_up(life_df["nation_F_age"], "Code", "q(Natural only)", NatLocCode) * nat_nation_weight) / 1000
    life_df["x_amr_acc_M_term_0"] = look_up(life_df["loc_M_age"], "Code", "q(Non-natural only)", NatLocCode) / 1000
    life_df["x_amr_acc_F_term_0"] = look_up(life_df["loc_F_age"], "Code", "q(Non-natural only)", NatLocCode) / 1000
    life_df["x_asp_nat_B_term_0"] = 1 - np.mean([life_df["x_amr_nat_M_term_0"], life_df["x_amr_nat_F_term_0"]])
    life_df["x_asp_acc_B_term_0"] = 1 - np.mean([life_df["x_amr_acc_M_term_0"], life_df["x_amr_acc_F_term_0"]])

    cumul_rel_M = 1
    cumul_rel_F = 1
    for t_str, t_int in zip(terms_str[:-1], terms_int[:-1]):
        cumul_rel_M *= life_df[f"x_x_cmi_M_rel_{t_str}"].iloc[0]
        cumul_rel_F *= life_df[f"x_x_cmi_F_rel_{t_str}"].iloc[0]
        life_df[f"x_asp_nat_B_term_{str(t_int+1)}"] = 1 - np.mean([life_df["x_amr_nat_M_term_0"] * cumul_rel_M, life_df["x_amr_nat_F_term_0"] * cumul_rel_F])
        life_df[f"x_asp_acc_B_term_{str(t_int+1)}"] = 1 - np.mean([life_df["x_amr_acc_M_term_0"] * cumul_rel_M, life_df["x_amr_acc_F_term_0"] * cumul_rel_F])

    cumul_asp_nat = 1
    cumul_asp_acc = 1
    cumul_asp_any = 1
    for t_str, t_int in zip(terms_str, terms_int):
        life_df[f"x_asp_any_B_term_{t_str}"] = life_df[f"x_asp_nat_B_term_{t_str}"] + life_df[f"x_asp_acc_B_term_{t_str}"] - 1
        
        cumul_asp_nat *= life_df[f"x_asp_nat_B_term_{t_str}"]
        life_df[f"x_tmr_nat_B_term_{t_str}"] = 1 - cumul_asp_nat

        cumul_asp_acc *= life_df[f"x_asp_acc_B_term_{t_str}"]
        life_df[f"x_tmr_acc_B_term_{t_str}"] = 1 - cumul_asp_acc

        cumul_asp_any *= life_df[f"x_asp_any_B_term_{t_str}"]
        life_df[f"x_tmr_any_B_term_{t_str}"] = 1 - cumul_asp_any

        life_df[f"x_rpm_nat_B_term_{str(t_int+1)}"] = ratio(life_df[f"x_tmr_nat_B_term_{t_str}"], t_int + 1) * 1000
        life_df[f"x_rpm_acc_B_term_{str(t_int+1)}"] = ratio(life_df[f"x_tmr_acc_B_term_{t_str}"], t_int + 1) * 1000
        life_df[f"x_rpm_any_B_term_{str(t_int+1)}"] = ratio(life_df[f"x_tmr_any_B_term_{t_str}"], t_int + 1) * 1000

    # Exit loop and calculate rates for the selected term only
    term = life_df["term"].iloc[0]
    t_int = term - 1
    t_str = str(t_int)

    coverage = life_df["coverage"].iloc[0]
    smoker_status = life_df["smoker_status"].iloc[0]
    adjustment = country_mod * (1 + rga_load_mult) * discount_factor

    life_df[f"bzl_ns_nat_B_term_{str(t_int+1)}"] = life_df[f"x_rpm_nat_B_term_{str(t_int+1)}"] * occ_1_adj * (1 + rga_load_mult) + rga_load_add
    life_df[f"bzl_ns_acc_B_term_1"] = life_df[f"x_rpm_acc_B_term_1"] * occ_1_adj * (1 + rga_load_mult) + rga_load_add
    life_df[f"bzl_ns_any_B_term_{str(t_int+1)}"] = life_df[f"x_rpm_any_B_term_{str(t_int+1)}"] * occ_1_adj * (1 + rga_load_mult) + rga_load_add

    life_df[f"bzl_s_nat_B_term_{str(t_int+1)}"] = life_df[f"x_rpm_nat_B_term_{str(t_int+1)}"] * occ_4_adj * (1 + rga_load_mult) + rga_load_add
    life_df[f"bzl_s_acc_B_term_1"] = life_df[f"x_rpm_acc_B_term_1"] * occ_4_adj * (1 + rga_load_mult) + rga_load_add
    life_df[f"bzl_s_any_B_term_{str(t_int+1)}"] = life_df[f"x_rpm_any_B_term_{str(t_int+1)}"] * occ_4_adj * (1 + rga_load_mult) + rga_load_add

    life_df[f"rga_ns_nat_B_term_{str(t_int+1)}"] = ratio(
        look_up(life_df["age_next_bday"], "Age", str(t_int+1), NatCauseNonSmoker) * adjustment + rga_load_add, (1 - brokerage_ri)
    )
    life_df[f"rga_ns_acc_B_term_1"] = ratio(
        look_up(life_df["age_next_bday"], "Age", "Non-Smoker", AccidentalDeathNonSmoker) * adjustment + rga_load_add, (1 - brokerage_ri)
    )
    life_df[f"rga_ns_any_B_term_{str(t_int+1)}"] = ratio(
        look_up(life_df["age_next_bday"], "Age", str(t_int+1), AnyCauseNonSmoker) * adjustment + rga_load_add, (1 - brokerage_ri)
    )

    life_df[f"rga_s_nat_B_term_{str(t_int+1)}"] = ratio(
        look_up(life_df["age_next_bday"], "Age", str(t_int+1), NatCauseSmoker) * adjustment + rga_load_add, (1 - brokerage_ri)
    )
    life_df[f"rga_s_acc_B_term_1"] = ratio(
        look_up(life_df["age_next_bday"], "Age", "Smoker", AccidentalDeathSmoker) * adjustment + rga_load_add, (1 - brokerage_ri)
    )
    life_df[f"rga_s_any_B_term_{str(t_int+1)}"] = ratio(
        look_up(life_df["age_next_bday"], "Age", str(t_int+1), AnyCauseSmoker) * adjustment + rga_load_add, (1 - brokerage_ri)
    )

    life_df[f"bm_ns_nat_B_term_{str(t_int+1)}"] = ratio(
        ratio(life_df[f"bzl_ns_nat_B_term_{str(t_int+1)}"] * bzl_payout_no_surplus, benchmark_lr) + life_df[f"rga_ns_nat_B_term_{str(t_int+1)}"] * rga_payout_no_surplus,
        (1 - brokerage_direct) * sum_insured
    )
    life_df[f"bm_ns_acc_B_term_1"] = ratio(
        ratio(life_df[f"bzl_ns_acc_B_term_1"] * bzl_payout_no_surplus, benchmark_lr) + life_df[f"rga_ns_acc_B_term_1"] * rga_payout_no_surplus,
        (1 - brokerage_direct) * sum_insured
    )
    life_df[f"bm_ns_any_B_term_{str(t_int+1)}"] = ratio(
        ratio(life_df[f"bzl_ns_any_B_term_{str(t_int+1)}"] * bzl_payout_no_surplus, benchmark_lr) + life_df[f"rga_ns_any_B_term_{str(t_int+1)}"] * rga_payout_no_surplus,
        (1 - brokerage_direct) * sum_insured
    )

    life_df[f"bm_s_nat_B_term_{str(t_int+1)}"] = ratio(
        ratio(life_df[f"bzl_s_nat_B_term_{str(t_int+1)}"] * bzl_payout_no_surplus, benchmark_lr) + life_df[f"rga_s_nat_B_term_{str(t_int+1)}"] * rga_payout_no_surplus,
        (1 - brokerage_direct) * sum_insured
    )
    life_df[f"bm_s_acc_B_term_1"] = ratio(
        ratio(life_df[f"bzl_s_acc_B_term_1"] * bzl_payout_no_surplus, benchmark_lr) + life_df[f"rga_s_acc_B_term_1"] * rga_payout_no_surplus,
        (1 - brokerage_direct) * sum_insured
    )
    life_df[f"bm_s_any_B_term_{str(t_int+1)}"] = ratio(
        ratio(life_df[f"bzl_s_any_B_term_{str(t_int+1)}"] * bzl_payout_no_surplus, benchmark_lr) + life_df[f"rga_s_any_B_term_{str(t_int+1)}"] * rga_payout_no_surplus,
        (1 - brokerage_direct) * sum_insured
    )

    # Beazley to pay RGA
    rate_col = f"{input_mapping[smoker_status]}_{input_mapping[coverage]}_B_term_{str(term)}"
    rga_rate_col = f"rga_{rate_col}"
    life_df["rga_rate"] = life_df[rga_rate_col] * (1 - brokerage_ri)
    life_df["rga_premium"] = life_df["rga_rate"] * rga_payout_w_surplus / 1000

    # RI Brokerage
    life_df["gross_rga_premium"] = ratio(life_df["rga_premium"], (1 - brokerage_ri))
    life_df["brokerage_ri_amount"] = life_df["gross_rga_premium"] * brokerage_ri

    # Beazley to charge
    bzl_rate_col = f"bm_{rate_col}"
    life_df["bzl_rate"] = life_df[bzl_rate_col]
    life_df["bzl_premium"] = life_df[bzl_rate_col] * sum_insured / 1000

    # Get key TP params and calculate EL
    tp = tp_components(hxd)
    nmp_load = tp["nmp_load"]
    net_rate_col = f"bzl_{rate_col}"
    life_df["expected_loss_cost"] = life_df[net_rate_col] * bzl_payout_w_surplus * (1 + nmp_load) / 1000

    # Push to hxd
    output_cols = [
        "age_attained",
        "rga_rate", 
        "rga_premium",
        "brokerage_ri_amount",
        "gross_rga_premium",
        "bzl_rate", 
        "bzl_premium"
    ]
    write_pd_to_hxd(life_df, life, output_cols)

    # Produce rating summary - with override for gross quoted premium
    layer.quoted_premium_ind.calculated = life_df["bzl_premium"].iloc[0]
    layer.quoted_premium = layer.quoted_premium_ind.selected # Assign to CDS standard field
    layer.quoted_rate = ratio(layer.quoted_premium, sum_insured) * 1000
    
    layer.expected_loss_cost = life_df["expected_loss_cost"].iloc[0]
    rga_premium = life_df["rga_premium"].iloc[0]
    layer.quoted_premium_net = layer.quoted_premium - rga_premium

    benchmark_premium_net = ratio(layer.expected_loss_cost, benchmark_lr)
    layer.benchmark_premium = ratio(benchmark_premium_net, (1-layer.brokerage))
    layer.bpi = ratio(layer.quoted_premium_net, layer.benchmark_premium)

    # Set key TP params
    che = tp["che"]
    fixed_exp = 0 # No fixed exp for Individual as written under a single facility
    technical_lr = tp["technical_lr"]

    # Calculate technical premium
    share_expected_loss = layer.expected_loss_cost * layer.written_line
    technical_premium_net = ratio(
        ratio((share_expected_loss*(1+che) + fixed_exp), technical_lr),
        layer.written_line
    )
    layer.technical_premium = ratio(technical_premium_net, (1-layer.brokerage))
    layer.tpi = ratio(layer.quoted_premium_net, layer.technical_premium)

    layer.written_line_view = layer.written_line
    layer.section_reference_view = hxd.cds.standard_fields.policy_reference
    layer.brokerage_view = layer.brokerage
    layer.status_view = layer.status

    if hxd.cds.standard_fields.rating_methodology == "Case Priced":
        layer.quoted_premium_case_priced_view = layer.quoted_premium
        layer.bpi_case_priced_view = layer.bpi