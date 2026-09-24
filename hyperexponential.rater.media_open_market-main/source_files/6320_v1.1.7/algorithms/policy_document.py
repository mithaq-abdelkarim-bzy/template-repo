import hx
import json
from datetime import datetime
from algorithms.rate_utilities import pd_df_from_hx_list
import html as _html
from html.parser import HTMLParser
import re
import algorithms.rate_utilities as utils


# Format data in dictionary for Excel
def clean_data_for_policy_doc(data):
    for key, value in data.items():
        if value is None:
            data[key] = ""
        elif value is True:
            data[key] = "Yes"
        elif value is False:
            data[key] = "No"
        elif key in ["inception_date", "expiry_date"]:
            date_str = str(value)
            data[key] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    return data


def list_converter(hx_list, col_order = []):
    df = pd_df_from_hx_list(hx_list)
    if col_order:
        df = df[col_order]

    dict_of_lists = df.to_dict(orient='records')

    return dict_of_lists

def _html_to_plaintext(html_str: str) -> str:
    if html_str is None:
        return ""
    s = str(html_str)

    class _Mini(HTMLParser):
        def __init__(self):
            super().__init__()
            self.out = []
            self.ol = []
            self.in_li = False
            self.in_cell = False
            self.first_cell = True

        def _nl(self):
            if self.out and not str(self.out[-1]).endswith("\n"):
                self.out.append("\n")

        def handle_starttag(self, tag, attrs):
            tag = tag.lower()
            if tag in ("p", "div", "h2", "h3"):
                if not self.in_li:
                    self._nl()
            elif tag == "br":
                self.out.append(" " if (self.in_li or self.in_cell) else "\n")
            elif tag == "ul":
                self.ol.append(None)
            elif tag == "ol":
                self.ol.append(1)
            elif tag == "li":
                self.in_li = True
                self._nl()
                if self.ol:
                    if self.ol[-1] is None:
                        self.out.append("• ")
                    else:
                        self.out.append(f"{self.ol[-1]}. ")
                        self.ol[-1] += 1
            elif tag == "tr":
                self._nl()
                self.first_cell = True
            elif tag in ("td", "th"):
                if not self.first_cell:
                    self.out.append("\t")
                self.first_cell = False
                self.in_cell = True

        def handle_endtag(self, tag):
            tag = tag.lower()
            if tag in ("ul", "ol"):
                if self.ol:
                    self.ol.pop()
                    self._nl()
            elif tag == "li":
                self.in_li = False
                self._nl()
            elif tag == "tr":
                self._nl()
            elif tag in ("td", "th"):
                self.in_cell = False
            elif tag in ("p", "div", "h2", "h3"):
                self._nl()

        def handle_data(self, data):
            if not data:
                return
            txt = _html.unescape(data)
            txt = re.sub(r"[ \t\u00A0]+", " ", txt)
            self.out.append(txt)

        def get(self):
            t = "".join(self.out)
            t = re.sub(r"\n{3,}", "\n\n", t).strip()
            return t

    if not re.search(r"<[A-Za-z]", s):
        return s.replace("\r\n", "\n")
    p = _Mini()
    p.feed(s)
    return p.get()


# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
    cds = hxd.cds
    primary = hxd.cds.primary
    sf = hxd.cds.standard_fields
    rf = hxd.cds.rating_factors
    layer = hxd.cds.layers[0]
    option = hxd.cds.options[0]
    exp = hxd.cds.exposure.granular
    
    # Primary layer for selected option
    option_selected = cds.option_selected
    option_selected = int("".join([c for c in option_selected if c.isdigit()])) # Pull out integer
    options_df = utils.pd_df_from_hx_list(cds.options)

    bound_option = options_df.iloc[option_selected - 1]
    # Add scalr fields below
    # Data tables are added after
    retention_field = bound_option.retention
    if(cds.coverage_name in ["Media Liability","Music Liability","Annual TV & Film LARGE"]):
        retention_field = bound_option.retention
    else:
        retention_field = bound_option.eec_excess  
    data = {
        
        "brokerage": layer.brokerage,
        "expiry_date": sf.expiry_date,
        "inception_date": sf.inception_date,
        "insured_name": sf.insured_name,
        "coverage_name": cds.coverage_name,
        "underwriter": sf.underwriter,
        "section_reference": layer.section_reference,
        "source_currency": cds.currencies.source_currency,
        "term": rf.policy_term,
        "written_line": layer.written_line,
        "status": layer.status,
                
        "bound_premium": primary.bound_premium_input,
        "benchmark_premium": primary.benchmark_premium,
        "technical_premium": primary.technical_premium,
        "bpi": primary.bpi,
        "tpi": primary.tpi,
        "underwriter_adjustment": layer.uw_adj_impact,
        "uw_comments": _html_to_plaintext(sf.uw_rationale),

        "eec_limit": bound_option.eec_limit,
        "limit_aggregate": bound_option.aggregate_limit,
        "retention": retention_field,
        
        "rate_change": layer.rate_change.risk_adjusted_rate_change

    }


    # Add data tables here, need to convert to a dictionary for storate in the data dictionary using 'list_converter'
    # You do not have to output all cols 
    # exposure_cols = ["exposure_measure","base_rate"]
    # exposure_lst = list_converter(exp.exposure_details, col_order=exposure_cols)
    # data["exposure_df"] = exposure_lst


    
    # Add URL of hx policy
    p_id = hx.meta.policy_id
    po_id = hx.meta.policy_option_id
    policy_url = f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}"
    data["policy_url"] = policy_url

    # Format data
    formatted_data = clean_data_for_policy_doc(data)
    json_data = json.dumps(formatted_data)

    return json_data

    # Function to generate an HTML table
