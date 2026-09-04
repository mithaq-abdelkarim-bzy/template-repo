import hx
from mailmerge import MailMerge
import pandas as pd
import numpy as np
import datetime

# import hx, pyodbc
# import pandas as pd
# import numpy as np
# import datetime     #use to build date - datetime.date(1990,1,1)
# import algorithms.rate_constants as const
# from dateutil.relativedelta import relativedelta
# from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides



def eso_outputs(hxd):

    cds     = hxd.cds
    eso     = cds.eso
    layers   = cds.layers

    eso.authorising_comments_info = "*Please ensure amount signed off on is explicit including if FAC purchased if not authorised*"
    eso.info = "*Please ensure ESO is uploaded to Underwriting System or W:Drive within 21 days of Bind date/Endorsement bind date to ensure compliance with Control*"


    # Get a list of bound section Refernces
    # section_ref_names = ""
    # for layer in layers: 
    #     if layer.status in ["Bound", "Post Bind Complete"]:
    #         section_ref_names += f" {layer.option_name} : {layer.section_reference},"

    # section_ref_names = section_ref_names[:-1]    
    # eso.section_references = section_ref_names


    eso.options.coverage.label = "Option"
    eso.options.include_option.label = "Inlcude in Totals?"
    eso.label = "All figures are Beazley's Share (Based on QS selected on the Rating Summary Tab)"

    if cds.policy_info.fundamental_top_up_flag:
        eso.term.calculated = f" General Warranties: {cds.rating_factors.sev.general_warranties.term} years from closing; Tax Warranties/Deed: {cds.rating_factors.sev.tax_warranties.term} years from closing; Fundamental: {cds.rating_factors.fun_top_up.term} years from closing"
    else:
        eso.term.calculated = f" General Warranties: {cds.rating_factors.sev.general_warranties.term} years from closing; Tax Warranties/Deed: {cds.rating_factors.sev.tax_warranties.term} years from closing"

    # gets a list of selected sections refrences and adds up prem and exposure
    section_ref_names = ""
    running_prem_total = 0
    running_limit_total = 0

    for idx, layer in enumerate(layers):
        setattr(eso.options.show_hide, f"option_{idx}", True)
        setattr(eso.options.coverage,f"option_{idx}",layer.option_name)
        if getattr(eso.options.include_option, f"option_{idx}"):
            section_ref_names += f" {layer.option_name}: {layer.section_reference}\n"
            running_prem_total += layer.quoted_premium * layer.written_line if (layer.quoted_premium is not None and layer.written_line is not None) else running_prem_total
            running_limit_total += layer.limit * layer.written_line if (layer.limit is not None and layer.written_line is not None) else running_limit_total
            
            

    section_ref_names = section_ref_names.rstrip() #[:-1]     
    eso.section_references = section_ref_names
    eso.premium_total.calculated = running_prem_total
    eso.limit_total.calculated = running_limit_total
    pass

def generate_eso_doc (hxd, progress):
    cds     = hxd.cds
    eso     = cds.eso


    policy_reference =     eso.section_references
    bind_date =            eso.bind_date.strftime("%d %b %Y")                   if eso.bind_date is not None else ""
    premium =              f"{eso.premium_total.selected:,.0f}"                 if eso.premium_total.selected is not None else "" 
    exposure =             f"{eso.exposure_total.selected:,.0f}"                if eso.exposure_total.selected is not None else ""
    term =                 f"{eso.term.selected} \n {eso.additional_term_info}" if eso.additional_term_info is not None else f"{eso.term.selected}"
    over_lining =          eso.over_lining
    cob =                  eso.cob
    authorising_comments = eso.authorising_comments
    approving_uw =         eso.approving_uw
    authorisation_date =   eso.authorisation_date.strftime("%d %b %Y")           if eso.authorisation_date is not None else "" 




    # Set template
    template = "eso_template.docx"
    template_path = f"./model/algorithms/policy_doc_templates/{template}"
    document = MailMerge(template_path)

    document.merge(
        policy_reference = policy_reference
        , bind_date = bind_date
        , premium = premium
        , exposure = exposure
        , term = term
        , over_lining = over_lining
        , cob = cob
        , authorising_comments = authorising_comments
        , approving_uw = approving_uw
        , authorisation_date = authorisation_date
    )

    
    with hxd.cds.eso.document.open("b") as f:
        document.write(f)