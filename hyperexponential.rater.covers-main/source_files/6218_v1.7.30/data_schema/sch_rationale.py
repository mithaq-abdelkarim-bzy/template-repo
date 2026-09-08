
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_rationale(cds):
        
    # Extending cds nodes for RMS
    cds.extend_node_rater_defined("cds", {
        "rationale": hx.Structure(children={
            "coverholder_background_info" : hx.Str(mode="input", default="Should include info on Coverholder, how long they have been in business, \nwhat classes do they write and where their main offices are located", view={"read_only": True}),
            "coverholder_background" : hx.Str(mode="input", default=None, optionality="optional", async_input=["generate_uw_rationale_doc_task"], view={"info": "Should include info on Coverholder, how long they have been in business, what classes do they write and where their main offices are located"}),
            # Fields for Binder Overview
            "contract_summary" : hx.Str(mode="override", async_input=["generate_uw_rationale_doc_task"]),
            "risk_type" : hx.Str(mode="override", async_input=["generate_uw_rationale_doc_task"], view={"label": "Risk Type"}),
            "construction" : hx.Str(mode="override", async_input=["generate_uw_rationale_doc_task"], async_output=["run_bordereau_rater_task" , "simulate_pc_task"], view={"label": "Construction"}),
            "risk_limit" : hx.Float(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional", view={"label": "Risk Limit (100%)", "format": thousands_format(0)}),
            "avg_limit" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], async_output=["run_bordereau_rater_task" , "simulate_pc_task"], view={"label": "Average Limit (100%)", "format": thousands_format(0)}),
            "top_counties" : hx.Str(mode="override", async_input=["generate_uw_rationale_doc_task"], async_output=["run_bordereau_rater_task" , "simulate_pc_task"], view={"label": "Top Counties"}),
            "avg_rate" : hx.Float(mode="override", async_input=["generate_uw_rationale_doc_task"], async_output=["run_bordereau_rater_task" , "simulate_pc_task"], view={"label": "Average Rate", "format": thousands_format(2)}),
            "curr_epi" : hx.Float(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional", view={"label": "Current Year EPI (GG 100%)", "format": thousands_format(0)}),
            "prev_epi" : hx.Float(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional", view={"label": "Previous Year EPI (GG 100%)", "format": thousands_format(0)}),
            "curr_rc" : hx.Float(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional", view={"label": "Current Year Rate Change", "format": percent_format(2)}),
            "prev_rc" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Previous Year Rate Change", "format": percent_format(2)}),
            
            "gg_att_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Attr GG LR pre UW adj", "format": percent_format(1)}),
            "att_uw_adj" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Attr UW adj", "format": percent_format(1)}),
            "gg_att_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Attr GG LR post UW adj", "format": percent_format(1)}),
            "gg_large_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Large GG LR pre UW adj", "format": percent_format(1)}),
            "large_uw_adj" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Large UW adj", "format": percent_format(1)}),
            "gg_large_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Large GG LR pst UW adj", "format": percent_format(1)}),
            "gg_cat_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Cat GG LR pre UW adj", "format": percent_format(1)}),
            "cat_uw_adj" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Cat UW adj", "format": percent_format(1)}),
            "gg_cat_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Cat GG LR pst UW adj", "format": percent_format(1)}),
            "gg_total_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Total GG LR pre UW adj", "format": percent_format(1)}),
            "gg_total_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Total GG LR pst UW adj", "format": percent_format(1)}),
           


            "gn_att_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Attr GN LR pre UW adj", "format": percent_format(1)}),
            "gn_att_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Attr GN LR post UW adj", "format": percent_format(1)}),
            "gn_large_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Large GN LR pre UW adj", "format": percent_format(1)}),
            "gn_large_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Large GN LR pst UW adj", "format": percent_format(1)}),
            "gn_cat_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Cat GN LR pre UW adj", "format": percent_format(1)}),
            "gn_cat_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Cat GN LR pst UW adj", "format": percent_format(1)}),
            "gn_total_lr_pre" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Total GN LR pre UW adj", "format": percent_format(1)}),
            "gn_total_lr_pst" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Total GN LR pst UW adj", "format": percent_format(1)}),
           

            # need to decide if we remove this as the view of expenses to just add 20% feels broad brush compared to other metrics
            "comb_ratio_pre_adj_exc_pc" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Combined Ratio pre UW adj (exc pc)", "format": percent_format(1)}),
            "comb_ratio_pre_adj_inc_pc" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Combined Ratio pre UW adj (inc pc)", "format": percent_format(1)}),
            "comb_ratio_pst_adj_exc_pc" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Combined Ratio pst UW adj (exc pc)", "format": percent_format(1)}),
            "comb_ratio_pst_adj_inc_pc" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Combined Ratio pst UW adj (inc pc)", "format": percent_format(1)}),
            "prm_aal_ratio" : hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Prem:AAL multiple", "format": thousands_format(1)}),

            # More commentary boxes
            "uw_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "rc_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "tc_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "agglim_util_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "risk_profile_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "territory_profile_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "exposure_change_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "large_losses_commentary" : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),

            # Commentary box titles
            "uw_commentary_info" : hx.Str(mode="input", default="Should include discussion on past performance; slip changes, audit,\nrisk bdx queries, claims handling, deductions, PC etc...", view={"read_only": True}),
            "risk_profile_commentary_info" : hx.Str(mode="input", default="Do risks bound match anticipated risk profile?\nComment on changes and expected effect on loss development.\nE.g. more exposure in higher bands could lead to larger losses", view={"read_only": True}),
            "territory_profile_commentary_info" : hx.Str(mode="input", default="Discuss where business is bound, not only by State but discuss impact of coastal business.\nReview last year's Agg caps and utilisation and changes made for new term.", view={"read_only": True}),
            "exposure_change_commentary_info" : hx.Str(mode="input", default="Will any expected change in underlying exposure such as more frame\nor distance to the coast affect the AAL or N/A?", view={"read_only": True}),
            "large_losses_commentary_info" : hx.Str(mode="input", default="Discuss any individual large losses. Is there a trend for Frequency / Severity?", view={"read_only": True}),

            #supporting files (2 per comment box)
            "uw_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "uw_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "rc_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "rc_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "tc_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "tc_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "agglim_util_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "agglim_util_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "risk_profile_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "risk_profile_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "territory_profile_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "territory_profile_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "exposure_change_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "exposure_change_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "large_losses_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "large_losses_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),

            #actuarial commentary
            "actuarial_review"              : hx.Str(mode="input", default="No",       view={"label": "Actuarial Reviewed?"},       options_table="lst_yn", options_column="YesNo"),
            "actuarial_notes"               : hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default=None, optionality="optional"),
            "actuarial_view"                : hx.Bool(mode="input", default=False,                       view={"label": "Keep Actuarial view active:"}),
            "actuarial_commentary_file1" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),
            "actuarial_commentary_file2" : hx.File(mode="input", async_input=["generate_uw_rationale_doc_task"]),

             #output file from document generation
            "document": hx.File(mode="output", file_name="uw_rationale_doc.docx", async_output=["generate_uw_rationale_doc_task"], view={"label": "Document"}),

        }),
    })
