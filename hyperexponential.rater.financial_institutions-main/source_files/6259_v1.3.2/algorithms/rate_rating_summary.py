import math
from datetime import datetime, timedelta
from copy import deepcopy

import hx
import numpy as np

from algorithms import calcs_helper, parameter_tables_schema
from algorithms import rate_constants as constants
from algorithms.rate_risk_information import get_coverage_matrix, get_industry_matrix
from algorithms.rate_utilities import get_layer_labels, ordered_uniquify, ratio, str_isblank


def poisson_distribution(k, lambda_):
    return (
        1
        if k == 0 and lambda_ == 0
        else (lambda_**k * math.exp(-lambda_)) / math.factorial(k)
    )


def ilf(y, x, power):
    if y == 0:
        y = 0.01  # protect against missing retention and excess
    alpha = np.log(power) / np.log(2)
    l = 1000000
    r = 100000
    k = x / y
    k0 = l / r
    k1 = y / r

    ilf_value = k1**alpha * ((1 + k) ** alpha - 1) / ((1 + k0) ** alpha - 1)

    return ilf_value


def calculate_ilf_factor(
    sir_by_coverage,
    layer_coverages,
    limits_by_coverage,
    is_coverage_type_included,
    is_primary,
):
    # Calculate ilf curve
    ilf_factor_by_coverage = {
        "crime": {"manager": 0, "fund": 0},
        "pi": {"manager": 0, "fund": 0},
        "A": {"manager": 0, "fund": 0},
        "B": {"manager": 0, "fund": 0},
        "C": {"manager": 0, "fund": 0},
        "Dic": {"manager": 0, "fund": 0},
    }

    for coverage in layer_coverages:
        for coverage_type in ["manager", "fund"]:
            if coverage in ["crime", "pi"]:
                if not is_coverage_type_included[coverage][coverage_type]:
                    continue
            elif not is_coverage_type_included["do"][coverage_type]:
                continue
            sir = (
                0
                if (coverage == "A" or coverage == "do") and is_primary
                else sir_by_coverage[coverage][coverage_type]
            )
            ilf_x = max(25000, sir)
            ilf_y = limits_by_coverage[coverage][coverage_type]
            power = constants.selected_ilf_factor[coverage]["power_ilf"]
            ilf_factor = ilf(ilf_x, ilf_y, power)
            ilf_factor_by_coverage[coverage][coverage_type] = ilf_factor

    return ilf_factor_by_coverage


def calculate_reinstatement_factor_by_coverage(
    is_direct,
    reinstatement_factor,
    reinstatement_by_coverage,
    limits_by_coverage,
    sir_by_coverage,
):
    reinstatement_factor_by_coverage = {
        "crime": {"manager": 1, "fund": 1},
        "pi": {"manager": 1, "fund": 1},
        "A": {"manager": 1, "fund": 1},
        "B": {"manager": 1, "fund": 1},
        "C": {"manager": 1, "fund": 1},
        "Dic": {"manager": 1, "fund": 1},
    }
    if is_direct:
        for key, value in reinstatement_by_coverage.items():
            for coverage_type in ["manager", "fund"]:
                reinstatement_factor_by_coverage[key][coverage_type] = (
                    1 + reinstatement_factor
                ) ** (value or 0)
    else:
        for key, value in reinstatement_by_coverage.items():
            if (value is None) or (value == 0):
                continue
            for coverage_type in ["manager", "fund"]:
                a = limits_by_coverage[key][coverage_type] / value
                b = sir_by_coverage[key][coverage_type] / (value / 2)
                c = reinstatement_factor
                reinstatement_factor_by_coverage[key][coverage_type] = ((a + b) * c) + 1
    return reinstatement_factor_by_coverage


