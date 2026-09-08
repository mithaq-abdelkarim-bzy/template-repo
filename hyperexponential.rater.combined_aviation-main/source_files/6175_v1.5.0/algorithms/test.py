import json
import os
import hx_data_schema as hx

# json_path = os.path.join(os.path.dirname(__file__), "name.json")

# with open(json_path, "r") as f:
#     name_dict = json.load(f)

# file_name = name_dict.get("name") or "Test"
# file_name += ".csv"

# print(file_name)

# file_dict = {"file": hx.File(mode="output", async_output="doc_task", file_name=file_name)} # define in algorithms folder and import in data_schema.py


# ### Put below in task.py

# @hx.task
# def name_task(hxd, progress):
#     json_path = os.path.join(os.path.dirname(__file__), "name.json")
#     name_dict = {"name": hxd.debug_str}

#     with open(json_path, "w") as f:
#         json.dump(name_dict, f)


# @hx.task
# def doc_task2(hxd, progress):
#     json_path = os.path.join(os.path.dirname(__file__), "name.json")

#     with open(json_path, "r") as f:
#         name_dict = json.load(f)

#     hxd.debug_str2 = name_dict.get("name")