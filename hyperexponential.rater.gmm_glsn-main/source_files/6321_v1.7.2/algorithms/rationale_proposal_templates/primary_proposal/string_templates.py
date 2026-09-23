from string import Template

# Templates for the various sections of the email.
# Variables ending in _TEMPLATE are Template objects where we need to substitute values
# Variables ending in _SECTION are hardcoded string sections where we have no substitutions

QUOTE_OPTIONS_TEMPLATE_GMM = Template("""<strong>Option $option_number</strong>

    Premium: $quote_premium

    •	HPL: $hpl
    •	E&O: $eo
    •	GL: $gl
    •	Damage to Rented Premises ($$50,000/$$100,000)
    •	Medical Payments ($$5,000/$$25,000)
    •	EBL: $ebl
    •	PCO: $pco
    •	CT: $ct
    •	SML: $sml

    Overall policy aggregate of $policy_aggregate

""")


QUOTE_OPTIONS_TEMPLATE_GLS = Template("""<strong>Option $option_number</strong>

    Premium: $quote_premium

    •	PCO: $pco
    •	E&O: $eo
    •	HPL: $hpl
    •	Damage to Rented Premises ($$50,000/$$100,000)
    •	Medical Payments ($$5,000/$$25,000)
    •	EBL: $ebl
    •	GL: $gl
    •	SML: $sml
    •	PR: $pr
    •	CT: $ct

    Overall policy aggregate of $policy_aggregate

""")


MINIMUM_EARNED_SECTION = """30%"""


RETROACTIVE_DATES_TEMPLATE_GMM = Template("""HPL: $hpl_retroactive_date

    GL: $gl_retroactive_date

    EBL: $ebl_retroactive_date

    PCO: $pco_retroactive_date

    E&O: $eo_retroactive_date

    CT: $ct_retroactive_date

    SML: $sml_retroactive_date

""")

RETROACTIVE_DATES_TEMPLATE_GLS = Template("""PCO: $pco_retroactive_date

    E&O: $eo_retroactive_date

    HPL: $hpl_retroactive_date

    GL: $gl_retroactive_date

    SML: $sml_retroactive_date

    EBL: $ebl_retroactive_date

    PR: $pr_retroactive_date

    CT: $ct_retroactive_date

""")


ERP_SECTION = """12 months – 150%

    24 months – 175%

    36 months – 200%
"""

COMMENTS_SECTION = """•	For HNOA the sublimit will be limited within the GL, excess any valid and collectible insurance. We would require that the Insured confirm they annually check MVRs and require all drivers to state mandated minimum personal auto insurance.  No coverage for transportation of Clients/Patients. 
 
    •	HELPLINE Only:  Beazley is pleased to offer Risk Management Services via OmniSure at no additional cost to the Insured upon binding.  The Insured would have unlimited access to RiskFit Essentials online programs and HelpLine which provides advice-on-demand from a certified consultant.
    OR

    •	ASSESSMENT (ONLY OVER $100k premium):  Beazley is pleased to offer Risk Management Services via OmniSure at no additional cost to the Insured upon binding.  The Insured would have unlimited access to RiskFit Essentials online programs and HelpLine which provides advice-on-demand from a certified consultant.  There is also a risk assessment included providing the Insured with individualized risk management recommendations following an interactive consultation.  AND

    •	When Mandatory: We would require the risk assessment be conducted by OmniSure within 120 days of binding.
    OR

    •	When Optional:  We would require confirmation of an assessment request at time of binding, along with the complete Risk Manager information as requested in the subjectivities.
    
    •	MANU explanations - please include detailed comment that describes intent for UA to include in order form
    
"""

ENDORSEMENTS_KEY_SECTION = """Endorsements<br><br>
 
    Endt Library:
    <a href='http://bic.beazley.com/applications/endorsementlibrary/default.asp?formPost=Y' target='_blank' style='color:#004A7C;'>MiscMed 2023</a><br><br>

    Endt Log/Mapping:
    <a href='https://beazley.sharepoint.com/:x:/r/sites/USMMLS/Shared Documents/General/MiscMed Mod/MiscMed Mod Endorsement Mapping.xlsx?d=w0be94f0cdddb4211ac026f6d715fc544&csf=1&web=1&e=ydCPl0&xsdata=MDV8MDJ8QWRyaWFuYS5Sb3NjYUBiZWF6bGV5LmNvbXwyZmRlOTRkN2VkMTc0ZDRiZDBlZTA4ZGRkM2Y1ZmVlOHw5YTUwZWJhODc1Njg0NDdhYmNiOTI3YTBkNDY0YWE4MHwwfDB8NjM4ODk5Nzc1Njg0NzI4MTE0fFVua25vd258VFdGcGJHWnNiM2Q4ZXlKRmJYQjBlVTFoY0draU9uUnlkV1VzSWxZaU9pSXdMakF1TURBd01DSXNJbEFpT2lKWGFXNHpNaUlzSWtGT0lqb2lUV0ZwYkNJc0lsZFVJam95ZlE9PXwwfHx8&sdata=WUtlRTIybEJUZWxPMHdsMDBYQ21mNzZUVGRPRU9iMkQzS1MxOHlEYjE0cz0%3d' target='_blank' style='color:#004A7C;'><< OLE Object: Picture (Device Independent Bitmap) >> MiscMed Mod Endorsement Mapping.xlsx</a><br><br>

    Shared Drive:
    <a href='file://bfl.local/us/public/_SL/Healthcare/Healthcare - End - MiscMed Mod (Word Format)' target='_blank' style='color:#004A7C;'>R Drive Folder</a>

"""

