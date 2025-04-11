from copy import deepcopy
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo


def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
    new = deepcopy(field)
    new.default = default
    new.annotation = Optional[field.annotation]  # type: ignore
    return (new.annotation, new)


BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


def to_optional(model: Type[BaseModelT]) -> Type[BaseModelT]:
    """Transform a schema into an equivalent optional schema"""
    # https://github.com/pydantic/pydantic/issues/3120#issuecomment-1528030416
    return create_model(  # type: ignore
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )


def clean(m: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
    if isinstance(m, list):
        for r in m:
            r.pop("category")
    else:
        m.pop("category")
    return m


def dump(m: BaseModel) -> dict:
    d = m.model_dump()
    d["category"] = m.model_json_schema()["title"]
    return d


# From https://stackoverflow.com/a/79431514/439048
type_mapping: dict[str, type] = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def json_schema_to_base_model(
    schema: dict[str, Any], name: Optional[str] = None, base=BaseModel
) -> Type[BaseModel]:
    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])
    model_fields = {}

    def process_field(field_name: str, field_props: dict[str, Any]) -> tuple:
        """Recursively processes a field and returns its type and Field instance."""
        json_type = field_props.get("type", "string")
        enum_values = field_props.get("enum")

        # Handle Enums
        if enum_values:
            enum_name: str = f"{field_name.capitalize()}Enum"
            field_type = Enum(enum_name, {v: v for v in enum_values})
        # Handle Nested Objects
        elif json_type == "object" and "properties" in field_props:
            field_type = json_schema_to_base_model(
                field_props
            )  # Recursively create submodel
        # Handle Arrays with Nested Objects
        elif json_type == "array" and "items" in field_props:
            item_props = field_props["items"]
            if item_props.get("type") == "object":
                item_type: type[BaseModel] = json_schema_to_base_model(item_props)
            else:
                item_type: type = type_mapping.get(item_props.get("type"), Any)
            field_type = list[item_type]
        else:
            field_type = type_mapping.get(json_type, Any)

        # Handle default values and optionality
        default_value = field_props.get("default", ...)
        nullable = field_props.get("nullable", False)
        description = field_props.get("title", "")

        if nullable:
            field_type = Optional[field_type]

        if field_name not in required_fields:
            default_value = field_props.get("default", None)

        return field_type, Field(default_value, description=description)

    # Process each field
    for field_name, field_props in properties.items():
        model_fields[field_name] = process_field(field_name, field_props)

    return create_model(name or schema.get("title"), **model_fields, __base__=base)
