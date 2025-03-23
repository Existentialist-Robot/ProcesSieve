from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)

metamodel_version = "None"
version = "None"

class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass

class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root

linkml_meta = LinkMLMeta({'default_prefix': 'prs',
     'default_range': 'string',
     'id': 'https://processieve.com/schemas/v0#',
     'imports': ['linkml:types'],
     'name': 'processieve',
     'prefixes': {'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'prs': {'prefix_prefix': 'prs',
                          'prefix_reference': 'https://processieve.com/schemas/v0#'}},
     'source_file': 'schema.yaml',
     'types': {'JSON': {'base': 'str',
                        'description': 'JSON data',
                        'from_schema': 'https://processieve.com/schemas/v0#',
                        'name': 'JSON',
                        'uri': 'xsd:string'},
               'JSONSchema': {'base': 'str',
                              'description': 'A Json schema',
                              'from_schema': 'https://processieve.com/schemas/v0#',
                              'name': 'JSONSchema',
                              'uri': 'xsd:string'}}} )

class Status(str, Enum):
    draft = "draft"
    current = "current"
    superseded = "superseded"

class Person(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'Process',
                       'Role',
                       'Criterion']} })
    email: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'email', 'domain_of': ['Person']} })

class Organization(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'Process',
                       'Role',
                       'Criterion']} })
    base_narrative: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'base_narrative', 'domain_of': ['Organization']} })
    subunits: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'subunits', 'domain_of': ['Organization']} })
    cases: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'cases', 'domain_of': ['Organization']} })
    case_templates: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'case_templates', 'domain_of': ['Organization']} })

class Case(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'Process',
                       'Role',
                       'Criterion']} })
    narratives: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'narratives', 'domain_of': ['Case']} })
    selected_template: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'selected_template', 'domain_of': ['Case']} })
    considered_templates: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'considered_templates', 'domain_of': ['Case']} })
    brief: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'brief', 'domain_of': ['Case']} })
    reports: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'reports', 'domain_of': ['Case']} })
    outcome: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'outcome', 'domain_of': ['Case']} })
    outcome_analysis: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'outcome_analysis', 'domain_of': ['Case']} })
    evaluations: Optional[List[Evaluation]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'evaluations', 'domain_of': ['Case']} })

class CaseTemplate(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'Process',
                       'Role',
                       'Criterion']} })
    authors: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'authors', 'domain_of': ['CaseTemplate', 'Process', 'Narrative']} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['CaseTemplate', 'Process', 'Role', 'Criterion']} })
    status: Optional[Status] = Field(default='draft', json_schema_extra = { "linkml_meta": {'alias': 'status',
         'domain_of': ['CaseTemplate', 'Process', 'Narrative'],
         'ifabsent': 'Status(draft)'} })
    schema_def: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'schema_def', 'domain_of': ['CaseTemplate', 'OutcomeTemplate']} })
    prompt: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'prompt', 'domain_of': ['CaseTemplate', 'OutcomeTemplate']} })
    process: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'process', 'domain_of': ['CaseTemplate']} })
    addresses: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'addresses', 'domain_of': ['CaseTemplate']} })
    expected_outcome: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'expected_outcome', 'domain_of': ['CaseTemplate']} })
    superseded_by: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'superseded_by', 'domain_of': ['CaseTemplate']} })

class OutcomeTemplate(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    prompt: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'prompt', 'domain_of': ['CaseTemplate', 'OutcomeTemplate']} })
    schema_def: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'schema_def', 'domain_of': ['CaseTemplate', 'OutcomeTemplate']} })

class Process(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'Process',
                       'Role',
                       'Criterion']} })
    authors: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'authors', 'domain_of': ['CaseTemplate', 'Process', 'Narrative']} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['CaseTemplate', 'Process', 'Role', 'Criterion']} })
    status: Optional[Status] = Field(default='draft', json_schema_extra = { "linkml_meta": {'alias': 'status',
         'domain_of': ['CaseTemplate', 'Process', 'Narrative'],
         'ifabsent': 'Status(draft)'} })
    roles: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'roles', 'domain_of': ['Process']} })
    subprocesses: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'subprocesses', 'domain_of': ['Process']} })
    follows_process: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'follows_process', 'domain_of': ['Process']} })

class Role(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'Process',
                       'Role',
                       'Criterion']} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['CaseTemplate', 'Process', 'Role', 'Criterion']} })

class Narrative(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    authors: Optional[List[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'authors', 'domain_of': ['CaseTemplate', 'Process', 'Narrative']} })
    status: Optional[Status] = Field(default='draft', json_schema_extra = { "linkml_meta": {'alias': 'status',
         'domain_of': ['CaseTemplate', 'Process', 'Narrative'],
         'ifabsent': 'Status(draft)'} })
    when: datetime  = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'when', 'domain_of': ['Narrative']} })
    title: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'title', 'domain_of': ['Narrative']} })
    content: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'content', 'domain_of': ['Narrative']} })

class Criterion(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'OutcomeTemplate',
                       'Process',
                       'Role',
                       'Narrative',
                       'Criterion']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Person',
                       'Organization',
                       'Case',
                       'CaseTemplate',
                       'Process',
                       'Role',
                       'Criterion']} })
    description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['CaseTemplate', 'Process', 'Role', 'Criterion']} })

class Evaluation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://processieve.com/schemas/v0#'})

    criterion: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'criterion', 'domain_of': ['Evaluation']} })
    value: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'value', 'domain_of': ['Evaluation']} })

# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Person.model_rebuild()
Organization.model_rebuild()
Case.model_rebuild()
CaseTemplate.model_rebuild()
OutcomeTemplate.model_rebuild()
Process.model_rebuild()
Role.model_rebuild()
Narrative.model_rebuild()
Criterion.model_rebuild()
Evaluation.model_rebuild()

