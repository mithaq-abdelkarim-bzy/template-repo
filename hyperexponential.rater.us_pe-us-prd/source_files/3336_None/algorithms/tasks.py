import hx


# Update example task below
@hx.task
def example_empty_task(hxd, progress):
    pass


# Importing expiring policy for rate change
"""
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
"""


@hx.task
def generate_email(hxd, progress):
    # Not sure exactly what to do here yet
    raise ValueError("Hi, generate email is not implemented yet")


@hx.task
def bind_option(hxd, progress):
    # Not sure exactly what to do here yet
    raise ValueError("Hi, bind_option is not implemented yet")


@hx.task
def expiring_policy_fetch_task(hxd, progress):
    user = hx.secrets.rest_api_user
    password = hx.secrets.rest_api_password

    expiring_policy_option_id = hxd.expiring_policy_option_id.selected
    # expiring_policy_option_id = 75787     # Uncomment for build / debugging

    # URL for the API
    # SA: you should be using the v2 API. v1 will be depreciated at some point. HCM: Updated
    url = f"https://api.beazley.hxrenew.com/api/v2-beta/policy-options/{expiring_policy_option_id}/snapshot"

    # Update the below params variable to include all the variables which will be needed for the rate change calculation

    params = {
        "path": [
            # UPDATE FROM HERE >>
            "/brokerage",
            "/insured",
            "/policy_reference",
            "/final_premium",
            "/hx_core/inception_date",
            "/yoa",
            # ~~~~~~~
        ]
    }

    # Call to API (do not update)
    try:
        response = requests.get(url, params=params, auth=(user, password))
    except requests.RequestException:
        hx.errors.fatal("Unable to connect to Renew REST API")

    # Function assigns the data from the expiring policy option to variables in the current policy.
    # It can handle loops and functions.

    # Error handling based on status code returned by API (do not update)
    if response.ok:
        # results stored in dict : {data:{variable_name: value}}
        result = response.json()
        data = result["data"]

        # UPDATE FROM HERE >>

        hxd.expiring_brokerage = data["brokerage"]
        hxd.expiring_insured_name = data["insured"] + " - " + str(data["yoa"])
        hxd.expiring_policy_reference = data["policy_reference"]
        hxd.expiring_premium = data["final_premium"]

        # ~~~~~~~~~~~~~~

    # Raises error if status code is not 200 (do not update)
    else:
        try:
            response_json = response.json()
            error = f"Error: {response_json.get('title')}"
            error += (
                f"\nDetail: {response_json.get('detail')}"
                if response_json.get("detail")
                else ""
            )
            hx.errors.fatal(error)
        except:
            hx.errors.fatal(f"Error: {response.text}")

    pass
