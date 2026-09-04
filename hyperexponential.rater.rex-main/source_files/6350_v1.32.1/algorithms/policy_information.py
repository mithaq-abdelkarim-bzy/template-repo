import hx, datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from algorithms.constant import MAX_ADDITIONAL_REFERENCES


def policy_information_mapping(hxd):
    '''
    Populate mapping for policy information section
    '''

    # Mapping for team/uw office and waiting period
    team_df = hx.params.team

    if hxd.policy_information.underwriter:
        team_df_row = team_df[team_df["Initials"] == hxd.policy_information.underwriter]
        hxd.policy_information.team = team_df_row["Team"].iloc[0]
        hxd.policy_information.uw_office = team_df_row["Office"].iloc[0]

    if hxd.policy_information.team in ["Open Market", "Renewables", "European Commercial Property"]:
        hxd.policy_information.bi_waiting_period.calculated = 2
        hxd.policy_information.bi_indemnity_period.calculated = 365
    elif hxd.policy_information.team == "NACP":
        hxd.policy_information.bi_waiting_period.calculated = 3
        hxd.policy_information.bi_indemnity_period.calculated = 30
    else:
        hxd.policy_information.bi_waiting_period.calculated = 0
        hxd.policy_information.bi_indemnity_period.calculated = 0
    
    # Mapping for policy length
    date_diff = (hxd.hx_core.expiry_date - hxd.hx_core.inception_date).days

    if date_diff == 0:
        hx.errors.validation("Expiry Date must not be prior or equal to Inception Date")      

    if hxd.policy_information.team in ["Open Market", "European Commercial Property"]:
        date_diff += 1

    leap_day = leap_day_in_duration(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    # hxd.policy_information.policy_length = date_diff / (365 + leap_day)
    hxd.policy_information.policy_length.calculated = date_diff / (365 + leap_day)


    # Is NACP/OM?
    hxd.policy_information.is_nacp = (hxd.policy_information.team == "NACP" or hxd.policy_information.team == "European Commercial Property")
    hxd.policy_information.is_om = (hxd.policy_information.team == "Open Market" or hxd.policy_information.team == "European Commercial Property")

    
    #show useful links
    generate_fac_powerapp_link(hxd)
    generate_user_guide_link(hxd)


def leap_day_in_duration(start_date, end_date):
    check_date = start_date
    while check_date <= end_date:
        if last_day_of_month(check_date).day == 29:  # this is true only on leap years in february
            return 1
        
        check_date = check_date + relativedelta(months=+6)

    return 0



def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - datetime.timedelta(days=next_month.day)

def generate_fac_powerapp_link(hxd):
    #Create URL for embedding
    url = "https://web.powerapps.com/apps/87badb17-daf7-49fc-baa2-4f868a63eb72"

    #Set note with url
    hxd.policy_information.fac_powerapp_note = f"[Click to open the Fac PowerApp]({url})"

def generate_user_guide_link(hxd):
    #Create URL for embedding
    url = f"https://beazley.sharepoint.com/:f:/r/sites/ActuarialPricing/Shared%20Documents/Property/Property%20User%20Guides/1.%20Commercial%20Property?csf=1&web=1&e=EZdr37"

    #Set note with url
    hxd.policy_information.user_guide_note = f"[User guide and training videos]({url})"


def upsert_hx_meta_pas_references(hxd):
    hx.meta.pas_references.clear()
    pas_references_set = set()

    valid_statuses = ["Bound", "MTA"]

    for layer in hxd.layers:
        # add the main reference for each layer
        if layer.status not in valid_statuses:
            continue

        reference = layer.reference
        if reference and len(reference) > 0:
            pas_references_set.add(reference)

        # add the additional references for each layer (if they exist)
        for i in range(1, MAX_ADDITIONAL_REFERENCES + 1):
            additional_reference = getattr(layer, f"additional_reference_{i}", "")
            if additional_reference:
                pas_references_set.add(additional_reference)


    if not pas_references_set:
        hx.errors.fatal("No bound layers found with a valid reference. PAS references not added.")
        return

    

    hx.meta.pas_references.extend(list(pas_references_set))


def generate_tags(hxd):
    df = pd.DataFrame(hx.params.team)
    df = df.set_index(df.columns[0])

    uw_initials = hxd.policy_information.underwriter

    # Replacing whitespace as HX does not accept whitespaces in tags
    uw_full_name = df.loc[uw_initials][df.columns[0]].replace(" ", "_")
    uw_team = hxd.policy_information.team.replace(" ", "")
    
    hx.meta.policy_tags = [uw_initials, uw_full_name, uw_team]