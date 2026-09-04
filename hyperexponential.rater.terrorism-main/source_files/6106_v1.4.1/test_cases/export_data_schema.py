import sys
import importlib
from importlib import util
import hx_data_schema as hx

class ExportDataSchema:

    def __init__(
            self, 
            output_file_path="/workspace/editing/data_schema/exported_data_schema.csv",
            module_name = "data_schema_static",
            module_path = "/workspace/editing/data_schema/data_schema_static.py",
            csv_str = '"Path","Name","Type","Mode","Optionality","Label","Default Value","Async Input","Async Output"\n',
            remove_string = """raise Exception(\"""This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your Data Schema that will allow easier debugging.
\""")"""
            ):
        self.__output_file_path = output_file_path
        self.__module_name = module_name
        self.__module_path = module_path
        self.__csv_str = csv_str
        self.__remove_string = remove_string

    def data_schema_static_to_csv(self):
        spec = importlib.util.spec_from_file_location(self.__module_name, self.__module_path)
        if spec is None:
            raise ImportError(f"Could not load spec for module '{self.__module_name}' at: {self.__module_path}")
        source = spec.loader.get_source(self.__module_name)
        new_source = source.replace(self.__remove_string, "")
        module = importlib.util.module_from_spec(spec)
        codeobj = compile(new_source, module.__spec__.origin, 'exec')
        exec(codeobj, module.__dict__)
        sys.modules[self.__module_name] = module
        sch = module.hx_calculation_legacy_initial_premium()
        self.__recurssive_schema("", sch)
        self._write_to_file(self.__csv_str)

    def __recurssive_schema(self, ppath, sch):
        for cpath in sch.children:
            if ppath == "":
                path = cpath
            else:
                path = ppath + '/' + cpath
            type = sch.children[cpath].type
            csv_str = '"' + path + '","' + cpath + '","' + type + '"'
            if sch.children[cpath].type == "structure" or sch.children[cpath].type == "list":
                mode = 'n/a'
                optionality = 'n/a'
                label = 'n/a'
                default_val = 'n/a'
                async_input = 'n/a'
                async_output = 'n/a'
                self.__recurssive_schema(path, sch.children[cpath])
            elif sch.children[cpath].type == "file" or sch.children[cpath].type == "triangle":
                mode = sch.children[cpath].__getattribute__("mode")
                optionality = "n/a"
                view = sch.children[cpath].__getattribute__("view")
                default_val = 'n/a'
                async_input = 'n/a'
                async_output = 'n/a'
                try:
                    label = view["label"]
                except:
                    label = 'Not set'
            else:
                mode = sch.children[cpath].__getattribute__("mode")
                view = sch.children[cpath].__getattribute__("view")
                async_input = sch.children[cpath].__getattribute__("async_input")
                async_output = sch.children[cpath].__getattribute__("async_output")
                try:
                    label = view["label"]
                except:
                    label = 'Not set'
                if mode == "input":
                    default_val = str(sch.children[cpath].__getattribute__("default"))
                    optionality = sch.children[cpath].__getattribute__("optionality")
                    if optionality == hx.nodes.UNDEFINED:
                        optionality = "required"        
                else:
                    default_val = 'n/a'
                    optionality = 'n/a'
                if default_val == hx.nodes.UNDEFINED:
                    default_val = 'default_index=' + str(sch.children[cpath].__getattribute__("default_index"))    
                if async_input == hx.nodes.UNDEFINED:
                    async_input = "n/a"
                if async_output == hx.nodes.UNDEFINED:
                    async_output = "n/a"
            csv_str = csv_str + ',"' + mode + '","' + optionality + '","' + label + '","' + str(default_val) + '","' + str(async_input) + '","' + str(async_output) + '"' + '\n'
            self.__csv_str += csv_str
        return ppath

    def _write_to_file(self, csv_str):
        with open(self.__output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(csv_str)
    
eds = ExportDataSchema()
eds.data_schema_static_to_csv()