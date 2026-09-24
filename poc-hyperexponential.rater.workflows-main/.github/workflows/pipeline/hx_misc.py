import json
import re
import os

def parse_model_version_label(label):
    label = str(label or '')
    pattern = r'^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)([^0-9].*?)?(-v(0|[1-9A-Za-z-][0-9A-Za-z-]*)(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'
    m = re.search(pattern, label)
    if m is not None:
        return {
            'version_valid': True,
            'version_major': m.group(1),
            'version_breaking': m.group(2),
            'version_non_breaking': m.group(3),
            'version_suffix': m.group(4),
            'version_number_as_string': f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
        }
    else:
        return {
            'version_valid': False,
            'version_major': None,
            'version_breaking': None,
            'version_non_breaking': None,
            'version_suffix': None,
            'version_number_as_string': None
        }
    
def parse_model_versions_label(model_versions, valid_labels_only = False):
    model_versions_temp = model_versions
    model_versions = []
    for v in model_versions_temp:
        parsed_label = parse_model_version_label(v["label"])
        v["parsed_label"] = parsed_label
        if valid_labels_only and parsed_label['version_valid'] == True and parsed_label['version_suffix'] is None:
            model_versions.append(v)
        elif not valid_labels_only:
            model_versions.append(v)
    return  model_versions

def read_model_versions_json(folder, testable = None, published = None, valid_labels_only = False, sort_descending = False):
    model_versions_json = "model_versions.json"
    filepath = os.path.join(folder, model_versions_json)
    try:
        # Read model_versions_json
        with open(filepath, 'r') as file:
            data = file.read()
        model_versions = json.loads(data)

        # Parse label
        for v in list(model_versions):
            v["parsed_label"] = parse_model_version_label(v["label"])

        # Filter testable
        if testable is not None:
            for v in list(model_versions):
                if v["testable"] != testable:
                    model_versions.remove(v)

        # Filter published
        if published is not None:
            for v in list(model_versions):
                if v["published"] != published:
                    model_versions.remove(v)

        # Filter valid labels
        if valid_labels_only:
            for v in list(model_versions):
                if v["parsed_label"]['version_valid'] == False or v["parsed_label"]['version_suffix'] is not None:
                    model_versions.remove(v)

        # Sort model versions descending
        if sort_descending:
            model_versions = sorted(model_versions, key=lambda x: x['id'], reverse=True)

    except IOError:
        model_versions = None
        print("ERROR!")
    return model_versions

def get_model_version_from_label(model_versions, model_version_label):
    for v in model_versions:
        if v["label"] == model_version_label:
            return v
        
def get_model_version_folder(path, model_version_id):
    if model_version_id == None:
        return None
    model_version_folder = None
    lu = f"{model_version_id}_"
    dirs = [d for d in os.listdir(path)]
    for d in dirs:
        if d.startswith(lu):
            model_version_folder = os.path.join(path, d)
            break
    return model_version_folder

def get_latest_model_version(model_versions, model_id = None, valid_labels_only = False):
        model_version_id = None
        model_version_label = None
        for v in model_versions:
            parsed_label = parse_model_version_label(v["label"])
            if valid_labels_only == False or parsed_label['version_valid'] == True: 
                if v['model']['id'] == model_id or model_id == None:
                    model_version_id = v['id']
                    model_version_label = v['label']
                    break
        return model_version_id, model_version_label