from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_prefix": "prs",
        "default_range": "string",
        "id": "https://processieve.com/schemas/v0#",
        "imports": ["linkml:types"],
        "name": "processieve",
        "prefixes": {
            "linkml": {
                "prefix_prefix": "linkml",
                "prefix_reference": "https://w3id.org/linkml/",
            },
            "prs": {
                "prefix_prefix": "prs",
                "prefix_reference": "https://processieve.com/schemas/v0#",
            },
        },
        "source_file": "schema.yaml",
        "types": {
            "JSON": {
                "base": "str",
                "description": "JSON data",
                "from_schema": "https://processieve.com/schemas/v0#",
                "name": "JSON",
                "uri": "xsd:string",
            },
            "JSONSchema": {
                "base": "str",
                "description": "A Json schema",
                "from_schema": "https://processieve.com/schemas/v0#",
                "name": "JSONSchema",
                "uri": "xsd:string",
            },
        },
    }
)


class Status(str, Enum):
    draft = "draft"
    current = "current"
    superseded = "superseded"


class Person(ConfiguredBaseModel):
    """
    A person involved in a process
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Rule",
                    "ProgramTemplate",
                    "Role",
                    "Criterion",
                ],
            }
        },
    )
    email: str = Field(
        default=...,
        json_schema_extra={"linkml_meta": {"alias": "email", "domain_of": ["Person"]}},
    )


class Organization(ConfiguredBaseModel):
    """
    An organization where persons work
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Rule",
                    "ProgramTemplate",
                    "Role",
                    "Criterion",
                ],
            }
        },
    )
    mission_statetement: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "mission_statetement",
                "domain_of": ["Organization"],
            }
        },
    )
    base_narrative: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "base_narrative", "domain_of": ["Organization"]}
        },
    )
    subunits: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "subunits", "domain_of": ["Organization"]}
        },
    )
    casebook: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "casebook", "domain_of": ["Organization"]}
        },
    )
    rulebook: Rulebook = Field(
        default=...,
        description="""The best practice workbook of the organization""",
        json_schema_extra={
            "linkml_meta": {"alias": "rulebook", "domain_of": ["Organization"]}
        },
    )
    considered_rules: Rulebook = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {"alias": "considered_rules", "domain_of": ["Organization"]}
        },
    )


class Rulebook(ConfiguredBaseModel):
    """
    A set of rules
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    status: Optional[Status] = Field(
        default="draft",
        json_schema_extra={
            "linkml_meta": {
                "alias": "status",
                "domain_of": ["Rulebook", "Narrative"],
                "ifabsent": "Status(draft)",
            }
        },
    )
    rules: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "rules", "domain_of": ["Rulebook"]}
        },
    )


class Case(ConfiguredBaseModel):
    """
    The narrative description of an individual work unit we have solved or intend to solve.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Rule",
                    "ProgramTemplate",
                    "Role",
                    "Criterion",
                ],
            }
        },
    )
    narratives: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "narratives", "domain_of": ["Case"]}
        },
    )
    idealized: bool = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {"alias": "idealized", "domain_of": ["Case"]}
        },
    )
    selected_template: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "selected_template", "domain_of": ["Case"]}
        },
    )
    considered_templates: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "considered_templates", "domain_of": ["Case"]}
        },
    )
    brief: List[str] = Field(
        default=...,
        json_schema_extra={"linkml_meta": {"alias": "brief", "domain_of": ["Case"]}},
    )
    outcome: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "outcome",
                "domain_of": ["Case", "ProgramTemplate"],
            }
        },
    )
    outcome_analysis: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "outcome_analysis", "domain_of": ["Case"]}
        },
    )


class Report(ConfiguredBaseModel):
    """
    A report contains a narrative and evaluations
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    narrative: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "narrative",
                "domain_of": ["Report", "Template", "ProgramTemplate"],
            }
        },
    )
    evaluations: Optional[List[Evaluation]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "evaluations", "domain_of": ["Report"]}
        },
    )
    based_on: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "based_on", "domain_of": ["Report"]}
        },
    )


class Rule(ConfiguredBaseModel):
    """
    The template that describes an entry in our best practice workbook, consisting of an (abstracted) situation we try to solve, and the process we intend to use to solve it.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Rule",
                    "ProgramTemplate",
                    "Role",
                    "Criterion",
                ],
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Rule", "Role", "Criterion"],
            }
        },
    )
    prompt: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "prompt", "domain_of": ["Rule", "Template"]}
        },
    )
    process: Optional[str] = Field(
        default=None,
        json_schema_extra={"linkml_meta": {"alias": "process", "domain_of": ["Rule"]}},
    )
    superseded_by: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "superseded_by", "domain_of": ["Rule"]}
        },
    )
    situation_schema: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "situation_schema", "domain_of": ["Rule"]}
        },
    )


