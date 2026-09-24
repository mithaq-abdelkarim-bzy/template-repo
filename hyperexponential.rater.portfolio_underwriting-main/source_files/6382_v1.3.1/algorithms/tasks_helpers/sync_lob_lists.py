from algorithms import rate_constants as constants
from algorithms.rate_utilities import rgetattr


def sync_lob_lists(hxd):
    
    def sync_list(node, lob_list_length):
        current_length = len(node)
        if current_length > lob_list_length:
            target_length = max(lob_list_length, 1)
            while len(node) > target_length:
                del node[len(node) - 1]
        elif current_length < lob_list_length:
            for _ in range(lob_list_length - current_length):
                node.append({})        


    ### Section of code below syncs the list driven by SELECTED LOB
    ################################################################
    cds                 = hxd.cds
    lob_list_length     = hxd.non_cds.global_fields.required_sel_lob_table_length
    paths               = constants.NODES_DRIVEN_BY_SELECTED_LOB

    # syncing list for typical lists
    for path in paths:
        node = rgetattr(cds, path)
        sync_list(node, lob_list_length)

    # syncing list for detail table list which is the product of #lobs and #yrs to consider
    detail_list_length  = lob_list_length * constants.YEARS_TO_CONSIDER_IN_OWN_EXPERIENCE
    node                = cds.projections_own_experience.detail_table
    sync_list(node, detail_list_length)

    # custom for syncing the interior list within an exterior list which has already been synced
    for row in cds.pc.cm_ovd:
        node = row.cm_col
        sync_list(node, lob_list_length)


    ### Section of code below syncs the list driven by FACILITY LOB
    ################################################################
    lob_list_length     = hxd.non_cds.global_fields.required_fac_lob_table_length
    paths               = constants.NODES_DRIVEN_BY_FACILITY_LOB

    # syncing list for typical lists
    for path in paths:
        node = rgetattr(cds, path)
        sync_list(node, lob_list_length)


    ### Section of code below syncs the list driven by SELECTED_LOB & RISK CODE together
    #######################################################################################
    lob_list_length     = hxd.non_cds.global_fields.required_riskcode_table_length
    paths               = constants.NODES_DRIVEN_BY_RISK_CODES

    # syncing list for typical lists
    for path in paths:
        node = rgetattr(cds, path)
        sync_list(node, lob_list_length)

    # syncing list for detail table list which is the product of #lobs and #yrs to consider
    detail_list_length  = lob_list_length * constants.YEARS_TO_CONSIDER_IN_LLOYDS_PROJECTIONS
    node_lloyds         = cds.projections_lloyds.detail_table
    node_beazley        = cds.projections_beazley.detail_table
    sync_list(node_lloyds,  detail_list_length)
    sync_list(node_beazley, detail_list_length)

