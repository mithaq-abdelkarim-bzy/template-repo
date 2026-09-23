import hx
import json
import copy
import time
import os
import pandas as pd
import numpy as np
import requests
import openpyxl
import datetime
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.rate_utilities import ratio, title_rc, one_layer, pd_df_from_hx_list, rsetattr, rgetkey
from algorithms.rate_rate_change import rate_change_buckets
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


@hx.task
def rarc_task(hxd, progress):
    layer, cvg = one_layer(hxd)
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected

    if not expiring_policy_option_id:
       hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get correct buckets based on coverage
    buckets = rate_change_buckets()

    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    # Allow for simulation of agg limits, PC/ NCB
    pi = hxd.cds.policy_info
    needs_sim = (
        (layer.aggregate_deductible is not None) or
        (layer.aggregate_limit is not None) or
        pi.has_profit_commission or
        pi.has_no_claims_bonus
    )
    
    if needs_sim:
        async_tasks = [simulate_years_task]
    else:
        # Check if the expiring data has aggs
        hx_renew = init_hx_renew_api()
        expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False).json()
        expiring_data = expiring_response["data"]

        expiring_aggregate_deductible = expiring_data["cds"]["layers"][0]["aggregate_deductible"]
        expiring_aggregate_limit = expiring_data["cds"]["layers"][0]["aggregate_limit"]

        if expiring_aggregate_deductible is not None or expiring_aggregate_limit is not None:
            async_tasks = [simulate_years_task]
        else:
            async_tasks = []

    # Rate Change with offline_hxd
    if layer.rate_change.is_from_inputs_only:
        rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=buckets,
            layers_path="cds/layers",
            expiring_actual_prem="quoted_premium",
            expiring_technical_prem="benchmark_premium",
            # Allow for migrated policies having no PC or NCB recorded
            current_actual_prem="totals/total_ex_pc_ncb/quoted_premium",
            current_technical_prem="totals/total_ex_pc_ncb/benchmark_premium",
            async_tasks=async_tasks,
            data_schema_static_path=data_schema_static_path
        )
    else:
        rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=buckets,
            layers_path="cds/layers",
            expiring_actual_prem="quoted_premium",
            expiring_technical_prem="benchmark_premium",
            async_tasks=async_tasks,
            data_schema_static_path=data_schema_static_path
        )

    rc_hxds = rc.calculate_repriced_values(
        # expiring_policy_option_id=129400
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()
    
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change = rarc_layer

    # Add comment specifying PC/NCB exclusion
    if layer.rate_change.is_from_inputs_only:
        layer.rate_change.rate_change.comments = "Excluding PC or NCB from premium"

# Import expiring policy for rate change
@hx.task
def expiring_policy_fetch_task(hxd, progress):
    layer, cvg = one_layer(hxd)

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: id used for testing
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False).json()
    expiring_data = expiring_response["data"]

    # Get fields from json response and push to hxd
    for idx, layer in enumerate(hxd.cds.layers):
        layer.rate_change.expiring_policy_info.expiring_premium = expiring_data["cds"]["layers"][idx]["quoted_premium"]
        layer.rate_change.expiring_policy_info.expiring_written_line = expiring_data["cds"]["layers"][idx]["written_line"]

    # Check if data is from inputs-only model
    lives_df = pd.DataFrame(expiring_data["cds"]["exposure"]["granular"]["lives"])
    layer.rate_change.is_from_inputs_only = True if lives_df["db_qx"].isnull().all() else False


