import hx
import requests
import math
import pandas as pd
import algorithms.utilities as util

def rate_change_rater(hxd):
    renewal_layer = hxd.rate_change.layer.renewal - 1

    hxd.rate_change.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id or 0

    fire_loss_curve_selection = hx.params.fire_loss_curve_selection
    flc = hx.params.flc

    if hxd.policy_information.large_schedule_model:
        num_locs = hxd.schedule.large_schedule_workflow.num_of_locations or 0
    else:
        num_locs = hxd.schedule.schedule_total.num_locs or 0
        
    expiring_num_locs = hxd.rate_change.expiring_policy_info.expiring_num_locs or 0

    tiv_total = hxd.schedule.schedule_total.tiv_total or 0
    expiring_tiv_total = hxd.rate_change.expiring_policy_info.expiring_tiv_total or 0

    # policy_length = hxd.policy_information.policy_length or 0
    policy_length = hxd.policy_information.policy_length.selected or 0
    expiring_policy_length = hxd.rate_change.expiring_policy_info.expiring_policy_length or 0

    for index, layer in enumerate(hxd.layers):
        if index == renewal_layer:
            
            writ_line = (layer.written_line_perc if layer.status in {'Bound', 'MTA', 'Cancellation'} else layer.quoted_line_perc) or 0
            expiring_writ_line = hxd.rate_change.expiring_policy_info.expiring_writ_line or 0

            achieved_premium = layer.achieved_premium_100_gg or 0
            expiring_achieved_premium = hxd.rate_change.expiring_policy_info.expiring_achieved_premium or 0
            hxd.rate_change.premium_policy_term.renewal = achieved_premium * writ_line
            hxd.rate_change.premium_policy_term.expiring = expiring_achieved_premium * expiring_writ_line

            premium_annualized = achieved_premium / policy_length if policy_length != 0 else 0
            expiring_premium_annualized =  expiring_achieved_premium / expiring_policy_length if expiring_policy_length != 0 else 0
            hxd.rate_change.premium_annualized.renewal = premium_annualized * writ_line
            hxd.rate_change.premium_annualized.expiring = expiring_premium_annualized * expiring_writ_line

            expected_loss = layer.pre_uw_adjustment.expected_loss.expected_loss or 0
            expiring_expected_loss = hxd.rate_change.expiring_policy_info.expiring_expected_loss or 0

            limit = layer.limit or 0
            expiring_limit = hxd.rate_change.expiring_policy_info.expiring_limit or 0
            excess = layer.excess or 0
            expiring_excess = hxd.rate_change.expiring_policy_info.expiring_excess or 0

            deductible = layer.perils.fire.deductible or 0
            expiring_deductible = hxd.rate_change.expiring_policy_info.expiring_deductible or 0

            brokerage = layer.brokerage or 0
            expiring_brokerage = hxd.rate_change.expiring_policy_info.expiring_brokerage or 0

            hxd.rate_change.premium_policy_term_100pct.renewal = achieved_premium
            hxd.rate_change.premium_policy_term_100pct.expiring = expiring_achieved_premium
            hxd.rate_change.premium_annualized_100pct.renewal = premium_annualized
            hxd.rate_change.premium_annualized_100pct.expiring = expiring_premium_annualized

            # AT Edit: exposure change ratio
            hxd.rate_change.exposure_change.renewal = tiv_total
            hxd.rate_change.exposure_change.expiring = expiring_tiv_total

            temp_exposure_change_ratio_1 = (tiv_total / expiring_tiv_total) if expiring_tiv_total != 0 else 1

            if pd.DataFrame(hxd.pricing_layer_segmentation.state).shape[0] > 0:
                largest_state_tiv = util.convert_hx_list_to_df(hxd.pricing_layer_segmentation.state)
                largest_state_tiv = largest_state_tiv.loc[largest_state_tiv["tiv"] == max(largest_state_tiv["tiv"])]["tiv"].iloc[0]
                largest_state_tiv_expiring = largest_state_tiv / temp_exposure_change_ratio_1

                pct_of_tiv_expiring_limit_renewal_tiv = (expiring_excess + expiring_limit) / largest_state_tiv if largest_state_tiv != 0  else 0
                pct_of_tiv_expiring_limit_expiring_tiv = (expiring_excess + expiring_limit) / largest_state_tiv_expiring if largest_state_tiv_expiring != 0 else 0
                pct_of_tiv_expiring_excess_renewal_tiv = expiring_excess / largest_state_tiv if largest_state_tiv != 0 else 0
                pct_of_tiv_expiring_excess_expiring_tiv = expiring_excess / largest_state_tiv_expiring if largest_state_tiv_expiring != 0 else 0
            else: 
                pct_of_tiv_expiring_limit_renewal_tiv = (expiring_excess + expiring_limit) / tiv_total if tiv_total != 0  else 0
                pct_of_tiv_expiring_limit_expiring_tiv = (expiring_excess + expiring_limit) / expiring_tiv_total if expiring_tiv_total != 0 else 0
                pct_of_tiv_expiring_excess_renewal_tiv = expiring_excess / tiv_total if tiv_total != 0 else 0
                pct_of_tiv_expiring_excess_expiring_tiv = expiring_excess / expiring_tiv_total if expiring_tiv_total != 0 else 0


            temp_exposure_change_ratio_2 = (interpolate(pct_of_tiv_expiring_limit_renewal_tiv) - interpolate(pct_of_tiv_expiring_excess_renewal_tiv)) / (interpolate(pct_of_tiv_expiring_limit_expiring_tiv) - interpolate(pct_of_tiv_expiring_excess_expiring_tiv)) if interpolate(pct_of_tiv_expiring_limit_expiring_tiv) - interpolate(pct_of_tiv_expiring_excess_expiring_tiv) > 0 else 1
            
            hxd.rate_change.exposure_change.ratio = temp_exposure_change_ratio_1 * temp_exposure_change_ratio_2 if temp_exposure_change_ratio_1 * temp_exposure_change_ratio_2 != 0 else 1
            # ~~

            # setting risk characteristics rate change factor to 1 to avoid including size discount into rate change. Changes made on 21/02/2014 and sould be reverted back after a year. 
            # hxd.rate_change.risk_characteristics_change.renewal = expected_loss
            # hxd.rate_change.risk_characteristics_change.expiring = expiring_expected_loss
            # hxd.rate_change.risk_characteristics_change.ratio = (expected_loss / expiring_expected_loss) if expiring_expected_loss != 0 else 1

            # AT Edit: risk characterisics change ratio
            hxd.rate_change.risk_characteristics_change.ratio = 1
            # ~~

            # AT Edit: deductible change ratio
            pct_of_tiv = deductible / (tiv_total / num_locs) if num_locs != 0 and tiv_total != 0 else 0
            expiring_pct_of_tiv = expiring_deductible / (tiv_total / num_locs) if num_locs != 0 and tiv_total != 0 else 0

            hxd.rate_change.deductible_change.renewal = deductible
            hxd.rate_change.deductible_change.expiring = expiring_deductible
            hxd.rate_change.deductible_change.ratio = 1 - (interpolate(pct_of_tiv) - interpolate(expiring_pct_of_tiv))
            # ~~

            # AT Edit: limit change ratio
            if pd.DataFrame(hxd.pricing_layer_segmentation.state).shape[0] > 0:
                pct_of_tiv_renewal_limit_renewal_tiv = (excess + limit) / largest_state_tiv if largest_state_tiv != 0  else 0
                pct_of_tiv_expiring_limit_renewal_tiv = (expiring_excess + expiring_limit) / largest_state_tiv if largest_state_tiv != 0 else 0
                pct_of_tiv_renewal_excess_renewal_tiv = excess / largest_state_tiv if largest_state_tiv != 0 else 0
                pct_of_tiv_expiring_excess_renewal_tiv = expiring_excess / largest_state_tiv if largest_state_tiv != 0 else 0
            else:
                pct_of_tiv_renewal_limit_renewal_tiv = (excess + limit) / tiv_total if tiv_total != 0  else 0
                pct_of_tiv_expiring_limit_renewal_tiv = (expiring_excess + expiring_limit) / tiv_total if tiv_total != 0 else 0
                pct_of_tiv_renewal_excess_renewal_tiv = excess / tiv_total if tiv_total != 0 else 0
                pct_of_tiv_expiring_excess_renewal_tiv = expiring_excess / tiv_total if tiv_total != 0 else 0

            hxd.rate_change.limit_change.renewal = limit
            hxd.rate_change.limit_change.expiring = expiring_limit
            hxd.rate_change.limit_change.ratio = (interpolate(pct_of_tiv_renewal_limit_renewal_tiv) - interpolate(pct_of_tiv_renewal_excess_renewal_tiv)) / (interpolate(pct_of_tiv_expiring_limit_renewal_tiv) - interpolate(pct_of_tiv_expiring_excess_renewal_tiv)) if (interpolate(pct_of_tiv_expiring_limit_renewal_tiv) - interpolate(pct_of_tiv_expiring_excess_renewal_tiv)) > 0 else 1
            # ~~

            # AT Edit: terms and conditions change ratio
            hxd.rate_change.terms_and_conditions_change.ratio = 1
            # ~~

            hxd.rate_change.other_change.renewal_brokerage = brokerage
            hxd.rate_change.other_change.renewal_signed_line = writ_line
            hxd.rate_change.other_change.expiring_brokerage = expiring_brokerage
            hxd.rate_change.other_change.expiring_signed_line = expiring_writ_line
            hxd.rate_change.other_change.ratio = (
                (((1 - expiring_brokerage)/(1 - brokerage)) * (writ_line / expiring_writ_line)) 
                if brokerage != 1 and achieved_premium != 0 and expiring_writ_line != 0 else 1
            )

            hxd.rate_change.exposure_change.ratio_uw.calculated = hxd.rate_change.exposure_change.ratio 
            hxd.rate_change.risk_characteristics_change.ratio_uw.calculated = hxd.rate_change.risk_characteristics_change.ratio 
            hxd.rate_change.deductible_change.ratio_uw.calculated = hxd.rate_change.deductible_change.ratio 
            hxd.rate_change.limit_change.ratio_uw.calculated = hxd.rate_change.limit_change.ratio 
            hxd.rate_change.terms_and_conditions_change.ratio_uw.calculated = hxd.rate_change.terms_and_conditions_change.ratio 
            hxd.rate_change.other_change.ratio_uw.calculated = hxd.rate_change.other_change.ratio 

            hxd.rate_change.total_factor.technical = ((
                        hxd.rate_change.exposure_change.ratio * 
                        hxd.rate_change.risk_characteristics_change.ratio * 
                        hxd.rate_change.deductible_change.ratio * 
                        hxd.rate_change.limit_change.ratio * 
                        hxd.rate_change.terms_and_conditions_change.ratio * 
                        hxd.rate_change.other_change.ratio * 
                        (expiring_writ_line / writ_line)
                    ) or 1) if writ_line else 1
                
            hxd.rate_change.total_factor.underwriter = ((
                        hxd.rate_change.exposure_change.ratio_uw.selected * 
                        hxd.rate_change.risk_characteristics_change.ratio_uw.selected * 
                        hxd.rate_change.deductible_change.ratio_uw.selected * 
                        hxd.rate_change.limit_change.ratio_uw.selected * 
                        hxd.rate_change.terms_and_conditions_change.ratio_uw.selected * 
                        hxd.rate_change.other_change.ratio_uw.selected * 
                        (expiring_writ_line / writ_line)
                    ) or 1) if writ_line else 1

            hxd.rate_change.simple_rate_change = (
                ((premium_annualized / tiv_total) / (expiring_premium_annualized / expiring_tiv_total))
                if tiv_total != 0 and expiring_tiv_total != 0 and expiring_premium_annualized != 0 else 1
                )
                
            hxd.rate_change.risk_adjusted_rate_change.technical = (
                (premium_annualized / (expiring_premium_annualized * hxd.rate_change.total_factor.technical)) 
                if expiring_premium_annualized * hxd.rate_change.total_factor.technical != 0 else 1
                )

            hxd.rate_change.risk_adjusted_rate_change.underwriter = (
                (premium_annualized / (expiring_premium_annualized * hxd.rate_change.total_factor.underwriter)) 
                if expiring_premium_annualized * hxd.rate_change.total_factor.underwriter != 0 else 1
                )

            if (
                hxd.rate_change.risk_adjusted_rate_change.technical > 1.3 or 
                hxd.rate_change.risk_adjusted_rate_change.underwriter > 1.3 or 
                hxd.rate_change.risk_adjusted_rate_change.technical < 1 or 
                hxd.rate_change.risk_adjusted_rate_change.underwriter < 1
            ):
                hxd.rate_change.error_message = "Rate change exceed our standard 100% to 130% threshold, confirm with the underwriter that it is accurate before binding"


