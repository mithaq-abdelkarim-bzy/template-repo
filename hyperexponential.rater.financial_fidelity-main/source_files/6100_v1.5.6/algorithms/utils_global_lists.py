import hx
import pandas as pd
import numpy as np

# LRE states
lre_states = [
    'Alaska',
    'Arizona',
    'Colorado',
    'District of Columbia',
    'Illinois',
    'Indiana',	
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Massachusetts',
    'Michigan',
    'Nebraska',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York (Free Trade Zone)',
    'Oklahoma',
    'Pennsylvania',
    'Rhode Island',
    'South Dakota',
    'Virginia'
    ]

cover_names = [
    'Basic Bond',
    'Insuring Agreement D (Forgery & Alteration)',
    'Agents',
    'Audit Expense',
    'Electronic Data Processors',
    'Extortion — Threats to Persons',
    'Extortion — Threats to Property',
    'Faithful Performance of Duty',
    'Fraudulent Real Property Mortgages',
    'Fraudulent Transfer Instructions',
    'Issuers of Register Checks or Personal Money Orders',
    'Misplacement',
    'Partners/Members',
    'Registered Reps. (NASD)',
    'Servicing Contractors',
    'Trading Loss',
    'Transit Cash Letter',
    'Unattended ATMs',
    'Insuring Agreement E (Securities)',

    'Computer Systems Fraud (FI)',
    'Data Processing Service Operations (FI)',
    'Voice Initiated Transfer Fraud (FI)',
    'Telefacsimile Transfer Fraud (FI)',

    'Liability of Depository (SD)',
    'Loss of Property and Damage (SD)',

    'Computer Systems Fraud',
    'Data Processing Service Operations',
    'Voice Initiated Transfer Fraud',
    'Telefacsimile Transfer Fraud',
    'Destruction of Data or Programs by Hacker',
    'Destruction of Data or Programs by Virus',
    'Voice Computer Systems Fraud',
    'Account Takeover'
]


cover_str_static = [
    'cover_1_basic_bond',
    'cover_2_insuring_agreement_d',
    'cover_3_agents',
    'cover_4_audit_expense',
    'cover_5_electronic_data_processors',
    'cover_6_extortion_persons',
    'cover_7_extortion_property',
    'cover_8_faithful_duty',
    'cover_9_fraudulent_mortgages',
    'cover_10_fraudulent_instructions',
    'cover_11_issuers_orders',
    'cover_12_misplacement',
    'cover_13_partners_members',
    'cover_14_registered_reps',
    'cover_15_servicing_contractors',
    'cover_16_trading_loss',
    'cover_17_transit_cash_letter',
    'cover_18_unattended_atms',
    'cover_19_insuring_agreement_e',

    'cover_20_computer_fraud_fi',
    'cover_21_data_processing_fi',
    'cover_22_voice_transfer_fraud_fi',
    'cover_23_telefacsimile_transfer_fraud_fi',

    'cover_24_liability_depository',
    'cover_25_loss_property_damage',

    'cover_26_computer_fraud',
    'cover_27_data_processing',
    'cover_28_voice_transfer_fraud',
    'cover_29_telefacsimile_transfer_fraud',
    'cover_30_hacker',
    'cover_31_virus',
    'cover_32_voice_computer_fraud',
    'cover_33_account_takeover'
]

# cover_str_rate_change = [item + "_rc" for item in cover_str_static]


# Define hxd variables for rating 

def cover_hxd_vbl(hxd): 
    layer = hxd.cds.layers[0]
    cov = layer.coverages
    cover_hxd_vbl = [getattr(cov, item) for item in cover_str_static]
    return cover_hxd_vbl


def cover_hxd_vbl_rc(hxd):
    hxd_rc = hxd.rate_change
    cover_hxd_vbl_rc = [getattr(hxd_rc, item) for item in cover_str_static]
    return cover_hxd_vbl_rc


rate_change_list_static = [
    "exposure_change", 
    "risk_characteristics_change", 
    "deductible_change", 
    "limit_change", 
    "terms_conditions_change", 
    "brokerage_change", 
    "other_change"
    ]


# Computer crime label dictionary


computer_crime_labels = {
    'independent_software_contractors': 'Independent software contractors',
    'access_to_computer': 'Access to system',
    'atms_accessed_to_system': 'Owned or leased ATMs',
    'does_include_clearing_houses': 'Automated clearing houses',
    'does_use_fed_wire': 'Does insured use Fed Wire?',
    'additional_computer_system': 'Additional computer system',
    'other_atm_systems': 'Other participatory ATMs',
    'use_telex': 'Does insured use telex?',
    }

