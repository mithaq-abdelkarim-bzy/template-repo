import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, create_node
from algorithms import rate_constants as constants


def get_node_mode(calculated_value=None, is_summary=False):
    if is_summary:
        return 'output'
    return calculated_value



def generate_common_nodes(is_summary):
    children = {
        'lob': create_node('Line of Business', mode=get_node_mode("override", is_summary), type='str', async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'selected_lob': create_node('Selected Line\n of Business', mode=get_node_mode("override", is_summary), type='str', async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'assigned_trifocus': create_node('Assigned Trifocus', mode=get_node_mode("override", is_summary), type='str', async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'max_limit_at_100_per': create_node('Maximum Limit\n @ 100%', mode=get_node_mode("input", is_summary), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'avg_limit_at_100_per': create_node('Average Limit\n @ 100%', mode=get_node_mode("input", is_summary), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'avg_attachment_point': create_node('Average Attachment\n Point', mode=get_node_mode("input", is_summary), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'primary': create_node('Primary %', mode=get_node_mode("input", is_summary), format=percent_format(0), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'max_limit_at_bst_share': create_node('Maximum Limit\n @ BST Share', mode=get_node_mode("input", is_summary), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'future_ultimate_gross_prem': create_node('Future Ultimate Gross\n Premium @ 100%', mode=get_node_mode("input", is_summary), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'bst_share_line_size': create_node('BST Share / Line Size', mode=get_node_mode("override", is_summary), format=percent_format(2), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'bst_share_ultimate_gross_premium': create_node('BST Share Ultimate\n Gross Premium', mode='output',  async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'bst_deductions': create_node('BST Deductions',  mode='output', format=percent_format(2), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'bst_net_premium': create_node('BST Net Premium', mode=get_node_mode("override", is_summary), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
        'portfolio_composition': create_node("Portfolio Composition", mode=get_node_mode("override", is_summary), format=percent_format(1), async_input=["sync_lob_lists_task",'calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task']),
    }

    if not is_summary:
        additional_fields = {
            'is_row_visible': hx.Bool(mode='output', async_input=['calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task'])
        }
        children.update(additional_fields)
    return children


def sch_premium_and_limit_profile(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "prem_limit_profile": hx.Structure(
                children={
                    "table": hx.List(
                        mode='input',
                        default_element_count=constants.DEFAULT_NUM_LOB,
                        async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                        async_input=['calculate_profit_commission_task',  'generate_word_document_task', 'generate_excel_document_task'],
                        children=generate_common_nodes(False)
                    ),
                    "summary": hx.Structure(
                        view={"label": "Total"},
                        children=generate_common_nodes(True)
                    )
                }
            )
        }
    )
