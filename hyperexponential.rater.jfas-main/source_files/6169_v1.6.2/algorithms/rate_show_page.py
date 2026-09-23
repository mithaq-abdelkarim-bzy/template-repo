import hx
import pandas as pd
import numpy as np
from operator import itemgetter
from statistics import mean

def rate_show_page(hxd):
    cds = hxd.cds

    cds.show_page.show_risk_information = False
    cds.show_page.show_rate_change = False
    cds.show_page.show_other = False
    cds.show_page.show_jb = False
    cds.show_page.show_fa = False
    cds.show_page.show_cit = False
    cds.show_page.show_gs = False

    if cds.model_state.show_after_landing_page:
        cds.show_page.show_risk_information = True

        if cds.standard_fields.benchmark_class is not None:
            cds.show_page.show_jb = cds.jb_masking
            cds.show_page.show_fa = cds.fa_masking
            cds.show_page.show_cit = cds.cit_masking
            cds.show_page.show_gs = cds.gs_masking
            cds.show_page.show_other = True
            if cds.standard_fields.is_renewal:
                cds.show_page.show_rate_change = True



