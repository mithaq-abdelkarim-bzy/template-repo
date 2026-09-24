import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
import unicodedata

def project_type_calcs(hxd):
    
    # PROJECT TYPE SECTION ##############################################################
        
    # Category loadings table
    param_category_table = hx.params.tbl_category_type

    mapping = {
        "target": hxd.cds.exposure.aggregate.project_type_category.cat_type_target,
        "average": hxd.cds.exposure.aggregate.project_type_category.cat_type_average,
        "expensive": hxd.cds.exposure.aggregate.project_type_category.cat_type_expensive,
        "refer": hxd.cds.exposure.aggregate.project_type_category.cat_type_refer,
        "decline": hxd.cds.exposure.aggregate.project_type_category.cat_type_decline,
    }

    for _, row in param_category_table.iterrows():
        key = row["category"].strip().lower()
        if key in mapping:
            mapping[key].code = row["code"]
            if key != "decline":
                mapping[key].category_factor = row["factor"]

    # Look up index and code based on Project Type Name
    def norm(s: str) -> str:
        s = s or ""
        s = unicodedata.normalize("NFKC", s)
        s = s.replace("\xa0", " ")        
        s = s.strip()
        s = " ".join(s.split())           
        return s.casefold()               

    pt = hx.params.tbl_project_type.copy()

    def pick(df, *cands):
        for c in cands:
            if c in df.columns:
                return c
        raise KeyError(f"None of {cands} found in parameter table columns: {list(df.columns)}")

    name_col = pick(pt, "Project Type", "project_type", "Project Type Name")
    idx_col  = pick(pt, "Index", "index")
    code_col = pick(pt, "E&O", "code", "Code")

    pt[name_col] = pt[name_col].astype(str).map(norm)
    pt[idx_col]  = pd.to_numeric(pt[idx_col], errors="coerce")
    pt[code_col] = pd.to_numeric(pt[code_col], errors="coerce")

    name_to_index = pt.set_index(name_col)[idx_col].to_dict()
    name_to_code  = pt.set_index(name_col)[code_col].to_dict()

    for row in hxd.cds.exposure.granular.project_type:
        key = norm(row.project_type_name)
        row.project_type_index = name_to_index.get(key)
        row.code_e_o           = name_to_code.get(key)


    # Calculate proportional loading
    #   1. Sum the % fees by category code using the granular table
    #   2. Multiply Factor and % Fees by each category code
    #   3. Sum proportional loading of the whole table (cats 1-4)

    project_df = utils.pd_df_from_hx_list(hxd.cds.exposure.granular.project_type)

    project_category = hxd.cds.exposure.aggregate.project_type_category

    # Initialising totals to zero to avoid NoneType errors
    project_category.cat_type_total.fee_percentage = 0
    project_category.cat_type_total.proportional_loading = 0
 
    for i, code in enumerate(["target", "average", "expensive", "refer", "decline"], start=1):
        category = getattr(project_category, f"cat_type_{code}")
        category.fee_percentage = project_df.loc[project_df["code_e_o"] == i, "fee_percentage"].sum()

        if code != "decline":
            category.proportional_loading = category.fee_percentage * category.category_factor
            project_category.cat_type_total.proportional_loading += category.proportional_loading or 0
        
        project_category.cat_type_total.fee_percentage += category.fee_percentage or 0