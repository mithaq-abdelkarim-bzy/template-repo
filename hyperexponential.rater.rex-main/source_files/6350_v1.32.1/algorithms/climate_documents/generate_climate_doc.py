import hx
import datetime
import os
from mailmerge import MailMerge
import pandas as pd
import polars as pl
from operator import itemgetter, attrgetter
   
# Generate climate change spotlight one-pager from climate tab
def generate_climate_doc(hxd, progress):

    #### Only execute if Flood Climate Scoring has been run 
    if hxd.non_layer_summary.climate_metrics.flood.flood_climate_risk_score and hxd.policy_information.small_schedule_model:
    
        ############################################################################################################
        #### Set up hurricane scoring parameters
        cgear_score_df = hx.params.cgear_score
        cgear_score_df = cgear_score_df.rename(columns={"Zip": "zip", "C-GEAR Score": "cgear_score"})

        columns = [
            "loc_id" ,"zip", "street_name", "tiv_total_usd"
            ]
    
        portfolio = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.schedule.schedule_table])

        portfolio["country"] = [x if x != "Georgia" else "Georgia (Country)" for x in [row.address_dropdown.country for row in hxd.schedule.schedule_table]]
        portfolio["state"] = [row.address_dropdown.state for row in hxd.schedule.schedule_table]
        portfolio["county"] = [row.address_dropdown.county for row in hxd.schedule.schedule_table]
        portfolio["city"] = [row.address_dropdown.city for row in hxd.schedule.schedule_table]

        us_state_code = pd.DataFrame(hx.params.us_state_code)[["US States", "US State Code"]].rename({
            "US States": 'state_name', 
            "US State Code": "state"
        }, axis=1)
        portfolio = portfolio.merge(us_state_code, how="left", on="state")

        # attach c-gear score
        portfolio = portfolio.merge(cgear_score_df, how = "left", on="zip")
        portfolio['state_or_country'] = portfolio.apply(lambda row: row['state_name'] if row['country'] == "United States" else row['country'], axis=1)
        
        cgear_tiv_summary = portfolio[["street_name", "city", "county", "state_name", "tiv_total_usd", "cgear_score"]]
        cgear_tiv_summary = cgear_tiv_summary.sort_values(by = ['cgear_score', 'tiv_total_usd'], ascending = False)
        cgear_tiv_summary = cgear_tiv_summary.head(10)
    
        cgear_summary = pd.DataFrame(columns=["street_name", "city", "county", "country", "state_name", "tiv_total_usd", "cgear_score"], index=range(10))
        cgear_tiv_summary = cgear_tiv_summary.append(cgear_summary, ignore_index=True)
        cgear_tiv_summary = cgear_tiv_summary.fillna("")

        score_locations = hxd.non_layer_summary.climate_metrics.score_locations

        scores = []
        aals = []
        tiv_tot_cgear = []
        
        # Collect scores, AALs and tivs 
        for i in range(6):
            score_i = getattr(score_locations, f"score_{i}", None)
            scores.append(score_i.score if score_i.score else 0)
            aals.append(score_i.aal_weighted_cgear if score_i.aal_weighted_cgear else 0)
            tiv_tot_cgear.append(score_i.total_tiv if score_i.total_tiv else 0)
        
        # AAL weighted hurricane score 
        aal_sum = sum(aals)
        aal_cgear_sum = sum(a * s for a, s in zip(aals, scores))
        hurr_sc = (aal_cgear_sum / aal_sum) if aal_sum > 0 else 0

        # TIV proportional hurricane score
        tiv_cgear_sum = sum(tiv_tot_cgear)
        tiv_prop_cgear = [(tiv / tiv_cgear_sum) if tiv > 0 else 0 for tiv in tiv_tot_cgear]
        hurr_sc_tiv = sum(p * s for p, s in zip(tiv_prop_cgear, scores))

        # Unpack variables
        (score_0, score_1, score_2, score_3, score_4, score_5) = scores
        (aal_0, aal_1, aal_2, aal_3, aal_4, aal_5) = aals
        (tiv_tot_cgear_0, tiv_tot_cgear_1, tiv_tot_cgear_2, tiv_tot_cgear_3, tiv_tot_cgear_4, tiv_tot_cgear_5) = tiv_tot_cgear
        (tiv_prop_cgear_0, tiv_prop_cgear_1, tiv_prop_cgear_2, tiv_prop_cgear_3, tiv_prop_cgear_4, tiv_prop_cgear_5) = tiv_prop_cgear

        ############################################################################################################
    
        #### Set up flood scoring parameters

        # Policy flood climate score 
        fl_sc = hxd.non_layer_summary.climate_metrics.flood.flood_climate_risk_score

        # Bring in table for location calcs
        columns = [
            "loc_id", "street_name", "state", "tiv_total_usd", "el_post_uw_usd_100_fl_total", "bzly_loc_score"
            ]

        flood_df = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.non_layer_summary.climate_metrics.flood.flood_climate_table])

        flood_df = flood_df.merge(us_state_code, on = "state", how = "left")

        # Calculate TIV proportions by climate score
        flood_prop = (
            flood_df.groupby("bzly_loc_score").agg({"tiv_total_usd": "sum"})
        )
        fl_tiv_total = flood_prop["tiv_total_usd"].sum()

        temp_fl_prop = pd.DataFrame({"bzly_loc_score": range(6)})
        flood_prop = temp_fl_prop.merge(flood_prop, on = "bzly_loc_score", how = "left")

        flood_prop["tiv_total_usd"] = flood_prop["tiv_total_usd"].fillna(0)
        flood_prop["fl_tiv_prop"] = flood_prop["tiv_total_usd"] / fl_tiv_total

        flood_prop = flood_prop.sort_values(by = "bzly_loc_score")
        flood_prop_list = flood_prop["fl_tiv_prop"].tolist()

        # calculate top 10 locations by flood ELs
        flood_top_10 = flood_df.sort_values(by = "el_post_uw_usd_100_fl_total", ascending=False).head(10)
        flood_top_10 = flood_top_10.sort_values(by = ["bzly_loc_score", "tiv_total_usd"], ascending=[False, False])
        
        # set up list for top 10 info
        fl_str_ad_list = flood_top_10["street_name"].tolist()
        fl_state_list = flood_top_10["state_name"].tolist()
        fl_tiv_list = flood_top_10["tiv_total_usd"].tolist()
        fl_score_list = flood_top_10["bzly_loc_score"].tolist()

        for i in range(len(fl_score_list)):
            fl_score_list[i] = str(fl_score_list[i])
        fl_score_str = "-".join(fl_score_list)

        fl_str_ad_list += [""] * (10 - len(fl_str_ad_list))
        fl_state_list += [""] * (10 - len(fl_state_list))
        fl_tiv_list += [""] * (10 - len(fl_tiv_list))
        fl_score_list += [""] * (10 - len(fl_score_list))

        ############################################################################################################
        #### Merge variables to the document
        template = os.path.join(os.path.dirname(__file__), "climate_change_spotlight.docx")
        document = MailMerge(template)

        # Insured details fields
        merge_fields = {
            "insured_name": hxd.quote_documents.bpro_outputs.insured_name,
            "start_date": hxd.quote_documents.bpro_outputs.insured_from.strftime("%d-%b-%Y"),
            "end_date": hxd.quote_documents.bpro_outputs.insured_until.strftime("%d-%b-%Y"),
            "total_tiv": f"${tiv_cgear_sum:,.0f}",
            "hs": f"{hurr_sc:.0f}",
            "fl_sc": f"{fl_sc:.0f}", 
        }

        # Hurricane score fields
        hs_fields = {
            f"p{i}": f"{tiv_prop * 100:,.0f}%" if tiv_prop else "0%" for i, tiv_prop in enumerate(tiv_prop_cgear)
        }
        merge_fields.update(hs_fields)

        # Hurricane top 10 locations
        for i in range(10):
            row = cgear_tiv_summary.iloc[i] if i < len(cgear_tiv_summary) else pd.Series

            merge_fields.update({
                f"str_ad_{i}": f"{row.get('street_name', '')}," if row.get("street_name") else "",
                f"state_{i}": f"{row.get('state_name', '')}" if row.get("state_name") else "",
                f"tiv_{i}": f"${row.get('tiv_total_usd', 0):,.0f}" if row.get("tiv_total_usd") else "",
                f"cgear_sc_{i}": f"{int(row.get('cgear_score', ''))}" if row.get("cgear_score") else ""
            })
        
        # Flood score fields
        fl_fields = {
            f"fl_p{i}": f"{val * 100:.0f}%" for i, val in enumerate(flood_prop_list)
        }
        merge_fields.update(fl_fields)

        # Flood top 10 locations
        for i in range(10):
            merge_fields.update({
                f"fl_str_ad_{i}": f"{fl_str_ad_list[i]}," if fl_str_ad_list[i] else "",
                f"fl_state_{i}": f"{fl_state_list[i]}" if fl_state_list[i] else "",
                f"fl_tiv_{i}": f"${fl_tiv_list[i]:,.0f}" if fl_tiv_list[i] else "",
                f"fl_score_{i}": f"{fl_score_list[i]}"
            })
            
        #### Perform the merge 
        document.merge(**merge_fields)

        with hxd.non_layer_summary.climate_metrics.document.open("b") as f:
            document.write(f)