# Async task (triggered by clicking a button) to import data from an expiring policy option into the current policy for rate change and analysis of movement
def expiring_policy_fetch(hxd, progress):
    user = hx.secrets.rest_api_user
    password = hx.secrets.rest_api_password

    expiring_policy_option_id = hxd.rate_change.expiring_policy_option_id.selected
    # expiring_policy_option_id = 64362

    environment_name = hx.secrets.environment_name.lower()

    # URL for the API
    url = f"https://api.{environment_name}.hxrenew.com/api/v1/policies/options/{expiring_policy_option_id}/snapshot"

    params = {
        "path": [
            "/policy_information/policy_length",
            "/layers/achieved_premium_100_gg",
            "/layers/perils/fire/deductible",
            "/layers/limit",
            "/layers/excess",
            "/layers/brokerage",
            "/layers/written_line_perc",
            "/layers/pre_uw_adjustment/expected_loss/expected_loss",
            "/schedule/schedule_total/tiv_total",
            "/schedule/schedule_total/num_locs",
            "/quote_documents/premium/total_exc_fees"
        ]
    }

    # Call to API
    try:
        response = requests.get(url, params=params, auth=(user, password))
    except requests.RequestException:
        hx.errors.fatal("Unable to connect to Renew REST API")

    # Error handling based on status code returned by API
    if response.ok:
        # results stored in dict : {data:{variable_name: value}}
        result = response.json()
        data = result["data"]

        expiring_layer = hxd.rate_change.layer.expiring - 1

        # DL EDIT 13.11.23 -- need to allow for two instances of the policy length given we have changed this to be an override. New policies have overrides, old don't
        if isinstance(data["policy_information"]["policy_length"], dict):
            hxd.rate_change.expiring_policy_info.expiring_policy_length = data["policy_information"]["policy_length"]["selected"] or 0
        else:
            hxd.rate_change.expiring_policy_info.expiring_policy_length = data["policy_information"]["policy_length"] or 0
        
        hxd.rate_change.expiring_policy_info.expiring_num_locs = data["schedule"]["schedule_total"]["num_locs"] or 0
        hxd.rate_change.expiring_policy_info.expiring_tiv_total = data["schedule"]["schedule_total"]["tiv_total"] or 0
        hxd.rate_change.expiring_policy_info.expiring_achieved_premium = data["layers"][expiring_layer]["achieved_premium_100_gg"] or 0
        hxd.rate_change.expiring_policy_info.expiring_limit = data["layers"][expiring_layer]["limit"]
        hxd.rate_change.expiring_policy_info.expiring_excess = data["layers"][expiring_layer]["excess"]
        hxd.rate_change.expiring_policy_info.expiring_deductible = data["layers"][expiring_layer]["perils"]["fire"]["deductible"]
        hxd.rate_change.expiring_policy_info.expiring_brokerage = data["layers"][expiring_layer]["brokerage"]
        hxd.rate_change.expiring_policy_info.expiring_writ_line = data["layers"][expiring_layer]["written_line_perc"]
        hxd.rate_change.expiring_policy_info.expiring_expected_loss = data["layers"][expiring_layer]["pre_uw_adjustment"]["expected_loss"]["expected_loss"]
        hxd.rate_change.expiring_bpro_premium = data["quote_documents"]["premium"]["total_exc_fees"] or data["layers"][expiring_layer]["achieved_premium_100_gg"]
        
    # Raises error if status code is not 200
    else:
        try:
            response_json = response.json()
            error = f"Error: {response_json.get('title')}"
            error += f"\nDetail: {response_json.get('detail')}" if response_json.get("detail") else ""
            hx.errors.fatal(error)
        except:
            hx.errors.fatal(f"Error: {response.text}")


def interpolate(val, table=hx.params.flc, col="MH4"):
    bounds = table["% of TIV"].to_list()

    bounds.sort()  # just in case
    smallest_upper_bound = next((x for x in bounds if x > val), 1)

    bounds.reverse()
    largest_lower_bound = next((x for x in bounds if x < val), 0)

    filtered_table = table[table["% of TIV"].isin([smallest_upper_bound, largest_lower_bound])][col]
    return ((val - largest_lower_bound) / (smallest_upper_bound - largest_lower_bound)) * (filtered_table.iloc[1] - filtered_table.iloc[0]) + filtered_table.iloc[0]