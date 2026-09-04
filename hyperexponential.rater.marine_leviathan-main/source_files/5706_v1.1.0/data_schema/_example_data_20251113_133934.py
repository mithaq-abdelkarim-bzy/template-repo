import hx_data_schema as hx


@hx.data_schema
def hx_calculation_legacy_initial_premium():
    return hx.Structure(children={
        "cds": hx.Structure(view={"label": "Cds"}, children={
            "experience_rating": hx.Structure(view={"label": "Experience Rating"}, children={
                "claims_available": hx.Bool(mode="input", default=False, view={"label": "Claims Available"}),
                "claims_fgu": hx.Bool(mode="input", default=False, view={"label": "Claims Fgu"}),
            }),
            "layers": hx.List(mode="input", children={
                "limit": hx.Float(mode="input", default=0, view={"label": "Limit"}),
                "excess": hx.Float(mode="input", default=0, view={"label": "Excess"}),
                "deductible": hx.Float(mode="input", default=0, view={"label": "Deductible"}),
                "quoted_premium": hx.Int(mode="input", default=0, view={"label": "Quoted Premium"}),
                "brokerage": hx.Float(mode="input", default=0, view={"label": "Brokerage"}),
                "written_line": hx.Float(mode="input", default=0, view={"label": "Written Line"}),
            }),
            "standard_fields": hx.Structure(view={"label": "Standard Fields"}, children={
                "is_renewal": hx.Bool(mode="input", default=False, view={"label": "Is Renewal"}),
            }),
            "rate_change": hx.Structure(view={"label": "Rate Change"}, children={
                "expiring_policy_option_id": hx.Structure(view={"label": "Expiring Policy Option Id"}, children={
                    "calculated": hx.???(mode="output", view={"label": "Calculated"}),
                    "override": hx.Int(mode="input", default=0, view={"label": "Override"}),
                    "is_dirty": hx.Bool(mode="input", default=False, view={"label": "Is Dirty"}),
                    "is_overridden": hx.Bool(mode="input", default=False, view={"label": "Is Overridden"}),
                    "overridden_calculated": hx.???(mode="output", view={"label": "Overridden Calculated"}),
                    "selected": hx.???(mode="output", view={"label": "Selected"}),
                }),
            }),
            "exposure": hx.Structure(view={"label": "Exposure"}, children={
                "aggregate": hx.Structure(view={"label": "Aggregate"}, children={
                    "example_aggregate_exposure": hx.Float(mode="input", default=0, view={"label": "Example Aggregate Exposure"}),
                }),
                "granular": hx.Structure(view={"label": "Granular"}, children={
                    "example_exposure": hx.List(mode="input", children={
                        "country": hx.Str(mode="input", default="", view={"label": "Country"}),
                        "city": hx.Str(mode="input", default="", view={"label": "City"}),
                        "type": hx.Str(mode="input", default="", view={"label": "Type"}),
                        "tiv": hx.Int(mode="input", default=0, view={"label": "Tiv"}),
                    }),
                }),
            }),
        }),
    })
