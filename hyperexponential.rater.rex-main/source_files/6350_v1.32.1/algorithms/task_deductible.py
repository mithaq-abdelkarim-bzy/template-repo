import hx
from operator import attrgetter
from algorithms.constant import MAX_LAYERS
from algorithms.utilities import generate_layer_location_ded_options

def copy_fire_ded(hxd):
    '''
    Copy fire deductible to other perils
    '''
    for layer in hxd.layers:
        for peril in ["named_windstorm", "scs", "flood", "quake"]:
            peril_structure = attrgetter(f"perils.{peril}")(layer)
            setattr(peril_structure, "per_occurrence_ded", layer.perils.fire.deductible)
        layer.perils.wildfire.deductible = layer.perils.fire.deductible


def named_storm_ws(hxd):
    '''
    Default deductibles for Named Windstorm Only - WS
    '''
    hxd.non_layer_perils.named_windstorm.num_options = 1
    for layer in hxd.layers:
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.region = "All"
        layer.perils.named_windstorm.location_ded.option_1.type = "Percentage uncapped"
    

def all_tier_fl_ws(hxd):
    '''
    Default deductibles for All, Tier and FL - WS
    '''
    hxd.non_layer_perils.named_windstorm.num_options = 3
    for layer in hxd.layers:
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.region = "All"
        layer.perils.named_windstorm.location_ded.option_1.type = "Percentage uncapped"
        layer.perils.named_windstorm.location_ded.option_1.percent = 0.02

        layer.perils.named_windstorm.location_ded.option_2.region_dropdown.region = "Tier"
        layer.perils.named_windstorm.location_ded.option_2.type = "Percentage uncapped"
        layer.perils.named_windstorm.location_ded.option_2.percent = 0.03

        layer.perils.named_windstorm.location_ded.option_3.region_dropdown.region = "State"
        layer.perils.named_windstorm.location_ded.option_3.region_dropdown.state = "FL"
        layer.perils.named_windstorm.location_ded.option_3.type = "Percentage uncapped"
        layer.perils.named_windstorm.location_ded.option_3.percent = 0.05


def fl_ws(hxd):
    '''
    Default deductibles for FL - WS
    '''
    hxd.non_layer_perils.named_windstorm.num_options = 1
    for layer in hxd.layers:
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.region = "State"
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.state = "FL"
        layer.perils.named_windstorm.location_ded.option_1.type = "Percentage uncapped"
        layer.perils.named_windstorm.location_ded.option_1.percent = 0.05


def tx_ws(hxd):
    '''
    Default deductibles for TX - WS
    '''
    hxd.non_layer_perils.named_windstorm.num_options = 1
    for layer in hxd.layers:
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.region = "State"
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.state = "TX"
        layer.perils.named_windstorm.location_ded.option_1.type = "Percentage uncapped"
        layer.perils.named_windstorm.location_ded.option_1.percent = 0.05


def tier_fl_ws(hxd):
    '''
    Default deductibles for Tier, FL - WS
    '''
    hxd.non_layer_perils.named_windstorm.num_options = 2
    for layer in hxd.layers:    
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.region = "Tier"
        layer.perils.named_windstorm.location_ded.option_1.type = "Percentage uncapped"
        layer.perils.named_windstorm.location_ded.option_1.percent = 0.03

        layer.perils.named_windstorm.location_ded.option_2.region_dropdown.region = "State"
        layer.perils.named_windstorm.location_ded.option_2.region_dropdown.state = "FL"
        layer.perils.named_windstorm.location_ded.option_2.type = "Percentage uncapped"
        layer.perils.named_windstorm.location_ded.option_2.percent = 0.05


def all_wind_ws_scs(hxd):
    '''
    Default deductibles for All Wind - WS/ SCS
    '''
    hxd.non_layer_perils.named_windstorm.num_options = 1
    hxd.non_layer_perils.scs.num_options = 1
    for layer in hxd.layers:
        layer.perils.named_windstorm.location_ded.option_1.region_dropdown.region = "All"
        layer.perils.named_windstorm.location_ded.option_1.type = "Percentage uncapped"

        layer.perils.scs.location_ded.option_1.region_dropdown.region = "All"
        layer.perils.scs.location_ded.option_1.type = "Percentage uncapped"


