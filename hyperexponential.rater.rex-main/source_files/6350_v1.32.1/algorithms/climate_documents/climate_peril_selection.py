import hx

# this is a hardcoded duplicate from data_schema.dropdown_list, due to hx limitations it can't be directly imported in algorithms folder
climate_perils = ["Hurricane", "Flood"]

def climate_peril_selection(hxd):
    ''' 
    Controls which peril section is shown in the Climate page
    '''
    hxd.non_layer_summary.climate_metrics.perils.ws_selected = False
    hxd.non_layer_summary.climate_metrics.perils.fl_selected = False

    if hxd.non_layer_summary.climate_metrics.perils.peril_selection == climate_perils[0]: # Hurricane
        hxd.non_layer_summary.climate_metrics.perils.ws_selected = True
    elif hxd.non_layer_summary.climate_metrics.perils.peril_selection == climate_perils[1]: # Flood
        hxd.non_layer_summary.climate_metrics.perils.fl_selected = True
    return hxd.non_layer_summary.climate_metrics.perils.ws_selected, hxd.non_layer_summary.climate_metrics.perils.fl_selected

        
