import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils
from hx import params as hx_params
import pandas as pd

all_area_codes = pd.concat([hx_params.table_area_code_can_car, hx_params.table_area_code_europe, hx_params.table_area_code_far_east_amei, hx_params.table_area_code_us_aus], axis = 0)
us_rds_regions = hx_params.table_rds_regions_all

non_us_area_codes = all_area_codes[~all_area_codes["field"].isin(us_rds_regions["area_code"])]
us_area_codes = all_area_codes[all_area_codes["field"].isin(us_rds_regions["area_code"])]

def sch_additional_pages(cds):
    cds.extend_node_rater_defined('cds', {
    ## Populate Policy
    "populate_model": hx.Structure(children={
        "policy_option_id": hx.Str(mode="input", default=None, optionality="optional", async_input = ["populate_model_task"], view={"label": "Policy Option ID"}),
    }),
    ## Rationale
    "rationale": hx.Structure(children={
        "knowledge_comments": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task", "send_eso_task"], view={"label": "Knowledge of the reinsured"}),
        "portfolio_comments": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task", "send_eso_task"], view={"label": "Portfolio Fit"}),
        "basis_comments": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task", "send_eso_task"], view={"label": "Basis of risk selection"}),
        "unusual_comments": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task", "send_eso_task"], view={"label": "Any unusual or complex considerations"}),
        "facts_comments": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task", "send_eso_task"], view={"label": "Facts which affect the underwriter's decision"})
    }),
    ## Pre Bind
    "pre_bind": hx.Structure(children={
        "question": hx.Structure(view={"label": "Question"}, children={
            "q_1": hx.Str(mode="input", default = "Does there exist, attached to the risk at time of bind, a contract or wording on which we can base a judgement of a claim?", optionality="optional", view = {"label": "Q 1.", "read_only": True}),
            "q_2": hx.Str(mode="input", default = "Are the key parties (insured, reinsured) identified on the slip, including corporate contact information?", optionality="optional", view = {"label": "Q 2.", "read_only": True}),
            "q_3": hx.Str(mode="input", default = "Are the key components of the contract clearly identified, including : class of insurance, period of coverage, limits of cover provided, territorial limits and choice of law & jurisdiction.", optionality="optional", view = {"label": "Q 3.", "read_only": True}),
            "q_4": hx.Str(mode="input", default = "Are we licensed to do this class / type of business in the jurisdiction(s) stated in the contract?", optionality="optional", view = {"label": "Q 4.", "read_only": True}),
            "q_5": hx.Str(mode="input", default = "Does the contract / wording meet any specific regulatory requirements for the jurisdiction / type of business.", optionality="optional", view = {"label": "Q 5.", "read_only": True}),
            "q_6": hx.Str(mode="input", default = "Have you confirmed that the contract is not in breach of any requirements or prohibitions on economic, trade and financial sanctions?", optionality="optional", view = {"label": "Q 6.", "read_only": True}),
            "q_7": hx.Str(mode="input", default = "Have you confirmed that all appropriate taxes and responsibility for paying them is detailed in the contract or wording?", optionality="optional", view = {"label": "Q 7.", "read_only": True}),
        }),
        "answer": hx.Structure(view={"label": "Answer"}, children={
            "q_1": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_2": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_3": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_4": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_5": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_6": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_7": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
        }),
        "uw_signature": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Underwriter Signature"}),
        "date": hx.Date(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Date (Must be pre-bind or on day of binding the contract):"}),
     }),
    ## Post Bind
    "post_bind": hx.Structure(children={
        "question": hx.Structure(view={"label": "Question"}, children={
            # APPLICABLE TO ALL SLIP HEADINGS WITHIN THIS SLIP SECTION:
            "q_1": hx.Str(mode="input", default="Have the wordings and all clauses been attached / referenced in the slip?", optionality="optional", view = {"read_only": True}),
            "q_2": hx.Str(mode="input", default = """Where a wording is dependent on another wording (for example, "as expiring" or "as original"), is the latter either attached or identified?""", optionality="optional", view = {"read_only": True}),
            "q_3": hx.Str(mode="input", default = """Are all broker/insurer arrangements stated?""", optionality="optional", view = {"read_only": True}),
            # APPLICABLE TO WHOLE SLIP:
            "q_4": hx.Str(mode="input", default = """Are all currencies referenced e.g. via use of three letter ISO currency codes?""", optionality="optional", view = {"read_only": True}),
            "q_5": hx.Str(mode="input", default = """Are all provisions relevant to the risk and its administration to ensure that the contract is clear and unambiguous?""", optionality="optional", view = {"read_only": True}),
            "q_6": hx.Str(mode="input", default = """Ensure that there are no terms to be agreed (TBAs) or other terms remaining undefined.""", optionality="optional", view = {"read_only": True}),
            # CONDITIONS
            "q_7": hx.Str(mode="input", default = """Where the perils of radioactive contamination and/or nuclear incident are considered to be relevant to the scope of coverage, and it is the intention not to cover them, check that an appropriate exclusion clause has been included. """, optionality="optional", view = {"read_only": True}),
            "q_8": hx.Str(mode="input", default = """Some clauses and wordings contain set deductibles and limits. Where this is the case ensure that the currency is consistent with the rest of the contract.""", optionality="optional", view = {"read_only": True}),
            # SUBJECTIVITIES
            "q_9": hx.Str(mode="input", default = """Are any subjectivities clearly expressed; i.e. do they set out all of: 1) the condition/action that needs to occur, by whom and to what standard, 2) the applicable timescale, if any, within which the condition is to be met, 3) the terms which are to apply until the condition is met and 4) any consequences which follow if the condition is not met?""", optionality="optional", view = {"read_only": True}),
            # CHOICE OF LAW & JURISDICTION/CONDITIONS: 
            "q_10": hx.Str(mode="input", default = """Where the "Service of Suit" or similar clause is referenced on the submission is the nominee also stated?""", optionality="optional", view = {"read_only": True}),
            # PREMIUM
            "q_11": hx.Str(mode="input", default = """Is the premium or rate expressed?""", optionality="optional", view = {"read_only": True}),
            "q_12": hx.Str(mode="input", default = """Are any payment terms identified?""", optionality="optional", view = {"read_only": True}),
            # INSURER CONTRACT DOCUMENTATION: 
            "q_13": hx.Str(mode="input", default = """Does the slip state the type of insurer contract documentation to be produced, by whom it is to be produced and any particular requirements e.g. any requirement for an insurer approved policy? Has consideration been given to contract change documentation?""", optionality="optional", view = {"read_only": True}),
            # INFORMATION
            "q_14": hx.Str(mode="input", default = """Is the information provided by the insured referenced in the placing documents?""", optionality="optional", view = {"read_only": True}),
            # (RE)INSURER'S LIABILITY:
            "q_15": hx.Str(mode="input", default = """All open market policies (including MRC slips) must include a suitable several liability/signing clause that establishes the several liability of each underwriting member subscribing to the risk from every other member and of any insurance company.  That clause will ordinarily be in the terms of LMA 3333 (or in respect of a line slip declaration in the terms of LMA 5123).""", optionality="optional", view = {"read_only": True}),
            # SIGNING PROVISIONS: 
            "q_16": hx.Str(mode="input", default = """If there is more than one participating insurer check that a signing provisions clause is included.""", optionality="optional", view = {"read_only": True}),
            # INSURER'S WRITTEN LINE:  
            "q_17": hx.Str(mode="input", default = """Wherever possible, line conditions should be shown under the most appropriate contract section and heading. Stamp conditions should be removed and recorded elsewhere in the contract, where there is provision to do so. Ensure that any such conditions applied by an insurer are relevant to the administration of the risk, and are clearly and fully expressed.""", optionality="optional", view = {"read_only": True}),
            # SLIP LEADER: 
            "q_18": hx.Str(mode="input", default = """Is the leader identified?""", optionality="optional", view = {"read_only": True}),
            # CONTRACT CHANGES
            "q_19": hx.Str(mode="input", default = """Is the basis of agreement to contract changes identified?""", optionality="optional", view = {"read_only": True}),
            "q_20": hx.Str(mode="input", default = """OTHER AGREEMENT PARTIES FOR CONTRACT CHANGES, FOR PART 2 GUA CHANGES ONLY: Where GUA applies to the contract, ensure that this heading is present and that either details of any other parties for part 2 of GUA are identified or it is clear that such changes will be agreed by the slip leader only.""", optionality="optional", view = {"read_only": True}),
            "q_21": hx.Str(mode="input", default = """AGREEMENT PARTIES FOR CONTRACT CHANGES, FOR THEIR PROPORTION ONLY: Are details of parties who will agree contract changes for their own proportion (if any) clearly identified?""", optionality="optional", view = {"read_only": True}),
            # CLAIMS
            "q_22": hx.Str(mode="input", default = """Is the Basis of Claims Agreement clearly identified?  For contracts with more than one participating Lloyd's Syndicate this is the Lloyd's 2006 Claims Scheme. [Please note that for certain classes the Lloyd's 2006 Claims Scheme has been amended by the 2010 Pilot Scheme - the scope of this pilot and the applicable slip language relating to this heading are set out in Market Bulletin Y4341 dated 30 November 2009]""", optionality="optional"),
            "q_23": hx.Str(mode="input", default = """Are the claims agreement parties identified?  For contracts with more than one participating Lloyd's Syndicate, within the scope of the Lloyd's 2006 Claims Scheme, these are the leading Lloyd's underwriter and XCS, not XIS, (although a second Lloyd's underwriter may opt to be an additional agreement party only on "Special Category claims" and this must be stated as such on the contract) only. [Please note that for certain classes the Lloyd's 2006 Claims Scheme has been amended by the 2010 Pilot Scheme - the scope of this pilot, the applicable slip language relating to this heading, and the requirement to identify which managing agent(s) will fulfil the claims agreement party roles, are set out in Market Bulletin Y4341 dated 30 November 2009]""", optionality="optional", view = {"read_only": True}),
            "q_24": hx.Str(mode="input", default = """Is the basis of claims administration specified?""", optionality="optional", view = {"read_only": True}),
            # RULES AND EXTENT OF ANY OTHER DELEGATED CLAIMS AUTHORITY: 
            "q_25": hx.Str(mode="input", default = """Are the rules and extent of any other delegated claims authority specified?""", optionality="optional", view = {"read_only": True}),
            # EXPERT(S) FEES COLLECTION: 
            "q_26": hx.Str(mode="input", default = """Are arrangements for collection of expert fees stated?""", optionality="optional", view = {"read_only": True}),
            # OVERSEAS BROKER: 
            "q_27": hx.Str(mode="input", default = """Any business placed via a Canadian domiciled intermediary (either open market or delegated authority) will cause the risk to be "insure in Canada a risk" even if it does not cover a Canadian insured or Canadian location. The Canadian domiciled intermediary will need to be an approved Open Market Correspondent or Coverholder. Ensure premium monies are converted into either CAD or USD prior to submission for processing and settlement, and that the contract of insurance (including premium notices and applications for insurance) includes the "made in Canada" wording. Please refer to market bulletin Y4329 and Crystal for further information """, optionality="optional", view = {"read_only": True}),
            # US CLASSIFICATION: 
            "q_28": hx.Str(mode="input", default = """Ensure that the contract shows the correct US classification if the original premium is in US Dollars or the original premium is in another currency and the Country of Origin is the US.""", optionality="optional", view = {"read_only": True}),
            # CLIENT CLASSIFICATION: 
            "q_29": hx.Str(mode="input", default = """Ensure that the Market Reform Contract includes the Regulatory Client Classification heading in the Fiscal and Regulatory section and check that one of the six available options is stated: Consumer, Consumer exempt, Commercial customer, Large risk, Group risks or Reinsurance.""", optionality="optional", view = {"read_only": True}),
            # DISTANCE MARKETING DIRECTIVE: 
            "q_30": hx.Str(mode="input", default = """Where the FSA Client Classification heading shows "Consumer" or "Consumer exempt", ensure that the Distance Marketing Directive heading is included on the Market Reform Contract (Fiscal and Regulatory section) and is completed either 'yes' or 'no'.""", optionality="optional", view = {"read_only": True}),
            # DEDUCTIONS
            "q_31": hx.Str(mode="input", default = """Is the brokerage expressed?""", optionality="optional", view = {"read_only": True}),
            "q_32": hx.Str(mode="input", default = """Are other deductions from premium expressed?""", optionality="optional", view = {"read_only": True}),
            # SYNDICATE SPLIT
            "q_33": hx.Str(mode="input", default = """Does the stamp or contract accurately reflect the correct syndicate split?""", optionality="optional", view = {"read_only": True}),
            # Regulatory Risk Location
            "q_34": hx.Str(mode="input", default = """Have you confirmed that a section on the regulatory risk location appears in the contract and that it has been completely corrected?""", optionality="optional", view = {"read_only": True}),
        }),
        "answer": hx.Structure(view={"label": "Answer"}, children={
            "q_1": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_2": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_3": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_4": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_5": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_6": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_7": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_8": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_9": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_10": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_11": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_12": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_13": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_14": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_15": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_16": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_17": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_18": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_19": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_20": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_21": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_22": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_23": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_24": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_25": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_26": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_27": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_28": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_29": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_30": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_31": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_32": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_33": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"}),
            "q_34": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No", "N/A"], async_input = ["synergy_send_rate_change_task"], view={"label": "Answer"})
        }),
        "comments": hx.Structure(view={"label": "Comments"}, children={
            "q_1": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_2": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_3": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_4": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_5": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_6": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_7": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_8": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_9": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_10": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_11": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_12": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_13": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_14": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_15": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_16": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_17": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_18": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_19": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_20": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_21": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_22": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_23": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_24": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_25": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_26": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_27": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_28": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_29": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_30": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_31": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_32": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_33": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], view={"label": "Comments"}),
            "q_34": hx.Str(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], options=["Yes", "No", "N/A"], view={"label": "Answer"})
        }),
     }),
    ## Area Code
    "blank_label": hx.Str(mode="input", default=None, optionality = "optional"),    
    "area_code_label": hx.Str(mode="input", default="Area Code", optionality = "optional"),
    "area_code_comments": hx.Str(mode="input", default=None, optionality = "optional"),
    "area_codes_select": hx.Structure(children={
        **{f"{field}": hx.Str(mode="input", default=f"{code}", optionality="optional", view={"label": f"{name}", "read_only": True}) 
            for field, code, name in zip(all_area_codes["field"], all_area_codes["code"], all_area_codes["name"])
        },
    }),
    ## Send Rate Change
    "send_rate_change": hx.Structure(children={
        "peril_allocation_run": hx.Bool(mode="input", default=False, view = {"label": "Peril Allocation Run?", "read_only": True}),
        "confirm_area_codes": hx.Bool(mode="input", default=False, view = {"label": "Confirm Area Codes"}),
        "confirm_rms_el_allocation": hx.Bool(mode="input", default=False, view = {"label": "Confirm RMS EL Allocation"}),
        "confirm_rate_change": hx.Bool(mode="input", default=False, view = {"label": "Confirm Rate Change"}),
        "total_error_count": hx.Float(mode="output"),

        "message": hx.Str(mode="input", default="""Once all validation errors have been fixed (top right exclamation mark), 'Send Rate Change' task will appear.""", optionality = "optional", view={"read_only": True}),
        "show_send_rate_change": hx.Bool(mode="output"),        
    }),
    ## ESO
    "eso_template": hx.Structure(children={
        "email_recipients": hx.Str(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view={"label": "Email Recipients - separate with semicolon"}),

        "team": hx.Str(mode="input", default="Treaty", optionality="optional", async_input = ["send_eso_task"], view = {"label": "Team", "read_only": True}),
        "cob_code": hx.Str(mode="input", default=None, optionality="optional", options_table="table_cob_list", options_column="cob", async_input = ["send_eso_task"], view = {"label": "COB Code"}),

        "authorising_uw": hx.Str(mode="input", default= None, optionality="optional", options_table="table_input_underwriters", options_column="underwriter", async_input = ["send_eso_task"], view = {"label": "Authorising Underwriter"}),
        "date_of_authorisation": hx.Date(mode="input", default = None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "Date of Authorisation Request"}),

        "requested": hx.Structure(view={"label": "Requested"}, children={
            "request_note": hx.Str(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "NB", "style_cell": "hx-input"}),
            "loa_premium": hx.Float(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Premium (Bzly Share)", "format": utils.thousands_format(0)}),
            "loa_exposure": hx.Float(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Exposure (Bzly Share)", "format": utils.thousands_format(0)}),
            "loa_term": hx.Float(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Policy Term", "format": utils.thousands_format(0)}),
            "loa_exposure_stacking": hx.Float(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Exposure (Stacking)", "format": utils.thousands_format(0)}),
            "unauthorised_cob_mop": hx.Str(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "Unauthorised COB or MOP"})
        }),
        "uw_authority": hx.Structure(view={"label": "UW Authority"}, children={
            "loa_premium": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Premium (Bzly Share)", "format": utils.thousands_format(0)}),
            "loa_exposure": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Exposure (Bzly Share)", "format": utils.thousands_format(0)}),
            "loa_term": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Policy Term", "format": utils.thousands_format(0)}),
            "loa_exposure_stacking": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Exposure (Stacking)", "format": utils.thousands_format(0)})
        }),
        "authorising_uw_authority": hx.Structure(view={"label": "Authorising UW Authority"}, children={
            "loa_premium": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Premium (Bzly Share)", "format": utils.thousands_format(0)}),
            "loa_exposure": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Exposure (Bzly Share)", "format": utils.thousands_format(0)}),
            "loa_term": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Policy Term", "format": utils.thousands_format(0)}),
            "loa_exposure_stacking": hx.Float(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "LOA - Exposure (Stacking)", "format": utils.thousands_format(0)}),
            "authority_as_at": hx.Date(mode="output", optionality="optional", async_input = ["send_eso_task"], view = {"label": "Central Authority Last Update"})
        }),

        "rag_level": hx.Str(mode="input", default=None, optionality="optional", options = ["Red", "Amber", "Green"], async_input = ["send_eso_task"], view = {"label": "RAG Level"}),
        "rag_triggers": hx.Str(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "RAG Triggers"}),

        "commentary": hx.Str(mode="input", default=None, optionality="optional", async_input = ["send_eso_task"], view = {"label": "Commentary"}),

    })


    })

    cds.extend_node_rater_defined("cds/layers",
     { 
        "area_code_x_eu_ws": hx.Bool(mode="input", default=False, view = {"label": "EU EX WS?"}),
        "area_codes_select": hx.Structure(children={
            **{f"{field}": hx.Bool(mode="input", default=False, async_input = ["synergy_send_rate_change_task"], view={"label": f"{name}"}) 
                for field, code, name in zip(non_us_area_codes["field"], non_us_area_codes["code"], non_us_area_codes["name"])
            },
            **{f"{field}": hx.Str(mode="output", optionality = "optional", async_input = ["synergy_send_rate_change_task"], view={"label": f"{name}"}) 
                for field, code, name in zip(us_area_codes["field"], us_area_codes["code"], us_area_codes["name"])
            },
        }),
        "area_codes_perc": hx.Structure(children={
            **{f"{field}": hx.Float(mode="input", default=None, optionality="optional", async_input = ["synergy_send_rate_change_task"], validation={"min_value": 0, "max_value": 1}, view={"label": f"{name}", "format": utils.percent_format(1)}) 
                for field, code, name in zip(all_area_codes["field"], all_area_codes["code"], all_area_codes["name"])
            },
        }),
        "area_codes_summary": hx.Structure(children={
            "europe": hx.Float(mode="output", optionality="optional", view={"label": "Northern Europe, Southern Europe and CEE", "format": utils.percent_format(1)}),
            "us_aus": hx.Float(mode="output", optionality="optional", view={"label": "US, Latin America and Australia", "format": utils.percent_format(1)}),
            "can_car": hx.Float(mode="output", optionality="optional", view={"label": "Caribbean and Canada", "format": utils.percent_format(1)}),
            "far_east_amei": hx.Float(mode="output", optionality="optional", view={"label": "Far East and AMEI", "format": utils.percent_format(1)}),
            "total": hx.Float(mode="output", optionality="optional", view={"label": "Total", "format": utils.percent_format(1)}),
        }),
     })


    