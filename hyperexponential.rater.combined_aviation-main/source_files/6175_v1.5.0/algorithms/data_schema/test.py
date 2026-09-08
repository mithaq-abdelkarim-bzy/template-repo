import hx_data_schema as hx
from algorithms.data_schema.sch_rater_defined import exposure_dict
# b = []
a = exposure_dict["airlines"]

# for node in a:
#     b.append(node)
# print(b)

# for node in a.children:
#     print(node.view)

for k, v in a.children.items():
    print(type(v).__name__)


import hx_data_schema as hx  # Import your hx package

# Example node object instances
existing_nodes = a
include = existing_nodes["include"]

# Map from the class type to the corresponding hx function
node_type_map = {
    "BoolNode": hx.Bool,
    "FloatNode": hx.Float,
    "IntNode": hx.Int,
    "StrNode": hx.Str,
    "DateNode": hx.Date
}

def hx_node(existing_node):
    # Map from the class type to the corresponding hx function
    node_type_map = {
        "BoolNode": hx.Bool,
        "FloatNode": hx.Float,
        "IntNode": hx.Int,
        "StrNode": hx.Str,
        "DateNode": hx.Date
    }

    # Get the type name of the existing node (e.g., "BoolNode")
    node_type_name = type(existing_node).__name__
    
    # Map to the hx function (e.g., hx.Bool)
    hx_function = node_type_map.get(node_type_name)

    return hx_function

my_dict = {
    "include": hx_node(include)(mode="input")
}

print(my_dict["include"].mode)

# # Function to dynamically create a new node
# def create_dynamic_node(existing_node):
#     # Get the type name of the existing node (e.g., "BoolNode")
#     node_type_name = type(existing_node).__name__
    
#     # Map to the hx function (e.g., hx.Bool)
#     hx_function = node_type_map.get(node_type_name)

#     # If the node type is recognized and mapped to a function
#     if hx_function:
#         # Extract properties using vars() or __dict__ to access them as a dictionary
#         node_properties = {k: v for k, v in vars(existing_node).items() if v is not hx.UNDEFINED}

#         # Dynamically create a new node using the extracted properties
#         new_node = hx_function(**node_properties)
#         return new_node

# # Example usage
# new_nodes = {}
# for node_name, existing_node in existing_nodes.items():
#     # Create a new node based on the existing node
#     new_node = create_dynamic_node(existing_node)
#     # Store the new node in a dictionary
#     new_nodes[node_name] = new_node

# # Print the newly created nodes to verify
# for name, node in new_nodes.items():
#     print(f"{name}: {node}")