def calculate_values(idx, hxd, layer, base_rate_by_coverage, primaries):
    industry = hxd.cds.key_industry.code_name.lower() if hxd.cds.key_industry.code_name else None
    if not industry:
        return 

    global_params = calcs_helper.global_parameters(hxd)
    fixed_exp_live_cover = global_params["fx_live_cover"]     

    base_rate_by_coverage = deepcopy(base_rate_by_coverage)

    is_primary = layer.label == "Primary"

    #JC added 14/4/2026: To ensure the coverage change on primary layer impacts benchmark price
    primary_has_coverage_override = False
    primary_has_excess_override = False
    if is_primary:
        for tower_idx in range(1, constants.max_towers + 1):
            tower = getattr(layer, f"tower_{tower_idx}")
            if tower.coverage.is_overridden:
                primary_has_coverage_override = True
            if tower.excess.selected:
                primary_has_excess_override = True

    use_primary_defaults = is_primary and not primary_has_coverage_override

    #if is_primary: 
    #JC updated 14/4/2026: To ensure the coverage change on primary layer impacts benchmark price
    if use_primary_defaults:
        # Have to calculate these intermediate steps to calculate the primary values, so just fetch them from the primaries           
        layer_coverages = deepcopy(primaries["layer_coverages"])  
        is_coverage_type_included = deepcopy(primaries["is_coverage_type_included"])  
        towers_by_fund_manager = deepcopy(primaries["towers_by_fund_manager"])  
        coverage_by_tower = deepcopy(primaries["coverage_by_tower"])  
    else:
        layer_coverages = []
        is_coverage_type_included = constants.coverage_type_included_dict()
        towers_by_fund_manager = constants.towers_by_fund_manager_dict() 
        coverage_by_tower = constants.tower_dict()


        primary_layer = hxd.cds.rating_factors.cover_details.primary_layer

        if primary_layer.towers_all_manager.crime != "NA":
            is_coverage_type_included["crime"]["manager"] = True
            towers_by_fund_manager["manager"].append(primary_layer.towers_all_manager.crime.replace(" ", "_").lower())                
        else:
            base_rate_by_coverage["crime"]["manager"] = 0

        if primary_layer.towers_fund.crime != "NA":
            towers_by_fund_manager["fund"].append(primary_layer.towers_fund.crime.replace(" ", "_").lower())
            is_coverage_type_included["crime"]["fund"] = True
        else:
            base_rate_by_coverage["crime"]["fund"] = 0

        if primary_layer.towers_all_manager.pi != "NA":                
            towers_by_fund_manager["manager"].append(primary_layer.towers_all_manager.pi.replace(" ", "_").lower())                
            is_coverage_type_included["pi"]["manager"] = True
        else:
            base_rate_by_coverage["pi"]["manager"] = 0

        if primary_layer.towers_fund.pi != "NA":
            towers_by_fund_manager["fund"].append(primary_layer.towers_fund.pi.replace(" ", "_").lower())
            is_coverage_type_included["pi"]["fund"] = True
        else:
            base_rate_by_coverage["pi"]["fund"] = 0

        if primary_layer.towers_all_manager.do != "NA":
            if primary_layer.do_type:
                towers_by_fund_manager["manager"].append(primary_layer.towers_all_manager.do.replace(" ", "_").lower())                       
                is_coverage_type_included["do"]["manager"] = True
            else:
                base_rate_by_coverage["A"]["manager"] = 0
                base_rate_by_coverage["B"]["manager"] = 0
                base_rate_by_coverage["C"]["manager"] = 0
                base_rate_by_coverage["Dic"]["manager"] = 0
        else:
            base_rate_by_coverage["A"]["manager"] = 0
            base_rate_by_coverage["B"]["manager"] = 0
            base_rate_by_coverage["C"]["manager"] = 0
            base_rate_by_coverage["Dic"]["manager"] = 0

        if primary_layer.towers_fund.do != "NA":
            if primary_layer.do_type:
                towers_by_fund_manager["fund"].append(primary_layer.towers_fund.do.replace(" ", "_").lower())
                is_coverage_type_included["do"]["fund"] = True            
            else:
                base_rate_by_coverage["A"]["fund"] = 0
                base_rate_by_coverage["B"]["fund"] = 0
                base_rate_by_coverage["C"]["fund"] = 0
                base_rate_by_coverage["Dic"]["fund"] = 0
        else:
            base_rate_by_coverage["A"]["fund"] = 0
            base_rate_by_coverage["B"]["fund"] = 0
            base_rate_by_coverage["C"]["fund"] = 0
            base_rate_by_coverage["Dic"]["fund"] = 0

        # Towers
        for i in range(1, constants.max_towers + 1):
            tower_show = getattr(hxd.non_cds.cover_details, f"tower_{i}_show")
            if tower_show:
                tower = getattr(layer, f"tower_{i}")
                coverage = tower.coverage.selected
                if not coverage:
                    continue
                tower_coverages = constants.coverage_switch.get(coverage, [])
                coverage_by_tower[f"tower_{i}"] = tower_coverages
                layer_coverages = layer_coverages + tower_coverages


    if use_primary_defaults and not any([getattr(layer, f"tower_{i}").excess.selected for i in range(1, constants.max_towers + 1)]):  # If any of the towers have excesses that are not None, don't treat this layer as primary here
        sir_by_coverage = deepcopy(primaries["sir_by_coverage"])
    else:
        sir_by_coverage = constants.coverage_dict()

        for i in range(1, constants.max_towers + 1):
            tower_show = getattr(hxd.non_cds.cover_details, f"tower_{i}_show")
            if tower_show:
                tower = getattr(layer, f"tower_{i}")
                coverage = tower.coverage.selected
                if not coverage:
                    continue
                tower_coverages = constants.coverage_switch.get(coverage, [])
                coverage_by_tower[f"tower_{i}"] = tower_coverages
                layer_coverages = layer_coverages + tower_coverages
                for tower_coverage in tower_coverages:
                    for coverage_type in ["manager", "fund"]:
                        if tower_coverage in ["crime", "pi"]:
                            sir_by_coverage_value = (
                                tower.excess.selected or 0
                                if is_coverage_type_included[tower_coverage][
                                    coverage_type
                                ]
                                else 0
                            )
                            sir_by_coverage[tower_coverage][coverage_type] = (
                                sir_by_coverage_value / fixed_exp_live_cover
                            )
                            sir_by_coverage[tower_coverage][coverage_type] = (
                                sir_by_coverage_value / fixed_exp_live_cover
                            ) + primaries["sir_by_coverage"][tower_coverage][
                                coverage_type
                            ]
                        else:
                            sir_by_coverage_value = (
                                tower.excess.selected or 0
                                if is_coverage_type_included["do"][coverage_type]
                                else 0
                            )
                            if tower_coverage == "A":
                                sir_by_coverage["A"][coverage_type] = (
                                    sir_by_coverage_value / fixed_exp_live_cover
                                )
                            else:
                                sir_by_coverage[tower_coverage][coverage_type] = (
                                    sir_by_coverage_value / fixed_exp_live_cover
                                ) + primaries["sir_by_coverage"][tower_coverage][
                                    coverage_type
                                ]
        
    is_sublimits = hxd.cds.rating_factors.cover_details.sublimits_req
    coverages_without_sublimits = {
        "crime": {
            "manager": False,
            "fund": False,
        },
        "pi": {
            "manager": False,
            "fund": False,
        },
        "do": {
            "manager": False,
            "fund": False,
        },
    }
    
    limits_by_coverage = constants.coverage_dict()

    if is_sublimits:
        for coverage_name in ["crime", "pi", "do"]:
            layer_coverage = getattr(layer.coverages, coverage_name)
            if layer_coverage.all_manager and layer_coverage.all_manager.sublimit:
                manager_limit = layer_coverage.all_manager.sublimit or 0
                manager_limit_after_conversion = (
                    manager_limit / fixed_exp_live_cover
                )
                if coverage_name == "do":
                    for do_coverage in ["A", "B", "C", "Dic"]:
                        limits_by_coverage[do_coverage][
                            "manager"
                        ] = manager_limit_after_conversion
                else:
                    limits_by_coverage[coverage_name][
                        "manager"
                    ] = manager_limit_after_conversion
            else:
                coverages_without_sublimits[coverage_name]["manager"] = True
            if layer_coverage.fund and layer_coverage.fund.sublimit:
                fund_limit = layer_coverage.fund.sublimit or 0
                fund_limit_after_conversion = fund_limit / fixed_exp_live_cover
                if coverage_name == "do":
                    for do_coverage in ["A", "B", "C", "Dic"]:
                        limits_by_coverage[do_coverage][
                            "fund"
                        ] = fund_limit_after_conversion
                else:
                    limits_by_coverage[coverage_name][
                        "fund"
                    ] = fund_limit_after_conversion
            else:
                coverages_without_sublimits[coverage_name]["fund"] = True

    for key, value in coverage_by_tower.items():
        for coverage in value:
            tower = getattr(layer, key)
            tower_limit = tower.limit or 0
            tower_limit_after_conversion = tower_limit / fixed_exp_live_cover
            for coverage_type in ["manager", "fund"]:
                if coverage in ["do", "A", "B", "C", "Dic"]:
                    if (
                        not is_sublimits
                        or coverages_without_sublimits["do"][coverage_type]
                    ):
                        if (
                            base_rate_by_coverage["A"][coverage_type] > 0
                        ):
                            limits_by_coverage["A"][
                                coverage_type
                            ] = tower_limit_after_conversion
                        if base_rate_by_coverage["B"][coverage_type] > 0:
                            limits_by_coverage["B"][
                                coverage_type
                            ] = tower_limit_after_conversion
                        if base_rate_by_coverage["C"][coverage_type] > 0:
                            limits_by_coverage["C"][
                                coverage_type
                            ] = tower_limit_after_conversion
                        if base_rate_by_coverage["Dic"][coverage_type] > 0:
                            limits_by_coverage["Dic"][
                                coverage_type
                            ] = tower_limit_after_conversion
                else:
                    if (
                        not is_sublimits
                        or coverages_without_sublimits[coverage][coverage_type]
                    ):
                        limits_by_coverage[coverage][
                            coverage_type
                        ] = tower_limit_after_conversion

    layer_coverages = list(set(layer_coverages))
    ilf_factor_by_coverage = calculate_ilf_factor(
        sir_by_coverage,
        layer_coverages,
        limits_by_coverage,
        is_coverage_type_included,
        is_primary if not any([getattr(layer, f"tower_{i}").excess.selected for i in range(1, constants.max_towers + 1)]) else False,  # Treat as primary only if excess is not overridden
    )

    # Calculate Reinstate Factor
    table_cover_factors = hx.params.table_cover_factors
    reinstatement_factor = table_cover_factors[
        table_cover_factors["type"] == "ReinstatementFactor"
    ]["value"].values[0]
    reinstatement_type = hxd.cds.rating_factors.cover_details.details_reinstatements
    reinstatement_factor_by_coverage = {
        "crime": {"manager": 1, "fund": 1},
        "pi": {"manager": 1, "fund": 1},
        "A": {"manager": 1, "fund": 1},
        "B": {"manager": 1, "fund": 1},
        "C": {"manager": 1, "fund": 1},
        "Dic": {"manager": 1, "fund": 1},
    }
    if reinstatement_type and reinstatement_type != "NA":
        reinstatement_by_coverage = {
            "crime": 0,
            "pi": 0,
            "A": 0,
            "B": 0,
            "C": 0,
            "Dic": 0,
        }
        reinstatement_by_tower = {
            "tower_1": 0,
            "tower_2": 0,
            "tower_3": 0,
            "tower_4": 0,
            "tower_5": 0,
            "tower_6": 0,
        }
        for i in range(1, constants.max_towers + 1):
            is_direct = reinstatement_type == "Direct"
            tower_show = getattr(hxd.non_cds.cover_details, f"tower_{i}_show")
            all_towers_same_value = (
                (hxd.cds.rating_factors.cover_details.no_direct_reinstatements if 0 <= (hxd.cds.rating_factors.cover_details.no_direct_reinstatements or 0) <= 10000 else 0)
                if is_direct
                else hxd.cds.rating_factors.cover_details.reinst_rtc_program_limit
            )
            if tower_show:
                tower = getattr(layer, f"tower_{i}")
                if all_towers_same_value:
                    reinstatement_by_tower[f"tower_{i}"] = all_towers_same_value
                else:
                    reinstatement_by_tower[f"tower_{i}"] = (
                        (tower.direct_reinstatements if 0 <= (tower.direct_reinstatements or 0) <= 10000 else 0)
                        if is_direct
                        else tower.rtc_reinstatements
                    )

        for key, value in coverage_by_tower.items():
            for coverage in value:
                if coverage == "do":
                    if base_rate_by_coverage["A"]["base_rate"] > 0:
                        reinstatement_by_coverage["A"] = reinstatement_by_tower[key]
                    if base_rate_by_coverage["B"]["base_rate"] > 0:
                        reinstatement_by_coverage["B"] = reinstatement_by_tower[key]
                    if base_rate_by_coverage["C"]["base_rate"] > 0:
                        reinstatement_by_coverage["C"] = reinstatement_by_tower[key]
                else:
                    reinstatement_by_coverage[coverage] = reinstatement_by_tower[key]
        reinstatement_factor_by_coverage = (
            calculate_reinstatement_factor_by_coverage(
                is_direct,
                reinstatement_factor,
                reinstatement_by_coverage,
                limits_by_coverage,
                sir_by_coverage,
            )
        )

    shared_limit_discount_by_coverage = {
        "crime": {"manager": 0, "fund": 0},
        "pi": {"manager": 0, "fund": 0},
        "A": {"manager": 0, "fund": 0},
        "B": {"manager": 0, "fund": 0},
        "C": {"manager": 0, "fund": 0},
        "Dic": {"manager": 0, "fund": 0},
    }
    discount_dict = (
        table_cover_factors[table_cover_factors["type"] == "LimShared"]
        .set_index("param")
        .to_dict()["value"]
    )
    for key, value in coverage_by_tower.items():
        coverages_after_do_filter = {
            "crime": 0,
            "pi": 0,
            "do": 0,
        }
        for coverage in list(set(value)):
            if coverage in ["do", "A", "B", "C", "Dic"]:
                do_base_rate_summation = 0
                for do_coverage in ["A", "B", "C", "Dic"]:
                    do_base_rate_summation += base_rate_by_coverage[do_coverage]["base_rate"]

                coverages_after_do_filter["do"] = (
                    2
                    if (
                        industry == "investment managers"
                        and is_coverage_type_included["do"]["manager"]
                        and is_coverage_type_included["do"]["fund"]
                        and key in towers_by_fund_manager["manager"]
                        and key in towers_by_fund_manager["fund"]
                        and do_base_rate_summation > 0
                    )
                    else 1 if do_base_rate_summation > 0 else 0
                )
            else:
                coverages_after_do_filter[coverage] += (
                    2
                    if (
                        industry == "investment managers"
                        and is_coverage_type_included[coverage]["fund"]
                        and is_coverage_type_included[coverage]["manager"]
                        and key in towers_by_fund_manager["manager"]
                        and key in towers_by_fund_manager["fund"]
                        and base_rate_by_coverage[coverage]["base_rate"] > 0
                    )
                    else 1 if base_rate_by_coverage[coverage]["base_rate"] > 0 else 0
                )

        coverages_counter = min(sum(coverages_after_do_filter.values()), 3)
        discount = discount_dict[coverages_counter]
        for rating in ["manager", "fund"]:
            if key not in towers_by_fund_manager[rating]:
                continue
            for coverage in value:
                if coverage =="Dic":
                    continue  # Hardcoded to 0
                if coverage == "do":
                    if base_rate_by_coverage["A"][rating] > 0:
                        shared_limit_discount_by_coverage["A"][rating] = min(
                            shared_limit_discount_by_coverage.get("A", {}).get(rating, 0), discount
                        )
                    if base_rate_by_coverage["B"][rating] > 0:
                        shared_limit_discount_by_coverage["B"][rating] = min(
                            shared_limit_discount_by_coverage.get("B", {}).get(rating, 0), discount
                        )
                    if base_rate_by_coverage["C"][rating] > 0:
                        shared_limit_discount_by_coverage["C"][rating] = min(
                            shared_limit_discount_by_coverage.get("C", {}).get(rating, 0), discount
                        )
                    # if base_rate_by_coverage["Dic"][rating] > 0:
                    #     shared_limit_discount_by_coverage["Dic"][rating] = min(
                    #         shared_limit_discount_by_coverage.get("Dic", {}).get(rating, 0), discount
                    #     )                        
                else:
                    shared_limit_discount_by_coverage[coverage][rating] = min(
                        shared_limit_discount_by_coverage.get(coverage, {}).get(rating, 0), discount
                    )
    limits_by_coverage_frequency_layer = {
        "crime": {"manager": 1, "fund": 1},
        "pi": {"manager": 1, "fund": 1},
        "A": {"manager": 1, "fund": 1},
        "B": {"manager": 1, "fund": 1},
        "C": {"manager": 1, "fund": 1},
        "Dic": {"manager": 1, "fund": 1},
    }
    expected_loss_by_layer_by_coverage = {
        "crime": {"manager": 0, "fund": 0},
        "pi": {"manager": 0, "fund": 0},
        "A": {"manager": 0, "fund": 0},
        "B": {"manager": 0, "fund": 0},
        "C": {"manager": 0, "fund": 0},
        "Dic": {"manager": 0, "fund": 0},
        "do": {"manager": 0, "fund": 0},
    }
    frquency_layer_by_coverage = {
        "crime": {"manager": 0, "fund": 0},
        "pi": {"manager": 0, "fund": 0},
        "A": {"manager": 0, "fund": 0},
        "B": {"manager": 0, "fund": 0},
        "C": {"manager": 0, "fund": 0},
        "Dic": {"manager": 0, "fund": 0},
        "do": {"manager": 0, "fund": 0},
    }
    frequency_ilf_factor_by_coverage = calculate_ilf_factor(
        sir_by_coverage,
        layer_coverages,
        limits_by_coverage_frequency_layer,
        is_coverage_type_included,
        is_primary if not any([getattr(layer, f"tower_{i}").excess.selected for i in range(1, constants.max_towers + 1)]) else False,  # Treat as primary only if excess is not overridden,
    )
    for coverage in layer_coverages:
        for coverage_type in ["manager", "fund"]:
            base_rate = base_rate_by_coverage[coverage][coverage_type]
            ilf_factor = ilf_factor_by_coverage[coverage][coverage_type]
            coverage_reinstatement_factor = reinstatement_factor_by_coverage[coverage][coverage_type]
            shared_limit_discount = 1 + shared_limit_discount_by_coverage[coverage][coverage_type]
            expected_loss = (
                base_rate
                * ilf_factor
                * coverage_reinstatement_factor
                * shared_limit_discount
                * 1000000
            )
            expected_loss_by_layer_by_coverage[coverage][
                coverage_type
            ] = expected_loss
            frquency_layer_by_coverage[coverage][coverage_type] = (
                base_rate
                * frequency_ilf_factor_by_coverage[coverage][coverage_type]
                * coverage_reinstatement_factor
                * shared_limit_discount
                * 1000000
            )
    expected_loss_by_layer_by_coverage["do"] = {
        "manager": ((expected_loss_by_layer_by_coverage["A"]["manager"]
        + expected_loss_by_layer_by_coverage["B"]["manager"]
        + expected_loss_by_layer_by_coverage["C"]["manager"]
        + expected_loss_by_layer_by_coverage["Dic"]["manager"]) 
        if 
            (hxd.cds.rating_factors.cover_details.primary_layer.sir_all_manager.do_side_c 
            or hxd.non_cds.cover_details.do_side_a_show 
            or hxd.non_cds.cover_details.do_side_b_show 
            or hxd.cds.rating_factors.cover_details.primary_layer.sir_all_manager.do_side_c) 
        else 0
        ),
        "fund": ((expected_loss_by_layer_by_coverage["A"]["fund"]
        + expected_loss_by_layer_by_coverage["B"]["fund"]
        + expected_loss_by_layer_by_coverage["C"]["fund"]
        + expected_loss_by_layer_by_coverage["Dic"]["fund"]) 
        if 
            (hxd.cds.rating_factors.cover_details.primary_layer.sir_all_manager.do_side_c 
            or hxd.non_cds.cover_details.do_side_a_show 
            or hxd.non_cds.cover_details.do_side_b_show 
            or hxd.cds.rating_factors.cover_details.primary_layer.sir_fund.do_side_c) 
        else 0),
    }
    frquency_layer_by_coverage["do"] = {
        "manager": frquency_layer_by_coverage["A"]["manager"]
        + frquency_layer_by_coverage["B"]["manager"]
        + frquency_layer_by_coverage["C"]["manager"]
        + frquency_layer_by_coverage["Dic"]["manager"],
        "fund": frquency_layer_by_coverage["A"]["fund"]
        + frquency_layer_by_coverage["B"]["fund"]
        + frquency_layer_by_coverage["C"]["fund"]
        + frquency_layer_by_coverage["Dic"]["fund"],
    }
    afb_exposure_by_coverage = {
        "crime": {"manager": 0, "fund": 0},
        "pi": {"manager": 0, "fund": 0},
        "A": {"manager": 0, "fund": 0},
        "B": {"manager": 0, "fund": 0},
        "C": {"manager": 0, "fund": 0},
        "Dic": {"manager": 0, "fund": 0},
        "do": {"manager": 0, "fund": 0},
    }
    is_premium_split_across_all_layers = (
        hxd.non_cds.cover_details.is_premium_split_all_layers
    )
    if is_premium_split_across_all_layers:
        for key, value in coverage_by_tower.items():
            coverages_after_do_filter = []
            for coverage in value:
                if (
                    (coverage == "A")
                    or (coverage == "B")
                    or (coverage == "C")
                    or (coverage == "Dic")
                ):
                    if "do" not in coverages_after_do_filter:
                        coverages_after_do_filter.append("do")
                else:
                    coverages_after_do_filter.append(coverage)
            for coverage_type in ["manager", "fund"]:
                for coverage in coverages_after_do_filter:
                    used_coverage = (
                        coverage if coverage in ["crime", "pi"] else "do"
                    )
                    premium_split = (
                        getattr(
                            hxd.cds.rating_factors.cover_details.premium_split_all_layers,
                            used_coverage,
                        )
                        or 0
                    )
                    tower = getattr(layer, key)
                    beazley_line = tower.beazley_line or 0
                    afb_exposure = beazley_line * premium_split
                    afb_exposure_by_coverage[coverage][coverage_type] = afb_exposure
                    if coverage in ["A", "B", "C", "Dic"]:
                        afb_exposure_by_coverage["do"][coverage_type] = max(
                            afb_exposure,
                            afb_exposure_by_coverage["do"][coverage_type],
                        )
    else:
        for key, value in coverage_by_tower.items():
            for coverage_type in ["manager", "fund"]:
                for coverage in value:
                    used_coverage = (
                        coverage if coverage in ["crime", "pi"] else "do"
                    )
                    hxd_coverage = getattr(layer.coverages, used_coverage)
                    premium_split = hxd_coverage.premium_split or 0
                    tower = getattr(layer, key)
                    beazley_line = tower.beazley_line or 0
                    afb_exposure = beazley_line * premium_split
                    afb_exposure_by_coverage[coverage][coverage_type] = afb_exposure
                    if coverage in ["A", "B", "C", "Dic"]:
                        afb_exposure_by_coverage["do"][coverage_type] = max(
                            afb_exposure,
                            afb_exposure_by_coverage["do"][coverage_type],
                        )
    attritional_by_coverage = {
        "crime": 0,
        "pi": 0,
        "do": 0,
    }

    table_aum = hx.params.table_aum_parameters
    table_att_cat = hx.params.table_att_cat
    for coverage in attritional_by_coverage.keys():
        if coverage == "pi":
            exposure = (
                hxd.cds.exposure.aggregate.total_amounts.revenues
                / global_params["fx_live_expo"]
            ) or 0
            # value 2
            if hxd.non_cds.exposure_details.total_aum_show:
                aum = (
                    hxd.cds.exposure.aggregate.total_amounts.aum or 0
                ) / global_params["fx_live_expo"]
                if aum:
                    conversion_factor = table_aum.query(
                        'coverage == "pi" and category == "conversion factor"'
                    ).parameter.item()
                    weight_aum = table_aum.query(
                        'coverage == "pi" and category == "weight to aum"'
                    ).parameter.item()
                    exposure = (
                        conversion_factor * aum * weight_aum
                        + (1 - weight_aum) * exposure
                    )
            cat_param = table_att_cat.query(f'label == "CatParam"')[
                coverage
            ].values[0]
            attritional_value = (exposure / 1000000) ** cat_param
            attritional_by_coverage[coverage] = (
                attritional_value if (attritional_value < 1) else 1
            )
        else:
            attritional_rows = table_att_cat.query(f'label == "AttritionalPC"')[
                coverage
            ].values
            if attritional_rows and len(attritional_rows) > 0:
                attritional_by_coverage[coverage] = attritional_rows[0]
    attritional_el = 0
    attirional_el_crime = attritional_by_coverage["crime"] * (
        expected_loss_by_layer_by_coverage["crime"]["manager"]
        + expected_loss_by_layer_by_coverage["crime"]["fund"]
    )
    attirional_el_pi = attritional_by_coverage["pi"] * (
        expected_loss_by_layer_by_coverage["pi"]["manager"]
        + expected_loss_by_layer_by_coverage["pi"]["fund"]
    )
    attirional_el_do = attritional_by_coverage["do"] * (
        expected_loss_by_layer_by_coverage["do"]["manager"]
        + expected_loss_by_layer_by_coverage["do"]["fund"]
    )
    attritional_el = attirional_el_crime + attirional_el_pi + attirional_el_do
    total_expected_loss = (
        expected_loss_by_layer_by_coverage["crime"]["manager"]
        + expected_loss_by_layer_by_coverage["crime"]["fund"]
        + expected_loss_by_layer_by_coverage["pi"]["manager"]
        + expected_loss_by_layer_by_coverage["pi"]["fund"]
        + expected_loss_by_layer_by_coverage["do"]["manager"]
        + expected_loss_by_layer_by_coverage["do"]["fund"]
    )
    layer.expected_loss_cost_annualised = total_expected_loss
    calcs_helper.calculate_net_rol(idx, layer, hxd)
    
    cat_el = total_expected_loss - attritional_el
    total_el = cat_el + attritional_el
    att_percentage = 0 if total_el == 0 else attritional_el / total_el
    cat_percentage = 0 if total_el == 0 else cat_el / total_el
    net_benchmark_premium = total_expected_loss / 0.7
    all_brokerage = hxd.non_cds.cover_details.is_brokerage_all_layers
    brokerage = 0
    ncb = 0
    lta = 0
    if all_brokerage:
        brokerage = (
            hxd.cds.rating_factors.cover_details.brokerage_all_layers.brk or 0
        )
        ncb = hxd.cds.rating_factors.cover_details.brokerage_all_layers.ncb or 0
        lta = hxd.cds.rating_factors.cover_details.brokerage_all_layers.lta or 0
    else:
        brokerage = layer.brokerage or 0
        ncb = layer.ncb or 0
        lta = layer.lta or 0
    total_frequency_by_layer = (
        frquency_layer_by_coverage["crime"]["manager"]
        + frquency_layer_by_coverage["crime"]["fund"]
        + frquency_layer_by_coverage["pi"]["manager"]
        + frquency_layer_by_coverage["pi"]["fund"]
        + frquency_layer_by_coverage["do"]["manager"]
        + frquency_layer_by_coverage["do"]["fund"]
    )
    zero_claims_ncb_calcs = poisson_distribution(0, total_frequency_by_layer) or 0
    gross_premium = (net_benchmark_premium) / (
        1 - brokerage - lta - (ncb * zero_claims_ncb_calcs)
    )
    total_afb_exposure_by_coverage = {
        "crime": 0,
        "pi": 0,
        "do": 0,
        "total": 0,
    }
    for coverage in ["crime", "pi", "do"]:
        total_expected_loss_by_coverage = (
            expected_loss_by_layer_by_coverage[coverage]["manager"]
            + expected_loss_by_layer_by_coverage[coverage]["fund"]
        )
        if total_expected_loss_by_coverage == 0:
            continue
        total_afb_exposure_by_coverage_manager = (
            expected_loss_by_layer_by_coverage[coverage]["manager"]
            * afb_exposure_by_coverage[coverage]["manager"]
            / total_expected_loss_by_coverage
        )
        total_afb_exposure_by_coverage_fund = (
            expected_loss_by_layer_by_coverage[coverage]["fund"]
            * afb_exposure_by_coverage[coverage]["fund"]
            / total_expected_loss_by_coverage
        )
        total_afb_exposure_by_coverage[coverage] = (
            total_afb_exposure_by_coverage_manager
            + total_afb_exposure_by_coverage_fund
        )
        total_afb_exposure_by_coverage["total"] += total_afb_exposure_by_coverage[
            coverage
        ]

    layer.written_line = total_afb_exposure_by_coverage["total"]

    afb_net_premium_by_coverage = {
        "crime": 0,
        "pi": 0,
        "do": 0,
        "total": 0,
    }
    net_premium = (layer.net_premium or 0) / fixed_exp_live_cover
    afb_net_premium_by_coverage["total"] = (
        net_premium * total_afb_exposure_by_coverage["total"]
    )
    is_premium_split_all_layers = (
        hxd.non_cds.cover_details.is_premium_split_all_layers
    )
    premium_by_coverage = {
        "crime": 0,
        "pi": 0,
        "do": 0,
    }
    for coverage in ["crime", "pi", "do"]:
        split = 0
        afb_net_premium_by_coverage[coverage] = (
            net_premium * total_afb_exposure_by_coverage[coverage]
        )
        if is_premium_split_all_layers:
            split = (
                getattr(
                    hxd.cds.rating_factors.cover_details.premium_split_all_layers,
                    coverage,
                )
                or 0
            )
        else:
            full_coverage = getattr(layer.coverages, coverage)
            split = full_coverage.premium_split or 0
        premium_by_coverage[coverage] = net_premium * split
    afb_gross_premium = (
        total_afb_exposure_by_coverage["total"]
        * (layer.quoted_premium_pro_rata_100 or 0)
        / fixed_exp_live_cover
    )
    attritional_net_benchmark_premium_by_coverage = {
        "crime": 0,
        "pi": 0,
        "do": 0,
    }
    cat_net_benchmark_premium_by_coverage = {
        "crime": 0,
        "pi": 0,
        "do": 0,
    }
    inception_date = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    for coverage in ["crime", "pi", "do"]:
        if premium_by_coverage[coverage] == 0 or total_expected_loss == 0:
            attritional_net_benchmark_premium_by_coverage[coverage] = 0
            cat_net_benchmark_premium_by_coverage[coverage] = 0
        else:
            total_expected_loss_by_coverage = (
                expected_loss_by_layer_by_coverage[coverage]["manager"]
                + expected_loss_by_layer_by_coverage[coverage]["fund"]
            )
            attritional_net_benchmark_premium = (
                attritional_by_coverage[coverage]
                * (total_expected_loss_by_coverage / total_expected_loss)
                * net_benchmark_premium
                * (
                    afb_net_premium_by_coverage[coverage]
                    / premium_by_coverage[coverage]
                )
            )
            date_result = 1
            if not inception_date or not expiry_date:
                diff_days = (expiry_date - inception_date).days
                next_year_date = datetime(
                    inception_date.year + 1,
                    inception_date.month,
                    inception_date.day,
                ) - timedelta(days=1)
                diff_days_next_year = (next_year_date - inception_date).days
                date_result = (
                    diff_days / diff_days_next_year
                    if diff_days_next_year != 0
                    else 1
                )
            attritional_net_benchmark_premium_by_coverage[coverage] = (
                attritional_net_benchmark_premium * date_result
            )
            cat_net_benchmark_premium_a = (
                total_expected_loss_by_coverage / total_expected_loss
            ) * net_benchmark_premium
            cat_net_benchmark_premium_b = (
                (total_expected_loss_by_coverage / total_expected_loss)
                * net_benchmark_premium
                * attritional_by_coverage[coverage]
            )
            cat_net_benchmark_premium = (
                (cat_net_benchmark_premium_a - cat_net_benchmark_premium_b)
                * (
                    afb_net_premium_by_coverage[coverage]
                    / premium_by_coverage[coverage]
                )
                * date_result
            )
            cat_net_benchmark_premium = (
                0 if cat_net_benchmark_premium < 0 else cat_net_benchmark_premium
            )
            cat_net_benchmark_premium_by_coverage[coverage] = (
                cat_net_benchmark_premium
            )
    afb_el = (
        0
        if net_premium == 0
        else (afb_net_premium_by_coverage["total"] / net_premium)
        * total_expected_loss
    )
    afb_el_ncb = afb_el / (1 - (ncb * zero_claims_ncb_calcs) - lta)
    tot_el_ncb_100 = total_expected_loss / (1 - (ncb * zero_claims_ncb_calcs) - lta)

    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = parameter_tables_schema.tp_parameters.df()
    yoa = hxd.hx_core.inception_date.year
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if yoa in list(tp_params_df["year"]):
        tp_year = yoa
    else:
        tp_year = tp_params_df["year"].max()
    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class
    bp_class = "Financial Institutions"  # PLACEHOLDER

    # Define function to look up bp class
    def tp_lookup(vbl, bp_class):
        out = tp_params_df[
            (tp_params_df["business_plan_class"] == bp_class)
            & (tp_params_df["year"] == tp_year)
        ][vbl].iloc[0]
        return out

    # Set up tp params
    che = tp_lookup("che", bp_class)
    var_exp = tp_lookup("var_exp", bp_class)
    inv_inc = tp_lookup("inv_inc", bp_class)
    cost_of_ri = tp_lookup("cost_of_ri", bp_class)
    ri_rec = tp_lookup("ri_rec", bp_class)
    roc = tp_lookup("roc", bp_class)
    fixed_exp_usd = tp_lookup("fixed_exp", bp_class)
    capital_req = tp_lookup("capital_req", bp_class)
    nmp_load = tp_lookup("nmp_load", bp_class)

    che_value = afb_el_ncb * che
    var_exp_value = (afb_el_ncb + che_value + fixed_exp_usd) * var_exp

    afb_net_tp = (afb_el_ncb * (1 + che) + fixed_exp_usd) / (
        1 - (cost_of_ri - ri_rec) - (capital_req * roc) - var_exp + inv_inc
    )

    tot_net_tp_100 = (tot_el_ncb_100 * (1 + che) + fixed_exp_usd) / (
        1 - (cost_of_ri - ri_rec) - (capital_req * roc) - var_exp + inv_inc
    )

    total_exp = (che_value + fixed_exp_usd) + (afb_net_tp * var_exp)

    cost_of_ri_value = afb_net_tp * (cost_of_ri - ri_rec)

    cost_of_capital = capital_req * roc * afb_net_tp

    inv_inc_value = afb_net_tp * inv_inc

    afb_gross_tp = afb_net_tp / (1 - brokerage)

    tot_gross_tp_100 = tot_net_tp_100 / (1 - brokerage)

    brokerage_value = afb_gross_tp * brokerage

    afb_net_tp_pre_uw_adj = (afb_el_ncb / (1 + (hxd.cds.modifiers.risk_category.uw_adj or 0)) * (1 + che) + fixed_exp_usd) / (
        1 - (cost_of_ri - ri_rec) - (capital_req * roc) - var_exp + inv_inc
    )

    afb_gross_tp_pre_uw_adj = afb_net_tp_pre_uw_adj / (1 - brokerage)

    calcs_helper.calculate_afb_net_premium(idx, layer, hxd, afb_net_premium_by_coverage["total"])
    calcs_helper.calculate_net_rol(idx, layer, hxd)
    calcs_helper.calculate_actual_ilf(idx, layer, hxd)
    calcs_helper.calculate_annualised_benchmark_premium(idx, layer, hxd, gross_premium)
    calcs_helper.calculate_pro_rated_benchmark_premium(idx, layer, hxd)

    if layer.quoted_premium_pro_rata_100:
        calcs_helper.calculate_bpi(idx, layer, hxd)
        calcs_helper.calculate_losses_split(idx, layer, hxd, expected_loss_by_layer_by_coverage)
        calcs_helper.calculate_net_lol(idx, layer, hxd, brokerage, ncb, lta, zero_claims_ncb_calcs)
        calcs_helper.calculate_model_ilf(idx, layer, hxd)
        calcs_helper.calculate_expected_loss_cost_att(idx, layer, hxd, att_percentage)
        calcs_helper.calculate_expected_loss_cost_cat(idx, layer, hxd, cat_percentage)
        calcs_helper.calculate_annualised_technical_premium(idx, layer, hxd, afb_gross_tp)
        calcs_helper.calculate_pro_rated_technical_premium(idx, layer, hxd, afb_gross_tp_pre_uw_adj, tot_gross_tp_100)
        calcs_helper.calculate_tpi(idx, layer, hxd, afb_gross_premium)



