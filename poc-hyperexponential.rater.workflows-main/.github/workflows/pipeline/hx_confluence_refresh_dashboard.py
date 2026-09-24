#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Refresh Dashboard
#' Author: Mark Fleet
#' Date: 12/03/2025
#' Description: Refreshes Confluence dashboard showing the Hx Model Versions in each environment
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from hx_auth import AzureADCredentials, HxRenewAuth
from api_requests import api_request_retry
from hx_misc import parse_model_versions_label, get_latest_model_version
import json
import os
from atlassian import Confluence
from pandas import DataFrame, read_html
from io import StringIO

# Load secrets/variables from GitHub Actions environment variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
environment = os.environ.get("ENVIRONMENT")
confluence_base_url = os.environ.get("CONFLUENCE_BASE_URL")
confluence_dashboard_page_id = os.getenv("CONFLUENCE_DASHBOARD_PAGE_ID")
confluence_api_username = os.getenv("CONFLUENCE_API_USERNAME")
confluence_api_token = os.getenv("CONFLUENCE_API_TOKEN")
hx_base_url = os.environ.get("HX_API_BASE_URL")
hx_tenant_id = os.environ.get("HX_AZURE_AD_TENANTID")
hx_client_id = os.environ.get("HX_AZURE_AD_CLIENTID")
hx_client_secret = os.environ.get("HX_AZURE_AD_CLIENTSECRET")
hx_scope = os.environ.get("HX_AZURE_AD_SCOPE")
hx_models_string = os.environ.get("HX_MODELS_STRING")

# Confluence Auth
conf = Confluence(
    url = confluence_base_url,
    username = confluence_api_username,
    password = confluence_api_token)

# Hx Auth
hx_auth = HxRenewAuth(
    AzureADCredentials(
        azure_ad_tenant = hx_tenant_id,
        client_id = hx_client_id,
        client_secret = hx_client_secret,
        grant_type="client_credentials",
        scope = hx_scope,
    )
)

# Hx headers
hx_headers = {"Authorization": f"Bearer {hx_auth.bearer_token}"}

def main():

    # Get the existing Confluence table
    existing_content = fetch_confluence_page()
    df = read_table(existing_content)

    # Dashboard environment heading
    dashboard_environment = get_environment_dashboard_heading(environment)

    # Parse models
    hx_models = json.loads(hx_models_string)

    # Model versions url
    if dashboard_environment == "PROD":
        model_versions_url = f"{hx_base_url}model-versions?sort=-id&limit=1000&published=true"
    else:
        model_versions_url = f"{hx_base_url}model-versions?sort=-id&limit=1000&testable=true"

    # Get model versions
    model_versions_resp = api_request_retry("get", model_versions_url, headers=hx_headers)
    if model_versions_resp.status_code != 200:
        raise Exception(f"Failed to get published model versions")
    model_versions = model_versions_resp.json()

    # Parse model versions
    model_versions = parse_model_versions_label(model_versions, True)

    # Loop through model mappings
    df_new = df.copy()
    for m in hx_models:

        # Get latest model version id for each model
        model_id = m['model_id'][environment]
        model_name = m['model_name']
        model_version_id, model_version_label = get_latest_model_version(model_versions, model_id)

        # Update table with label
        update_table_value(df_new, model_name, dashboard_environment, model_version_label)

        # For Prod, update the 'Is Rater Live?' column
        if dashboard_environment == "PROD":
            update_table_value(df_new, model_name, 'Is Rater Live?', model_version_id != None)

    # Clean table rows not in model mappings
    df_new = filter_table_rows(df_new, [m['model_name'] for m in hx_models])

    # Check if dashboard already in sync
    dashboard_in_sync = df_new.equals(df)

    # Replace NaN and None
    df_new = df_new.fillna('N/A')
            
    # Update the Confluence page if required
    if dashboard_in_sync:
        print("Dashboard already in sync")
    else:
        print("Updating Dashboard")
        new_content = create_page_content(df_new)
        update_confluence_page(new_content)

def get_environment_dashboard_heading(environment):
    match environment:
        case 'us-dev':
            return 'DEV'
        case 'us-tst':
            return 'TST'
        case 'us-pre-prod':
            return 'PREPROD'
        case 'us-prd':
            return 'PROD'
        case _:
            return environment

def fetch_confluence_page():
    page = conf.get_page_by_id(confluence_dashboard_page_id, expand='body.view')
    page_content = page['body']['view']['value']
    return page_content

def read_table(page_content):
    try:
        tables = read_html(StringIO(page_content), header = 0, index_col = 0)
        df = tables[0]
    except:
        df = create_empty_table()
    return df

def create_empty_table():
    df = DataFrame(columns=['DEV','TST','PREPROD','PROD','Is Rater Live?'])
    return df

def create_page_content(df):
    table_html = df.to_html(bold_rows = True)
    page_content = f"""<p>This dashboard provides model label details of the latest model version of all the rater’s on each of the Hyperexponential environment. </p>
        <p><em>(This page is automatically updated by the workflows that are used to move models between the various Hyperexponential environments)</em></p>
        <div class="table-wrap">
        {table_html}
        </div>"""
    return page_content

def update_confluence_page(page_content):
    conf.update_page(
        confluence_dashboard_page_id,
        title="Hx Rater Model Version Dashboard",
        body=page_content,
        parent_id=None,
        type='page',
        representation='storage',
        minor_edit=True
    )

def update_table_value(df, row, column, value):
    df.at[row, column] = value

def filter_table_rows(df, in_list):
    df_filtered = df[df.index.isin(in_list)]
    return df_filtered

if __name__ == "__main__":
    main()

