import hx_data_schema as hx_ds
import json
import datetime
from data_schema.data_schema import data_schema as data_schema_function


def incremental_triangle_data(triangle):

    full_results = []
    for origin_period in range(triangle.incremental_data.height):
        result = []
        for dev_period in range(triangle.incremental_data.width):
            result.append(triangle.incremental_data[origin_period, dev_period])

        full_results.append(result)

    return full_results

def triangle_data(triangle):
    return {
        "first_dev_period": triangle.get("first_dev_period", 0), 
        "dev_period_increment" : triangle.get("dev_period_increment", 0),
        "dev_period_count": triangle.get("dev_period_count", 0),
        "origin_period_count": triangle.get("origin_period_count", 0),
        "tail_factor": triangle.get("tail_factor", 0),
        "origin_periods":  list(map(str, triangle.get("origin_periods", 0))),
        "idf_overrides": [
            {"dev_period_index": idx, "value":idf} 
            for idx, idf in enumerate(triangle.get("idf_overrides", 0))
        ],
        "incremental_data": triangle.get("incremental_data", [])
    }

class ExampleDataOutputException(Exception):
    pass
class ExampleDataOverrideException(Exception):
    pass
def generate_example_data(input_json, data_schema_node):
    if isinstance(data_schema_node, hx_ds.Structure):
        example_data = {}
        if not isinstance(input_json, dict):
            raise ExampleDataOutputException
        for key, item in data_schema_node.children.items():
            try:

                if not isinstance(item, hx_ds.Structure) and item.mode == "output":
                    continue
                else:
                    if (key in input_json.keys()):
                        example_data[key] = generate_example_data(input_json.get(key), item)
            except ExampleDataOutputException:
                pass
        if not example_data:
            raise ExampleDataOutputException()
        return example_data
    elif isinstance(data_schema_node, hx_ds.List):
        if data_schema_node.mode == "output":
            raise ExampleDataOutputException()
        example_data = []
        for row in input_json:
            row_data = generate_example_data(row, hx_ds.Structure(children=data_schema_node.children))
            example_data.append(row_data)
        return example_data
    elif isinstance(data_schema_node, hx_ds.File):
        pass
    elif isinstance (data_schema_node, hx_ds.Triangle):
        if data_schema_node.mode == "output":
            raise ExampleDataOutputException()
        triangle = triangle_data(input_json)
        return triangle
    else:
        if data_schema_node.mode == "input":
            if isinstance(input_json, datetime.date):
                return str(input_json)
            else:
                return input_json
        elif data_schema_node.mode == "override" and isinstance(input_json, dict):
            if input_json["is_overridden"]:
                return {
                    "is_overridden": input_json["is_overridden"],
                    "override": input_json["override"],
                }
    raise ExampleDataOutputException()


def create_example_data(input_json):
    from data_schema.data_schema import data_schema as data_schema_function
    ds = data_schema_function()
    example_data = generate_example_data(input_json, ds)

    return example_data
