import math
from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Optional, Tuple, Union


class Undefined:
    __slots__: Tuple[str, ...] = ()


UNDEFINED: Undefined = Undefined()


def json_serializable(value: object, root_level: bool = True) -> bool:
    if root_level and isinstance(value, Undefined):
        return True

    if value is None:
        return True
    elif isinstance(value, float):
        return math.isfinite(value)
    elif isinstance(value, (int, bool, str, Node)):
        return True
    elif isinstance(value, (tuple, list)):
        return all(json_serializable(item, root_level=False) for item in value)
    elif isinstance(value, dict):
        return all(isinstance(key, str) and json_serializable(item, root_level=False) for key, item in value.items())
    return False


class Node(ABC):
    __slots__ = ()

    def __dir__(self) -> Iterable[str]:
        return (prop for prop in object.__dir__(self) if not prop.startswith("_"))

    def __setattr__(self, key: object, value: object) -> None:
        if not isinstance(key, str):
            raise TypeError("node attributes must be str")

        if key == "children":
            if not isinstance(value, (dict, Undefined)):
                raise TypeError("Children property must be a dict")
            if not isinstance(value, dict):
                value = dict()

        if not json_serializable(value):
            raise ValueError(f"Cannot set property '{key}' to '{repr(value)}'. value is invalid")

        object.__setattr__(self, key, value)

    def __delattr__(self, key: object) -> None:
        if not isinstance(key, str):
            raise TypeError("node attributes must be str")

        setattr(self, key, UNDEFINED)

    @property
    @abstractmethod
    def type(self) -> str:
        pass


class ChildrenNode(Node, ABC):
    __slots__ = ("children",)

    def __init__(self, children: Union[Undefined, Dict[str, Node]]) -> None:
        self.children: Dict[str, Node] = children  # type: ignore

    def __getitem__(self, key: str) -> Node:
        return self.children[key]

    def __setitem__(self, key: object, value: object) -> None:
        if not isinstance(key, str):
            raise TypeError("Children names needs to be of type str")

        if not json_serializable(value, root_level=False):
            raise ValueError(f"cannot set children value '{value}' as it is invalid")

        self.children[key] = value  # type: ignore

    def __delitem__(self, key: str) -> None:
        del self.children[key]


class StructureNode(ChildrenNode):
    @property
    def type(self) -> str:
        return "structure"

    __slots__ = (
        "linked_options",
        "linked_options_columns",
        "linked_default_index",
        "linked_options_table",
        "linked_options_data",
        "linked_options_fields",
        "view",
    )

    def __init__(
        self,
        *,
        children: Union[Undefined, Dict[str, Node]] = UNDEFINED,
        linked_options: Union[Undefined, List[List[Optional[Union[str, int, float, bool]]]]] = UNDEFINED,
        linked_options_table: Union[Undefined, str] = UNDEFINED,
        linked_options_columns: Union[Undefined, List[str]] = UNDEFINED,
        linked_options_data: Union[Undefined, str] = UNDEFINED,
        linked_options_fields: Union[Undefined, List[str]] = UNDEFINED,
        linked_default_index: Union[Undefined, int] = UNDEFINED,
        view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = UNDEFINED,
    ):
        super().__init__(children)
        self.linked_options: Union[Undefined, List[List[Optional[Union[str, int, float, bool]]]]] = linked_options
        self.linked_options_table: Union[Undefined, str] = linked_options_table
        self.linked_options_columns: Union[Undefined, List[str]] = linked_options_columns
        self.linked_options_data: Union[Undefined, str] = linked_options_data
        self.linked_options_fields: Union[Undefined, List[str]] = linked_options_fields
        self.linked_default_index: Union[Undefined, int] = linked_default_index
        self.view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = view


