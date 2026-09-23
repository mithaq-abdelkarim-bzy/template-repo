import hx_data_schema as hx

# Extending coverages for the required cds items
def cds_set_coverages(cds):
    cds.extend_node_items("cds/layers/coverages", {
        # Jewellers Block
        **{
            f"jb_{sub_group}": {"label": f"{sub_group}".capitalize()}
            for sub_group in ["premises", "travel", "additional"]
        },
        f"jb_premises": {"label": f"jb_premises"},
        f"jb_travel": {"label": f"jb_travel"},
        f"jb_specific": {"label": "jb_specific"},

        # Cash in Transit
        **{
            f"cit_{sub_group}": {"label": f"{sub_group}".capitalize()}
            for sub_group in ["premises", "additional"]
        },

        # General Specie
        **{
            f"gs_{type_in}": {"label": f"{type_in}".capitalize()}
            for type_in in ["metals", "cash", "securities", "additional"]
        },
        f"gs_metals": {"label": "gs_metals"},
        f"gs_cash": {"label": "gs_cash"},
        f"gs_securities": {"label": "gs_securities"},
        f"gs_additional": {"label": "Additional"},

        # Fine Art
        **{
            f"fa_{type_in}": {"label": f"{type_in}".capitalize()}
            for type_in in ["premises", "travel", "additional"]
        },
        **{
            f"fa_{premise}_summary": {"label": f"{premise}".capitalize()}
            for premise in ["static_art", "exhibitions", "fa_misc"]
        },
        **{
            f"fa_{premise}_summary_rates": {"label": f"fa_{premise}_summary_rates"}
            for premise in ["static_art", "exhibitions", "fa_misc"]
        },
        **{
            f"fa_{premise}_summary_subtotal": {"label": f"Sub-Total"}
            for premise in ["static_art", "exhibitions", "fa_misc"]
        },
        f"fa_travel": {"label": ""},
        f"fa_specific": {"label": ""},

        # Final Selections and Summary
        **{
            f"final_jb_{sub_group}_summary": {"label": f"final_jb_{sub_group}_summary"}
            for sub_group in ["premises", "travel", "additional"]
        },
        **{
            f"final_fa_{sub_group}_summary": {"label": f"final_fa_{sub_group}_summary"}
            for sub_group in ["premises", "travel", "additional"]
        },
        **{
            f"final_gs_{sub_group}_summary": {"label": f"final_gs_{sub_group}_summary"}
            for sub_group in ["metals", "cash", "securities"]
        },
        **{
            f"final_cit_{sub_group}_summary": {"label": f"final_cit_{sub_group}_summary"}
            for sub_group in ["premises", "additional"]
        }
    })