@hx.task
def start_renewal_task(hxd, progress):
    layer, cvg = one_layer(hxd)
    sf = hxd.cds.standard_fields
    ms = hxd.model_state

    ms.pressed_start_renewal_task = True

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hx.meta.expiring_policy_option_id #or 55165 # NOTE: For testing in dev mode
    expiring_nodes = [
        "cds/policy_info", # getting and setting all the structure at once
        "cds/standard_fields/insured_name",
        "cds/standard_fields/broker",
        "cds/standard_fields/underwriter",
        "cds/standard_fields/rating_methodology",
        "cds/currencies/source_currency",
        "cds/layers/written_line_input",
        "cds/layers/brokerage",
        "cds/layers/aggregate_limit",
        "cds/layers/aggregate_deductible",
        "cds/layers/coverages/death/cover_type",
        "cds/layers/coverages/additional_death/is_covered",
        "cds/layers/coverages/death/accidental_death_adj",
        "cds/layers/coverages/death/sick_affluence",
        "cds/layers/coverages/death/sick_weight_to_nationality",
        "cds/layers/coverages/death/accidental_death_rate",
        "cds/layers/coverages/terminal_illness/is_covered",
        "cds/layers/coverages/critical_illness/is_covered",
        "cds/layers/coverages/critical_illness/benefit",
        "cds/layers/coverages/critical_illness/benefit_amount_fixed",
        "cds/layers/coverages/critical_illness/benefit_amount_pct",
        "cds/layers/coverages/critical_illness/cap_amount",
        "cds/layers/coverages/critical_illness/cap_pct",
        "cds/layers/coverages/repat_exp/is_covered",
        "cds/layers/coverages/repat_exp/limit",
        "cds/experience_rating/claims_available",
        "cds/experience_rating/death_or_all_risks",
        "cds/quote/exclusions",
        "cds/quote/conditions"
    ]   

    try: 
        # raise ValueError("test") # NOTE: For testing in dev mode

        expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False).json()
        expiring_data = expiring_response["data"]

        # Check if policy is Individual
        if rgetkey(expiring_data, "cds/is_individual"):
            hxd.cds.rater = "Individual"
            sf.is_renewal = True
            hxd.cds.policy_info.application_date = datetime.date.today()
            layer.status = "Quoted"
            return
        
        # Push expiring data to hxd
        for node in expiring_nodes:
            value = rgetkey(expiring_data, node)
            rsetattr(hxd, node, value)

        # Treat claims separately to allow for 1-year offset
        # NOTE: this could be more robust if the expiring claim years matched the current claim years (instead on relying on the offset)
        expiring_claims_list = rgetkey(expiring_data, "cds/experience_rating/claims")
        claims_list = expiring_claims_list[:-1]

        if claims_list: # Check list is not empty
            input_fields = {"no_lives": 0, "sum_insured": 0, "incurred": 0, "number": 0}
            input_claims_list = [{k: claim[k] for k in input_fields.keys() if k in claim} for claim in claims_list]
            input_claims_list.insert(0, input_fields) # Offset by 1 year
            hxd.cds.experience_rating.claims = input_claims_list

        sf.is_renewal = True
        hxd.cds.policy_info.application_date = datetime.date.today()
        layer.status = "Quoted"

    except Exception as e:
        ms.landing_page_info = "❗❗ Failed to fetch expiring data. Please proceed and enter data manually. ❗❗"
        # ms.landing_page_info = e # NOTE: for debugging
        ms.has_import_failed = True
        

@hx.task
def quote_to_excel_task(hxd, progress):

    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/policy_doc_template/group_life_template.xlsx"

    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(template_path)
    sheet = workbook.active

    # Fill the named ranges with data
    for key, value in data.items():
        if key in workbook.defined_names:
            # Get the cell corresponding to the named range
            cells = workbook.defined_names[key].destinations
            for title, coord in cells:
                if title == sheet.title:  # Ensure the named range is in the correct sheet
                    sheet[coord] = value

    # Protect the sheet to prevent changes
    # sheet.protection.enable()
    # sheet.protection.set_password(excel_password)

    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)

    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Life"
    new_bug_report(hxd, progress, model_name)

@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)

@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)

@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)

@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)       





#Change to include simulation method for PC and NCB:
# No change for Agg losses
# Added stochastic NCB using no_claim_prob (all coverages)
# Added stochastic PC after NCB
# Output mean pc and ncb payment 