def generate_html_table(data, title):
    html = f"<h2 class='section-title'>{title}</h2><table>"
        
        # Check if data is a list of dictionaries
    if isinstance(data, list) and all(isinstance(row, dict) for row in data):
            # Create table headers from the keys of the first dictionary
        headers = data[0].keys()
        html += "<tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
            
            # Create table rows
        for row in data:
            html += "<tr>" + "".join(f"<td>{row.get(header, '')}</td>" for header in headers) + "</tr>"
        # If data is a single dictionary (two-column table)
    elif isinstance(data, dict):
        for key, value in data.items():
            html += f"""
                <tr>
                    <td><strong>{key}</strong></td>
                    <td>{value}</td>
                </tr>"""
        
    html += "</table><br>"  # Add space after each table
    return html

# Create data dictionary to write to Email file
def create_dict_for_email(hxd):
    cds = hxd.cds
    primary = hxd.cds.primary
    sf = hxd.cds.standard_fields
    rf = hxd.cds.rating_factors
    layer = hxd.cds.layers[0]
    exp = hxd.cds.exposure.granular

    # Primary layer for selected option
    option_selected = cds.option_selected
    option_selected = int("".join([c for c in option_selected if c.isdigit()])) # Pull out integer
    options_df = utils.pd_df_from_hx_list(cds.options)

    bound_option = options_df.iloc[option_selected - 1]
    
    # Data tables 
    risk_information = {
        "Inception Date": sf.inception_date,
        "Expiry Date": sf.expiry_date,
        "Underwriter": sf.underwriter,
        "Insured Name": sf.insured_name,
        "Coverage Name": cds.coverage_name,
        "Policy Reference": layer.section_reference,
        "Currency": cds.currencies.source_currency,
        "Written Line": f"{layer.written_line:.1%}" if  layer.written_line is not None else "",
        "Brokerage":  f"{layer.brokerage:.1%}" if  layer.brokerage is not None else "" ,
        "Term (Years)": rf.policy_term,
        "Status": layer.status
    }

    retention_field = bound_option.retention
    if(cds.coverage_name in ["Media Liability","Music Liability","Annual TV & Film LARGE"]):
        retention_field = bound_option.retention
    else:
        retention_field = bound_option.eec_excess    

    summary_data = {
        "Bound Premium":  f"{primary.bound_premium:,.0f}" if primary.bound_premium is not None else "",
        "UW Adjustment":  f"{layer.uw_adj_impact:.0%}"  if layer.uw_adj_impact is not None else "",
        "Bound EEC Limit": f"{bound_option.eec_limit:,.0f}" if bound_option.eec_limit is not None else "",
        "Bound Aggregate Limit": f"{bound_option.aggregate_limit:,.0f}" if bound_option.aggregate_limit  is not None else "",
        "Bound Retention": f"{retention_field:,.0f}" if retention_field is not None else "",
        "Technical Premium":  f"{primary.technical_premium:,.0f}" if primary.technical_premium is not None else "",
        "TPI": f"{primary.tpi :.1%}"  if  primary.tpi is not None else "" ,
        "Benchmark Premium":   f"{primary.benchmark_premium:,.0f}" if primary.benchmark_premium is not None else "",
        "BPI": f"{primary.bpi:.1%}"  if  primary.bpi is not None else "" ,
        "Rate Change (if renewal)": f"{layer.rate_change.risk_adjusted_rate_change :.1%}" if layer.rate_change.risk_adjusted_rate_change is not None else ""
    }

    html_tables = generate_html_table(risk_information, "Risk Information")
    html_tables += generate_html_table(summary_data, "Summary Data")

    # Put all the tables together in HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; font-size: 12px; }}
            h1 {{ color: #004A7C; font-size: 16px; }}
            h2 {{ color: #CC007F; font-size: 14px; margin-top: 20px; }}
            table {{ width: 50%; border-collapse: collapse; font-size: 12px; margin: 0 auto; }}
            td, th {{ border: 1px solid #000; padding: 4px; text-align: left; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
            .section-title {{ color: #CC007F; font-weight: bold; }}
        </style>
    </head>
    <body>
    <h1>{sf.insured_name}</h1>
    {html_tables}
    
    <h2 class='section-title'> Underwriter Comments </h2><p>{sf.uw_rationale}</p>

    </body>
    </html>
    """
    return html_content    

# Push dictionary to hxd for storage
def store_policy_data(hxd):
    # If there are multiple layers you'll need to update
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been input
    if not layer.quoted_premium:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False

    data_email = create_dict_for_email(hxd)
    hxd.cds.email.data_dict = data_email


