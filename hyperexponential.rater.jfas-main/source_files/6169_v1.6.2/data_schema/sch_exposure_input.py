import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_exposure_input(cds):
    cds.extend_node_rater_defined("cds", {
        "schedule": hx.List(mode="input", default_element_count=20, children={
            "risk_class": hx.Str(mode="output", view={"label": "Class"}),
            "region": hx.Str(mode="output", view={"label": "Region"}),
            "country": hx.Str(mode="input", default=None, optionality="optional", async_output=["clear_exposure_input_task"], view={"label": "Country"}, options_table="table_input_country_region", options_column="countries"),
            "currency": hx.Str(mode="input", default_index=0, async_output=["clear_exposure_input_task"], view={"label": "Currency"}, options_table="table_input_currency", options_column="ccy"), #"currency": hx.Str(mode="override", view={"label": "Currency"}, options_table="table_input_currency", options_column="ccy"),
            "type": hx.Str(mode="input", default=None, async_output=["clear_exposure_input_task"], view={"label": "Type"}, options_data="../../../risk_info/type_dropdown", options_field="type", optionality="optional"),
            "tsi": hx.Float(mode="input", default=0, async_output=["clear_exposure_input_task"], view={"label": "TSI", "format": thousands_format()}),
            "tsi_cnv": hx.Float(mode="output", view={"label": "TSI (cnv)", "format": thousands_format()}),
            "sanctioned_country": hx.Str(mode="output", view={"label": "Sanctioned\nCountry"}),
            "tsi_band_1": hx.Float(mode="output", view={"label": "500", "format": thousands_format()}),
            "tsi_band_2": hx.Float(mode="output", view={"label": "1,000", "format": thousands_format()}),
            "tsi_band_3": hx.Float(mode="output", view={"label": "2,000", "format": thousands_format()}),
            "tsi_band_4": hx.Float(mode="output", view={"label": "3,000", "format": thousands_format()}),
            "tsi_band_5": hx.Float(mode="output", view={"label": "5,000", "format": thousands_format()}),
            "tsi_band_6": hx.Float(mode="output", view={"label": "10,000", "format": thousands_format()}),
            "tsi_band_7": hx.Float(mode="output", view={"label": "20,000", "format": thousands_format()}),
            "tsi_band_8": hx.Float(mode="output", view={"label": "50,000", "format": thousands_format()}),
            "tsi_band_9": hx.Float(mode="output", view={"label": "100,000", "format": thousands_format()}),
            "tsi_band_10": hx.Float(mode="output", view={"label": ">100,000", "format": thousands_format()}),
        }),
        "schedule_prior": hx.List(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], children={
            "risk_class": hx.Str(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Class"}),
            "region": hx.Str(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Region"}),
            "country": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Country"}, options_table="table_input_country_region", options_column="countries"),
            "currency": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Currency"}, options_table="table_input_currency", options_column="ccy"),
            "type": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Type"}, optionality="optional"),
            "tsi": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "TSI", "format": thousands_format()}),
            "tsi_cnv": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label": "TSI (cnv)", "format": thousands_format()}),
            "sanctioned_country": hx.Str(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Sanctioned\nCountry"}),
            "tsi_band_1": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"],view={"label": "500", "format": thousands_format()}),
            "tsi_band_2": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "1,000", "format": thousands_format()}),
            "tsi_band_3": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "2,000", "format": thousands_format()}),
            "tsi_band_4": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "3,000", "format": thousands_format()}),
            "tsi_band_5": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "5,000", "format": thousands_format()}),
            "tsi_band_6": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "10,000", "format": thousands_format()}),
            "tsi_band_7": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "20,000", "format": thousands_format()}),
            "tsi_band_8": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "50,000", "format": thousands_format()}),
            "tsi_band_9": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "100,000", "format": thousands_format()}),
            "tsi_band_10": hx.Float(mode="output",async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": ">100,000", "format": thousands_format()}),
        }),
    })
        

        # "hx_core": hx.Structure(children={
        #     "inception_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Inception Date"}),
        #     "expiry_date": hx.Date(default="2018-12-31", mode="input", view={"label": "Expiry Date"}),
        #     "model_premium": hx.Float(mode="output", view={"label": "Model Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "charged_premium": hx.Float(mode="output", view={"label": "Charged Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        #     "premium_currency": hx.Str(mode="output", view={"label": "Premium Currency"}),
        #     "ulr": hx.Float(mode="output", view={"label": "ULR", "format": {"output": "percent", "mantissa": 1}}),
        #     "class_code": hx.Str(mode="output", view={"label": "Class Code"}),
        # }),