@hx.task
def simulate_years_task(hxd, progress):
    layer, cvg = one_layer(hxd)
    death_cover = layer.coverages.death
    temp = layer.temp
    db = cvg.death
    expo = hxd.cds.exposure.granular

    pi = hxd.cds.policy_info
    has_pc  = bool(pi.has_profit_commission)
    pc      = float(pi.profit_commission or 0.0)
    pc_exp  = float(pi.pc_expenses or 0.0)
    pc_def  = float(pi.pc_deficit or 0.0)
    
    brokerage = layer.brokerage or 0

    has_ncb = bool(pi.has_no_claims_bonus)
    ncb     = float(pi.ncb_pct or 0.0)

    tot_ex = layer.totals.total_ex_pc_ncb
    tot_tot = layer.totals.total
    

    # Quoted premium
    quoted_premium = float(tot_ex.quoted_premium or 0.0)
    p_pre_q_net = quoted_premium * (1 - brokerage)

    no_claim_prob = float(
        getattr(layer, "no_claim_prob", None)
        or getattr(temp, "no_claim_prob", None)
        or 0.0
    )

    no_claim_prob = min(max(no_claim_prob, 0.0), 1.0)

    # Parameters
    n_years = int(1e5)  # Number of years
    np.random.seed(1)  # Fix the simulation seed
    agg_deductible = layer.aggregate_deductible or 0 # Allow for agg deductible to be empty
    agg_limit = layer.aggregate_limit or int(1e99) # Allow for agg limit to be empty

    # # Check agg_limit and agg_deductible are full
    # if (layer.aggregate_deductible is None) and (layer.aggregate_limit is None) and not(has_ncb) and not(has_pc):
    #     hx.errors.fatal("Please fill in the PC/NCB, aggregate deductible and/or limit in Risk Information.")

    # Get the simulation df ready
    #lives = expo.lives

    sim_dict = [{
        "sum_insured": life.sum_insured,
        "db_qx": life.db_qx
    } for life in expo.lives]

    sim_df = pd.DataFrame(sim_dict)

    if sim_df["db_qx"].isnull().all() or sim_df["db_qx"].empty:
        hx.errors.fatal("Mortality rate for Death Benefit must be calculated first.")    

    sim_df.loc[:, "db_qx"] = sim_df["db_qx"] / 1000

    # --- Simulate loss years
    sum_insured = sim_df["sum_insured"]
    db_qx = sim_df["db_qx"]

    try:
        # raise ValueError("test") # NOTE: for testing task failure in dev

        # Generate random uniform numbers
        random_numbers = np.random.uniform(size=(n_years, len(db_qx)))

        # Compare with mortality rates
        death_occurrences = random_numbers < db_qx.to_numpy()

        # Calculate losses
        individual_losses = sum_insured.to_numpy() * death_occurrences

        # Sum the losses for each year
        annual_losses = np.sum(individual_losses, axis=1)
        db.el_cost_post_sim_pre_agg = float(np.mean(annual_losses))
        annual_losses = np.maximum(annual_losses, 0)

        # Calculated layered losses and take mean as the EL cost
        annual_losses_layer = np.minimum(np.maximum(annual_losses - agg_deductible, 0), agg_limit)
        # db.el_cost_post_sim.calculated = np.mean(annual_losses_layer)
        # YZ: Consider to add a mean before the layer is applied. This is to remove the simulation noise.
        el_sim = float(np.mean(annual_losses_layer))
        db.el_cost_post_sim.calculated = el_sim

        # Benchmark premium including the adjustment from the Agg
        # This benchmark premium position is not correct as this is pre the aggregate limit applied
        benchmark_premium_pre_agg = float(tot_ex.benchmark_premium or 0.0) 
        benchmark_rate_pre_agg = float(tot_ex.benchmark_rate or 0.0) 
        total_si = benchmark_premium_pre_agg / benchmark_rate_pre_agg 

        death_benchmark_premium_pre_agg = death_cover.benchmark_rate * total_si 
        death_benchmark_premium_post_agg = death_benchmark_premium_pre_agg * el_sim / db.el_cost_post_sim_pre_agg
        benchmark_premium = benchmark_premium_pre_agg - death_benchmark_premium_pre_agg + death_benchmark_premium_post_agg
        p_pre_net = benchmark_premium * (1 - brokerage)
            
        #Simulate NCB
        # Why the two methods not reconcile?
        if has_ncb and ncb and no_claim_prob > 0:
            ncb_indicator = np.random.binomial(1, no_claim_prob, size=n_years)
        else:                                                             
            ncb_indicator = np.zeros(n_years, dtype=float)
        # if using from simulation method, only consider the death rate
        # ncb_indicator = (annual_losses_layer == 0).astype(int)
              
        
        # NCB payable per year - store NET for now - check
        # Benchmark NCB
        # I can use the simulated reulsts to get the payout?
        ncb_payable_net = p_pre_net * ncb * ncb_indicator
        exp_ncb = float(np.mean(ncb_payable_net))

        # Quoted NCB
        ncb_payable_net_q = p_pre_q_net * ncb * ncb_indicator
        exp_ncb_q = float(np.mean(ncb_payable_net_q))


        
        #PC calculation per year from simulation results
        # Benchmark PC
        # pc_exp is gross or net?
        profit_base = (
            p_pre_net * (1 - pc_exp)
            - annual_losses_layer
            - pc_def
        )

        if has_pc and pc > 0:
            pc_pay = pc * np.maximum(profit_base, 0.0)
        else:
            pc_pay = np.zeros(n_years)

        exp_pc = float(np.mean(pc_pay))

        # Quoted PC
        profit_base_q = (
            p_pre_q_net * (1 - pc_exp)
            - annual_losses_layer
            - pc_def
        )

        if has_pc and pc > 0:
            pc_pay_q = pc * np.maximum(profit_base_q, 0.0)
        else:
            pc_pay_q = np.zeros(n_years)

        exp_pc_q = float(np.mean(pc_pay_q))


        # Store benchmark results 
        temp.exp_pc_payment_net_sim = exp_pc
        temp.exp_pc_payment_gross_sim = exp_pc / (1 - brokerage)

        temp.exp_ncb_payment_net_sim = exp_ncb
        temp.exp_ncb_payment_gross_sim = exp_ncb / (1 - brokerage)

        # Store quoted results
        temp.exp_pc_payment_quoted_net_sim = exp_pc_q
        temp.exp_pc_payment_quoted_gross_sim = exp_pc_q / (1 - brokerage)

        temp.exp_ncb_payment_quoted_net_sim = exp_ncb_q
        temp.exp_ncb_payment_quoted_gross_sim = exp_ncb_q / (1 - brokerage)

    
        temp.task_update_msg = "✅ Simulation + Premium adjustment from PC/NCB and (or) Agg structure completed."




    except Exception:
        temp.task_update_msg = "❌ Simulation failed."

    # Store agg limits and PC/NCB
    temp.aggregate_deductible = layer.aggregate_deductible
    temp.aggregate_limit = layer.aggregate_limit
    temp.profit_commission = pi.profit_commission
    temp.pc_expenses = pi.pc_expenses
    temp.pc_deficit = pi.pc_deficit
    temp.ncb_pct = pi.ncb_pct
    temp.total_quoted_rate_excl_pc_ncb = tot_ex.quoted_rate
    temp.is_agg_priced = True


    print("Benchmark PC:", temp.exp_pc_payment_net_sim)
    print("Quoted PC:", temp.exp_pc_payment_quoted_net_sim)
    print("Benchmark NCB:", temp.exp_ncb_payment_net_sim)
    print("Quoted NCB:", temp.exp_ncb_payment_quoted_net_sim)

    

