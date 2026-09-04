import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_model_state(cds):
    '''
    Internal Model State that controls the workflow
    '''
    # SA: Do these need to be in the cds?
    cds.extend_node_rater_defined("cds", {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task":   hx.Bool(mode="output"),
            "migrated_record":              hx.Bool(mode="output", view={"label": "Migrated Policy?"}), # this field is reset to False after running the renewal task
            "show_landing_page":            hx.Bool(mode="output"),
            "show_after_landing_page":      hx.Bool(mode="output"),
            "expiring_policy":              hx.Int( mode="input",    default=None, optionality="optional", view={"label": "recorded expiring policy ref"}) 
        }),
        "landing_page_note":    hx.Str(     mode    = "input"
                                          , default = "Please import expiring policy data using the button in the top right corner before pressing 'Start Policy'"
                                          , view    = { "options": {"read_only_option": {"read_only": True}}}),
                                        })