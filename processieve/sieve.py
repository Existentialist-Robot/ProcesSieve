from typing import Dict, List, Tuple, Type

import dspy
from pydantic import BaseModel

from . import linkMlDb
from .utils import json_schema_to_base_model
from .models import Template, OutcomeTemplate, SituationSchema

models_by_name: Dict[str, Type[Template]] = dict(
    SituationSchema=SituationSchema, OutcomeTemplate=OutcomeTemplate
)

_template_cache: Dict[Tuple[str, str], Type[Template]] = {}
_schema_cache: Dict[Tuple[str, str], BaseModel] = {}
_module_cache: Dict[Tuple[str, str], BaseModel] = {}


def get_template(schema_id: str, schema_type: str) -> BaseModel:
    global _template_cache
    tmpl = _template_cache.get((schema_id, schema_type))
    if not tmpl:
        assert schema_type in (models_by_name), f"Unexpected schema type: {schema_type}"
        res = linkMlDb.find(dict(category=schema_type, id=schema_id))
        assert res.num_rows, f"Could not find {schema_id}"
        row = res.rows[0]
        assert row.pop("category") == schema_type
        tmpl = models_by_name[schema_type](row)
        _template_cache[(schema_id, schema_type)] = tmpl
    return tmpl


def get_schema(schema_id: str, schema_type: str) -> BaseModel:
    global _schema_cache
    schema = _schema_cache.get((schema_id, schema_type))
    if not schema:
        tmpl = get_template(schema_id)
        schema = json_schema_to_base_model(
            tmpl.schema_def, f"{schema_type}_{schema_id}"
        )
        _schema_cache[(schema_id, schema_type)] = schema
    return schema


def get_dspy_module(schema_id: str, schema_type: str):
    global _module_cache
    module = _module_cache.get((schema_id, schema_type))
    if not module:
        module = dspy.Predict(get_schema(schema_id))
        _module_cache[(schema_id, schema_type)] = module
    return module


async def evaluate_one(
    text: str, schema_id: str, schema_type: str = "ProgramTemplate"
) -> Tuple[BaseModel, float]:
    module = get_dspy_module(schema_id, schema_type)
    # TODO: Add metrics
    return (module.Predict(text), 1.0)


async def evaluate_many(
    text: str, schema_type: str = "ProgramTemplate", include_draft=False
) -> List[Tuple[str, BaseModel, float]]:
    # TODO: Only those connected to an org
    res = linkMlDb.find(dict(category=schema_type, status="current"))
    # TODO: Union drafts if required
    result = []
    for row in res.rows:
        (m, score) = await evaluate_one(text, row["id"], schema_type)
        result.append[(m, row["id"], score)]
    result.sort(key=lambda x: (x[2], x[1]), reverse=True)
    return result
