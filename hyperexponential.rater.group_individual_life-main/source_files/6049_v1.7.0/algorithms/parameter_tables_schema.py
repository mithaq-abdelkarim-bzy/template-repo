from libraries.tp_parameters.algorithms.parameter_tables import ParameterTable


tp_parameters = ParameterTable.from_csv("libraries/tp_parameters/algorithms/parameter_tables/tp_parameters.csv", schema={
    "business_plan_class": "str",
    "year": "int",
    "che": "float",
    "var_exp": "float",
    "inv_inc": "float",
    "cost_of_ri": "float",
    "ri_rec": "float",
    "roc": "float",
    "fixed_exp": "float",
    "capital_req": "float",
    "nmp_load": "float",
})

fx_rates = ParameterTable.from_csv("libraries/fx_rates/algorithms/parameter_tables/fx_rates.csv", schema={
    "ccy": "str",
    "fx_rate": "float",
})