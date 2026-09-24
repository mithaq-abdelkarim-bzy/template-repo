import hx 

def shownby_conditions_pcl(hxd, state_info):
    # set out the conditional statements for the shownby tables in the view
    hxd.non_cds.is_table_cw = state_info.get("schedule_rating_table") == "tblPCL_ScheduleRatingCW"
    hxd.non_cds.is_table_ca = state_info.get("schedule_rating_table") == "tblPCL_ScheduleRatingCA"
    hxd.non_cds.is_table_la = state_info.get("schedule_rating_table") == "tblPCL_ScheduleRatingLA"
    hxd.non_cds.is_table_mo = state_info.get("schedule_rating_table") == "tblPCL_ScheduleRatingMO"
    hxd.non_cds.is_state_ne = state_info["state_code"] == "NE"
    hxd.non_cds.is_surplus = True if state_info["state_code"] == "Surplus" else False
    hxd.non_cds.is_pcl_finished_rating = not(hxd.cds.package_information.finished_rating)

    #set the premium label
    if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
        hxd.non_cds.pcl_premium_label = "Surplus Premium"
    else:
        hxd.non_cds.pcl_premium_label = "Admitted Premium"