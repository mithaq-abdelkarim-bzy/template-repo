import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_claims(cds):
    cds.extend_node_rater_defined("cds", {

        # As At Date
        "as_at_date": hx.Date(default="2024-07-22", mode="input", view={"label": "As At Date"}),

        # Threshold
        "threshold": hx.Int(mode="input", default= None , optionality="optional", view={"label": "Threshold"}),

        # Claims net of retentions?
        "claims_net_ret": hx.Str(mode="input", default="No", options=["Yes", "No"], view={"label": "Claims net of retentions?"}),

        # Table
        "claims": hx.List(mode="input", children={
            "claimant_name": hx.Str(mode="input", default="", view={"label": "Claimant Name"}),
            "claim_description": hx.Str(mode="input", default="", view={"label": "Claim Description"}),
            "date_claim_made": hx.Str(mode="input", default= None , optionality="optional", view={"label": "Date Claim Made"}),
            "date_claim_closed": hx.Str(mode="input", default= None , optionality="optional", view={"label": "Date Claim Closed"}),
            "current_status": hx.Str(mode="input", default=None, optionality="optional", options=["OPEN", "CLOSED"], view={"label": "Current Status"}),
            "paid_defense": hx.Int(mode="input", default= None , optionality="optional", view={"label": "Paid Defense"}),
            "out_defense": hx.Int(mode="input", default= None , optionality="optional", view={"label": "Outstanding Defense"}),
            "paid_indemnity": hx.Int(mode="input", default= None , optionality="optional", view={"label": "Paid Indemnity"}),
            "out_indemnity": hx.Int(mode="input", default= None , optionality="optional", view={"label": "Outstanding Indemnity"}),
            "attachment": hx.Int(mode="input", default= None , optionality="optional", view={"label": "Attachment"}),
            "limit": hx.Int(mode="input", default= None , optionality="optional", view={"label": "Limit"}),
            "currency_claims": hx.Str(mode="input", default=None, optionality="optional", options=["ADP", "AFA", "AON", "AOR", "ATS", "AZM", "BEF", "BGL", "BRE", "BUK", "BYB", "BYR", "CSD", "CSK", "CYP", "DDM", "DEM", "ECS", "EEK", "ESP", "FIM", "FRF", "GHC", "GRD", "GWP", "HRK", "IEP", "ITL", "LTL", "LUF", "LVL", "MGF", "MRO", "MTL", "MXP", "MZM", "NIC", "NLG", "PES", "PLZ", "PTE", "ROL", "RUR", "SDD", "SDP", "SIT", "SKK", "SRG", "STD", "SUR", "TRL", "UYP", "VEB", "VEF", "XEU", "YUM", "ZMK", "ZRN", "ZRZ", "ZWD", "ZWR", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BOV", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHE", "CHF", "CHW", "CLF", "CLP", "CNY", "COP", "COU", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HTG", "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MXV", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "USN", "UYI", "UYU", "UYW", "UZS", "VED", "VES", "VND", "VUV", "WST", "XAF", "XAG", "XAU", "XBA", "XBB", "XBC", "XBD", "XCD", "XDR", "XOF", "XPD", "XPF", "XPT", "XSU", "XTS", "XUA", "XXX", "YER", "ZAR", "ZMW", "ZWL"], view={"label": "Currency Claims"}),
            "claim_type": hx.Str(mode="input", default="", view={"label": "Claim Type"}),
            "claim_location": hx.Str(mode="input", default="", view={"label": "Claima Location"}),
            "area_of_practice": hx.Str(mode="input", default="", view={"label": "Area of Practice"}),
            "year": hx.Str(mode="output", view={"label": "Year"}),
            "inc_claims_unr": hx.Str(mode="output", view={"label": "inc claims Unrevalued fgu"}),
            "pd_claims_unr": hx.Str(mode="output", view={"label": "pd claims Unrevalued fgu"}),
            "inc_claims_rev": hx.Str(mode="output", view={"label": "inc claims Revalued for inflation fgu"}),
            "pd_claims_rev": hx.Str(mode="output", view={"label": "pd claims Revalued for inflation fgu"}),
            "inc_claims_unr": hx.Str(mode="output", view={"label": "Inc claims", "group": "Unrevalued FGU"}),
            "pd_claims_unr": hx.Str(mode="output", view={"label": "Pd claims", "group": "Unrevalued FGU"}),
            "inc_claims_rev": hx.Str(mode="output", view={"label": "Inc claims", "group": "Revalued for inflation FGU"}),
            "pd_claims_rev": hx.Str(mode="output", view={"label": "Pd claims", "group": "Revalued for inflation FGU"}),
        })

    })


