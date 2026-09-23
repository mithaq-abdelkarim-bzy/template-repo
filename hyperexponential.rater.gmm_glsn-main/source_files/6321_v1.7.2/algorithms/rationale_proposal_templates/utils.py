from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum

class EmailType(Enum):
    PRIMARY = "Primary"
    EXCESS = "Excess"

# MAPPINGS
# These list mappings must be a 1:1 match, each element in 'coverages' corresponding to the appropriate one from 'fields'.
# The order is important - hence why they're lists 
GMM_COVERAGES = ["professional_liability", "general_liability", "product_liability", "eo", "sexual_abuse", "employee_benefits_liability",  "tech_eo_products_media"]
GMM_FIELDS = ["hpl", "gl", "pco", "eo",  "sml", "ebl", "ct"]

GLS_COVERAGES = ["product_liability", "eo", "healthcare_professional_liability", "general_liability", "sexual_abuse", "employee_benefits_liability", "product_recall", "well_tech_eo_media"]
GLS_FIELDS = ["pco", "eo", "hpl", "gl", "sml", "ebl", "pr", "ct"]

GMM_RETRO_PRICINGS = ["professional_liability", "general_liability", "product_liability", "employee_benefits_liability", "eo", "tech_eo_products_media", "sexual_abuse"]
GMM_RETRO_FIELDS = ["hpl_retroactive_date", "gl_retroactive_date", "pco_retroactive_date", "ebl_retroactive_date", "eo_retroactive_date", "ct_retroactive_date", "sml_retroactive_date"]

GLS_RETRO_PRICINGS = ["product_liability", "eo", "healthcare_professional_liability", "general_liability", "sexual_abuse", "employee_benefits_liability", "product_recall", "well_tech_eo_media"]
GLS_RETRO_FIELDS = ["pco_retroactive_date", "eo_retroactive_date", "hpl_retroactive_date", "gl_retroactive_date", "sml_retroactive_date", "ebl_retroactive_date", "pr_retroactive_date", "ct_retroactive_date"]

LABELS_MAPPING = {
    "professional_liability": "PL",
    "eo": "E&O",
    "general_liability": "GL",
    "product_liability": "PCO",
    "employee_benefits_liability": "EBL",
    "tech_eo_products_media": "CT",
    "sexual_abuse": "SML",
    "healthcare_professional_liability": "HPL",
    "product_recall": "PR",
    "well_tech_eo_media": "CT"
}

EXCESS_COLUMN_ORDER = ["Carrier", "Coverage", "Limits", "Deductible"]

# FUNCTIONS
# Function to generate an HTML table
def generate_html_table(data, title):
    html = f'<h2 class="section-title">{title}</h2><table border="0" style="border-collapse:collapse; margin:0; padding:0;">'
    
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
            if value and isinstance(value, str) and value.startswith('<table '):
                td = f"""<td style="padding: 0;">{value}</td>"""
                
            elif value and isinstance(value, str) and not value.startswith('<table '):
                value = value.replace("\n", "<br>")
                td = f"""<td>{value}</td>"""

            html += f"""
            <tr>
                <td><strong>{key}</strong></td>
                {td}
            </tr>"""
    
    html += "</table><br>"  # Add new row after each table
    return html


def generate_email(table_fields, insured_name, sender, recipient, email_type: EmailType):
    title_html = f"<h1 style='color:#004A7C; font-family:Arial, sans-serif; font-weight: bold;'>{insured_name}</h1><br>"
    html_tables = ""
    html_tables += generate_html_table(table_fields, f"{email_type.value} Proposal")
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
    <h1>{insured_name}</h1>
    {html_tables}
    </body>
    </html>
    """
    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Rationale email - {insured_name}"
    msg["From"] = sender # NOTE: can have address of the relevant UWs here so they can just reply and send after downloading the message
    msg["To"] = recipient

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, "html"))

    return msg