class ListNode(ChildrenNode):
    @property
    def type(self) -> str:
        return "list"

    __slots__ = (
        "mode",
        "async_input",
        "async_output",
        "default_element_count",
        "fixed_element_count",
        "max_element_count",
        "min_element_count",
        "view",
    )

    def __init__(
        self,
        *,
        children: Union[Undefined, Dict[str, Node]] = UNDEFINED,
        mode: Union[Undefined, str] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = UNDEFINED,
        min_element_count: Union[Undefined, int] = UNDEFINED,
        max_element_count: Union[Undefined, int] = UNDEFINED,
        default_element_count: Union[Undefined, int] = UNDEFINED,
        fixed_element_count: Union[Undefined, int] = UNDEFINED,
        view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = UNDEFINED,
    ):
        super().__init__(children)
        self.mode: Union[Undefined, str] = mode
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = async_output
        self.min_element_count: Union[Undefined, int] = min_element_count
        self.max_element_count: Union[Undefined, int] = max_element_count
        self.default_element_count: Union[Undefined, int] = default_element_count
        self.fixed_element_count: Union[Undefined, int] = fixed_element_count
        self.view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = view


class TriangleNode(Node):
    @property
    def type(self) -> str:
        return "triangle"

    __slots__ = (
        "mode",
        "async_input",
        "async_output",
        "view",
        "default_average",
        "averages",
    )

    def __init__(
        self,
        *,
        mode: Union[Undefined, str] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = UNDEFINED,
        view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = UNDEFINED,
        default_average: Union[Undefined, str] = UNDEFINED,
        averages: Union[Undefined, Dict[str, Dict[str, Optional[Union[str, bool, int]]]]] = UNDEFINED,
    ) -> None:
        self.mode: Union[Undefined, str] = mode
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = async_output
        self.view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = view
        self.default_average: Union[Undefined, str] = default_average
        self.averages: Union[Undefined, Dict[str, Dict[str, Optional[Union[str, bool, int]]]]] = averages


class FileNode(Node):
    @property
    def type(self) -> str:
        return "file"

    __slots__ = (
        "mode",
        "async_input",
        "async_output",
        "file_extension",
        "file_max_size",
        "file_name",
        "view",
    )

    def __init__(
        self,
        *,
        mode: Union[Undefined, str] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[str], None] = UNDEFINED,
        file_name: Union[Undefined, str] = UNDEFINED,
        file_extension: Union[Undefined, List[str]] = UNDEFINED,
        file_max_size: Union[Undefined, int] = UNDEFINED,
        view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = UNDEFINED,
    ) -> None:
        self.mode: Union[Undefined, str] = mode
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[str], None] = async_output
        self.file_name: Union[Undefined, str] = file_name
        self.file_extension: Union[Undefined, List[str]] = file_extension
        self.file_max_size: Union[Undefined, int] = file_max_size
        self.view: Union[Undefined, Dict[str, Union[str, Dict[str, str]]]] = view


class StrNode(Node):
    @property
    def type(self) -> str:
        return "str"

    __slots__ = (
        "mode",
        "default",
        "default_index",
        "allow_custom_value",
        "async_input",
        "async_output",
        "fixed_values",
        "fixed_values_column",
        "fixed_values_table",
        "optionality",
        "options",
        "options_column",
        "options_table",
        "options_data",
        "options_field",
        "view",
    )

    def __init__(
        self,
        *,
        mode: Union[Undefined, str] = UNDEFINED,
        default: Union[Undefined, Optional[str]] = UNDEFINED,
        default_index: Union[Undefined, int] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = UNDEFINED,
        allow_custom_value: Union[Undefined, bool] = UNDEFINED,
        fixed_values: Union[Undefined, List[Optional[str]]] = UNDEFINED,
        fixed_values_column: Union[Undefined, str] = UNDEFINED,
        fixed_values_table: Union[Undefined, str] = UNDEFINED,
        optionality: Union[Undefined, str] = UNDEFINED,
        options: Union[Undefined, List[str]] = UNDEFINED,
        options_column: Union[Undefined, str] = UNDEFINED,
        options_table: Union[Undefined, str] = UNDEFINED,
        options_data: Union[Undefined, str] = UNDEFINED,
        options_field: Union[Undefined, str] = UNDEFINED,
        view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = UNDEFINED,
    ) -> None:
        self.mode: Union[Undefined, str] = mode
        self.default: Union[Undefined, Optional[Union[str, int, float, bool]]] = default
        self.default_index: Union[Undefined, int] = default_index
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = async_output
        self.allow_custom_value: Union[Undefined, bool] = allow_custom_value
        self.fixed_values: Union[Undefined, List[Optional[str]]] = fixed_values
        self.fixed_values_column: Union[Undefined, str] = fixed_values_column
        self.fixed_values_table: Union[Undefined, str] = fixed_values_table
        self.optionality: Union[Undefined, str] = optionality
        self.options: Union[Undefined, List[str]] = options
        self.options_column: Union[Undefined, str] = options_column
        self.options_table: Union[Undefined, str] = options_table
        self.options_data: Union[Undefined, str] = options_data
        self.options_field: Union[Undefined, str] = options_field
        self.view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = view


