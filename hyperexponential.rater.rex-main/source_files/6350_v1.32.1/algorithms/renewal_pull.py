import hx
import requests

def start_renewal(hxd):

    if not hxd.policy_information.underwriter:
        hx.errors.fatal("Please press 'Undo' and 'Import Expiring Policy Data' at the top right corner")
        
    hxd.model_state.pressed_start_renewal_task = True
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

    user = hx.secrets.rest_api_user
    password = hx.secrets.rest_api_password
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    environment_name = hx.secrets.environment_name.lower()


    # URL for the API
    url = f"https://api.{environment_name}.hxrenew.com/api/v1/policies/options/{expiring_policy_option_id}/snapshot"

    params = {
        "path": [
            "/policy_information/insured",
            "/policy_information/accgrpid",
            "/policy_information/account_group_name",
            "/layers"
        ]
    }

    # Call to API
    try:
        response = requests.get(url, params=params, auth=(user, password))
    except requests.RequestException:
        hx.errors.fatal("Unable to connect to Renew REST API")

    # Error handling based on status code returned by API
    if response.ok:
        # results stored in dict : {data:{variable_name: value}}
        result = response.json()
        data = result["data"]

        hxd.policy_information.insured = data['policy_information']['insured']

        accgrpid_base = data['policy_information']['accgrpid']
        account_group_name_base = data['policy_information']['account_group_name']

        # use the calculated value after changed from override to input
        if isinstance(accgrpid_base, dict):
            hxd.policy_information.accgrpid = accgrpid_base['selected']
        else:
            hxd.policy_information.accgrpid = accgrpid_base

        if isinstance(account_group_name_base, dict):
            hxd.policy_information.account_group_name = account_group_name_base['selected']
        else:
            hxd.policy_information.account_group_name = account_group_name_base
       
        for layer in hxd.layers:
            layer.reference = ""
            layer.status = "Quote"
            layer.new_renewal = "Renewal"

        # Set the expiring written line percentage to the quoted line. Written line percentage will be wiped as part of the start renewal task (as async output)
        for index, layer in enumerate(hxd.layers):
            setattr(layer, "quoted_line_perc", data['layers'][index]['written_line_perc'])

        if hxd.rationale.note_section.underwriter_thoughts == "- Thought process of the trade\n- Future concerns, intentions, or items to monitor" and not (hxd.rationale.comments in {None, ""}):
            hxd.rationale.note_section.underwriter_thoughts = hxd.rationale.comments
        
        hxd.rationale.first_saved = None