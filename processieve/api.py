from typing import List, Dict, Any

from fastapi import HTTPException, status

from . import linkMlDb
from .models import (
    Person, Organization, Case, Report, Rule, SituationSchema,
    Objective, OutcomeTemplate, ProgramTemplate, Role, Narrative,
    Criterion, Evaluation,
)
from .utils import to_optional, dump, clean
from .main import api_router
from .sieve import evaluate_many, evaluate_one

class NotFound(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)

class BadRequest(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST , detail, headers)

@api_router.get('/organization')
def get_organizations() -> List[Organization]:
    res = linkMlDb.find({"category": "Organization"})
    return clean(res.rows)

@api_router.get('/organization/{id}')
def get_organization(id: str) -> Organization:
    res = linkMlDb.find(dict(category= "Organization", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/organization')
def add_organization(obj: Organization) -> Organization:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/organization/{id}')
def update_organization(id: str, obj: to_optional(Organization)) -> Organization:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_organization(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/organization/{id}')
def delete_organization(id: str) -> None:
    res = linkMlDb.find(dict(category= "Organization", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/case')
def get_cases() -> List[Case]:
    res = linkMlDb.find({"category": "Case"})
    return clean(res.rows)

@api_router.get('/case/{id}')
def get_case(id: str) -> Case:
    res = linkMlDb.find(dict(category= "Case", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/case')
def add_case(obj: Case) -> Case:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/case/{id}')
def update_case(id: str, obj: to_optional(Case)) -> Case:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_case(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/case/{id}')
def delete_case(id: str) -> None:
    res = linkMlDb.find(dict(category= "Case", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])



@api_router.get('/program_template')
def get_program_templates() -> List[ProgramTemplate]:
    res = linkMlDb.find({"category": "ProgramTemplate"})
    return clean(res.rows)

@api_router.get('/program_template/{id}')
def get_program_template(id: str) -> ProgramTemplate:
    res = linkMlDb.find(dict(category= "ProgramTemplate", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/program_template')
def add_program_template(obj: ProgramTemplate) -> ProgramTemplate:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/program_template/{id}')
def update_program_template(id: str, obj: to_optional(ProgramTemplate)) -> ProgramTemplate:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_program_template(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/program_template/{id}')
def delete_program_template(id: str) -> None:
    res = linkMlDb.find(dict(category= "ProgramTemplate", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/report')
def get_reports() -> List[Report]:
    res = linkMlDb.find({"category": "Report"})
    return clean(res.rows)

@api_router.get('/report/{id}')
def get_report(id: str) -> Report:
    res = linkMlDb.find(dict(category= "Report", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/report')
def add_report(obj: Report) -> Report:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/report/{id}')
def update_report(id: str, obj: to_optional(Report)) -> Report:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_report(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/report/{id}')
def delete_report(id: str) -> None:
    res = linkMlDb.find(dict(category= "Report", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])



@api_router.get('/narrative')
def get_narratives() -> List[Narrative]:
    res = linkMlDb.find({"category": "Narrative"})
    return clean(res.rows)

@api_router.get('/narrative/{id}')
def get_narrative(id: str) -> Narrative:
    res = linkMlDb.find(dict(category= "Narrative", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/narrative')
def add_narrative(obj: Narrative) -> Narrative:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/narrative/{id}')
def update_narrative(id: str, obj: to_optional(Narrative)) -> Narrative:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_narrative(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/narrative/{id}')
def delete_narrative(id: str) -> None:
    res = linkMlDb.find(dict(category= "Narrative", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/narrative')
def get_narratives() -> List[Narrative]:
    res = linkMlDb.find({"category": "Narrative"})
    return clean(res.rows)

@api_router.get('/narrative/{id}')
def get_narrative(id: str) -> Narrative:
    res = linkMlDb.find(dict(category= "Narrative", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/narrative')
def add_narrative(obj: Narrative) -> Narrative:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/narrative/{id}')
def update_narrative(id: str, obj: to_optional(Narrative)) -> Narrative:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_narrative(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/narrative/{id}')
def delete_narrative(id: str) -> None:
    res = linkMlDb.find(dict(category= "Narrative", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])



@api_router.get('/criterion')
def get_criteria() -> List[Organization]:
    res = linkMlDb.find({"category": "Organization"})
    return clean(res.rows)

@api_router.get('/criterion/{id}')
def get_criterion(id: str) -> Organization:
    res = linkMlDb.find(dict(category= "Organization", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/criterion')
def add_criterion(obj: Organization) -> Organization:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/criterion/{id}')
def update_criterion(id: str, obj: to_optional(Organization)) -> Organization:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_criterion(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/criterion/{id}')
def delete_criterion(id: str) -> None:
    res = linkMlDb.find(dict(category= "Organization", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/evaluation')
def get_evaluations() -> List[Evaluation]:
    res = linkMlDb.find({"category": "Evaluation"})
    return clean(res.rows)

@api_router.get('/evaluation/{id}')
def get_evaluation(id: str) -> Evaluation:
    res = linkMlDb.find(dict(category= "Evaluation", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/evaluation')
def add_evaluation(obj: Evaluation) -> Evaluation:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/evaluation/{id}')
def update_evaluation(id: str, obj: to_optional(Evaluation)) -> Evaluation:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_evaluation(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/evaluation/{id}')
def delete_evaluation(id: str) -> None:
    res = linkMlDb.find(dict(category= "Evaluation", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/person')
def get_persons() -> List[Person]:
    res = linkMlDb.find({"category": "Person"})
    return clean(res.rows)

@api_router.get('/person/{id}')
def get_person(id: str) -> Person:
    res = linkMlDb.find(dict(category= "Person", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/person')
def add_person(obj: Person) -> Person:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/person/{id}')
def update_person(id: str, obj: to_optional(Person)) -> Person:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_person(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/person/{id}')
def delete_person(id: str) -> None:
    res = linkMlDb.find(dict(category= "Person", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/role')
def get_roles() -> List[Role]:
    res = linkMlDb.find({"category": "Role"})
    return clean(res.rows)

@api_router.get('/role/{id}')
def get_role(id: str) -> Role:
    res = linkMlDb.find(dict(category= "Role", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/role')
def add_role(obj: Role) -> Role:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/role/{id}')
def update_role(id: str, obj: to_optional(Role)) -> Role:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_role(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/role/{id}')
def delete_role(id: str) -> None:
    res = linkMlDb.find(dict(category= "Role", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/outcome_template')
def get_outcome_templates() -> List[OutcomeTemplate]:
    res = linkMlDb.find({"category": "OutcomeTemplate"})
    return clean(res.rows)

@api_router.get('/outcome_template/{id}')
def get_outcome_template(id: str) -> OutcomeTemplate:
    res = linkMlDb.find(dict(category= "OutcomeTemplate", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/outcome_template')
def add_outcome_template(obj: OutcomeTemplate) -> OutcomeTemplate:
    res = linkMlDb.store(dump(obj))
    linkMlDb.commit()
    return res

@api_router.patch('/outcome_template/{id}')
def update_outcome_template(id: str, obj: to_optional(OutcomeTemplate)) -> OutcomeTemplate:
    if id != getattr(obj, 'id', id):
        raise BadRequest("Do not change the Id")
    res = get_outcome_template(id)
    res.update(obj)
    res = linkMlDb.update(obj)
    linkMlDb.commit()
    return res

@api_router.delete('/outcome_template/{id}')
def delete_outcome_template(id: str) -> None:
    res = linkMlDb.find(dict(category= "OutcomeTemplate", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])

@api_router.post('/case/{id}/evaluate')
async def evaluate_case(id: str) -> Case:
    case = get_case(id)
    narrative_ids = case.narratives
    # TODO: Make this into a single query
    narratives = [get_narrative(nid).description for nid in narrative_ids]
    if case.brief:
        brief = get_narrative(case.brief).description
        prompt1 = f"""This is a description of a client case. First the generic brief:

        {brief}

        And then how it was described by various people:

        {'\n\n'.join(narratives)}"""
    else:
        prompt1 = f"""This is a description of a client case. Here is how it was described by various people:

        {'\n\n'.join(narratives)}"""

    if case.selected_template:
        case.outcome_analysis = await evaluate_one(prompt1)
    else:
        results = await evaluate_many(prompt1)
        if results:
            case.outcome_analysis = results[0]
            case.selected_template = results[1]
    update_case(id, case)
    return case
