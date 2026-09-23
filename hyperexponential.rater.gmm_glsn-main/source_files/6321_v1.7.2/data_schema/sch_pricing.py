import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from libraries.common_data_schema.algorithms import parameter_tables_schema as params
from algorithms.rate_constants import max_layers, max_options
from hx import params as hx_params
import data_schema.sch_utilities as utils


def sch_pricing(cds):
    
    #----------------------------------------------------------------------------------------------#
    # Options to add excess layers as well as show/hide functionality stored in cds root
    #----------------------------------------------------------------------------------------------#
    cds.extend_node_rater_defined("cds", {
        **{f"add_excess_{index}": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Add Excess Layer"}, async_input=["generate_excess_proposal_template_task"]) for index in range(1,max_layers+1)},
        #Boolean for the Umbrella option show/hide
        **{f"show_option_{index}": hx.Bool(mode="output") for index in range(1,max_options+1)},
        "copy_option_from": hx.Str(mode="input", async_input=["pricing_copy_option"], optionality="required",default="Option 1", options=["Option 1", "Option 2", "Option 3", "Option 4","Option 5","Option 6"], view={"label": "Option to copy from"}),
        "copy_option_to": hx.Str(mode="input", async_input=["pricing_copy_option"], optionality="required",default="Option 2", options=["Option 1", "Option 2", "Option 3", "Option 4","Option 5","Option 6"], view={"label": "Option to paste to"}),
        "default_retention": hx.Float(mode="input", async_input= ["set_defaults_button"], default=10000, optionality="optional", view={"label": "Set Default: Retention","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}),
        "default_per_claim_limit": hx.Float(mode="input", async_input= ["set_defaults_button"], default=1000000, optionality="optional", view={"label": "Set Default: Per Claim Limit","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}),
        "default_aggregate_limit": hx.Float(mode="input", async_input= ["set_defaults_button"], default=3000000, optionality="optional", view={"label": "Set Default: Aggregate Limit","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000})
        })
    
    #----------------------------------------------------------------------------------------------#
    # This is the options structure. Coverage, primary details and all 10 excess layers are defined in here, outside the layers CDS. The selected option will be mapped to the layers node for reporting.
    #----------------------------------------------------------------------------------------------#
    cds.extend_node_rater_defined("cds", {
        "options": hx.List(mode="input", default_element_count= max_options, fixed_element_count= max_options, view= {"label":"Options"}, children={   
            "coverages": hx.Structure(view={"label": "Coverages"}, children={
                **{
                    item: hx.Structure(view={"label": label}, children={
                    "retention": hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False},{"task": "set_defaults_button", "reset": False}], default=None, optionality="optional", view={"label": "Retention","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}),
                    "per_claim_limit":hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False},{"task": "set_defaults_button", "reset": False}], default=None, optionality="optional", view={"label": "Per Claim Limit","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}),
                    "aggregate_limit":hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False},{"task": "set_defaults_button", "reset": False}], default=None, optionality="optional", view={"label": "Aggregate Limit","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}),
                    })
                    for item, label in zip(["professional_liability","product_liability","general_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","healthcare_professional_liability","tech_eo_products_media","product_recall","well_tech_eo_media"],
                    ["Professional Liability","Product Liability","General Liability","E&O","Sexual Abuse","Employee Benefits Liability","Employers Liability","Healthcare Professional Liability","Tech E&O/Products/Media","Product Recall Expenses","Well Tech E&O and Media"])
                },
             }),

            "tech_eo_primary_net_premium_usd": hx.Float(mode = "output", view = {"label": "Tech E&O Net Premium USD - Primary"}),
            "tech_eo_agg_ilf_primary_factor": hx.Float(mode = "output", view = {"label": "Agg Lim from Tech EO sheet"}),
            "tech_eo_retention_ratio_factor": hx.Float(mode = "output"),
            "tech_eo_eec_ilf": hx.Float(mode = "output"),
            #"tech_eo_agg_ilf": hx.Float(mode = "output"),
            "option_label": hx.Str(mode="output", view={"label": "Option"}),
            "agg_retention":hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=None, optionality="optional", view={"label": "Policy Aggregate Retention","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}),
            "agg_limit":hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option", "generate_primary_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=0, optionality="required", view={"label": "Policy Aggregate Limit","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}),
            "indemnity_only":hx.Bool(mode="input", async_input= ["rarc_task","pricing_copy_option"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=False, optionality="required", view={"label":"Indemnity Only Deductible"}),   
         
            "include_stop_gap_primary":hx.Bool(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=False, optionality="required", view={"label":"Stop Gap: Primary"}),
            "include_tria_primary":hx.Bool(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=False, optionality="required", view={"label":"TRIA: Primary"}),
            "include_punitive_damages_primary":hx.Bool(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=False, optionality="required", view={"label":"Punitive Damages: Primary"}),
            "include_costs_in_addition_primary":hx.Bool(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=False, optionality="required", view={"label":"Costs In Addition: Primary"}),
            "costs_in_addition_selection":hx.Str(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], optionality="required",default="None", options=["Each and Every", "Capped by Agg", "Unlimited", "None"], view={"label": "Selection"}),
            "include_auto_primary":hx.Bool(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=False, optionality="required", view={"label":"Auto HNOA: Primary"}),
            "auto_measure":hx.Str(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], optionality="optional",default=None, options=["Mileage", "No. of Drivers"], view={"label": "Measure"}),
            "auto_amount":hx.Float(mode="input", async_input=["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=None, optionality="optional", view={"label": "Amount","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000}),

            "brokerage_primary": hx.Float(mode="input", default=None, optionality="optional", async_input= ["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], view={"label": "Brokerage","format":utils.percent_format(2)}, validation={"min_value": 0, "max_value": 1}),
            "cyber_premium_primary":hx.Float(mode="output", view={"label": "Cyber Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]),
            "model_premium_primary":hx.Float(mode="output", view={"label": "Model Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]),
            "minimum_premium_primary":hx.Float(mode="output", view={"label": "Minimum Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]),
            "gross_premium_primary":hx.Float(mode="output", view={"label": "Gross Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]),
            "uplift_for_nmp_primary":hx.Float(mode="output", view={"label": "Uplift for Non-Modelled Perils","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]),
            "quoted_premium_primary":hx.Float(mode="input", async_input= ["pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=None, optionality="optional", view={"label": "Quoted Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000}),
            "bpi_primary": hx.Float(mode="output",  view={"label": "BPI%","format":utils.percent_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]),

            #Below loops set the limits, model premiums etc for each excess layer (1-10)
            **{f"per_claim_limit_{label}": hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=None, optionality="optional", view={"label": "Per Claim Limit","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
            **{f"aggregate_limit_{label}": hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=None, optionality="optional", view={"label": "Aggregate Limit","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
            **{f"brokerage_{label}": hx.Float(mode="input", async_input= ["rarc_task","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=None, optionality="optional", view={"label": "Brokerage","format":utils.percent_format(2)}, validation={"min_value": 0, "max_value": 1}) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},    
            **{f"supported_excess_premium_{label}":hx.Float(mode="output", view={"label": "Supported Excess Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},    
            **{f"umbrella_premium_{label}": hx.Float(mode="output", view={"label": "Umbrella Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},    
            **{f"model_premium_{label}": hx.Float(mode="output", view={"label": "Model Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
            **{f"uplift_for_nmp_{label}": hx.Float(mode="output", view={"label": "Uplift for Non-Modelled Perils","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},    
            **{f"minimum_premium_{label}": hx.Float(mode="output", view={"label": "Minimum Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},    
            **{f"gross_premium_{label}": hx.Float(mode="output", view={"label": "Gross Premium","format":utils.thousands_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},    
            **{f"quoted_premium_{label}": hx.Float(mode="input", async_input= ["pricing_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "pricing_copy_option", "reset": False}], default=None, optionality="optional", view={"label": "Quoted Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000}) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},    
            **{f"bpi_{label}": hx.Float(mode="output",  view={"label": "BPI%","format":utils.percent_format(0)},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
            **{f"tech_eo_net_premium_usd_{label}": hx.Float(mode="output",  view={"label": "Tech E&O Net Premium USD - Excess"},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
            **{f"comment_{label}": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment:"},async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},

            #GMM: This sets the umbrella premiums and cession splits for all 1-10 excess layers for each umbrealla coverage - within the option node as the same options need to exist for umbrella coverage         
            **{f"gmm_{item}": hx.Structure(view ={"label": label}, children = {
                **{f"premium_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.thousands_format(0)},async_input=["generate_email_task","generate_referral_email_task"]) 
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])},
                **{f"cession_premium_split_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.percent_format(1)})
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])},
            }) for item, label in zip(hx_params.table_gmm_umbrella["umbrella_name"], hx_params.table_gmm_umbrella["umbrella_label"])},

            #GLSN: This sets the umbrella premiums and cession splits for all 1-10 excess layers for each umbrealla coverage - within the option node as the same options need to exist for umbrella coverage 
            **{f"glsn_{item}": hx.Structure(view ={"label": label}, children = {
                **{f"premium_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.thousands_format(0)},async_input=["generate_email_task","generate_referral_email_task"]) 
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])},
                **{f"cession_premium_split_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.percent_format(1)})
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])}, 
            }) for item, label in zip(hx_params.table_glsn_umbrella["umbrella_name"], hx_params.table_glsn_umbrella["umbrella_label"])},

            #These are further umbrella terms, not part of the coverages, but still within the options node, and for each excess layer
            "umbrella_eel":hx.Structure(view ={"label": "EEL"}, children = {
                **{f"premium_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.thousands_format(0)})
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])}, 
                }),
            "umbrella_unsupported_net_premium":hx.Structure(view ={"label": "Unsupported Net Premium"}, children = {
                **{f"premium_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.thousands_format(0)})
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])}, 
                }),
            "umbrella_total_excess_net_premium":hx.Structure(view ={"label": "Total Excess Net Premium"}, children = {
                **{f"premium_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.thousands_format(0)})
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])}, 
                }), 
            "umbrella_munich_cession_net":hx.Structure(view ={"label": "Munich Cession (Net)"}, children = {
                **{f"premium_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.thousands_format(0)})
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])}, 
                }),
            "umbrella_munich_cession_gross":hx.Structure(view ={"label": "Munich Cession (Gross)"}, children = {
                **{f"premium_{excess}": hx.Float(mode="output", view={"label": name,"format":utils.thousands_format(0)})
                for excess, name in zip(["primary","1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"],["Primary","1XS",  "2XS", "3XS", "4XS","5XS","6XS","7XS","8XS","9XS","10XS"])}, 
                })      
          

        }),
        #The selected option from the pricing tab        
        "option_selected": hx.Str(mode="input", default="Option 1", optionality="optional", options_data="../options", options_field="option_label", view={"label": "Selected Option"},async_input=["generate_email_task","generate_referral_email_task","rarc_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"]), 
        "tech_eo_base_net_premium_usd": hx.Float(mode = "output")
        
    })
    