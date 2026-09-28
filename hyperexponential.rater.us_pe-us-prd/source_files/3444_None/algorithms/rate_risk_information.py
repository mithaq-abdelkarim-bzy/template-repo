import hx  # Importing the hx module


# Function to rate risk information and populate dynamic lists
def rate_risk_information(hxd):

    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id
