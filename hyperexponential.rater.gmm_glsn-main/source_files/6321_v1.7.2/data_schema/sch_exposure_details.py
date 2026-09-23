import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params



def sch_exposure_details(cds):
    
    #----------------------------------------------------------------------------------------------#
    # Aggregate exposure details 
    #----------------------------------------------------------------------------------------------#
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "revenue": hx.Float(mode="input", optionality = "required",default=0, async_input=["rarc_task","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], async_output=["roll_exposure_fields_task",{"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], view={"label": "Revenue", "format": utils.thousands_format(0), "options":{"mandatory":{"style_cell":"hx-neutral"}}}, validation={"min_value": 0, "max_value": 100000000000000}),
        "revenue_empty": hx.Bool(mode="output"),
        "revenue_filled": hx.Bool(mode="output"),
        "revenue_info": hx.Str(mode="output"),

        "total_venue_us_factor": hx.Float(mode="output", view={"label": "Total US Factor"}),  
        "total_venue_international_factor": hx.Float(mode="output", view={"label": "Total International Factor"}),
        "total_venue_factor": hx.Float(mode="output", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], view={"label": "Overall Venue Factor"}),
        "total_percentage_selected": hx.Float(mode="output", view={"label": "Total Selected","format":utils.percent_format(1)}, async_input=["generate_email_task","generate_referral_email_task","venue_factors_override_flag","venue_factors_calculate_selected", "venue_calculation_with_override"]), 

        "gmm_total_base_premium_current_year": hx.Float(mode="output", view={"label": "Base Premium - Current Year","format":utils.thousands_format(0)}),
        "gmm_total_base_premium_one_years_ago": hx.Float(mode="output", view={"label": "Base Premium - Previous Year","format":utils.thousands_format(0)}),
        "temp_gmm_total_base_premium_one_years_ago": hx.Float(mode="output", async_output=[{"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], view={"label": "Base Premium - Previous Year","format":utils.thousands_format(0)}),
        "gmm_total_base_premium_one_years_ago_info_by": hx.Str(mode="output", view={"label": " "}),
        "glsn_total_base_premium_current_year": hx.Float(mode="output", view={"label": "Base Premium - Current Year","format":utils.thousands_format(0)}),
        "glsn_total_base_premium_one_years_ago": hx.Float(mode="output", view={"label": "Base Premium - Previous Year","format":utils.thousands_format(0)}),
        "temp_glsn_total_base_premium_one_years_ago": hx.Float(mode="output", async_output=[{"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], view={"label": "Base Premium - Previous Year","format":utils.thousands_format(0)}),
        "glsn_total_base_premium_one_years_ago_info_by": hx.Str(mode="output", view={"label": " "})
    })


    #----------------------------------------------------------------------------------------------#
    # Show / Hides are housed just in cds root
    #----------------------------------------------------------------------------------------------#
    cds.extend_node_rater_defined("cds", {
        "rater_selection": hx.Str(mode="input", default="Global Misc Med Rater", options=["Global Misc Med Rater", "Global Life Sciences Rater"], view={"label": "Rater Selection"}),
        "gmm_masking": hx.Bool(mode="output",async_input=["roll_exposure_fields_task", "start_renewal_task","initialise_model","pricing_copy_option","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"]),
        "glsn_masking": hx.Bool(mode="output",async_input=["roll_exposure_fields_task", "start_renewal_task","initialise_model","pricing_copy_option"]),
        "triage_masking": hx.Bool(mode="output"),
        "exposure_masking": hx.Bool(mode="output"),
        "us_masking": hx.Bool(mode="output",async_input=["venue_factors_select_all","venue_factors_clear_all","venue_factors_calculate_selected"]),
        "international_masking": hx.Bool(mode="output",async_input=["venue_factors_select_all","venue_factors_clear_all","venue_factors_calculate_selected"]),
        "show_prior_exposure_years": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Show/Hide Previous Years"}),
        "show_prior_triage_years": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Show/Hide Previous Years"}),
        "us_and_international_masking": hx.Bool(mode="output"),
        "international_and_us_masking": hx.Bool(mode="output"),
        "cips": hx.Bool(mode="input", default=False, optionality="required", view={"label":"CIPS?"}),
        "punitive_damages_masking": hx.Bool(mode="output"),
    })



    cds.extend_node_rater_defined("cds",{
        #----------------------------------------------------------------------------------------------#
        # Rating Factors common to both GLSN and GMM are set out here
        #----------------------------------------------------------------------------------------------#
        "rating_factors": hx.Structure(view ={"label": "Rating Factors"}, children = {
            "currency": hx.Str(mode="override",async_input= ["rarc_task","generate_email_task","generate_referral_email_task","initialise_model","start_renewal_task"], options_table= "table_currency", options_column= "currency", optionality= "required",view={"label":"Currency"}),
            "temp_expiry_currency": hx.Str(mode="input", async_output=[{"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}],default="USD", view={"label": "Previous currency"}),
            "account_score": hx.Str(mode="output", view={"label": "Account Score"},async_input=["generate_email_task","generate_referral_email_task"]),
            "profit_status": hx.Str(mode="input", optionality="optional", default=None, options=["FP", "NFP", "GOV"], view={"label": "Profit Status"},async_input=["generate_email_task","generate_referral_email_task"]),
            "business_segment": hx.Str(mode="input", optionality="optional", default=None, options=["Mid-Market", "Small Business"], view={"label": "Business Segment"}),

            #This is the schema for the account scoring table and the total net account score
            "account_scoring":hx.Structure(view ={"label": "Account Scoring"}, children = {
                **{item: hx.Structure(view ={"label": label}, children = {
                    "value": hx.Float(mode="input", default=0, options=[1,0,-1], view={"label": "Score","format":utils.integer_format(0)},async_input=["generate_email_task","generate_referral_email_task"]),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"},async_input=["generate_email_task","generate_referral_email_task"])
                }) for item, label in zip(hx_params.table_account_scoring["account_scoring_name"], hx_params.table_account_scoring["account_scoring_label"])},
            }),

            "account_scoring_details" : hx.Structure(view ={"label": "Account Scoring Attributes"}, children={
                "show_account_scoring": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Show/Hide Account Scoring Attributes"}),
                "financials_quality": hx.Structure(view ={"label": "Financials Quality"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1", "read_only":True,"multiline":True},
                        default="We possess most recent audited financials and have reviewed and documented them. Insured shows profitability. Insured shows net tangible assets. Balance sheet is strong."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="We possess reliable summary of balance sheet and Profit/Loss statement. Insured is break even or profitable over time. The retention can be paid."), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="Insured is loss making on a continual basis.  We do not possess a reliable financial summary. “Goodwill” accounts for all equity. There is a “going concern” statement in the financials."),  
                }),
                "claims_handling": hx.Structure(view ={"label": "Claims Handling"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="Insured has an in-house dedicated team or quality TPA. Insured sets reserves and prepares or has others prepare loss runs. Beazley Claim Managers have a good relationship with the Insured/TPA."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="Insured works collaboratively with Beazley Claim Managers.  Even with some claims frequency or severity, the relationship with Beazley is good. "), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="Insured has no dedicated claims or risk management team.  Insured/broker can be combative with the Beazley Claims Managers or take unreasonable positions. "),  
                }),
                "claims_experience": hx.Structure(view ={"label": "Claims Experience"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="Insured has few claims and what it has it manages well. Severity is contained."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="Some claims frequency and/or severity. Long term, the risk is a profitable account by Beazley measures."), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="Once a claims target, always a claims target.  Insured has a loss on the books that would take more than 5 years to recover on pricing. "),  
                }),
                "jurisdiction_venue": hx.Structure(view ={"label": "Jurisdiction / Venue"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="While captured in rater, the Insured operates in favorable locations."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="National account, or account is located in a mix of jurisdictions which do not skew too favorable or negative. "), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="Located or operating in one or more judicial hellholes or counties, cities, not adequately depicted in the rater. "),  
                }),
                "wordings": hx.Structure(view ={"label": "Wordings"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="We are employing Beazley forms and endorsements, or a carrier form we hold in high regard, and we have documented the favorable features. Coverage terms are favorable. We are using current Beazley updated endorsements (e.g., cyber, pregnancy termination)"),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="Our form is heavily manuscripted, not necessarily with favorable terms. We are using a Beazley form, but it is outdated or not the current version. "), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="We are using a broker form or one with which we do not have a lot of experience. Underlying forms difficult to read or interpret. Some terms and conditions not favorable. We do not possess all underlying wordings. "),  
                }),
                "level_of_service": hx.Structure(view ={"label": "Level of Service"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="Smooth sailing with the broker and Insured. Reasonable and professional interactions."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="Insured/broker require some touch. Delays in answering subjectivities or opaque answers to queries. "), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="Insured frequently needs AI endorsements which overreach. Provider schedules need frequent updating. Need to repeatedly chase on subjectivities. Heavy touch."),  
                }),
                "knowledge_of_account": hx.Structure(view ={"label": "Knowledge of Acount / Risk"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="We know the Insured well. We have face to face meetings/visits. Submission complete. The account clicks. Insured is forthcoming with changes to profile."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="We are new to the account and are still figuring it out. Information so far is good. Insured keeps us apprised of critical developments."), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="It is hard to get information from the Insured or broker. The full story is not complete. Broker does not know the account well."),  
                }),
                "nfp_gov_fp": hx.Structure(view ={"label": "NFP / GOV / FP"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="The Insured is not for profit and has a long history of low frequency and low severity. The Insured or the Insured's clients are governmental or quasi-government. There is a favorable sovereign immunity."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="Insured is for profit, but not a target for litigation. Governmental risk Sovereign immunities may not inure to our benefit. Government entity position may not present any tort protections. "), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="For profit. The Insured is vulnerable to “profits over people” arguments. The Insured is vulnerable to social inflation claims on damages/liability. "),  
                }),
                "broker": hx.Structure(view ={"label": "Broker"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="High integrity wants to work with us. High bind to quote ratios. Does not waste our time. Can sell price and terms."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="Average broker, average relationship.Ok bind and submit ratios. "), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="Difficult to work or communicate with the broker. Broker spins our wheels. Broker does not understand or appreciate our approach. "),  
                }),
                "corporate_integrity": hx.Structure(view ={"label": "Corporate Identity"}, children={
                    "pro_example":hx.Str(mode="input",view={"label": "Pro (A/B) Example: \n Attribute +1","read_only":True,"multiline":True},
                        default="ESG compliant per syndicate standards. Socially conscious. Great place to work. Has stated visions/plan."),
                    "neutral_example":hx.Str(mode="input",view={"label": "Neutral (C) Example: \n Attribute 0", "read_only":True,"multiline":True},
                        default="Do not fully know Insured's ESG posture, but we are investigating. "), 
                    "con_example":hx.Str(mode="input",view={"label": "Con (D/F) Example: \n Attribute -1", "read_only":True,"multiline":True},
                        default="Recent or pending Regulatory actions. No ESG complaint per syndicate standards. We do not know the Insured's profile. "),  
                }),
                "parameters": hx.List(mode="input",view ={"label": "Parameters"}, default_element_count=1,children={
                    "five_or_more":hx.Str(mode="output",view={"label": '5 or more net Pros is an “A”',"multiline":True}),
                    "three_or_more":hx.Str(mode="output",view={"label": '3 or more net Pros is a “B”',"multiline":True}), 
                    "two_or_fewer":hx.Str(mode="output",view={"label": '2 or fewer net Pros / net Cons is a “C”',"multiline":True}),
                    "three_or_more_cons":hx.Str(mode="output",view={"label": '3 or more net Cons is a “D”',"multiline":True}),
                    "five_or_more_cons":hx.Str(mode="output",view={"label": '5 or more net Cons is an "F”',"multiline":True}),
                    "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"})

                })
            }),

            "total_net_score": hx.Structure(view={"label": "Total Net Score"},children={
                "value": hx.Float(mode="output", view={"label": "Total Net Score","format":utils.integer_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),
                }),

            #This sets whether the account is US or international as well as the choice of law
            "us_international_choice_of_law" : hx.Structure(linked_options_table="table_choice_of_law", linked_options_columns=["us_international", "choice_of_law"], children={
                "us_international": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"],optionality="optional",default=None, view={"label":"US/International"}),
                "choice_of_law": hx.Str(mode="input",optionality="optional", async_input=["generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],default=None, view={"label": "Choice of Law"}),
            }),

            "mix_of_exposure_measures_message": hx.Str(mode="output", view={"label": "Warning!"}),
            "exposure_measures_message_show":hx.Bool(mode="output"),

            "current_year_label": hx.Str(mode="output", view={"label": " "}),
            "one_years_ago_label": hx.Str(mode="output", view={"label": " "}),
            "two_years_ago_label": hx.Str(mode="output", view={"label": " "}),
            "three_years_ago_label": hx.Str(mode="output", view={"label": " "}),
            "four_years_ago_label": hx.Str(mode="output", view={"label": " "}),
            "five_years_ago_label": hx.Str(mode="output", view={"label": " "}),
            

            # This is purely for the rating summary view page. It sets the first row to be retention and all other fields as outputs.
            "retention": hx.Structure(view ={"label": "Retention"}, children = {
                "limit": hx.Float(mode="output", view={"label": "Each Loss Limit","format":utils.thousands_format(0)}),
                "aggregate_limit": hx.Float(mode="output", view={"label": "Aggregate Limit","format":utils.thousands_format(0)}),
                "brokerage": hx.Float(mode="output", view={"label": "Brokerage","format":utils.thousands_format(0)}),
                "model_premium": hx.Float(mode="output", view={"label": "Model Premium","format":utils.thousands_format(0)}),
                "quoted_premium": hx.Float(mode="output", view={"label": "Quoted Premium","format":utils.thousands_format(0)}),
                "quoted_rate": hx.Float(mode="output", view={"label": "Quoted Rate","format":utils.thousands_format(0)}),
                "bound_premium": hx.Float(mode="output", view={"label": "Bound Premium","format":utils.thousands_format(0)}),
                "bound_rate": hx.Float(mode="output", view={"label": "Bound Rate","format":utils.thousands_format(0)}),
                "section_reference": hx.Float(mode="output", view={"label": "Policy Reference","format":utils.thousands_format(0)}),
                "status": hx.Float(mode="output", view={"label": "Status", "options": {"input": {"label": "Status"}, }}),
                "net_written_premium": hx.Float(mode="output", view={"label": "Net Written Premium","format":utils.thousands_format(0)}),
                "benchmark_premium": hx.Float(mode="output", view={"label": "Benchmark Premium","format":utils.thousands_format(0)}),
                "bpi": hx.Float(mode="output", view={"label": "BPI %","format":utils.thousands_format(0)}),
                "technical_premium": hx.Float(mode="output", view={"label": "Technical Premium","format":utils.thousands_format(0)}),
                "tpi": hx.Float(mode="output", view={"label": "TPI %","format":utils.thousands_format(0)}),
                "bpi_case_priced": hx.Float(mode="output", view={"label": "BPI Case Priced %","format":utils.thousands_format(0)}),
            }),

            "pricing": hx.Structure(view={"label": "Pricing"}, children={
                #These elements of each of the pricing coverages are defined outside the options node as they do not vary with option
                **{item: hx.Structure(view={"label": label}, children={
                    "selection":hx.Bool(mode="input", default=False, optionality="required", view={"label":"Include Coverage?"}, async_input=["generate_email_task","generate_referral_email_task","set_defaults_button"]),
                    "include_primary":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], default=False, optionality="required", view={"label":"Include in Primary?"}),
                    "include_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Include in Excess?"}),
                    "claims_basis":hx.Str(mode="output", view={"label": "Claims Basis"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "retroactive_date": hx.Date(default=None, async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],async_output=[{"task": "set_defaults_button", "reset": False}], mode="input", optionality="optional",view={"label": "Retroactive Date"}),
                    "significant_coverage": hx.Str(mode="output", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], view={"label": "Significant Coverage"}),
                    "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "label": hx.Str(mode="output", view={"label": "Default struct label"}),
                })
                for item, label in zip(["professional_liability","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media","product_recall"],
                ["Professional Liability","Sexual Abuse","EBL","Employers Liability","Tech E&O/Products/Media","Product Recall Expenses"])},
                
                # Have to define these outside the loop as they are slightly different inputs to the above
                "product_liability": hx.Structure(view={"label": "Product Liability"}, children={
                    "selection":hx.Bool(mode="input", default=False, optionality="required", view={"label":"Include Coverage?"}, async_input=["generate_email_task","generate_referral_email_task","set_defaults_button"]),
                    "include_primary":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], default=False, optionality="required", view={"label":"Include in Primary?"}),
                    "include_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Include in Excess?"}),
                    "claims_basis":hx.Str(mode="output", view={"label": "Claims Basis"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "retroactive_date": hx.Date(default=None, mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],async_output=[{"task": "set_defaults_button", "reset": False}], optionality="optional",view={"label": "Retroactive Date"}),
                    "significant_coverage": hx.Str(mode= "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default= None, options= ["Significant", "Medium", "Insignificant"], view={"label": "Significant Coverage"}),
                    "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}, async_input=["generate_email_task","generate_referral_email_task"])
                }),
                "eo": hx.Structure(view={"label": "E&O"}, children={
                    "selection":hx.Bool(mode="input", default=False, optionality="required", view={"label":"Include Coverage?"}, async_input=["generate_email_task","generate_referral_email_task","set_defaults_button"]),
                    "include_primary":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], default=False, optionality="required", view={"label":"Include in Primary?"}),
                    "include_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Include in Excess?"}),
                    "claims_basis":hx.Str(mode="output", view={"label": "Claims Basis"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "retroactive_date": hx.Date(default=None, async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],async_output=[{"task": "set_defaults_button", "reset": False}], mode="input", optionality="optional",view={"label": "Retroactive Date"}),
                    "significant_coverage": hx.Str(mode= "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default= None, options= ["Significant", "Medium", "Insignificant"], view={"label": "Significant Coverage"}),
                    "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "label": hx.Str(mode="output", view={"label": "Default struct label"}),
                }),
                "healthcare_professional_liability": hx.Structure(view={"label": "Healthcare Professional Liability"}, children={
                    "selection":hx.Bool(mode="input", default=False, optionality="required", view={"label":"Include Coverage?"}, async_input=["generate_email_task","generate_referral_email_task","set_defaults_button"]),
                    "include_primary":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], default=False, optionality="required", view={"label":"Include in Primary?"}),
                    "include_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Include in Excess?"}),
                    "claims_basis":hx.Str(mode="output", view={"label": "Claims Basis"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "retroactive_date": hx.Date(default=None, async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task"],async_output=[{"task": "set_defaults_button", "reset": False}], mode="input", optionality="optional",view={"label": "Retroactive Date"}),
                    "significant_coverage": hx.Str(mode= "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default= None, options= ["Significant", "Medium", "Insignificant"], view={"label": "Significant Coverage"}),
                    "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}, async_input=["generate_email_task","generate_referral_email_task"])
                }),
                "general_liability": hx.Structure(view={"label": "General Liability"}, children={
                    "selection":hx.Bool(mode="input", default=False, optionality="required", view={"label":"Include Coverage?"}, async_input=["generate_email_task","generate_referral_email_task","set_defaults_button"]),
                    "include_primary":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], default=False, optionality="required", view={"label":"Include in Primary?"}),
                    "include_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Include in Excess?"}),
                    "claims_basis": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default="Claims-Made", optionality="optional", options=["Occurrence", "Claims-Made"], view={"label": "Claims Basis"}),
                    "retroactive_date": hx.Date(default=None, mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],async_output=[{"task": "set_defaults_button", "reset": False}], optionality="optional",view={"label": "Retroactive Date"}),
                    "significant_coverage": hx.Str(mode="output", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], view={"label": "Significant Coverage"}),
                    "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "label": hx.Str(mode="output", view={"label": "Default struct label"}),
                }),
                "well_tech_eo_media": hx.Structure(view={"label": "Well Tech E&O and Media"}, children={
                    "selection":hx.Bool(mode="input", default=False, optionality="required", view={"label":"Include Coverage?"}, async_input=["generate_email_task","generate_referral_email_task","set_defaults_button"]),
                    "include_primary":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], default=False, optionality="required", view={"label":"Include in Primary?"}),
                    "include_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Include in Excess?"}),
                    "claims_basis":hx.Str(mode="output", view={"label": "Claims Basis"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    "retroactive_date": hx.Date(default=None, async_input=["rarc_task","generate_email_task","generate_referral_email_task","set_defaults_button", "generate_primary_proposal_template_task"],async_output=[{"task": "set_defaults_button", "reset": False}], mode="input", optionality="optional",view={"label": "Retroactive Date"}),
                    "significant_coverage": hx.Str(mode= "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default= None, options= ["Significant", "Medium", "Insignificant"], view={"label": "Significant Coverage"}),
                    "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}, async_input=["generate_email_task","generate_referral_email_task"])
                }),
                "include_stop_gap_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Stop Gap: Excess"}),
                "include_tria_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"TRIA: Excess"}),
                "include_punitive_damages_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Punitive Damages: Excess"}),
                "include_costs_in_addition_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Costs In Addition: Excess"}),
                "include_auto_excess":hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, optionality="required", view={"label":"Auto HNOA: Excess"}),
                **{f"claims_basis_{label}":hx.Str(mode="output", view={"label": "Claims Basis"}) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
                **{f"retroactive_date_{label}": hx.Date(mode="override", async_input=["rarc_task"], view={"label": "Retroactive Date"}) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
            }),


            #----------------------------------------------------------------------------------------------#
            # Structure housing GLSN Rating Factors
            #----------------------------------------------------------------------------------------------#
            
            "glsn": hx.Structure(view ={"label": "GLSN Rating Factors"}, children = {
                #This is the schema for the glsn supply chain section
                "supply_chain": hx.Str(mode = "input", async_input=["rarc_task"], default = "Not Applicable",options_table = "table_glsn_supply_chain", options_column = "supply_chain_label", view = {"label": "Supply Chain Function"}),
                "supply_chain_factor": hx.Float(mode="output", view={"label": "Factor","format":utils.integer_format(2)}),

                #This is the schema for the glsn clinical trial section
                "clinical_trial": hx.Str(mode = "input", async_input=["rarc_task"], default = "Not Applicable",options_table = "table_glsn_clinical_trial", options_column = "clinical_trial_label", view = {"label": "Clinical Trial Role"}),
                "clinical_trial_factor": hx.Float(mode="output", view={"label": "Factor","format":utils.integer_format(2)}),

                "brag_status": hx.Str(mode="input", optionality="optional",default=None, options=["Green", "Amber", "Red", "Pink", "Blocked"], view={"label": "BRAG Status"}),
                "form": hx.Str(mode="override", options_table="table_glsn_form",options_column="form", async_input=["generate_email_task","generate_referral_email_task"], view={"label": "Form"}),
                
                #GlSN size discount curve selection
                "number_of_participants": hx.Float(mode="output", view={"label": "Number of Participants","format":utils.integer_format(2)}),
                "size_discount_selection": hx.Str(mode="override", async_input=["rarc_task"],  options=["Revenue", "Participants"], view={"label": "Basis for Size Discount"}),

                "umbrella": hx.Structure(view={"label": "Umbrella"}, children={
                    **{item: hx.Structure(view ={"label": label}, children = {
                        "underlying_ee": hx.Float(mode="output", view={"label": "Actual EE Underlying","format":utils.thousands_format(0)}, async_input=["generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_agg": hx.Float(mode="output", view={"label": "Actual Agg Underlying","format":utils.thousands_format(0)}, async_input=["generate_email_task","generate_referral_email_task"], validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_premium": hx.Float(mode="output", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], view={"label": "Underlying Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),     
                        "occurrence_cover": hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"],default=False, view={"label": "Occurrence Cover"}),
                    }) if item == "general_liability" else
                        hx.Structure(view ={"label": label}, children = {
                        "underlying_ee": hx.Float(mode="input", async_input= ["rarc_task","generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], optionality="optional",default=None, view={"label": "Actual EE Underlying","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_agg": hx.Float(mode="input", async_input= ["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default=None, view={"label": "Actual Agg Underlying","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_premium": hx.Float(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default=None, view={"label": "Underlying Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),
                        "occurrence_cover": hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"],default=False, view={"label": "Occurrence Cover"}),
                    })
                    for item, label in zip(hx_params.table_glsn_umbrella["umbrella_name"], hx_params.table_glsn_umbrella["umbrella_label"])},
                })
            }),

            #----------------------------------------------------------------------------------------------#
            # Structure housing GMM Rating Factors
            #----------------------------------------------------------------------------------------------#
            
            "gmm": hx.Structure(view ={"label": "GLSN Rating Factors"}, children = {
                "product_override": hx.Str(mode="input", optionality="optional",default="Misc Med", options=["Misc Med", "Virtual Care"], async_input=["generate_email_task","generate_referral_email_task"], view={"label": "Product Override"}),

                "umbrella": hx.Structure(view={"label": "Umbrella"}, children={
                    **{item: hx.Structure(view ={"label": label}, children = {
                        "underlying_ee": hx.Float(mode="output", view={"label": "Actual EE Underlying","format":utils.thousands_format(0)}, async_input=["generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_agg": hx.Float(mode="output", view={"label": "Actual Agg Underlying","format":utils.thousands_format(0)}, async_input=["generate_email_task","generate_referral_email_task"], validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_premium": hx.Float(mode="output", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], view={"label": "Underlying Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),     
                        "occurrence_cover": hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"],default=False, view={"label": "Occurrence Cover"}),
                    }) if item == "general_liability" else
                        hx.Structure(view ={"label": label}, children = {
                        "underlying_ee": hx.Float(mode="input", async_input= ["rarc_task","generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], optionality="optional",default=None, view={"label": "Actual EE Underlying","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_agg": hx.Float(mode="input", async_input= ["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default=None, view={"label": "Actual Agg Underlying","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),
                        "underlying_premium": hx.Float(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default=None, view={"label": "Underlying Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}),     
                        "occurrence_cover": hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=False, view={"label": "Occurrence Cover"}),
                    })
                    for item, label in zip(hx_params.table_gmm_umbrella["umbrella_name"], hx_params.table_gmm_umbrella["umbrella_label"])},
                })
            }),

            #----------------------------------------------------------------------------------------------#
            # Structure housing Cyber rating factors
            #----------------------------------------------------------------------------------------------#
            
            "cyber": hx.Structure(view ={"label": "Cyber Rating Factors"}, children = {
                "first_or_third_party": hx.Str(mode="input", async_input=["generate_email_task","generate_referral_email_task"], optionality="required",default="First Party and Third Party", options=["First Party and Third Party", "Third Party Only"], view={"label":"Coverage Requested"}),
                "first_or_third_party_note": hx.Str(mode="output", view={"label":" "}),
                "first_and_third_party_show": hx.Bool(mode="output"),
                "third_party_only_show": hx.Bool(mode="output"),
                "bbr_rater_info_by": hx.Str(mode="output", view={"label":" "}),
                "third_party_only_info_by": hx.Str(mode="output", view={"label":" "}),
                "product": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default=None, options=["BBR", "InfoSec"], view={"label":"Cyber Product"}),
                "include_excess":hx.Bool(mode="input", async_input=["rarc_task"], default=False, optionality="required", view={"label":"Include in Excess?"}), 
                "excess_cyber_note": hx.Str(mode="output", view={"label":" "}),
                "excess_cyber_calc_note": hx.Str(mode="output", view={"label":" "})
            }), 

            #----------------------------------------------------------------------------------------------#
            # Structure housing Tech E&O rating factors
            #----------------------------------------------------------------------------------------------#
            "tech_eo": hx.Structure(view={"label": "Tech E&O"},children={
                "contingent_bi_pd": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="required",default="No", options=["Yes", "No"], view={"label": "Include?"}),
                "contingent_bi_pd_factor": hx.Float(mode="output", view={"label": "Contingent Bodily Injury / Property Damage Default","format":utils.percent_format(0)}),
            })

        })
    })


    
    #----------------------------------------------------------------------------------------------#
    # Structure housing granular exposure details 
    #----------------------------------------------------------------------------------------------#

    cds.extend_node_rater_defined("cds/exposure/granular", {

        #Defining the linked options table to select the primary GMM product
        "gmm_product": hx.Structure(linked_options_table="table_gmm_product_class", linked_options_columns=["product", "cob_code_description","cob_class"], children={
                "product": hx.Str(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model","generate_email_task","generate_referral_email_task"],optionality="optional",default = None,  view={"label":"Product"}),
                "cob_code_description": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],optionality="optional", default = None,view={"label": "COB Code"}),
                "cob_class": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"],optionality="optional",default = None, view={"label": "Class"}),
            }),
    
        #Defining the linked options table to select the primary GLSN product
        "glsn_product": hx.Structure(linked_options_table="table_glsn_product_class", linked_options_columns=["product", "cob_code_description"], children={
                "product": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"],optionality="optional",default=None, view={"label":"Product"}),
                "cob_code_description": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],optionality="optional",default=None, view={"label": "COB Code"}),
            }),

        #This is the schema for the US Venue factors table
        **{item: hx.Structure(view ={"label": label}, children = {
            "factor": hx.Float(mode="output", view={"label":"Factor"},async_input=["generate_email_task","generate_referral_email_task"]),
            "percentage": hx.Float(mode="input",optionality="required",default=0, async_input=["rarc_task","venue_factors_select_all","venue_factors_clear_all","venue_factors_calculate_selected","generate_email_task","generate_referral_email_task"], async_output=["venue_factors_select_all","venue_factors_clear_all",{"task": "venue_factors_calculate_selected", "reset": False},{"task": "venue_calculation_with_override","reset": False}], view={"label": "Venue Split","format":utils.percent_format(2)}, validation={"min_value": 0, "max_value": 1}), 
                # view={"label": "Venue Split","format":utils.percent_format(2), "options":{"mandatory":{"style_cell":"hx-good"}}}, validation={"min_value": 0, "max_value": 1}), # IR edit
            # "percentage_complete" : hx.Bool(mode="output"), # IR edit
            "selection": hx.Bool(mode="input", default=False, optionality="required",async_input = ["rarc_task","venue_factors_calculate_selected","generate_email_task","generate_referral_email_task","venue_calculation_with_override"],async_output=["venue_factors_select_all","venue_factors_clear_all"] ,view={"label":"Venue Selection"}),
            "percentage_output_copy": hx.Float(mode = "output", view={"label":"Percentage Output Copy","format":utils.percent_format(2)}, async_input=["venue_factors_select_all","venue_factors_clear_all","venue_factors_calculate_selected","venue_factors_override_flag","venue_calculation_with_override"]),
            "percentage_async_copy": hx.Float(mode = "output", view = {"label": "Percentage Async Copy","format":utils.percent_format(2)}, async_output=["venue_factors_select_all","venue_factors_clear_all",{"task":"venue_factors_calculate_selected", "reset": False},{"task":"venue_calculation_with_override", "reset": False}], async_input=["venue_factors_override_flag"]),
            "override_flag":hx.Bool(mode = "output",  async_output=[{"task":"venue_factors_override_flag", "reset":False},{"task":"venue_factors_calculate_selected", "reset": True},"venue_factors_select_all","venue_factors_clear_all",{"task":"venue_calculation_with_override","reset":False}],view = {"label": "Override Flag"} , async_input = ["venue_factors_calculate_selected"])
        }) for item, label in zip(hx_params.table_venue_us["venue_name"], hx_params.table_venue_us["venue_label"])},
 
        "include_international_venues": hx.Bool(mode="input", default=False, optionality="required", async_input=["venue_factors_calculate_selected"], view={"label":"Include International Venues?"}),

        #This is the schema for the International Venue factors table
        **{item: hx.Structure(view ={"label": label}, children = {
            "factor": hx.Float(mode="output", view={"label":"Factor"},async_input=["generate_email_task","generate_referral_email_task"]),
            "percentage": hx.Float(mode="input",optionality="required",default=0, async_input=["rarc_task","venue_factors_select_all","venue_factors_clear_all","venue_factors_calculate_selected","generate_email_task","generate_referral_email_task"], async_output=["venue_factors_select_all","venue_factors_clear_all",{"task": "venue_factors_calculate_selected", "reset": False}, {"task": "venue_calculation_with_override","reset": False}], #view={"label": "Venue Split","format":utils.percent_format(2)}, validation={"min_value": 0, "max_value": 1}),
                view={"label": "Venue Split","format":utils.percent_format(2), "options":{"mandatory":{"style_cell":"hx-good"}}}, validation={"min_value": 0, "max_value": 1}), # IR edit
            "percentage_complete" : hx.Bool(mode="output"), # IR edit
            "selection": hx.Bool(mode="input", default=False, optionality="required",async_input = ["rarc_task","venue_factors_calculate_selected","generate_email_task","generate_referral_email_task","venue_calculation_with_override"],async_output=["venue_factors_select_all","venue_factors_clear_all"] ,view={"label":"Venue Selection"}),
            "percentage_output_copy": hx.Float(mode = "output", view={"label":"Percentage Output Copy","format":utils.percent_format(2)}, async_input=["venue_factors_select_all","venue_factors_clear_all","venue_factors_calculate_selected","venue_factors_override_flag","venue_calculation_with_override"]),
            "percentage_async_copy": hx.Float(mode = "output", view = {"label": "Percentage Async Copy","format":utils.percent_format(2)}, async_output=["venue_factors_select_all","venue_factors_clear_all",{"task":"venue_factors_calculate_selected", "reset": False},{"task":"venue_calculation_with_override", "reset": False}], async_input=["venue_factors_override_flag"]),
            "override_flag":hx.Bool(mode = "output", async_output=[{"task":"venue_factors_override_flag", "reset":False},{"task":"venue_factors_calculate_selected", "reset": True},"venue_factors_select_all","venue_factors_clear_all",{"task":"venue_calculation_with_override","reset":False}], view = {"label": "Override Flag"} , async_input = ["venue_factors_calculate_selected"])
        }) for item, label in zip(hx_params.table_venue_international["venue_name"], hx_params.table_venue_international["venue_label"])},

        "include_us_venues": hx.Bool(mode="input", default=False, optionality="required", async_input=["venue_factors_calculate_selected"], view={"label":"Include US Venues?"}),



        

        #This list sets out the primary exposure details for GMM and all fields needed for the primary exposure table
        "gmm_primary_exposure_details": hx.List(mode="input", async_input=["generate_email_task","generate_referral_email_task"],default_element_count=22,children={
            "exposure_class": hx.Str(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label":"Class"}),
            "exposure_measure": hx.Str(mode="output", async_input=["generate_email_task","generate_referral_email_task"],view={"label": "Exposure Measure"}),
            "base_rate": hx.Float(mode="output", async_input=["generate_email_task","generate_referral_email_task"],view={"label": "Base Rate","format":utils.thousands_format(4)}),
            "formatted_base_rate": hx.Str(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label":"Base Rate"}),
            # "five_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            # "four_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            # "three_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            # "two_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            # "one_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
            # "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task", "generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}),
            "selection": hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"], default=False, optionality="required", view={"label":"Use for Calculation?"}),
            "base_premium": hx.Float(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label": "Base Premium","format":utils.thousands_format(0)}),
            "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}),
            
            "five_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False},{"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "four_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False},{"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "three_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False},{"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "two_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False},{"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "one_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False},{"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
            "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task", "generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}, "clear_exposures_task"], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}),
            "stg_five_years_ago": hx.Float(mode="input", async_output=[ {"task": "initialise_model", "reset": False},{"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional", view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "stg_four_years_ago": hx.Float(mode="input", async_output=[ {"task": "initialise_model", "reset": False},{"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional", view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "stg_three_years_ago": hx.Float(mode="input", async_output=[ {"task": "initialise_model", "reset": False},{"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task"],default=0, optionality="optional", view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "stg_two_years_ago": hx.Float(mode="input", async_output=[ {"task": "initialise_model", "reset": False},{"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional", view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "stg_one_years_ago": hx.Float(mode="input", async_output=[ {"task": "initialise_model", "reset": False},{"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional", view={"label": "Previous Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
            "stg_current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model", "generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}, {"task": "initialise_model", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}),
         }),
        
        
        #This list sets out the primary exposure details for GLSN and all fields needed for the primary exposure table
        "glsn_primary_exposure_details": hx.List(mode="input", default_element_count=22,children={
            "cob": hx.Str(mode="output", view={"label":"Class of Business"},async_input=["generate_email_task","generate_referral_email_task"]),
            "exposure_base": hx.Str(mode="output", view={"label": "Exposure Base"},async_input=["generate_email_task","generate_referral_email_task"]),
            "exposure_measure": hx.Str(mode="output", view={"label": "Exposure Measure"},async_input=["generate_email_task","generate_referral_email_task"]),
            "base_rate": hx.Float(mode="output", view={"label": "Base Rate","format":utils.thousands_format(4)},async_input=["generate_email_task","generate_referral_email_task"]),
            "formatted_base_rate": hx.Str(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label":"Base Rate"}),
            # "five_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            # "four_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            # "three_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            # "two_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            # "one_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task","rarc_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}),
            # "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000000000}),
            "selection": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Use for Calculation?"},async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"]),
            "base_premium": hx.Float(mode="output", view={"label": "Base Premium","format":utils.thousands_format(0)},async_input=["generate_email_task","generate_referral_email_task"]),
            "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"}),

            "five_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "four_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "three_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "two_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "one_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], async_input=["rarc_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}),
            "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}, "clear_exposures_task"], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000000000}),        
            "stg_five_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"],  default=0, optionality="optional",view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "stg_four_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"],  default=0, optionality="optional",view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "stg_three_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"],  default=0, optionality="optional",view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "stg_two_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"],  default=0, optionality="optional",view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "stg_one_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task","rarc_task"], default=0, optionality="optional",view={"label": "Previous Year","format":utils.thousands_format(0)}),
            "stg_current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000000000}),        

         }),
        

        #Schema for the secondary exposure details
        "gmm_secondary_exposure_details": hx.List(mode="input", default_element_count=10, children={
            "gmm_secondary_exposure": hx.Structure(linked_options_table="table_gmm_exposure_classes", linked_options_columns=["class", "exposure_measure"], children={
                "exposure_class": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"], optionality="optional", default = None, view={"label":"Class"}),
                "exposure_measure": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"], optionality="optional", default = None, view={"label": "Exposure Measure"}),
            }),
            "base_rate": hx.Float(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label": "Base Rate","format":utils.thousands_format(4)}),
            "formatted_base_rate": hx.Str(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label":"Base Rate"}),
            # "five_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            # "four_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            # "three_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            # "two_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            # "one_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}),
            # "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
            "selection": hx.Bool(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"], default=False, optionality="required", view={"label":"Use for Calculation?"}),
            "base_premium": hx.Float(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label": "Base Premium","format":utils.thousands_format(0)}),
            
            "five_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"],  view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "four_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"],  view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "three_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"],  view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "two_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"],  view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "one_years_ago": hx.Float(mode="output",async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], async_input=["rarc_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}),
            "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
            "stg_five_years_ago": hx.Float(mode="input",async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "stg_four_years_ago": hx.Float(mode="input",async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "stg_three_years_ago": hx.Float(mode="input",async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "stg_two_years_ago": hx.Float(mode="input",async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "stg_one_years_ago": hx.Float(mode="input",async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["rarc_task","roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Previous Year","format":utils.thousands_format(0)}),
            "stg_current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
         }),
        "glsn_secondary_exposure_details": hx.List(mode="input", default_element_count=10, children={
            "glsn_secondary_exposure": hx.Structure(linked_options_table="table_glsn_exposure_classes", linked_options_columns=["cob", "exposure_base","exposure_measure"], children={
                "cob": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"],optionality="optional", default = None, view={"label":"Class of Business"}),
                "exposure_base": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"], optionality="optional", default = None, view={"label": "Exposure Base"}),
                "exposure_measure": hx.Str(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"], optionality="optional", default = None, view={"label": "Exposure Measure"}),
            }),
            "base_rate": hx.Float(mode="output", view={"label": "Base Rate","format":utils.thousands_format(4)}, async_input=["generate_email_task","generate_referral_email_task"]),
            "formatted_base_rate": hx.Str(mode="output", async_input=["generate_email_task","generate_referral_email_task"], view={"label":"Base Rate"}),
            # "five_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            # "four_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            # "three_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            # "two_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["roll_exposure_fields_task", "start_renewal_task"], view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            # "one_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}),
            # "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
            "selection": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Use for Calculation?"}, async_input=["rarc_task","generate_email_task","generate_referral_email_task"], async_output=["clear_exposures_task"]),
            "base_premium": hx.Float(mode="output", view={"label": "Base Premium","format":utils.thousands_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),

            "five_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "four_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "three_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "two_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "one_years_ago": hx.Float(mode="output", async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], async_input=["rarc_task"], view={"label": "Previous Year","format":utils.thousands_format(0)}),
            "current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False},"clear_exposures_task"], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),
            "stg_five_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Five Years Ago","format":utils.thousands_format(0)}),
            "stg_four_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Four Years Ago","format":utils.thousands_format(0)}),
            "stg_three_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Three Years Ago","format":utils.thousands_format(0)}),
            "stg_two_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["roll_exposure_fields_task"], default=0, optionality="optional",view={"label": "Two Years Ago","format":utils.thousands_format(0)}),
            "stg_one_years_ago": hx.Float(mode="input", async_output=[ {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], async_input=["rarc_task","roll_exposure_fields_task"],default=0, optionality="optional", view={"label": "Previous Year","format":utils.thousands_format(0)}),
            "stg_current_year": hx.Float(mode="input", async_input=["rarc_task","roll_exposure_fields_task", "start_renewal_task","initialise_model","generate_email_task","generate_referral_email_task"],async_output=[{"task": "roll_exposure_fields_task", "reset": False}, {"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], default=0, optionality="optional", view={"label": "Current Year","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000000}),            
         }),

         

         #The following relate to the aggregation details page for the GLSN model
         "glsn_aggregation_details": hx.List(mode="input", default_element_count=10,children={
            "type": hx.Str(mode="input", optionality="optional",default=None,options_table="table_glsn_aggregation_type",options_column="type", view={"label": "Type"}),
            "name": hx.Str(mode="input",optionality="optional", default = " ",view={"label": "Name"}),
            "beazley_insured": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Beazley Insured"}),
            "aggregated_capacity": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Aggregated Capacity","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000000}),
            "notes": hx.Str(mode="input",optionality="optional", default = " ",view={"label": "Notes"}),
         }),
        
        #These are the structures for the aggregation details of dangerous ingredients for the GLSN rater
         **{item: hx.Structure(view ={"label": label}, children = {
            "exposed": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Exposed?"}),
            "revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Applicable Revenue","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000000}),
            "notes": hx.Str(mode="input",optionality="optional", default = " ",view={"label": "Notes"}),
        }) for item, label in zip(hx_params.table_glsn_danger_ingred_1["ingredient_name"], hx_params.table_glsn_danger_ingred_1["ingredient_label"])},

        **{item: hx.Structure(view ={"label": label}, children = {
            "exposed": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Exposed?"}),
            "revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Applicable Revenue","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000000}),
            "notes": hx.Str(mode="input",optionality="optional", default = " ",view={"label": "Notes"}),
        }) for item, label in zip(hx_params.table_glsn_danger_ingred_2["ingredient_name"], hx_params.table_glsn_danger_ingred_2["ingredient_label"])},
        
        "glsn_dangerous_ingredient_other_selection": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Other Dangerous Ingredient Selection"}),
        
        "glsn_dangerous_ingredient_other": hx.List(mode="input", default_element_count=4,children={
            "name": hx.Str(mode="input",optionality="optional", default = " ",view={"label": "Name"}),
            "exposed": hx.Bool(mode="input", default=False, optionality="required", view={"label":"Exposed?"}),
            "revenue": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Applicable Revenue","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000000}),
            "notes": hx.Str(mode="input",optionality="optional", default = " ",view={"label": "Notes"}),
        }),

    })
    
    #----------------------------------------------------------------------------------------------#
    # UW Rationale set out in cds root
    #----------------------------------------------------------------------------------------------#
    cds.extend_node_rater_defined("cds", {
        #Finally for the rationale page - slightly different fields to the standard schema fields
        "uw_notes": hx.Str(mode="input", optionality="optional", default=None,async_input=["generate_email_task","generate_referral_email_task"], async_output=[{"task":"roll_exposure_fields_task","reset":False},{"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}, "clear_uw_rationale_task"], view={"label": "Underwriter Notes"}),
        "mid_term_adjustments": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_email_task","generate_referral_email_task"], view={"label": "Mid Term Adjustments"}),
        "historical_comments": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_email_task","generate_referral_email_task"], async_output=[{"task":"roll_exposure_fields_task","reset":False},{"task": "start_renewal_task", "reset": False},{"task": "initialise_model", "reset": False}], view={"label": "Historical Comments"}),
        "file_upload_1": hx.File(mode="input", async_input=["file_upload"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_2": hx.File(mode="input", async_input=["file_upload"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_3": hx.File(mode="input", async_input=["file_upload"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_4": hx.File(mode="input", async_input=["file_upload"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_5": hx.File(mode="input", async_input=["file_upload"], view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        # Email nodes
        "email": hx.Structure(children={
            "rationale_file": hx.File(mode="output", async_output=["generate_email_task","generate_referral_email_task"], file_name="Rationale_Summary.eml", view={"label": "Click to download summary email"}),
            "referral_file": hx.File(mode="output", async_output=["generate_email_task","generate_referral_email_task"], file_name="Referral_Summary.eml", view={"label": "Click to download summary email"}),
            "sender": hx.Str(mode="input", default="your_uw@beazley.com", async_input=["generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], async_output=[{"task": "generate_email_task", "reset": True}, {"task": "generate_referral_email_task", "reset": True}, {"task": "generate_primary_proposal_template_task", "reset": True}, {"task": "generate_excess_proposal_template_task", "reset": True}], view={"label": "Sender"}),
            "recipient": hx.Str(mode="input", default="uw_assistant@beazley.com", async_input=["generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"], async_output=[{"task": "generate_email_task", "reset": True}, {"task": "generate_referral_email_task", "reset": True}, {"task": "generate_primary_proposal_template_task", "reset": True}, {"task": "generate_excess_proposal_template_task", "reset": True}], view={"label": "Recipient"})
        }),
        "primary_proposal_template_file": hx.File(mode="output", async_output=["generate_primary_proposal_template_task"], file_name="Primary_Proposal.eml", view={"label": "Click to download primary proposal template email"}),
        "excess_proposal_template_file": hx.File(mode="output", async_output=["generate_excess_proposal_template_task"], file_name="Excess_Proposal.eml", view={"label": "Click to download excess proposal template email"}),


    })
        # Updates for email async task
    cds.override_node_properties("cds/standard_fields/broker", { "async_input" : ["generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"],"view": {"label": "Brokerage Firm"}})
    cds.override_node_properties("cds/broker_contact", { "async_input" : ["generate_email_task","generate_referral_email_task"]})