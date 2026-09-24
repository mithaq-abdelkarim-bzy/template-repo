import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from algorithms.exposure_calcs import exposure_calcs
from algorithms.discipline_baserate_calcs import discipline_baserate_calcs
from algorithms.project_type_calcs import project_type_calcs

def rate_pricing(hxd):
    exposure_calcs(hxd)
    discipline_baserate_calcs(hxd)
    project_type_calcs(hxd)