class DateNode(Node):
    @property
    def type(self) -> str:
        return "date"

    __slots__ = (
        "mode",
        "default",
        "async_input",
        "async_output",
        "fixed_values",
        "fixed_values_column",
        "fixed_values_table",
        "optionality",
        "validation",
        "view",
    )

    def __init__(
        self,
        *,
        mode: Union[Undefined, str] = UNDEFINED,
        default: Union[Undefined, Optional[str]] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = UNDEFINED,
        fixed_values: Union[Undefined, List[Optional[str]]] = UNDEFINED,
        fixed_values_column: Union[Undefined, str] = UNDEFINED,
        fixed_values_table: Union[Undefined, str] = UNDEFINED,
        optionality: Union[Undefined, str] = UNDEFINED,
        validation: Union[Undefined, Dict[str, str]] = UNDEFINED,
        view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = UNDEFINED,
    ) -> None:
        self.mode: Union[Undefined, str] = mode
        self.default: Union[Undefined, Optional[Union[str, int, float, bool]]] = default
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = async_output
        self.fixed_values: Union[Undefined, List[Optional[str]]] = fixed_values
        self.fixed_values_column: Union[Undefined, str] = fixed_values_column
        self.fixed_values_table: Union[Undefined, str] = fixed_values_table
        self.optionality: Union[Undefined, str] = optionality
        self.validation: Union[Undefined, Dict[str, str]] = validation
        self.view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = view


class IntNode(Node):
    @property
    def type(self) -> str:
        return "int"

    __slots__ = (
        "mode",
        "default",
        "default_index",
        "allow_custom_value",
        "async_input",
        "async_output",
        "fixed_values",
        "fixed_values_column",
        "fixed_values_table",
        "optionality",
        "options",
        "options_column",
        "options_table",
        "options_data",
        "options_field",
        "validation",
        "view",
    )

    def __init__(
        self,
        *,
        mode: Union[Undefined, str] = UNDEFINED,
        default: Union[Undefined, Optional[int]] = UNDEFINED,
        default_index: Union[Undefined, int] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = UNDEFINED,
        allow_custom_value: Union[Undefined, bool] = UNDEFINED,
        fixed_values: Union[Undefined, List[Optional[int]]] = UNDEFINED,
        fixed_values_column: Union[Undefined, str] = UNDEFINED,
        fixed_values_table: Union[Undefined, str] = UNDEFINED,
        optionality: Union[Undefined, str] = UNDEFINED,
        options: Union[Undefined, List[int]] = UNDEFINED,
        options_column: Union[Undefined, str] = UNDEFINED,
        options_table: Union[Undefined, str] = UNDEFINED,
        options_data: Union[Undefined, str] = UNDEFINED,
        options_field: Union[Undefined, str] = UNDEFINED,
        validation: Union[Undefined, Dict[str, int]] = UNDEFINED,
        view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = UNDEFINED,
    ):
        self.mode: Union[Undefined, str] = mode
        self.default: Union[Undefined, Optional[int]] = default
        self.default_index: Union[Undefined, int] = default_index
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = async_output
        self.allow_custom_value: Union[Undefined, bool] = allow_custom_value
        self.fixed_values: Union[Undefined, List[Optional[int]]] = fixed_values
        self.fixed_values_column: Union[Undefined, str] = fixed_values_column
        self.fixed_values_table: Union[Undefined, str] = fixed_values_table
        self.optionality: Union[Undefined, str] = optionality
        self.options: Union[Undefined, List[int]] = options
        self.options_column: Union[Undefined, str] = options_column
        self.options_table: Union[Undefined, str] = options_table
        self.options_data: Union[Undefined, str] = options_data
        self.options_field: Union[Undefined, str] = options_field
        self.validation: Union[Undefined, Dict[str, int]] = validation
        self.view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = view


