import io
import polars as pl
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def generate_html_table(data, title):
    html = f"<h2>{title}</h2><table>"

    def make_header_cell(header, index):
        # First 5 headers are lighter color, the rest are darker
        color = "#4B0050" if index < 5 else "#DC199B"
        return f"<th style='background-color:{color}; color:white;'>{header}</th>"

    # Polars DataFrame handling
    if isinstance(data, pl.DataFrame):
        rows = data.to_dicts()
        headers = data.columns

        # Header row with colored TH
        html += "<tr>" + "".join(
            make_header_cell(h, i) for i, h in enumerate(headers)
        ) + "</tr>"

        # Data rows
        for row in rows:
            html += "<tr>" + "".join(
                f"<td>{row.get(h, '')}</td>" for h in headers
            ) + "</tr>"

    # List of dictionaries handling
    elif isinstance(data, list) and all(isinstance(row, dict) for row in data):
        headers = list(data[0].keys())

        html += "<tr>" + "".join(
            make_header_cell(h, i) for i, h in enumerate(headers)
        ) + "</tr>"

        for row in data:
            html += "<tr>" + "".join(
                f"<td>{row.get(h, '')}</td>" for h in headers
            ) + "</tr>"

    # Single dictionary handling
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value.startswith("<table"):
                td = f"""<td style="padding: 0;">{value}</td>"""
            else:
                if isinstance(value, str):
                    value = value.replace("\n", "<br>")
                td = f"""<td>{value}</td>"""

            html += f"""
            <tr>
                <td><strong>{key}</strong></td>
                {td}
            </tr>"""

    html += "</table><br>"
    return html




def generate_email(data, hxd, insured_name, sender="", recipient=""):
    html_tables = generate_html_table(data, f"Industry / Occupancy Comparison Table")
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; font-size: 12px; }}
                h1, h2 {{ color: #4B0050; font-size: 14px; }}
                table {{ width: 50%; border-collapse: collapse; font-size: 12px; margin: 0 auto; }}
                td, th {{ border: 1px solid #000; padding: 4px; text-align: left; }}
                th {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>{insured_name}</h1>
            The NAICS Industry/Occupancy selections in the Rex schedule have been updated and now imply a different ATC occupancy, which may require remodelling. Please forward this email and its attachment for inclusion in the Exposure Management workflow.
            {html_tables}
        </body>
    </html>
    """
    # Create the email message
    accgrpid = hxd.policy_information.accgrpid

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"Remodelling Required - {insured_name} - {accgrpid}"
    msg["From"] = sender # NOTE: can have address of the relevant UWs here so they can just reply and send after downloading the message
    msg["To"] = recipient

    csv_buffer = io.StringIO()
    try:
        # Try writing CSV using Polars, in our current version v0.17.2 this will fail as write_csv expects a filepath, not bytes.
        data.write_csv(csv_buffer)
    except Exception as e:
        pdf = data.to_pandas()
        pdf.to_csv(csv_buffer, index=False)

    file_name = f"Remodelling Report {accgrpid}.csv"
    csv_bytes = csv_buffer.getvalue().encode("utf-8")
    attachment = MIMEApplication(csv_bytes, _subtype="csv")
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=file_name
    )

    # Attach the HTML content to the email
    alternative_part = MIMEMultipart("alternative")
    alternative_part.attach(MIMEText(html_content, "html"))
    msg.attach(alternative_part)

    # Attach the csv
    msg.attach(attachment)

    return msg