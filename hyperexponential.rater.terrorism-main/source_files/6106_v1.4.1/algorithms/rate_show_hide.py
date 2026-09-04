

import hx
import pandas as pd
import numpy as np

def rate_show_hide(hxd):
    cds = hxd.cds

    cds.show_hide.page.show_actuarial               = False

    if (cds.rationale.actuarial_review in {'Yes'}):                         cds.show_hide.page.show_actuarial       = True