class FloatNode(Node):
    @property
    def type(self) -> str:
        return "float"

    __slots__ = (
        "mode",
        "default",
        "default_index",
        "allow_custom_value",
        "async_input",
        "async_output",
        "fixed_values",
        "fixed_values_column",
        "fixed_values_table",
        "optionality",
        "options",
        "options_column",
        "options_table",
        "options_data",
        "options_field",
        "validation",
        "view",
    )

    def __init__(
        self,
        *,
        mode: Union[Undefined, str] = UNDEFINED,
        default: Union[Undefined, Optional[float]] = UNDEFINED,
        default_index: Union[Undefined, int] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = UNDEFINED,
        allow_custom_value: Union[Undefined, bool] = UNDEFINED,
        fixed_values: Union[Undefined, List[Optional[float]]] = UNDEFINED,
        fixed_values_column: Union[Undefined, str] = UNDEFINED,
        fixed_values_table: Union[Undefined, str] = UNDEFINED,
        optionality: Union[Undefined, str] = UNDEFINED,
        options: Union[Undefined, List[float]] = UNDEFINED,
        options_column: Union[Undefined, str] = UNDEFINED,
        options_table: Union[Undefined, str] = UNDEFINED,
        options_data: Union[Undefined, str] = UNDEFINED,
        options_field: Union[Undefined, str] = UNDEFINED,
        validation: Union[Undefined, Dict[str, float]] = UNDEFINED,
        view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = UNDEFINED,
    ):
        self.mode: Union[Undefined, str] = mode
        self.default: Union[Undefined, Optional[float]] = default
        self.default_index: Union[Undefined, int] = default_index
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = async_output
        self.allow_custom_value: Union[Undefined, bool] = allow_custom_value
        self.fixed_values: Union[Undefined, List[Optional[float]]] = fixed_values
        self.fixed_values_column: Union[Undefined, str] = fixed_values_column
        self.fixed_values_table: Union[Undefined, str] = fixed_values_table
        self.optionality: Union[Undefined, str] = optionality
        self.options: Union[Undefined, List[float]] = options
        self.options_column: Union[Undefined, str] = options_column
        self.options_table: Union[Undefined, str] = options_table
        self.options_data: Union[Undefined, str] = options_data
        self.options_field: Union[Undefined, str] = options_field
        self.validation: Union[Undefined, Dict[str, float]] = validation
        self.view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = view


class BoolNode(Node):
    @property
    def type(self) -> str:
        return "bool"

    __slots__ = (
        "mode",
        "default",
        "async_input",
        "async_output",
        "fixed_values",
        "fixed_values_column",
        "fixed_values_table",
        "optionality",
        "view",
    )

    def __init__(
        self,
        *,
        mode: Union[Undefined, str] = UNDEFINED,
        default: Union[Undefined, Optional[bool]] = UNDEFINED,
        async_input: Union[Undefined, List[str], None] = UNDEFINED,
        async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = UNDEFINED,
        fixed_values: Union[Undefined, List[Optional[bool]]] = UNDEFINED,
        fixed_values_column: Union[Undefined, str] = UNDEFINED,
        fixed_values_table: Union[Undefined, str] = UNDEFINED,
        optionality: Union[Undefined, str] = UNDEFINED,
        view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = UNDEFINED,
    ):
        self.mode: Union[Undefined, str] = mode
        self.default: Union[Undefined, Optional[bool]] = default
        self.async_input: Union[Undefined, List[str], None] = async_input
        self.async_output: Union[Undefined, str, List[Union[str, Dict[str, Union[str, bool]]]], None] = async_output
        self.fixed_values: Union[Undefined, List[Optional[bool]]] = fixed_values
        self.fixed_values_column: Union[Undefined, str] = fixed_values_column
        self.fixed_values_table: Union[Undefined, str] = fixed_values_table
        self.optionality: Union[Undefined, str] = optionality
        self.view: Union[
            Undefined,
            Dict[
                str,
                Union[
                    bool,
                    str,
                    Dict[str, Union[int, bool, str]],
                    Dict[str, Union[bool, str, Dict[str, Union[int, bool, str]]]],
                ],
            ],
        ] = view
