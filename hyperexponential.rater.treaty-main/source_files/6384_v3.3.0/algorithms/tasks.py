import hx, os, json, requests, openpyxl
import pandas as pd
#from algorithms.rate_rate_change import rate_change_buckets
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
#from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib

from algorithms.async_curve_aggregator import aggregate_curves, pull_pml_curves
from algorithms.async_rms_el_allocation import rms_el_allocation
from algorithms.async_nmp_calc import nmp_calc
from algorithms.async_simulation import file_processing, run_simulation, file_formatter_read, file_formatter_write
from algorithms.async_peril_allocation import peril_allocation
from algorithms.async_rate_change import rate_change
from algorithms.async_fetch_bi_data import bi_data_fetch
from algorithms.async_generate_tags import generate_tags
from algorithms.synergy_upload.async_synergy_upload import synergy_send_front_sheet, synergy_send_rate_change, send_eso
from algorithms.async_exposure_simulation import run_exposure_simulation
from libraries.rate_change.algorithms.offline_hxd.offline_hxd import rgetattr, rsetattr
import algorithms.rate_utilities as utils

@hx.task
def rate_change_task(hxd, progress):
    rate_change(hxd, progress)

@hx.task
def peril_allocation_task(hxd, progress):
    peril_allocation(hxd, progress)

@hx.task
def pull_pml_curves_task(hxd, progress):
    pull_pml_curves(hxd, progress)

@hx.task
def aggregate_curves_task(hxd, progress):
    aggregate_curves(hxd, progress)

@hx.task
def rms_el_allocation_task(hxd, progress):
    rms_el_allocation(hxd, progress)

@hx.task
def nmp_calc_task(hxd, progress):
    nmp_calc(hxd, progress)

@hx.task
def file_processing_task(hxd, progress):
    file_processing(hxd, progress)

@hx.task
def run_simulation_task(hxd, progress):
    run_simulation(hxd, progress)

@hx.task
def file_formatter_read_task(hxd, progress):
    file_formatter_read(hxd, progress)

@hx.task
def file_formatter_write_task(hxd, progress):
    file_formatter_write(hxd, progress)

@hx.task
def bi_data_fetch_task(hxd, progress):
    bi_data_fetch(hxd, progress)

@hx.task
def generate_tags_task(hxd, progress):
    generate_tags(hxd, progress)

@hx.task
def synergy_send_front_sheet_task(hxd, progress):
    synergy_send_front_sheet(hxd, progress)

@hx.task
def synergy_send_rate_change_task(hxd, progress):
    synergy_send_rate_change(hxd, progress)

@hx.task
def send_eso_task(hxd, progress):
    send_eso(hxd, progress)

@hx.task
def populate_model_task(hxd, progress):
    populate_model(hxd, progress)

@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

@hx.task
def run_exposure_simulation_task(hxd, progress):
    run_exposure_simulation(hxd, progress)


