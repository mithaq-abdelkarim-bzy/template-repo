import hx
import datetime
import os
##from mailmerge import MailMerge
import pandas as pd
import polars as pl
from operator import itemgetter, attrgetter
   
# Generate climate change spotlight one-pager from climate tab
def generate_climate_doc(hxd, progress):
    pass


    # template = os.path.join(os.path.dirname(__file__), "climate_litigation_spotlight.docx")
    # document = MailMerge(template)

    # # View available merge fields
    # print(document.get_merge_fields())

    # document.merge(
    #     insured_name = f"{hxd.cds.standard_fields.insured_name}",
    #     insured_jurisdiction = f"{hxd.cds.standard_fields.insured_country}",
    #     insured_sector = f"{hxd.cds.key_industry.code_name}",
    #     cli_appetite = "appetite",
    #     cli_focus = "focus",
    #     cli_tools = "tools"
    # )

    # with hxd.cds.risk_information.climate_document.open("b") as f:
    #     document.write(f)
