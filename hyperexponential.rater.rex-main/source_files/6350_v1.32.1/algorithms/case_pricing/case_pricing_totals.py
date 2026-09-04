import hx 


def case_pricing_totals(hxd):

    us_perils = ["us_ws", "us_eq", "us_tn", "us_ha", "us_fl", "us_wf"]
    intl_perils = ["intl_ws", "intl_eq", "intl_tn", "intl_ha", "intl_fl", "intl_wf"]
    all_perils = ["fire"] + us_perils + intl_perils

    team = hxd.policy_information.team or "NACP"
    tps_team = hx.params.assumption_1_in_250_team.set_index('Field')[team].to_dict()
    nmp_load = tps_team['NMP Load'] + 1

    for layer in hxd.layers:
        cp = layer.case_pricing
        el_obj = layer.case_pricing.expected_loss
        tech_obj = layer.case_pricing.tech_premium

        brokerage = layer.brokerage or 0
        quoted_prem = layer.achieved_premium_100_gg or 0

        # Sum totals exp loss
        cp.us_exp_loss = sum([getattr(el_obj, peril) or 0 for peril in us_perils])
        cp.intl_exp_loss = sum([getattr(el_obj, peril) or 0 for peril in intl_perils])
        cp.total_exp_loss = (cp.us_exp_loss + cp.intl_exp_loss + (el_obj.fire or 0)) * nmp_load

        # Sum totals tech premium
        cp.us_tech_prem = sum([getattr(tech_obj, peril) or 0 for peril in us_perils])
        cp.intl_tech_prem = sum([getattr(tech_obj, peril) or 0 for peril in intl_perils])
        cp.technical_premium = cp.us_tech_prem + cp.intl_tech_prem + (cp.nmp_premium or 0) + (tech_obj.fire or 0)


        cp.benchmark_premium = (cp.total_exp_loss / 0.7) / (1 - brokerage)
        cp.tpi = quoted_prem / cp.technical_premium if cp.technical_premium and quoted_prem else None
        cp.bpi = quoted_prem / cp.benchmark_premium if cp.benchmark_premium and quoted_prem else None
        cp.elr = cp.total_exp_loss / quoted_prem if quoted_prem else None

        # Set rate change (overwrite)
        hxd.rate_change.risk_adjusted_rate_change.technical = cp.risk_adj_rate_change or 0
       
        # Set TPI / BPI / ELR (in Rating Summary)
        layer.pre_uw_adjustment.expected_loss.elr = cp.elr
        layer.post_uw_adjustment.expected_loss.elr = cp.elr

        layer.pre_uw_adjustment.benchmark_premium.bpi = cp.bpi
        layer.post_uw_adjustment.benchmark_premium.bpi = cp.bpi

        layer.pre_uw_adjustment.gross_tech_prem.tpi = cp.tpi
        layer.post_uw_adjustment.gross_tech_prem.tpi = cp.tpi

    # Validation
    for layer in hxd.layers:
        if round(layer.case_pricing.technical_premium or 0) != round(layer.pre_uw_adjustment.gross_tech_prem.gross_tech_prem_total or 0):
            hx.errors.validation("Case priced premium does not match Rating Summary. Save results to continue. Actuary use only.")
            break
        




