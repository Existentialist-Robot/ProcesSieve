from types import Any, Dict, Type, Optional, List, Tuple
from enum import Enum

import dspy
from pydantic import BaseModel, Field, create_model

from . import linkMlDb
from .models import CaseTemplate, OutcomeTemplate

# From https://stackoverflow.com/a/79431514/439048
type_mapping: dict[str, type] = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
}

models_by_name = dict(CaseTemplate=CaseTemplate, OutcomeTemplate=OutcomeTemplate)

def json_schema_to_base_model(schema: dict[str, Any], name: Optional[str]=None) -> Type[BaseModel]:
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

    return create_model(name or schema.get("title"), **model_fields)


_template_cache: Dict[Tuple[str, str], BaseModel] = {}
_schema_cache: Dict[Tuple[str, str], BaseModel] = {}
_module_cache: Dict[Tuple[str, str], BaseModel] = {}


def get_template(schema_id: str, schema_type: str) -> BaseModel:
    global _template_cache
    tmpl = _template_cache.get((schema_id, schema_type), None)
    if not tmpl:
        assert schema_type in (models_by_name), f"Unexpected schema type: {schema_type}"
        res = linkMlDb.find(dict(category=schema_type, id=schema_id))
        assert res.num_rows, f"Could not find {schema_id}"
        row = res.rows[0]
        assert row.pop('category') == schema_type
        tmpl = models_by_name[schema_type](row)
        _template_cache[(schema_id, schema_type)] = tmpl
    return tmpl

def get_schema(schema_id: str, schema_type: str) -> BaseModel:
    global _schema_cache
    schema = _schema_cache.get((schema_id, schema_type), None)
    if not schema:
        tmpl = get_template(schema_id)
        schema = json_schema_to_base_model(tmpl.schema_def, f"{schema_type}_{schema_id}")
        _schema_cache[(schema_id, schema_type)] = schema
    return schema


def get_dspy_module(schema_id: str, schema_type: str):
    global _module_cache
    module = _module_cache.get((schema_id, schema_type), None)
    if not module:
        module = dspy.Predict(get_schema(schema_id))
        _module_cache[(schema_id, schema_type)] = module
    return module


async def evaluate_one(text: str, schema_id: str, schema_type:str="CaseTemplate") -> Tuple[BaseModel, float]:
    module = get_dspy_module(schema_id, schema_type)
    # TODO: Add metrics
    return (module.Predict(text), 1.0)


async def evaluate_many(text: str, schema_type:str="CaseTemplate", include_draft=False) -> List[Tuple[BaseModel, float]]:
    # TODO: Only those connected to an org
    res = linkMlDb.find(dict(category=schema_type, status='current'))
    # TODO: Union drafts if required
    result = []
    for row in res.rows:
        (m, score) = await evaluate_one(text, row['id'], schema_type)
        result.append[(m, score)]
    result.sort(key=lambda x: x[1], reverse=True)
    return result

