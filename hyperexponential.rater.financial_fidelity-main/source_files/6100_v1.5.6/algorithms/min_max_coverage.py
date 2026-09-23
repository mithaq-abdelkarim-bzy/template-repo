import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import format_f_string

# This rating file sets the minimum and maximum limits / deductible allowed for each coverage. 

# Note
# Most min / max coverages just take the basic bond inputted limit / deductible as their maxiumum although some differ
# the parameter table 'MinMaxCoverage' tells the model what to do via the following number system:
#       9:  basic bond mininum
#       8:  basic bond input coverage / ded
#       7:  Form 15 or basic bond min	
#       6:  None
# if the cell is not one of the above numbers the actual value in that cell is used. 


def min_max_coverage(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages


    # ~~~~~~~~~~~~~~~~~~~~~~~ SET MIN AND MAX COVERAGE ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    form_num = hx.params.InstitutionTypes[hx.params.InstitutionTypes["institution_type"] == hxd.cds.type_of_insured]["form_parent"].iloc[0]
    
    # Pull in the minimum and maxiumum limits / deductibles to use throughout 
    basic_bond_min_coverage = hx.params.BasicBondMinimumCoverage[hx.params.BasicBondMinimumCoverage["Assets"] <= exp_agg.average_assets][hxd.cds.policy_form_used].iloc[-1]
    basic_bond_max_coverage = None
    basic_bond_coverage = cov.cover_1_basic_bond.coverage
    
    basic_bond_min_deductible = 1000  # SA: Hardcoded value in code - again should this be in a central location
    basic_bond_max_deductible = None
    basic_bond_deductible = cov.cover_1_basic_bond.deductible

    # Set table which defines the min / max coverages & deductibles
    min_max_coverage_tbl = hx.params.MinMaxCoverage

    # Loop though each row in the input table, each row is a different cover 
    # SA: small thing but if each row represents a cover, why not name the variable cover instead of row?
    for index, row in min_max_coverage_tbl.iterrows():
        id_cover = row["Cover"]
        id_cover_hxd = getattr(cov, id_cover)

        # Min coverage
        if row['Min Coverage'] == 9:
            min_coverage = basic_bond_min_coverage
        elif row['Min Coverage'] == 8:
            min_coverage = basic_bond_coverage
        elif row['Min Coverage'] == 7:
            if form_num <= 15:
                min_coverage = 2500
            else:
                min_coverage = basic_bond_min_coverage
        else:
            min_coverage = row['Min Coverage']
        setattr(id_cover_hxd, 'min_coverage', min_coverage)

        # Max coverage
        if row['Max Coverage'] == 8:
            max_coverage = basic_bond_coverage
        elif row['Max Coverage'] == 6:
            max_coverage = None
        else:
            pass
        setattr(id_cover_hxd, 'max_coverage', max_coverage)

        # Min deductible
        if row['Min Deductible'] == 8:
            min_deductible = basic_bond_deductible
        elif row['Min Deductible'] == 6:
            min_deductible = None
        else:
            min_deductible = row['Min Deductible']
        setattr(id_cover_hxd, 'min_deductible', min_deductible)

        # Max deductible
        if row['Max Deductible'] == 8:
            max_deductible = basic_bond_deductible
        elif row['Max Deductible'] == 6:
            max_deductible = None
        else:
            max_deductible = row['Max Deductible']
        setattr(id_cover_hxd, 'max_deductible', max_deductible)
        
        pass
    
    # Set info label for each coverage 
    for cv in lst.cover_hxd_vbl(hxd):
        info_min_cov = f"The minimum permissible coverage is {format_f_string(cv.min_coverage)}"

        if cv.max_coverage is None:
            info_max_cov = " "
        else:
            info_max_cov = f" and the maximum is {format_f_string(cv.max_coverage)}"
        
        info_min_ded = f"The minimum permissible deductible is {format_f_string(cv.min_deductible)}"
        
        if cv.max_deductible is None:
            info_max_ded = " "
        else:
            info_max_ded = f" and the maximum is {format_f_string(cv.max_deductible)}"
       
        cv.info = info_min_cov + info_max_cov + "\n \n" + info_min_ded + info_max_ded
        




    


