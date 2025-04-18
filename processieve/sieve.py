from typing import Dict, List, Optional, Tuple, Type

import dspy
from orjson import loads
from pydantic import BaseModel, Field

from . import linkMlDb
from .models import ReportTemplate, SituationSchema, Template
from .utils import json_schema_to_base_model

models_by_name: Dict[str, Type[Template]] = dict(
    SituationSchema=SituationSchema, ReportTemplate=ReportTemplate
)

_template_cache: Dict[Tuple[str, str], Type[Template]] = {}
_schema_cache: Dict[Tuple[str, str], BaseModel] = {}
_module_cache: Dict[Tuple[str, str], BaseModel] = {}


class BaseModelWithConfidence(BaseModel):
    confidence: float = Field(
        ge=0, le=1, description="The confidence score for the answer"
    )


def get_template(schema_id: str, schema_type: str) -> BaseModel:
    global _template_cache
    tmpl = _template_cache.get((schema_id, schema_type))
    if not tmpl:
        assert schema_type in (models_by_name), f"Unexpected schema type: {schema_type}"
        res = linkMlDb.find(dict(category=schema_type, id=schema_id))
        assert res.num_rows, f"Could not find {schema_id}"
        row = res.rows[0]
        assert row.pop("category") == schema_type
        tmpl = models_by_name[schema_type](**row)
        _template_cache[(schema_id, schema_type)] = tmpl
    return tmpl


def get_schema(schema_id: str, schema_type: str) -> BaseModelWithConfidence:
    global _schema_cache
    schema = _schema_cache.get((schema_id, schema_type))
    if not schema:
        tmpl = get_template(schema_id, schema_type)
        json_schema = loads(tmpl.schema_def)
        # json_schema["properties"]["confidence"] = dict(
        #     type="integer",
        #     description="The confidence score for the answer",
        #     minimum=0,
        #     maximum=10,
        # )
        schema = json_schema_to_base_model(
            json_schema, f"{schema_type}_{schema_id}", BaseModelWithConfidence
        )
        _schema_cache[(schema_id, schema_type)] = schema
    return schema


def get_dspy_module(schema_id: str, schema_type: str):
    global _module_cache
    module = _module_cache.get((schema_id, schema_type))
    if not module:
        output_schema = get_schema(schema_id, schema_type)

        class Signature(dspy.Signature):
            """Answer the question based on the context and query provided, and on the scale of 0-1 tell how confident you are about the answer."""

            input: str = dspy.InputField()
            output: output_schema = dspy.OutputField()

        module = dspy.Predict(Signature)
        _module_cache[(schema_id, schema_type)] = module
    return module


async def evaluate_one(
    text: str, schema_id: str, schema_type: str = "ProgramTemplate"
) -> Optional[BaseModelWithConfidence]:
    """Evaluate a single text against a schema."""
    module = get_dspy_module(schema_id, schema_type)
    # TODO: Add metrics
    result = module(input=text)
    if result:
        return result.output


async def evaluate_many(
    text: str, schema_type: str = "ProgramTemplate", include_draft=False
) -> List[Tuple[str, BaseModel, float]]:
    # TODO: Only those connected to an org
    res = linkMlDb.find(dict(category=schema_type, status="current"))
    # TODO: Union drafts if required
    result = []
    for row in res.rows:
        m = await evaluate_one(text, row["id"], schema_type)
        if m:
            result.append[(m, row["id"], m.confidence)]
    result.sort(key=lambda x: (x[2], x[1]), reverse=True)
    return result
