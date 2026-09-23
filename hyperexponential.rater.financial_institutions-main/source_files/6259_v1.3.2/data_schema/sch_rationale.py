import hx_data_schema as hxd


def sch_rationale(cds):
    cds.extend_node_rater_defined("cds", {
        "rationale": hxd.Structure(children={
            "general_comments": hxd.Str(mode="input", default=""),
            "bpi_comments": hxd.Str(mode="input", default=""),
            "other_factors_comments": hxd.Str(mode="input", default=""),
            "esg_comments": hxd.Str(mode="input", default=""),
            "reason_comments": hxd.Str(mode="input", default=""),
            "additional_info_path": hxd.Str(mode="input", default="")
        })
    })
