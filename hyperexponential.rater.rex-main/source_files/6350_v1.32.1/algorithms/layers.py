import hx
from operator import attrgetter
from algorithms.constant import MAX_OPTIONS

def layers_calc(hxd):
    '''
    Function that evaluates layer input values (including perils and deductibles)
    '''
    

    # Evaluate the name of each layer
    for layer in hxd.layers:
        layer.layer_label = f"{amount_to_str(layer.limit)}x{amount_to_str(layer.excess)}"

    # Show/hide deductible section
    for peril in ["fire", "named_windstorm", "scs", "flood", "quake", "wildfire", "equipment_breakdown", "tria", "cyber"]:
        if (peril == "equipment_breakdown" or peril == "tria") and not hxd.policy_information.is_nacp:
            continue
        setattr(getattr(hxd.non_layer_perils, peril), "show_section", any([attrgetter(f"perils.{peril}.include")(layer) for layer in hxd.layers]))

    for index in range(1, MAX_OPTIONS + 1):
        for peril in ["named_windstorm", "scs", "flood", "quake"]:
            peril_structure = attrgetter(f"non_layer_perils.{peril}")(hxd)
            # Show the number of options
            setattr(peril_structure, f"show_option_{index}", index <= (peril_structure.num_options or 0))

            # Show and hide for each option
            show_fields = set()
            for layer in hxd.layers:
                option_structure = attrgetter(f"perils.{peril}.location_ded.option_{index}")(layer)
                if (region := option_structure.region_dropdown.region) in {"State", "Tier", "FEMA Zone"}:
                    show_fields.add(region)
                if (type_ := option_structure.type) in {"Percentage with a $ minimum", "Percentage uncapped", "Percentage capped by $ amount"}:
                    show_fields.add("percent")
                if (type_ := option_structure.type) in {"Percentage with a $ minimum", "Fixed $ amount", "Percentage capped by $ amount"}:
                    show_fields.add("min_max")
            
            setattr(peril_structure, f"show_state_{index}", "State" in show_fields)
            setattr(peril_structure, f"show_tier_{index}", ("Tier" in show_fields or "FEMA Zone" in show_fields))
            setattr(peril_structure, f"show_percent_{index}", "percent" in show_fields)
            setattr(peril_structure, f"show_location_min_max_{index}", "min_max" in show_fields)

    

def amount_to_str(value):
    '''
    Translate a value to abbreviated form with 1 decimal place
    Some example: 
        - value 123.45 -> 123.5
        - value 1,100 -> 1.1K
        - value 21,234,567 -> 21.2M
        - value 7,123,456,789 -> 7.1B
    '''
    value = float(value)
    if value == 0:
        return ".0"
    elif value < 1_000:
        return f"{round(value, 1)}"
    elif value < 1_000_000:
        return f"{round(value/1_000, 1)}K"
    elif value < 1_000_000_000:
        return f"{round(value/1_000_000, 1)}M"
    else:
        return f"{round(value/1_000_000_000, 1)}B"



def map_layers_usd(hxd, df, other_data, perils, perils_structure):
    '''
    Map layers related fields from risk currency to USD
    '''
    exchange_rate = hxd.policy_information.exchange_rate
    for index, layer in enumerate(hxd.layers, start=1):
        # Calculate Limit and Excess in USD
        other_data[f'policy_limit_usd_layer{index}'] = (layer.limit or 0) / exchange_rate if exchange_rate else 0
        other_data[f'policy_excess_usd_layer{index}'] = (layer.excess or 0) / exchange_rate if exchange_rate else 0

        for peril, peril_structure in zip(perils ,perils_structure):
            if peril == "fire" or peril == "wf":
                continue
            
            sublimit_node = getattr(hxd.sublimit, f"{peril}_sublimit")
            other_data[f"{peril}_policy_sublimit_usd_layer{index}"] = (sublimit_node or 0) / exchange_rate if exchange_rate else (sublimit_node or 0)

            for option_num in range(1, MAX_OPTIONS + 1):
                option_structure_node = getattr(getattr(layer.perils, peril_structure).location_ded, f"option_{option_num}")
                other_data[f"{peril}_sublimit_usd_layer{index}_option{option_num}"] = (option_structure_node.sublimit or 0) / exchange_rate if exchange_rate else (option_structure_node.sublimit or 0)

    