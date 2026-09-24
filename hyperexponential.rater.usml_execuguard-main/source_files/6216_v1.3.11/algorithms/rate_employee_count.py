import hx

from algorithms.rate_constants import states_list


def rate_employee_count(hxd):
    epl = hxd.cds.coverage_elections.epl    

    # set the boolean to show the employee count and epl page     
    hxd.non_cds.is_employee_count = epl    
    hxd.non_cds.coverage_elections.epl_pcl = (
        (epl or hxd.cds.coverage_elections.pcl) 
        and  hxd.model_state.show_after_landing_page
        and  hxd.cds.layers[0].is_primary_excess == "Primary"
    )


    # the target object must be defined inside the for loop otherwise it won't be used as a variable inside the for loop
    fte_total = 0
    pte_total = 0
    for state in states_list:
        target_object = getattr(hxd.cds.us_states, state)
        fte = target_object.fte or 0
        pte = target_object.pte or 0
        fte_total += fte
        pte_total += pte

    # set the front end values
    hxd.cds.us_states.Total.fte = fte_total
    hxd.cds.us_states.Total.pte = pte_total

    head_count = {
        "seasonal": hxd.cds.split.seasonal.head_count,
        "independent_contractors": hxd.cds.split.independent_contractors.head_count,
        "temporary": hxd.cds.split.temporary.head_count,
        "foreign": hxd.cds.split.foreign.head_count,
    }

    # if (
    #     (head_count["seasonal"] is not None or 
    #         head_count["independent_contractors"] is not None or
    #         head_count["temporary"] is not None or 
    #         head_count["foreign"] is not None) 
    #     and hxd.cds.comments == ""
    # ):    
    #     hx.errors.validation("Please enter rationale in Employee Count Comments.")