class Template(ConfiguredBaseModel):
    """
    A schema that can be applied to a story
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"abstract": True, "from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    prompt: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "prompt", "domain_of": ["Rule", "Template"]}
        },
    )
    schema_def: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "schema_def", "domain_of": ["Template"]}
        },
    )
    narrative: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "narrative",
                "domain_of": ["Report", "Template", "ProgramTemplate"],
            }
        },
    )


class SituationSchema(Template):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    prompt: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "prompt", "domain_of": ["Rule", "Template"]}
        },
    )
    schema_def: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "schema_def", "domain_of": ["Template"]}
        },
    )
    narrative: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "narrative",
                "domain_of": ["Report", "Template", "ProgramTemplate"],
            }
        },
    )


class Objective(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    addresses: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {"alias": "addresses", "domain_of": ["Objective"]}
        },
    )
    standard_of_evalution: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "standard_of_evalution",
                "domain_of": ["Objective"],
            }
        },
    )
    threshold: Optional[float] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "threshold", "domain_of": ["Objective"]}
        },
    )


class ReportTemplate(Template):
    """
    A template that describes a category of outcome we expect at the end of a ProcessTemplate, and especially the criteria we intend to measure at the end of the process.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    objectives: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "objectives", "domain_of": ["ReportTemplate"]}
        },
    )
    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    prompt: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "prompt", "domain_of": ["Rule", "Template"]}
        },
    )
    schema_def: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "schema_def", "domain_of": ["Template"]}
        },
    )
    narrative: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "narrative",
                "domain_of": ["Report", "Template", "ProgramTemplate"],
            }
        },
    )


class ProgramTemplate(ConfiguredBaseModel):
    """
    The actual process we will use to solve a given problem.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Rule",
                    "ProgramTemplate",
                    "Role",
                    "Criterion",
                ],
            }
        },
    )
    narrative: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "narrative",
                "domain_of": ["Report", "Template", "ProgramTemplate"],
            }
        },
    )
    roles: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "roles", "domain_of": ["ProgramTemplate"]}
        },
    )
    subprocesses: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "subprocesses", "domain_of": ["ProgramTemplate"]}
        },
    )
    follows_process: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "follows_process",
                "domain_of": ["ProgramTemplate"],
            }
        },
    )
    outcome: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "outcome",
                "domain_of": ["Case", "ProgramTemplate"],
            }
        },
    )


class Role(ConfiguredBaseModel):
    """
    A process involves certain actors playing certain roles in the process. This describes the roles.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Rule",
                    "ProgramTemplate",
                    "Role",
                    "Criterion",
                ],
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Rule", "Role", "Criterion"],
            }
        },
    )


class Narrative(ConfiguredBaseModel):
    """
    A narrative description of either a concrete or abstracted Case or ProgramTemplate. There can be many narratives.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    authors: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "authors", "domain_of": ["Narrative"]}
        },
    )
    status: Optional[Status] = Field(
        default="draft",
        json_schema_extra={
            "linkml_meta": {
                "alias": "status",
                "domain_of": ["Rulebook", "Narrative"],
                "ifabsent": "Status(draft)",
            }
        },
    )
    when: datetime = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {"alias": "when", "domain_of": ["Narrative"]}
        },
    )
    title: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "title", "domain_of": ["Narrative"]}
        },
    )
    content: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "content", "domain_of": ["Narrative"]}
        },
    )


class Criterion(ConfiguredBaseModel):
    """
    A description of a criterion by which outcomes will be evaluated. E.g. A KPI is a Criterion.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    id: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Report",
                    "Rule",
                    "Template",
                    "Objective",
                    "ProgramTemplate",
                    "Role",
                    "Narrative",
                    "Criterion",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": [
                    "Person",
                    "Organization",
                    "Case",
                    "Rule",
                    "ProgramTemplate",
                    "Role",
                    "Criterion",
                ],
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["Rule", "Role", "Criterion"],
            }
        },
    )
    unit: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "unit", "domain_of": ["Criterion"]}
        },
    )


class Evaluation(ConfiguredBaseModel):
    """
    The evaluation of an outcome with respect to one of the Program's Criteria
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "https://processieve.com/schemas/v0#"}
    )

    objective: str = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {"alias": "objective", "domain_of": ["Evaluation"]}
        },
    )
    value: float = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {"alias": "value", "domain_of": ["Evaluation"]}
        },
    )
    achieved: bool = Field(
        default=...,
        json_schema_extra={
            "linkml_meta": {"alias": "achieved", "domain_of": ["Evaluation"]}
        },
    )


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Person.model_rebuild()
Organization.model_rebuild()
Rulebook.model_rebuild()
Case.model_rebuild()
Report.model_rebuild()
Rule.model_rebuild()
Template.model_rebuild()
SituationSchema.model_rebuild()
Objective.model_rebuild()
ReportTemplate.model_rebuild()
ProgramTemplate.model_rebuild()
Role.model_rebuild()
Narrative.model_rebuild()
Criterion.model_rebuild()
Evaluation.model_rebuild()