def rate_rating_summary(hxd):
    rf = hxd.cds.rating_factors
    coverage = get_coverage_matrix(hxd)

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # Show/hide
    show_hide_fields(hxd)

    # Set label for the first rating summary table
    hxd.non_cds.rating_summary.table1_label = hxd.cds.risk_info.currency

    # Set layers label
    layer_labels = get_layer_labels()
    for i, layer in enumerate(hxd.cds.layers):
        layer.label = layer_labels[i]

    # Validations
    has_bound = False
    bound_has_quoted_premium = True
    bound_has_pol_ref = True
    inception_year = hxd.hx_core.inception_date.strftime("%y")
    pol_refs = []

    for layer in hxd.cds.layers:
        bound_layer = layer.status == "Bound"

        # At least one layer must be bound
        if not has_bound and bound_layer:
            has_bound = True

        # All bound layers must have premium
        if bound_has_quoted_premium and bound_layer and not layer.quoted_premium_pro_rata_100:
            bound_has_quoted_premium = False
            hx.errors.validation("- Gross Premium must be entered for all bound layers")

        # Coverage validations
        bound_has_pol_ref_coverage = False if bound_layer else True

        for c, _ in constants.coverages:
            if coverage[f"is_{c}"]:
                layer_coverage = getattr(layer.coverages, c)

                if not str_isblank(layer_coverage.pol_ref):
                    # All bound layers must have pol_ref in at least one coverage
                    if bound_has_pol_ref and not bound_has_pol_ref_coverage and bound_layer:
                        bound_has_pol_ref_coverage = True

                    # Policy reference must be 12 chars with char 7-8 to be inception year
                    if len(layer_coverage.pol_ref) != 12 or layer_coverage.pol_ref[6:8] != inception_year:
                        hx.errors.validation(f"- Policy {layer_coverage.pol_ref} must be 12 characters long with characters 7-8 representing the 2-digit inception year")

                    # Group all pol_refs and pol_ref_non_eea in a list to check for duplication
                    pol_refs.append(layer_coverage.pol_ref)
                    if not str_isblank(layer_coverage.pol_ref_non_eea):
                        pol_refs.append(layer_coverage.pol_ref_non_eea)

        # All bound layers must have pol_ref in at least one coverage
        if bound_has_pol_ref and not bound_has_pol_ref_coverage:
            bound_has_pol_ref = False
            hx.errors.validation("- Policy Reference must be entered for all bound layers")

    # At least one layer must be bound
    if not has_bound:
        hx.errors.validation("- At least one layer must be bound")

    # # Duplicate pol_ref. This error was requested to be removed by the UWs
    # if len(pol_refs) != len(set(pol_refs)):
    #     hx.errors.validation("- Policy references must be unique")

    # Build towers constants.coverages map
    towers_coverages_map = {t: [] for t in range(1, constants.max_towers + 1)}
    for c, label in constants.coverages:
        if coverage[f"is_{c}"]:
            towers = {
                'manager': getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_all_manager, c),
                'fund': getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_fund, c)
            }

            for k, v in towers.items():
                if v != "NA":
                    tower_num = int(v[-1])  # i.e Tower 1
                    towers_coverages_map[tower_num].append(label)
                    # Append D&O type
                    if c == "do":
                        do_type = hxd.cds.rating_factors.cover_details.primary_layer.do_type
                        if do_type:
                            towers_coverages_map[tower_num][-1] = towers_coverages_map[tower_num][-1] + " " + do_type

    # Apply constants.coverages selection on all layers
    for layer in hxd.cds.layers:
        for tower_idx in range(1, constants.max_towers + 1):
            if getattr(hxd.non_cds.cover_details, f"tower_{tower_idx}_show") and towers_coverages_map[tower_idx]:
                tower = getattr(layer, f"tower_{tower_idx}")
                tower.coverage.calculated = " / ".join(ordered_uniquify(towers_coverages_map[tower_idx]))

    # Initialize sir_by_coverage dictionary
    base_rate_by_coverage = calcs_helper.calculate_cover_factor(hxd)   
    primaries = calculate_primaries(hxd, base_rate_by_coverage)

    for i, layer in enumerate(hxd.cds.layers):
        calcs_helper.calculate_excess(i, layer, hxd)  # Calculates the excess float field
        calcs_helper.fill_excess_str(i, layer, hxd)  # Fills the excess string fields which is used for UI purposes
        calcs_helper.calculate_net_premium(i, layer, hxd)
        calcs_helper.calculate_exposure(i, layer, hxd)
        
        calculate_values(i, hxd, layer, base_rate_by_coverage, primaries)

        # Store annualised premiums for use in rate change calcs
        layer.quoted_premium_annualised = (layer.quoted_premium_pro_rata_100 or 0) / (rf.policy_term or 1)
        afb_premium = layer.afb_net_premium or 0
        net_premium = layer.net_premium or 0
        layer.benchmark_premium = (afb_premium / net_premium) * layer.benchmark_premium_pro_rata_100 if (layer.benchmark_premium_pro_rata_100 and (net_premium > 0)) else None
        layer.expected_loss_cost = layer.benchmark_premium * constants.benchmark_lr if layer.benchmark_premium else None
        layer.quoted_premium = layer.quoted_premium_pro_rata_100 * (afb_premium / net_premium) if (layer.quoted_premium_pro_rata_100 and (net_premium > 0) and (afb_premium > 0)) else None

    # Secondry rating summary table
    currency = hxd.cds.risk_info.currency
    hxd.non_cds.rating_summary.secondry_summary_show = currency != "USD"

    if hxd.non_cds.rating_summary.secondry_summary_show:
        hxd.cds.rating_summary.authorities_fx.calculated = calcs_helper.global_parameters(hxd)["fx_authorities"]
        fx_rate = hxd.cds.rating_summary.authorities_fx.selected
        if fx_rate:
            for idx, layer in enumerate(hxd.cds.layers):
                layer.net_premium_fx = ratio(layer.net_premium, fx_rate) if layer.net_premium else None
                layer.exposure_fx = ratio(layer.exposure, fx_rate) if layer.exposure else None
                layer.afb_net_premium_fx = ratio(layer.afb_net_premium, fx_rate) if layer.afb_net_premium else None
                layer.benchmark_premium_annualised_100_fx = ratio(layer.benchmark_premium_annualised_100, fx_rate) if layer.benchmark_premium_annualised_100 else None
                layer.quoted_premium_pro_rata_100_fx = ratio(layer.quoted_premium_pro_rata_100, fx_rate) if layer.quoted_premium_pro_rata_100 else None
                layer.benchmark_premium_pro_rata_100_fx = ratio(layer.benchmark_premium_pro_rata_100, fx_rate) if layer.benchmark_premium_pro_rata_100 else None
                layer.technical_premium_fx = ratio(layer.technical_premium, fx_rate) if layer.technical_premium else None
                layer.technical_premium_net_fx = ratio(layer.technical_premium_net, fx_rate) if layer.technical_premium_net else None

                for i in range(1, constants.max_towers + 1):
                    layer_tower = getattr(layer, f"tower_{i}")
                    if layer_tower.limit:
                        layer_tower.limit_fx = ratio(layer_tower.limit, fx_rate)
                    if layer_tower.excess.selected:
                        layer_tower.excess_fx = ratio(layer_tower.excess.selected, fx_rate)
                    if layer_tower.rtc_reinstatements:
                        layer_tower.rtc_reinstatements_fx = ratio(layer_tower.rtc_reinstatements, fx_rate)

                calcs_helper.fill_excess_str_fx(idx, layer, hxd)

                for c, _ in constants.coverages:
                    layer_coverage = getattr(layer.coverages, c)
                    if layer_coverage.all_manager.sublimit:
                        layer_coverage.all_manager.sublimit_fx = ratio(layer_coverage.all_manager.sublimit, fx_rate)
                    if layer_coverage.fund.sublimit:
                        layer_coverage.fund.sublimit_fx = ratio(layer_coverage.fund.sublimit, fx_rate)


    #Populate Section Reference
    for idx, layer in enumerate(hxd.cds.layers):
        layer.section_reference = (hxd.cds.layers[idx].coverages.crime.pol_ref or hxd.cds.layers[idx].coverages.pi.pol_ref or hxd.cds.layers[idx].coverages.do.pol_ref
                                    or hxd.cds.layers[idx].coverages.crime.pol_ref_non_eea or hxd.cds.layers[idx].coverages.pi.pol_ref_non_eea or hxd.cds.layers[idx].coverages.do.pol_ref_non_eea)
    

def show_hide_fields(hxd):
    coverage = get_coverage_matrix(hxd)
    industry = get_industry_matrix(hxd)
    sublimits_show = hxd.cds.rating_factors.cover_details.sublimits_req

    # Towers
    for i in range(1, constants.max_towers + 1):
        tower = getattr(hxd.non_cds.rating_summary, f"tower_{i}")
        tower_show = getattr(hxd.non_cds.cover_details, f"tower_{i}_show")
        cover_details_direct_reinstatements = hxd.cds.rating_factors.cover_details.no_direct_reinstatements
        cover_details_rtc = hxd.cds.rating_factors.cover_details.reinst_rtc_program_limit

        tower.direct_reinstatements_show = tower_show and hxd.non_cds.cover_details.direct_reinstatements_show and not cover_details_direct_reinstatements
        tower.rtc_reinstatements_show = tower_show and hxd.non_cds.cover_details.rtc_limit_show and not cover_details_rtc
        tower.coverage_show = tower_show and not hxd.non_cds.cover_details.show_different_towers_manager_fund_warning

    # Coverages
    for c, _ in constants.coverages:
        cover = getattr(hxd.non_cds.rating_summary, c)
        show_funds = coverage[f"is_{c}"] and industry["is_inv"] and sublimits_show

        setattr(cover, "sublimit_show", not show_funds and coverage[f"is_{c}"] and sublimits_show)
        setattr(cover, "all_manager_sublimit_show", show_funds and coverage[f"is_{c}"] and sublimits_show)
        setattr(cover, "fund_sublimit_show", show_funds)
        setattr(cover, "premium_split_show", coverage[f"is_{c}"] and not hxd.non_cds.cover_details.is_premium_split_all_layers)
        setattr(cover, "pol_ref_non_eea_show", coverage[f"is_{c}"] and hxd.cds.risk_info.eea_non_eea_indicator)

    # Rest of Fields
    hxd.non_cds.rating_summary.is_brokerage_per_layer = not hxd.non_cds.cover_details.is_brokerage_all_layers


def calculate_primaries(hxd, base_rate_by_coverage):
    primary_layer = hxd.cds.rating_factors.cover_details.primary_layer

    global_params = calcs_helper.global_parameters(hxd)
    fixed_exp_live_cover = global_params["fx_live_cover"]

    
    layer_coverages = []
    towers_by_fund_manager = {
        "manager": [],
        "fund": []
    }
    is_coverage_type_included = {
        "crime": {"manager": False, "fund": False},
        "pi": {"manager": False, "fund": False},
        "do": {"manager": False, "fund": False},
    }
    coverage_by_tower = {
        "tower_1": [],
        "tower_2": [],
        "tower_3": [],
        "tower_4": [],
        "tower_5": [],
        "tower_6": [],
    }

    if primary_layer.towers_all_manager.crime != "NA":
        layer_coverages.append("crime")
        towers_by_fund_manager["manager"].append(primary_layer.towers_all_manager.crime.replace(" ", "_").lower())
        tower = primary_layer.towers_all_manager.crime.replace(" ", "_").lower()
        coverage_by_tower[tower].append("crime")
        is_coverage_type_included["crime"]["manager"] = True
    if primary_layer.towers_fund.crime != "NA":                
        tower = primary_layer.towers_fund.crime.replace(" ", "_").lower()
        towers_by_fund_manager["fund"].append(primary_layer.towers_fund.crime.replace(" ", "_").lower())
        is_coverage_type_included["crime"]["fund"] = True
        if "crime" not in layer_coverages:
            layer_coverages.append("crime")
        if "crime" not in coverage_by_tower[tower]:
            coverage_by_tower[tower].append("crime")

    if primary_layer.towers_all_manager.pi != "NA":
        layer_coverages.append("pi")
        towers_by_fund_manager["manager"].append(primary_layer.towers_all_manager.pi.replace(" ", "_").lower())
        tower = primary_layer.towers_all_manager.pi.replace(" ", "_").lower()
        coverage_by_tower[tower].append("pi")
        is_coverage_type_included["pi"]["manager"] = True
    if primary_layer.towers_fund.pi != "NA":
        tower = primary_layer.towers_fund.pi.replace(" ", "_").lower()
        towers_by_fund_manager["fund"].append(primary_layer.towers_fund.pi.replace(" ", "_").lower())
        if "pi" not in coverage_by_tower[tower]:
            coverage_by_tower[tower].append("pi")
        if "pi" not in layer_coverages:
            layer_coverages.append("pi")
        is_coverage_type_included["pi"]["fund"] = True

    if primary_layer.towers_all_manager.do != "NA":
        is_coverage_type_included["do"]["manager"] = True
        tower = primary_layer.towers_all_manager.do.replace(" ", "_").lower()
        towers_by_fund_manager["manager"].append(primary_layer.towers_all_manager.do.replace(" ", "_").lower())
        if "do" not in layer_coverages:
            if primary_layer.do_type:
                layer_coverages += list(primary_layer.do_type)
            else:
                layer_coverages += list("A")

        if "do" not in coverage_by_tower[tower]:
            coverage_by_tower[tower].append("do")

    if primary_layer.towers_fund.do != "NA":
        is_coverage_type_included["do"]["fund"] = True
        tower = primary_layer.towers_fund.do.replace(" ", "_").lower()
        towers_by_fund_manager["fund"].append(primary_layer.towers_fund.do.replace(" ", "_").lower())
        if "do" not in layer_coverages:
            if primary_layer.do_type:
                layer_coverages += list(primary_layer.do_type)
            else:
                layer_coverages += list("A")

        if "do" not in coverage_by_tower[tower]:
            coverage_by_tower[tower].append("do")


    sir_by_coverage = {
        "crime": {"manager": 0, "fund": 0},
        "pi": {"manager": 0, "fund": 0},
        "A": {"manager": 0, "fund": 0},
        "B": {"manager": 0, "fund": 0},
        "C": {"manager": 0, "fund": 0},
        "Dic": {"manager": 0, "fund": 0},
    }

    do_sir_manager_value = (
        primary_layer.sir_all_manager.do or 0
        if is_coverage_type_included["do"]["manager"]
        else 0
    ) / fixed_exp_live_cover
    do_sir_fund_value = (
        primary_layer.sir_fund.do or 0
        if is_coverage_type_included["do"]["fund"]
        else 0
    ) / fixed_exp_live_cover

    sir_by_coverage["crime"]["manager"] = (
        primary_layer.sir_all_manager.crime
        or 0
        if is_coverage_type_included["crime"]["manager"]
        else 0
    ) / fixed_exp_live_cover
    sir_by_coverage["pi"]["manager"] = (
        primary_layer.sir_all_manager.pi
        or 0
        if is_coverage_type_included["pi"]["manager"]
        else 0
    ) / fixed_exp_live_cover
    sir_by_coverage["A"]["manager"] = (
        do_sir_manager_value if hxd.non_cds.cover_details.do_side_a_show else 0
    )
    sir_by_coverage["B"]["manager"] = (
        do_sir_manager_value if hxd.non_cds.cover_details.do_side_b_show else 0
    )
    sir_by_coverage["C"]["manager"] = (
        primary_layer.sir_all_manager.do_side_c or 0
    )
    sir_by_coverage["Dic"]["manager"] = 0 if (sir_by_coverage["A"]["manager"]
        +
        sir_by_coverage["B"]["manager"]
        +
        sir_by_coverage["C"]["manager"]) == 0 else (
        (sir_by_coverage["A"]["manager"] * base_rate_by_coverage["A"]["manager"]
        +
        sir_by_coverage["B"]["manager"] * base_rate_by_coverage["B"]["manager"]
        +
        sir_by_coverage["C"]["manager"] * base_rate_by_coverage["C"]["manager"])
        /
        (base_rate_by_coverage["A"]["manager"]
        +
        base_rate_by_coverage["B"]["manager"]
        +
        base_rate_by_coverage["C"]["manager"])
    )
    sir_by_coverage["crime"]["fund"] = (
        primary_layer.sir_fund.crime or 0
        if is_coverage_type_included["crime"]["fund"]
        else 0
    ) / fixed_exp_live_cover
    sir_by_coverage["pi"]["fund"] = (
        primary_layer.sir_fund.pi or 0
        if is_coverage_type_included["pi"]["fund"]
        else 0
    ) / fixed_exp_live_cover
    sir_by_coverage["A"]["fund"] = (
        do_sir_fund_value if hxd.non_cds.cover_details.do_side_a_show else 0
    )
    sir_by_coverage["B"]["fund"] = (
        do_sir_fund_value if hxd.non_cds.cover_details.do_side_b_show else 0
    )
    sir_by_coverage["C"]["fund"] = (
        primary_layer.sir_fund.do_side_c or 0
    )
    sir_by_coverage["Dic"]["fund"] = 0 if (sir_by_coverage["A"]["fund"]
        +
        sir_by_coverage["B"]["fund"]
        +
        sir_by_coverage["C"]["fund"]) == 0 else (
        (sir_by_coverage["A"]["fund"] * base_rate_by_coverage["A"]["fund"]
        +
        sir_by_coverage["B"]["fund"] * base_rate_by_coverage["B"]["fund"]
        +
        sir_by_coverage["C"]["fund"] * base_rate_by_coverage["C"]["fund"])
        /
        (base_rate_by_coverage["A"]["fund"]
        +
        base_rate_by_coverage["B"]["fund"]
        +
        base_rate_by_coverage["C"]["fund"])
    )

    primaries = {
        "is_coverage_type_included": is_coverage_type_included, 
        "sir_by_coverage": sir_by_coverage, 
        "layer_coverages": layer_coverages, 
        "towers_by_fund_manager": towers_by_fund_manager, 
        "coverage_by_tower": coverage_by_tower
    }

    return primaries