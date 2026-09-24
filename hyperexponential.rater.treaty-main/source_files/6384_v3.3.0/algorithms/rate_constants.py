import hx
from hx import params as hx_params
# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 20

max_curves = 30

benchmark_lr = 0.7

max_exposure_years = 50

peril_reference = hx_params.table_peril_name["peril_reference"]
peril_label = hx_params.table_peril_name["peril_label"]
return_periods = hx_params.table_return_periods["return_period"]

##TODO
sims = 50000

rp_peril_options = ["Curve Agg", "RMS AP", "RMS EQ", "RMS WS", "RMS SCS", "AIR AP", "AIR EQ", "AIR WS",  "AIR SCS", "AIR WF", "AIR Winter"]