@hx.task
def start_renewal_task(hxd, progress):
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    cds = hxd.cds
    ms = hxd.model_state
    sf = hxd.cds.standard_fields

    if not hxd.cds.standard_fields.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
    else:
        ms.pressed_start_renewal_task = True
        ms.expiring_policy_option_id = hx.meta.expiring_policy_option_id
        ## TODO: remove
        # use example data 10
        # ms.expiring_policy_option_id = 1602969
        sf.is_renewal = True

        # Initialise the hx_renew_api library
        hx_renew = init_hx_renew_api()

        expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=ms.expiring_policy_option_id, stream=False)

        if expiring_response.status_code != 200:
            raise Exception(expiring_response.json())

        expiring_data = expiring_response.json()["data"]

        # /risk_information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        cds.layer_totals.limit_ly = expiring_data["cds"]["layer_totals"]["limit"]

        # /pml_curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for curve_type in ["rms_curves", "air_curves", "other_curves", "nmp_curves"]:
            for index, curve in enumerate(getattr(cds.pml_curves, curve_type)):     
                for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
                    rsetattr(curve,f"rp_loss_prev.{rp}", expiring_data["cds"]["pml_curves"][f"{curve_type}"][index]["rp_loss"][f"{rp}"])

        # /modelling_account_level ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for child in ["carolinas_ws", "miami_dade_ws", "gulf_ws", "ne_ws", "fl_pinnelas_ws", "la_eq", "nm_eq", "nm_stress_eq", "sf_eq"]:
            setattr(cds.modelling_account_level.rds_gross_loss.previous_year, f"{child}" , expiring_data["cds"]["modelling_account_level"]["rds_gross_loss"]["this_year"][f"{child}"]) 

        # /exposure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for child in ["bespoke_total"]:
            setattr(cds.exposure.aggregate.ly_aggregates, f"{child}", expiring_data["cds"]["exposure"]["aggregate"]["ty_aggregates"][f"{child}"])
        
        for index, exposure in enumerate(cds.exposure.granular.exposures):
            exposure.ly_aggregate = expiring_data["cds"]["exposure"]["granular"]["exposures"][index]["ty_aggregate"]

        # /experience_rating ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for index, claim in enumerate(cds.experience_rating.claims):
            claim.previous_year_total = expiring_data["cds"]["experience_rating"]["claims"][index]["this_year_total"]

        ### once policy renewed, yoa increased by 1, therefore the rows of the exposure_listing table will be 1 year ahead of where they should be
        ### therefore, we need to shift each row up 1 to make sure the exposure correseponds to the correct year

        exposure_df = pd.DataFrame(expiring_data["cds"]["experience_rating"]["exposure"]["exposure_listing"])
        # Subset entire df except year and show row, shift upward one row, set new bottom row to 0.
        exposure_df.loc[:, exposure_df.columns.difference(["year", "show_row"])] = exposure_df.loc[:, exposure_df.columns.difference(["year", "show_row"])].shift(-1)
        exposure_df = exposure_df.fillna(0)

        utils.write_pd_to_hxd(exposure_df, cds.experience_rating.exposure.exposure_listing, ["gnepi_projected", "gnepi_actual", "exposure_value_1", "exposure_value_2", "exposure_value_3", "rate_change", "inflation_option_1", "inflation_option_2", "other_changes"])

        # /quote
        cds.quote.rol_ly.ulr = expiring_data["cds"]["quote"]["rol_ty"]["ulr"]
        cds.quote.rol_ly.tpi = expiring_data["cds"]["quote"]["rol_ty"]["tpi"]
        cds.quote.rol_ly.roc = expiring_data["cds"]["quote"]["rol_ty"]["roc"]

        # /summary

        ## multi year summary
        cds.summary.multi_year_summary_ly.line_written_summary_fx = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["line_written_summary_fx"]
        cds.summary.multi_year_summary_ly.line_estimated_summary_fx = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["line_estimated_summary_fx"]
        cds.summary.multi_year_summary_ly.line_signed_summary_fx = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["line_signed_summary_fx"]

        cds.summary.multi_year_summary_ly.epi_written_summary_fx = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["epi_written_summary_fx"]
        cds.summary.multi_year_summary_ly.epi_estimated_summary_fx = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["epi_estimated_summary_fx"]
        cds.summary.multi_year_summary_ly.epi_signed_summary_fx = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["epi_signed_summary_fx"]

        cds.summary.multi_year_summary_ly.mi_250 = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["mi_250"]
        cds.summary.multi_year_summary_ly.mi_250_prem_ratio = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["mi_250_prem_ratio"]
        cds.summary.multi_year_summary_ly.mi_250_estimate_prem_ratio = expiring_data["cds"]["summary"]["multi_year_summary_ty"]["mi_250_estimate_prem_ratio"]

        ## ly
        for child in  [
            "risk_adjusted_rate_change",
            "bpi",
            "fot_adequacy",
            "rms_adequacy",
            "ulr",
            "epi_adj_rate",
            "prem_full_line",
            "mi_250_prem_ratio",
            "mi_10_prem_ratio"            
        ]:
            setattr(cds.summary.ly, f"{child}" , expiring_data["cds"]["summary"]["ty"][f"{child}"]) 

        ## year before last
        for child in  [
            "risk_adjusted_rate_change",
            "bpi",
            "fot_adequacy",
            "rms_adequacy",
            "ulr",
            "epi_adj_rate",
            "prem_full_line",
            "mi_250_prem_ratio",
            "mi_10_prem_ratio"            
        ]:
            setattr(cds.summary.year_before_last, f"{child}" , expiring_data["cds"]["summary"]["ly"][f"{child}"]) 

        
        ## roll forward section_reference
        if cds.multi_year == "No":
            pol_ref = [layer.section_reference for layer in cds.layers]
            year = [int(x[6:8]) if x and len(x) >= 8 and x[6:8].isdigit() else "" for x in pol_ref]
            pol_ref_next_year = [x[:6] + str(year[i] + 1) + x[8:] if (x != None and year[i] != "") else "" for i, x in enumerate(pol_ref)]

            for index, layer in enumerate(cds.layers):
                layer.section_reference = pol_ref_next_year[index]


        # /layers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for index, layer in enumerate(cds.layers):

            to_write = [
                "section_reference",
                "loss_affected",
                "currency",
                "leader",
                "layer_description",
                "limit",
                "excess",
                "limit_cnv",
                "excess_cnv",
                "inner_type",
                "aggregate_deductible",
                "aggregate_deductible_cnv",
                "number_reins",
                "perc_reins_1",
                "perc_reins_2",
                "perc_reins_3",
                "layer_structure"
            ]
            for child in to_write:
                setattr(layer, child + "_ly", expiring_data["cds"]["layers"][index][f"{child}"])

            for model_type in ["total_rms_nmp", "total_ivor_nmp", "total_air_nmp", "rms", "ivor", "air", "nmp"]:
                for child in ["gross_el", "gross_sd"]: 
                    rsetattr(layer, f"model_prev.{model_type}.{child}", expiring_data["cds"]["layers"][index]["model"][f"{model_type}"][f"{child}"]) 

            for child in ["ws_el", "eq_el", "scs_el", "perc_us_el", "eu_ws_el", "jp_eq_el", "jp_ws_el", "can_eq_el", "caribbean_ws_el", "perc_us_el"]:
                rsetattr(layer, f"model_prev.rms.{child}", expiring_data["cds"]["layers"][index]["model"]["rms"][f"{child}"]) 

            for child in ["gross_el_incl_rol", "gross_sd_incl_rol", "additional_rol", "description"]:
                rsetattr(layer, f"model_prev.nmp.{child}", expiring_data["cds"]["layers"][index]["model"]["nmp"][f"{child}"])

            for child in ["north_east", "mid_atlantic", "carolinas", "fl_se", "fl_non_se", "al_miss", "louisiana", "tx_east", "tx_west", "cal_south", "cal_north", "pnw", "new_madrid", "hawaii", "mid_west_1", "mid_west_2", "second_event", "ca_wildfire"]:
                rsetattr(layer, f"rms_regional_prev.{child}", expiring_data["cds"]["layers"][index]["rms_regional"][f"{child}"])

            for child in ["treaty_us", "treaty_group", "treaty_us_quake", "treaty_intl"]:
                for rp in ["mi_250", "mi_10"]:
                    rsetattr(layer, f"marginal_impacts_prev.{child}.{rp}", expiring_data["cds"]["layers"][index]["marginal_impacts"][f"{child}"][f"{rp}"])

            ## /rate_change
            layer.rate_change.expiring_layer_to_use_ly = expiring_data["cds"]["layers"][index]["rate_change"]["expiring_layer_to_use"]

            layer.rate_change.expiring_layer_to_use = index + 1

            ## /quote
            for child in [
                "rol_rms",
                "rol_ivor", 
                "rol_air", 
                "rol_burn",
                "rol_burn_override",
                "weighting_rms", 
                "weighting_ivor", 
                "weighting_air",
                "weighting_burn",
                "lol_rms", 
                "lol_ivor", 
                "lol_air",
                "lol_burn",
                "lol_weighted", 
                "gross_lol_weighted", 
                "rol_afb_tech",
                "tpi",
                "roc", 
                "ulr",
                "bpi",
                "rol_quote",
                "rol_fot",
                "quote_fot_ratio", 
                "prem_full_line", 
                "quote_adequacy",
                "fot_adequacy",
                "rms_adequacy", 
                "written_line", 
                "estimated_signing",
                "signed_line",
                "epi_written",
                "epi_estimated", 
                "epi_signed", 
                "rp_quote_break_even",
                "rp_fot_break_even",
                "rp_attach", 
                "rp_exit", 
                "rp_pml_selection",
                "rp_attach_peak",
                "rp_exit_peak", 
                "rp_pml_selection_peak"
            ]:
                rsetattr(layer,f"quote.rol_ly.{child}", expiring_data["cds"]["layers"][index]["quote"]["rol_ty"][f"{child}"])

            ## /summary

            ### ly
            layer.summary.ly.next_year_section_reference = expiring_data["cds"]["layers"][index]["summary"]["year_after_next"]["section_reference"]
            layer.summary.ly.next_year_share = expiring_data["cds"]["layers"][index]["summary"]["year_after_next"]["share"]

            layer.summary.ly.current_year_section_reference = expiring_data["cds"]["layers"][index]["summary"]["next_year"]["section_reference"]
            layer.summary.ly.current_year_share = expiring_data["cds"]["layers"][index]["summary"]["next_year"]["share"]

            layer.summary.ly.risk_adjusted_rate_change = expiring_data["cds"]["layers"][index]["rate_change"]["risk_adjusted_rate_change"]

            for child in [
                "multi_year_period",
                "reinstatement_description",
                "bpi",
                "fot_adequacy",
                "rms_adequacy",
                "ulr", 
                "epi_adj_rate",
                "prem_full_line",
                "mi_250",
                "mi_250_prem_ratio",
                "mi_10",
                "mi_10_prem_ratio"
            ]:
                rsetattr(layer, f"summary.ly.{child}", expiring_data["cds"]["layers"][index]["summary"]["ty"][f"{child}"])

            ### year_before_last
            layer.summary.year_before_last.section_reference = expiring_data["cds"]["layers"][index]["section_reference_ly"]
            layer.summary.year_before_last.leader = expiring_data["cds"]["layers"][index]["leader_ly"]
            layer.summary.year_before_last.layer_description = expiring_data["cds"]["layers"][index]["layer_description_ly"]
            layer.summary.year_before_last.limit_cnv = expiring_data["cds"]["layers"][index]["limit_cnv_ly"]
            layer.summary.year_before_last.excess_cnv = expiring_data["cds"]["layers"][index]["excess_cnv_ly"]
            layer.summary.year_before_last.layer_structure_year_before_last = expiring_data["cds"]["layers"][index]["layer_structure_ly"]

            layer.summary.year_before_last.current_year_section_reference = expiring_data["cds"]["layers"][index]["summary"]["ly"]["next_year_section_reference"]
            layer.summary.year_before_last.current_year_share = expiring_data["cds"]["layers"][index]["summary"]["ly"]["next_year_share"]

            # (pulled from quote)
            layer.summary.year_before_last.epi_written = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["epi_written"]
            layer.summary.year_before_last.epi_estimated = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["epi_estimated"]
            layer.summary.year_before_last.epi_signed = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["epi_signed"]

            layer.summary.year_before_last.rol_quote = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["rol_quote"]
            layer.summary.year_before_last.rol_fot = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["rol_fot"]
            layer.summary.year_before_last.rol_afb_tech = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["rol_afb_tech"]
            layer.summary.year_before_last.roc = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["roc"]

            layer.summary.year_before_last.written_line = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["written_line"]
            layer.summary.year_before_last.estimated_signing = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["estimated_signing"]
            layer.summary.year_before_last.signed_line = expiring_data["cds"]["layers"][index]["quote"]["rol_ly"]["signed_line"]

            # (pulled from summary)
            for child in [
                "risk_adjusted_rate_change",
                "reinstatement_description",
                "bpi",
                "fot_adequacy",
                "rms_adequacy",
                "ulr",
                "epi_adj_rate",
                "prem_full_line",
                "mi_250",
                "mi_250_prem_ratio",
                "mi_10",
                "mi_10_prem_ratio"
            ]:
                rsetattr(layer, f"summary.year_before_last.{child}", expiring_data["cds"]["layers"][index]["summary"]["ly"][f"{child}"])

        # day 2 nodes (need to check if exist in schema before pulling in) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        ## risk information
        for field in [
            "is_facility",
            "effective_brokerage"
            ]:
            try:
                value = expiring_data["cds"][field]
                setattr(cds, f"{field}_ly", value)
            except (KeyError, AttributeError, TypeError):
                continue

        ## pml_curves 
        for curve_type in ["curve_aggregator", "burn_curve"]:    
            for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
                try:
                    rsetattr(cds.pml_curves, f"{curve_type}.rp_loss_prev.{rp}", expiring_data["cds"]["pml_curves"][f"{curve_type}"]["rp_loss"][f"{rp}"])
                except (KeyError, AttributeError, TypeError):
                    continue 

        for curve_type in ["rms_curves", "air_curves", "other_curves", "nmp_curves"]:
            for index, curve in enumerate(getattr(cds.pml_curves, curve_type)):     
                for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
                    rsetattr(curve,f"rp_loss_prev.{rp}", expiring_data["cds"]["pml_curves"][f"{curve_type}"][index]["rp_loss"][f"{rp}"])
        
        ## quote totals
        for field in [
            "bpi",
            "quote_adequacy",
            "fot_adequacy"
            ]:
            try:
                value = expiring_data["cds"]["quote"]["rol_ty"][field]
                setattr(cds.quote.rol_ly, field, value)
            except (KeyError, AttributeError, TypeError):
                continue   

        for index, layer in enumerate(cds.layers):
            try:
                renewal_layer = expiring_data["cds"]["layers"][index]["renewal_layer"]
                setattr(layer, "renewal_layer_ly", renewal_layer)
            except (KeyError, IndexError, TypeError):
                continue

        ## year before last summary totals
        for child in  [
            "rol_quote",
            "rol_fot",
            "roc"          
        ]:
            try:
                setattr(cds.summary.year_before_last, f"{child}" , expiring_data["cds"]["quote"]["rol_ly"][f"{child}"]) 
            except (KeyError, AttributeError, TypeError):
                    continue 

        ## expiring year summary totals
        for child in  [
            "rol_quote",
            "rol_fot",
            "roc",
            "risk_adjusted_rate_change",
            "bpi",
            "fot_adequacy",
            "rms_adequacy",
            "ulr",
            "epi_adj_rate",
            "prem_full_line",
            "mi_250_prem_ratio",
            "mi_10_prem_ratio"            
        ]:
            try:
                setattr(cds.summary.expiring_year, f"{child}" , expiring_data["cds"]["summary"]["year_before_last"][f"{child}"]) 
            except (KeyError, AttributeError, TypeError):
                    continue 

        ## expiring year summary layer
        for index, layer in enumerate(cds.layers):
            try:
                value = expiring_data["cds"]["layers"][index]["summary"]["year_before_last"]["layer_structure_year_before_last"]
                setattr(layer.summary.expiring_year, "layer_structure_expiring_year", value)
            except (KeyError, IndexError, TypeError):
                continue

        for index, layer in enumerate(cds.layers):
            for field in [
                "epi_written",
                "epi_estimated",
                "epi_signed",
                "section_reference",
                "leader",
                "layer_description",
                "limit_cnv",
                "excess_cnv",
                "rol_quote",
                "rol_fot",
                "rol_afb_tech",
                "reinstatement_description",
                "roc",
                "risk_adjusted_rate_change",
                "bpi",
                "fot_adequacy",
                "rms_adequacy",
                "ulr",
                "epi_adj_rate",
                "prem_full_line",
                "written_line",
                "estimated_signing",
                "signed_line",
                "mi_250",
                "mi_250_prem_ratio",
                "mi_10",
                "mi_10_prem_ratio"
                ]:
                try:
                    value = expiring_data["cds"]["layers"][index]["summary"]["year_before_last"][field]
                    setattr(layer.summary.expiring_year, field, value)
                except (KeyError, IndexError, TypeError):
                    continue

        ## RISK XL
        for index, layer in enumerate(cds.layers):
            for field in [
                "risk_xl_rol_exposure",
                "risk_xl_weighting_exposure",
                "risk_xl_lol_exposure",
                "layer_exposure",
                "roev"
                ]:
                try:
                    value = expiring_data["cds"]["layers"][index]["quote"]["rol_ty"][field]
                    setattr(layer.quote.rol_ly, field, value)
                except (KeyError, IndexError, TypeError):
                    continue

            for field in [
                "risk_xl_occurrence_limit",
                "risk_xl_occurrence_limit_cnv"
                "risk_xl_intl_pml_code",
                "risk_xl_us_pml_code"
                ]:
                try:
                    value = expiring_data["cds"]["layers"][index][field]
                    setattr(layer, field + "_ly", value)
                except (KeyError, IndexError, TypeError):
                    continue




        for index in range(1, 13):
            try:
                value = expiring_data["cds"]["risk_xl_exposure_rating"][f"exposure_segment_{index}"]["exposed_limit_ty"]
                rsetattr(cds, f"risk_xl_exposure_rating.exposure_segment_{index}.exposed_limit_ly", value)
            except (KeyError, IndexError, TypeError):
                continue

        try:
            value = expiring_data["cds"]["risk_xl_exposure_rating"][f"exposure_segment_total"]["exposed_limit_ty"]
            setattr(cds.risk_xl_exposure_rating.exposure_segment_total, "exposed_limit_ly", value)
        except (KeyError, IndexError, TypeError):
            pass



# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):    
    from openpyxl.utils.cell import coordinate_to_tuple
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/example_document_template.xlsx"

    # Load the workbook 
    workbook = openpyxl.load_workbook(template_path)

    # Fill the named ranges with data
    for key, value in data.items():
        if key in workbook.defined_names:
            # Get the cell corresponding to the named range
            cells = workbook.defined_names[key].destinations
            for sheet_name, coord in cells:
                # Get the relevant worksheet
                sheet = workbook[sheet_name]
                # If value is a list, write values dynamically
                if isinstance(value, list):
                    coord = coord.replace("$", "")
                    row, col = coordinate_to_tuple(coord)
                    for df_row_index, df_row in enumerate(value, start=row):
                        for df_col_index, (cell_key, cell_value) in enumerate(df_row.items(), start=col):
                            # Write each value into the corresponding cell
                            sheet.cell(row=df_row_index, column=df_col_index, value=cell_value)
                else:
                    # Assign single value to the cell
                    sheet[coord] = value


    # Protect the sheet to prevent changes
    # sheet.protection.enable()
    # sheet.protection.set_password(excel_password)

    # rationale_sheet = workbook['Rationale']
    # rationale_sheet.sheet_state = 'hidden'

    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)

    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict
