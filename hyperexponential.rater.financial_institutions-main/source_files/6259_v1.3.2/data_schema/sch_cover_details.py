import hx_data_schema as hxd

from algorithms.rate_constants import max_towers
from libraries.common_data_schema.data_schema.utilities import percent_format


def sch_cover_details_non_cds():
    return {
        "cover_details": hxd.Structure(children={
            "num_layers": hxd.Int(mode="input", default=1, async_input=["num_layers_task"], view={"label": "Number of Layers"}),
            "is_brokerage_all_layers": hxd.Bool(mode="input", default=True, view={"label": "Apply brokerage & discounts on all layers"}),
            "is_brokerage_all_layers_not": hxd.Bool(mode="output"),
            "is_premium_split_all_layers": hxd.Bool(mode="input", default=True, view={"label": "Apply split of premium on all layers"}),
            "premium_split_missing_amount": hxd.Float(mode="output", view={
                "label": "Missing Amounts", 
                "format": percent_format(mantissa=2), 
                "options": {"bad": {"style_cell": "hx-bad"}}
            }),
            "show_premium_split_missing_amount": hxd.Bool(mode="output"),
            "show_bad_premium_split_missing_amount": hxd.Bool(mode="output"),
            "all_manager_show": hxd.Bool(mode="output"),
            "fund_show": hxd.Bool(mode="output"),
            "do_side_a_show": hxd.Bool(mode="output"),
            "do_side_b_show": hxd.Bool(mode="output"),
            "do_side_c_show": hxd.Bool(mode="output"),
            "direct_reinstatements_show": hxd.Bool(mode="output"),
            "rtc_limit_show": hxd.Bool(mode="output"),
            "premium_split_show": hxd.Bool(mode="output"),
            "premium_split_coverages_show": hxd.Bool(mode="output"),
            "show_different_towers_manager_fund_warning": hxd.Bool(mode="output"),
            "different_towers_manager_fund_warning": hxd.Str(mode="input",
                default="Functionality to vary coverage offered up the tower is unavailable on 'Rating Summary' due to Manager/Fund being on different towers.",
                view={
                    "options": {"read_only_option": {"read_only": True}}
                }
             ),
            **get_towers_show_fields()
        })
    }


def get_towers_show_fields():
    return {
        **{f"tower_{i}_show": hxd.Bool(mode="output") for i in range(1, max_towers+1)}
    }
