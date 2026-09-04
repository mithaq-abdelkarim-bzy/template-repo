import hx


def inflation(hxd, other_data):

    # Load parameter tables
    inflation_df = hx.params.inflation

    # Calculate Inflation
    year_month = f"{hxd.hx_core.inception_date.year}{hxd.hx_core.inception_date.month}"
    if year_month not in set(inflation_df['Month']) or not hxd.policy_information.team:
        other_data['inflation'] = 1
    else:
        other_data['inflation'] = 1 + inflation_df[inflation_df['Month'] == year_month][hxd.policy_information.team].iloc[0]
 
    return other_data