ENDORSEMENTS_VALUE_SECTION = """NOT COMPREHENSIVE LIST – Please refer to links on left to confirm if you need MANU
 

    •	Additional Defense Costs Endorsement- Capped by Policy Aggregate Limit of Liability E15655112022 / Scheduled Limit E15656112022
    •	Additional Insured Endorsement - Blanket E15660112022
    •	Additional Insured Endorsement - Blanket with WOS and PNC E15658112022
    •	Additional Insured Endorsement - Scheduled E15998052023
    •	Additional Insured Endorsement - Scheduled With WOS, PNC and NOC E15666112022
    •	Additional Named Insured Endorsement E15668112022
    •	Amend Healthcare Professional Services Definition - Good Samaritan Acts E16181082023
    •	Amend Insured Definition Endorsement - Independent Contractors  E16314122023
    •	Amend Insured Definition Endorsement - Nurse Practitioners and Physician Assistants E15669112022
    •	Amend Sexual & Physical Misconduct Coverage - Healthcare Professional Services Only E16196082023
    •	Arbitration Endorsement E15984042023 (LA, WI, FL, HI, KY, WV, AR, SC, NM, Native American/Alaskan Native Lands)
    •	Beazley MM Risk Management Services: Helpline E15673052023 /Assessment E15672052023
    •	Compounded GLP-1s and GIPs Exclusion E16503032024
    •	Corporal Punishment Exclusion E16224092023
    •	Crisis Management Expense Endorsement $25,000/$50,000 E15675112022
    •	Disciplinary Proceeding Endorsement $25,000/$50,000 E15975042023
    •	Exclusion - Specific Individuals E16625052024
    •	Failure to Complete Background Check Exclusion E16495022024
    •	Foster Family Exclusion with Carveback for Vicarious Liability E15986102023 / Sublimit E16218092023
    •	General Liability Coverage for Healthcare Professional Services Operations Only E16126072023
    •	Healthcare Scheduled Communicable Disease Limitation Endorsement E15678112022
    •	HIPAA Endorsement $25,000/$50,000 E16043062023
    •	HNOA Sublimit $1,000,000/$1,000,000 E15679112022 (GL OCC) / E15680112022 (GL CM)
    •	Individual Insurance Requirement Endorsement - Physicians E16203082023
    •	Insurance Requirement Endorsement - Accident and Health E16597042024 (daycare risks)
    •	Legal Defense Proceeding Endorsement $25,000/$50,000 E15976042023
    •	Maximum Per Claim Limit Endorsement E16335122023
    •	No Timely Informed Consent Exclusion E16230092023
    •	Opioid Exclusion E15686112022 / Individual Plaintiff Carveback E15684112022
    •	Patient Loading and Unloading with Sublimit Endorsement E16317122023
    •	Physical Misconduct Coverage Endorsement E16262112023 (when SafeGuard writes SML)
    •	Scheduled Provider(S) With Retroactive Date(s) And Termination Date(s) E15978042023
    •	Scheduled Location(S) With Retroactive Date(s) And Termination Date(s) E15977042023
    •	Services Exclusion - Field Trips, Overnight Activities, Camps or Retreats E16073062023
    •	Services Exclusion - Foster Care and/ or Adoption Services E16095062023
    •	Services Exclusion - General Anesthesia E15689112022 / Or Conscious Sedation E16448012024
    •	Services Exclusion - Healthcare Professional Services Limitation for Minors E15690112022
    •	Services Exclusion - Laser E16471022024
    •	Services Exclusion - Patient Loading and Unloading E16452012024
    •	Services Exclusion - Residential and/or Overnight Services E16096062023
    •	Services Exclusion - Surgical and Invasive Procedures E15691112022
    •	Services Exclusion - Tracheostomy Ventilator Care E15692112022
    •	Services Exclusion - Ulcer Treatment E16231092023
    •	Specified Educational Services Exclusion E16140072023
    •	MANU – if it is copying MM Suite endt please reference old endt number for UA/Wordings

"""

SUBJECTIVITIES_SECTION = """1.	Application needs to be fully completed/signed/dated. Please include detailed breakout of projected exposures
    2.	Currently valued five year loss runs, any new claims will impact terms.
    3.	Current audited financial statements
    4.	Please provide details on recruitment and credentialing practices
    5.	Completed, signed and dated TRIA form
    6.	Please confirm the Insured's risk management contact name, email address, and phone number prior to bind to ensure delivery of the free OmniSure consulting services offered.

"""
