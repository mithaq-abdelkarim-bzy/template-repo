import hx_data_schema as hx



def sch_test_api():
    return {

        # TEST SCHEMA FOR API CALLS
         "companies_house" : hx.Structure(view = {"label" : "Companies House"}, children = {
            "fetch_status" : hx.Str(mode = "output", view = { "label" : "Fetch Status"}, async_output = ["get_companies_house"]),
            "company_name" : hx.Str(mode = "output", view = { "label" : "Company Name"}, async_output = ["get_companies_house"]),
            "company_status" : hx.Str(mode = "output", view = { "label" : "Company Status"}, async_output = ["get_companies_house"]),
            "creation_date" : hx.Str(mode = "output", view = { "label" : "Creation Date"}, async_output = ["get_companies_house"]),
            "address_line_2" : hx.Str(mode = "output", view = { "label" : "Addres Line 1"}, async_output = ["get_companies_house"]),
            "address_line_1" : hx.Str(mode = "output", view = { "label" : "Addres Line 2"}, async_output = ["get_companies_house"]),
            "locality" : hx.Str(mode = "output", view = { "label" : "Locality"}, async_output = ["get_companies_house"]),
            "postal_code" : hx.Str(mode = "output", view = { "label" : "Postal Code"}, async_output = ["get_companies_house"]),
            "accounts_overdue" : hx.Bool(mode = "input", default = None, optionality = "optional", view = { "label" : "Account Overdue"}, async_output = ["get_companies_house"]),
            "has_charges" : hx.Bool(mode = "input", default = None, optionality = "optional", view = { "label" : "Has Charges?"}, async_output = ["get_companies_house"]),
            "has_insolvency_history" : hx.Bool(mode = "input", default = None, optionality = "optional", view = { "label" : "Has Insolvency History?"}, async_output = ["get_companies_house"]),
            "company_id" : hx.Str(mode = "input", default = "", view = { "label" : "Company ID"}, async_input = ["get_companies_house"]),
         })

    }
