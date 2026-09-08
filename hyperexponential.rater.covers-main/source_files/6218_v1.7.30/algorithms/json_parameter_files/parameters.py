import os
import json


# Function takes the file name as an argument
def get_parameters(file_name):

    # Get the path to the parent directory
    parent_dir = os.path.dirname(__file__)

    # Get the path to the specific file by joining the parent directory with the file name
    file_path = os.path.join(parent_dir, file_name)

    # Return the json from the parameter file
    with open(file_path) as f:
        parameter_json = json.load(f)
    return parameter_json
