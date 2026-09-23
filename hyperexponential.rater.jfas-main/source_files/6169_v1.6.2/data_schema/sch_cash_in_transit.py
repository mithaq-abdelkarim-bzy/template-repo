import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_cash_in_transit(cds):
    for sub_group in ["premises", "additional"]:
        cds.extend_node_rater_defined(f"cds/layers/coverages/cit_{sub_group}", {
            "tsi": hx.Float(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
            # "deductible": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Ded", "format": thousands_format()}),
            "ded_perc": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Ded Perc", "format": percent_format()}),
            "credit": hx.Float(mode="output", view={"label": "Credit", "format": percent_format()}),
            # "uw_adj_impact": hx.Float(mode="input", default=None, optionality="optional", view={"label": "UW Select Credit", "format": percent_format()}),
            "prem_post_ded": hx.Float(mode="output", view={"label": "Prem Post Ded", "format": thousands_format()}),
            "implied_rate_post_ded": hx.Float(mode="output", view={"label": "Implied Rate Post Ded", "format": percent_format(3)}),
            "prem_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Prem Last Year", "format": thousands_format()}),
            "tsi_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "TSI Last Year (cnv)", "format": thousands_format()}),
            "ded_credit_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Ded Credit Last Year", "format": percent_format()}),
            "uw_adj_impact_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "UW Select Credit Last Year", "format": percent_format()}),
            "prem_post_ded_ly": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Prem Post Ded Last Year", "format": thousands_format()}),
        })

        cds.override_node_properties(f"cds/layers/coverages/cit_{sub_group}/premium", {"mode": "output", "view": {"label": "Premium"}})
        cds.override_node_properties(f"cds/layers/coverages/cit_{sub_group}/uw_adj_impact", {"mode": "input", "default": None, "optionality": "optional", "view": {"label": "Uw Select Credit", "format": percent_format(3)}})


    cds.extend_node_rater_defined(f"cds/layers", {
        "cit_general_summary": hx.List(mode="output", children={ 
            "country": hx.Str(mode="output", view={"label": "Country"}),
            "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
            "exp_band_1": hx.Float(mode="output", view={"label": "1m", "format": thousands_format()}),
            "exp_band_2": hx.Float(mode="output", view={"label": "3m", "format": thousands_format()}),
            "exp_band_3": hx.Float(mode="output", view={"label": "5m", "format": thousands_format()}),
            "exp_band_4": hx.Float(mode="output", view={"label": "10m", "format": thousands_format()}),
            "exp_band_5": hx.Float(mode="output", view={"label": "20m", "format": thousands_format()}),
            "exp_band_6": hx.Float(mode="output", view={"label": ">20m", "format": thousands_format()}),
            "rate_band_1": hx.Float(mode="output", view={"label": "1m", "format": percent_format(3)}),
            "rate_band_2": hx.Float(mode="output", view={"label": "3m", "format": percent_format(3)}),
            "rate_band_3": hx.Float(mode="output", view={"label": "5m", "format": percent_format(3)}),
            "rate_band_4": hx.Float(mode="output", view={"label": "10m", "format": percent_format(3)}),
            "rate_band_5": hx.Float(mode="output", view={"label": "20m", "format": percent_format(3)}),
            "rate_band_6": hx.Float(mode="output", view={"label": ">20m", "format": percent_format(3)}),
        })
    })

    cds.extend_node_rater_defined(f"cds/layers", {
        "cit_general_summary_subtotal": hx.Structure(children={
            "tsi": hx.Float(mode="output", view={"label": "TSI", "format": thousands_format()}),
            "exp_band_1": hx.Float(mode="output", view={"label": "1m", "format": thousands_format()}),
            "exp_band_2": hx.Float(mode="output", view={"label": "3m", "format": thousands_format()}),
            "exp_band_3": hx.Float(mode="output", view={"label": "5m", "format": thousands_format()}),
            "exp_band_4": hx.Float(mode="output", view={"label": "10m", "format": thousands_format()}),
            "exp_band_5": hx.Float(mode="output", view={"label": "20m", "format": thousands_format()}),
            "exp_band_6": hx.Float(mode="output", view={"label": ">20m", "format": thousands_format()}),
            "rate_band_1": hx.Float(mode="output", view={"label": "1m", "format": percent_format(3)}),
            "rate_band_2": hx.Float(mode="output", view={"label": "3m", "format": percent_format(3)}),
            "rate_band_3": hx.Float(mode="output", view={"label": "5m", "format": percent_format(3)}),
            "rate_band_4": hx.Float(mode="output", view={"label": "10m", "format": percent_format(3)}),
            "rate_band_5": hx.Float(mode="output", view={"label": "20m", "format": percent_format(3)}),
            "rate_band_6": hx.Float(mode="output", view={"label": ">20m", "format": percent_format(3)}),
        })
    })

    # Default coverages
    for coverage in range(9):
        cds.extend_node_rater_defined(f"cds/layers/coverages/cit_additional", {
            f"specific_{coverage}": hx.Structure(children={
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "usa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "USA", "format": thousands_format()}),
                "na_ex_usa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "North America (ex USA)", "format": thousands_format()}),
                "sa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "South America", "format": thousands_format()}),
                "uk": hx.Float(mode="input", default=None, optionality="optional", view={"label": "UK", "format": thousands_format()}),
                "europe": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Europe", "format": thousands_format()}),
                "asia": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Asia", "format": thousands_format()}),
                "oceania": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Oceania", "format": thousands_format()}),
                "africa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Africa", "format": thousands_format()}),
                "total": hx.Float(mode="output", view={"label": "Total", "format": thousands_format()}),
                "rate_usa": hx.Float(mode="output", view={"label": "USA", "format": percent_format(3)}),
                "rate_na_ex_usa": hx.Float(mode="output", view={"label": "North America (ex USA)", "format": percent_format(3)}),
                "rate_sa": hx.Float(mode="output", view={"label": "South America", "format": percent_format(3)}),
                "rate_uk": hx.Float(mode="output", view={"label": "UK", "format": percent_format(3)}),
                "rate_europe": hx.Float(mode="output", view={"label": "Europe", "format": percent_format(3)}),
                "rate_asia": hx.Float(mode="output", view={"label": "Asia", "format": percent_format(3)}),
                "rate_oceania": hx.Float(mode="output", view={"label": "Oceania", "format": percent_format(3)}),
                "rate_africa": hx.Float(mode="output", view={"label": "Africa", "format": percent_format(3)}),
                "rate_total": hx.Float(mode="output", view={"label": "Total", "format": percent_format(3)}),
            })
        })

    # User specified coverages
    cds.extend_node_rater_defined(f"cds/layers/coverages/cit_additional", {
        "specific_custom": hx.List(mode="input", children={ 
            "coverage": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Coverage"}),
            "usa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "USA", "format": thousands_format()}),
            "na_ex_usa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "North America (ex USA)", "format": thousands_format()}),
            "sa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "South America", "format": thousands_format()}),
            "uk": hx.Float(mode="input", default=None, optionality="optional", view={"label": "UK", "format": thousands_format()}),
            "europe": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Europe", "format": thousands_format()}),
            "asia": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Asia", "format": thousands_format()}),
            "oceania": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Oceania", "format": thousands_format()}),
            "africa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Africa", "format": thousands_format()}),
            "total": hx.Float(mode="output", view={"label": "Total", "format": thousands_format()}),
            "rate_usa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "USA", "format": percent_format(3)}),
            "rate_na_ex_usa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "North America (ex USA)", "format": percent_format(3)}),
            "rate_sa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "South America", "format": percent_format(3)}),
            "rate_uk": hx.Float(mode="input", default=None, optionality="optional", view={"label": "UK", "format": percent_format(3)}),
            "rate_europe": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Europe", "format": percent_format(3)}),
            "rate_asia": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Asia", "format": percent_format(3)}),
            "rate_oceania": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Oceania", "format": percent_format(3)}),
            "rate_africa": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Africa", "format": percent_format(3)}),
            "rate_total": hx.Float(mode="output", view={"label": "Total", "format": percent_format(3)}),
        })
    })
