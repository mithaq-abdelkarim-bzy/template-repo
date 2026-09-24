# v0.5.0
import hx, json, openpyxl


def tsk_policy_to_excel(hxd, progress):    
    from openpyxl.utils.cell import coordinate_to_tuple
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # setting the right policy url string
    if   hx.secrets.environment_name == 'beazley-dev':      data["ri.hx_link"] = data["dev_policy_url"]
    elif hx.secrets.environment_name == 'beazley-tst':      data["ri.hx_link"] = data["tst_policy_url"]
    else:                                                   data["ri.hx_link"] = data["prd_policy_url"]

    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/example_document_template.xlsx"

    # Load the workbook 
    workbook = openpyxl.load_workbook(template_path)

    # Fill the named ranges with data
    for key, value in data.items():
        if key in workbook.defined_names:
            # Get the cell corresponding to the named range
            cells = workbook.defined_names[key].destinations
            for sheet_name, coord in cells:
                # Get the relevant worksheet
                sheet = workbook[sheet_name]
                # If value is a list, write values dynamically
                if isinstance(value, list):
                    coord = coord.replace("$", "")
                    row, col = coordinate_to_tuple(coord)
                    for df_row_index, df_row in enumerate(value, start=row):
                        for df_col_index, (cell_key, cell_value) in enumerate(df_row.items(), start=col):
                            # Write each value into the corresponding cell
                            sheet.cell(row=df_row_index, column=df_col_index, value=cell_value)
                else:
                    # Assign single value to the cell
                    sheet[coord] = value


    ############################
    ### hiding extraneous rows/columns/sheets ####
    ############################

    # hide rows on Exposure Details when not populated
    worksheet         = workbook['Exposure']
    start_row         = 73
    end_row           = 173
    num_row           = len(data["expo.event_table"])
    start_hidden_row  = num_row     +     start_row
    if start_hidden_row < end_row:      
        worksheet.row_dimensions.group(  start = start_hidden_row,      end = end_row,        hidden= True)
  
    # hide Sheet NationalMourning when not selected
    worksheet           = workbook['NationalMourning']
    hide_me             = data["ri.old_nm_approach"] == "Yes"
    if hide_me:
        worksheet.sheet_state = 'hidden'

    # hide Sheet NonAppearance when not selected
    worksheet           = workbook['NonAppearance']
    hide_me             = data["ri.product_bool"] != "Yes"
    if hide_me:
        worksheet.sheet_state = 'hidden'

    # hide Sheets etc if  Case Priced
    hide_me             = data["ri.rater_priced"] == "Case Priced"
    if hide_me:
        # hide sheets
        workbook['Exposure'        ].sheet_state = 'hidden'
        workbook['NationalMourning'].sheet_state = 'hidden'
        workbook['ExperienceRating'].sheet_state = 'hidden'
        workbook['NonAppearance'   ].sheet_state = 'hidden'
        # hide rating summary rows
        workbook['RatingSummary'].row_dimensions.group(start = 50, end = 200,  hidden= True)        
    
    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)

    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict