from dict2xml import dict2xml

def get_xml_string():
    permissions_dict = {
        'addAllUsers': 'true',
        'denyExporting': 'true',
        'hideFromUI': 'true',
        'viewers': '',
        'managers': '',
        'owners': {
            'id': 'b995d186a3fd451b95d186a3fd151be8' # PROD id for user 'Hyperexponential Property Rater'
            # 'id': 'ed0394222d374c8b8394222d375c8bf5' # UAT id for user 'Hyperexponential Property Rater'
            }
        }

    notifications_dict = {
        'sendEmail': 'false',
        'clientNotification': 'false'
        }

    dataset_columns_list = [
            {
                'name': 'locid',
                'label': 'LocID',
                'type': 'Integer'
            },
            {
                'name': 'latitude',
                'label': 'Latitude',
                'type': 'Latitude'
            },
            {
                'name': 'longitude',
                'label': 'Longitude',
                'type': 'Longitude'
            },
            {
                'name': 'streetname',
                'label': 'StreetName',
                'type': 'Street'
            },
            {
                'name': 'city',
                'label': 'City',
                'type': 'City'
            },
            {
                'name': 'zip',
                'label': 'Zip',
                'type': 'PostalCode'
            },
            {
                'name': 'county',
                'label': 'County',
                'type': 'County'
            },
            {
                'name': 'statecode',
                'label': 'Statecode',
                'type': 'State'
            },
            {
                'name': 'country',
                'label': 'Country',
                'thematicLayer': {
                    'thematicDataset': 'Countries'
                    },        
                'type': 'CountryIso'
            },
            {
                'name': 'building_tiv',
                'label': 'Building TIV',
                'type': 'Decimal'
            },
            {
                'name': 'contents_tiv',
                'label': 'Contents TIV',
                'type': 'Decimal'
            },
            {
                'name': 'bi_tiv',
                'label': 'BI TIV',
                'type': 'Decimal'
            },
            {
                'name': 'other_tiv',
                'label': 'Other TIV',
                'type': 'Decimal'
            },
            {
                'name': 'total_tiv',
                'label': 'Total TIV',
                'type': 'Decimal'
            },
            {
                'name': 'occupancy',
                'label': 'Occupancy',
                'type': 'String'
            },
            {
                'name': 'sprinklered',
                'label': 'Sprinklered',
                'type': 'String'
            },
            {
                'name': 'constr_code',
                'label': 'Constr Code',
                'type': 'String'
            }
        ]
    
    point_thematic_layer_list = [
            {'thematicDataset': 'US_Counties'},
            {'thematicDataset': 'US_Postal'},
            {'thematicDataset': 'US_States'},
            {'thematicDataset': 'US_Counties'}
        ]

    dataset_dict = {
        'hybrid': {'geocoder': 'Bing'},
        'expireIn': 5760,
        'type': 'CSV',
        'name': 'RAPTOR Schedule',
        'description': '',
        'legacyMappingEnabled': 'true',
        'thematicLayer': {'thematicDataset': 'Countries'},
        'pointThematicLayer': point_thematic_layer_list,
        'datasetColumn': dataset_columns_list
        }

    import_dict = {
        'datasetImport': {
            'permissions': permissions_dict,
            'notifications': notifications_dict,
            'dataset': dataset_dict
            }
        }

    xml_string = dict2xml(import_dict, newlines=False)
    return xml_string