def ca_eq(hxd):
    '''
    Default deductibles for CA - EQ
    '''
    hxd.non_layer_perils.quake.num_options = 1
    for layer in hxd.layers:
        layer.perils.quake.location_ded.option_1.region_dropdown.region = "State"
        layer.perils.quake.location_ded.option_1.region_dropdown.state = "CA"
        layer.perils.quake.location_ded.option_1.type = "Percentage uncapped"
        layer.perils.quake.location_ded.option_1.percent = 0.05


def all_ca_eq(hxd):
    '''
    Default deductibles for All, CA - EQ
    '''
    hxd.non_layer_perils.quake.num_options = 2
    for layer in hxd.layers:
        layer.perils.quake.location_ded.option_1.region_dropdown.region = "All"
        layer.perils.quake.location_ded.option_1.type = "Percentage uncapped"
        layer.perils.quake.location_ded.option_1.percent = 0.02

        layer.perils.quake.location_ded.option_2.region_dropdown.region = "State"
        layer.perils.quake.location_ded.option_2.region_dropdown.state = "CA"
        layer.perils.quake.location_ded.option_2.type = "Percentage uncapped"
        layer.perils.quake.location_ded.option_2.percent = 0.05


def copy_primary_deductibles(hxd):
    if len(hxd.layers) + 1 > MAX_LAYERS:
        hx.errors.fatal("Maximum number of layers reached.")

    try:
        primary_layer = hxd.layers[0]
        data = {
            "reference": primary_layer.reference,
            "limit": primary_layer.limit,
            "excess": primary_layer.excess,
            "achieved_premium_100_gg": primary_layer.achieved_premium_100_gg,
            "brokerage": primary_layer.brokerage,
            "quoted_line_perc":  primary_layer.quoted_line_perc or 0,
            "written_line_perc": primary_layer.written_line_perc or 0,
            "new_renewal": primary_layer.new_renewal,
            "status": primary_layer.status,
            "sim_used": primary_layer.sim_used,
            "elt_for_sim": primary_layer.elt_for_sim,
            "perils": {
                "fire": {
                    "include": primary_layer.perils.fire.include,
                    "deductible": primary_layer.perils.fire.deductible
                },
                "named_windstorm": {
                    "include": primary_layer.perils.named_windstorm.include,
                    "per_occurrence_ded": primary_layer.perils.named_windstorm.per_occurrence_ded,
                    "location_ded": generate_layer_location_ded_options(primary_layer.perils.named_windstorm)
                },
                "scs": {
                    "include": primary_layer.perils.scs.include,
                    "per_occurrence_ded": primary_layer.perils.scs.per_occurrence_ded,
                    "location_ded": generate_layer_location_ded_options(primary_layer.perils.scs)
                },
                "flood": {
                    "include": primary_layer.perils.flood.include,
                    "per_occurrence_ded": primary_layer.perils.flood.per_occurrence_ded,
                    "location_ded": generate_layer_location_ded_options(primary_layer.perils.flood)
                },
                "quake": {
                    "include": primary_layer.perils.quake.include,
                    "per_occurrence_ded": primary_layer.perils.quake.per_occurrence_ded,
                    "ca_quake_include": primary_layer.perils.quake.ca_quake_include,
                    "location_ded": generate_layer_location_ded_options(primary_layer.perils.quake)
                },
                "wildfire": {
                    "include": primary_layer.perils.wildfire.include,
                    "deductible": primary_layer.perils.wildfire.deductible
                },
                "equipment_breakdown": {
                    "include": primary_layer.perils.equipment_breakdown.include
                },
                "tria": {
                    "include": primary_layer.perils.tria.include
                },
                "cyber":{
                    "include": primary_layer.perils.cyber.include,
                    "sublimit" : primary_layer.perils.cyber.sublimit,
                    "deductible": primary_layer.perils.cyber.deductible,
                }
            }
        }
        hxd.layers.append(data)
    except:
        hx.errors.fatal("An error happened when copying.")
