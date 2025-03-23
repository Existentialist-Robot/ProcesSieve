from typing import List, Dict, Any, Union

from pydantic import BaseModel
from fastapi import HTTPException, status

from .models import *
from .main import api_router
from . import linkMlDb
from .sieve import evaluate_many

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

def dump(m: BaseModel) -> dict:
    d = m.model_dump()
    d['category'] = m.schema()['title']
    return d


def clean(m: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
    if isinstance(m, list):
        for r in m:
            r.pop('category')
    else:
        m.pop('category')
    return m



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
def add_organization(org: Organization) -> Organization:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/organization/{id}')
def update_organization(id: str, org: Organization) -> Organization:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
def add_case(org: Case) -> Case:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/case/{id}')
def update_case(id: str, org: Case) -> Case:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
    linkMlDb.commit()
    return res

@api_router.delete('/case/{id}')
def delete_case(id: str) -> None:
    res = linkMlDb.find(dict(category= "Case", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])



@api_router.get('/case_template')
def get_case_templates() -> List[CaseTemplate]:
    res = linkMlDb.find({"category": "CaseTemplate"})
    return clean(res.rows)

@api_router.get('/case_template/{id}')
def get_case_template(id: str) -> CaseTemplate:
    res = linkMlDb.find(dict(category= "CaseTemplate", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/case_template')
def add_case_template(org: CaseTemplate) -> CaseTemplate:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/case_template/{id}')
def update_case_template(id: str, org: CaseTemplate) -> CaseTemplate:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
    linkMlDb.commit()
    return res

@api_router.delete('/case_template/{id}')
def delete_case_template(id: str) -> None:
    res = linkMlDb.find(dict(category= "CaseTemplate", id=id))
    if not res.num_rows:
        raise NotFound()
    linkMlDb.delete(res.rows[0])


@api_router.get('/process')
def get_processs() -> List[Process]:
    res = linkMlDb.find({"category": "Process"})
    return clean(res.rows)

@api_router.get('/process/{id}')
def get_process(id: str) -> Process:
    res = linkMlDb.find(dict(category= "Process", id=id))
    if not res.num_rows:
        raise NotFound()
    return clean(res.rows[0])

@api_router.post('/process')
def add_process(org: Process) -> Process:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/process/{id}')
def update_process(id: str, org: Process) -> Process:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
    linkMlDb.commit()
    return res

@api_router.delete('/process/{id}')
def delete_process(id: str) -> None:
    res = linkMlDb.find(dict(category= "Process", id=id))
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
def add_narrative(org: Narrative) -> Narrative:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/narrative/{id}')
def update_narrative(id: str, org: Narrative) -> Narrative:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
def add_narrative(org: Narrative) -> Narrative:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/narrative/{id}')
def update_narrative(id: str, org: Narrative) -> Narrative:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
def add_criterion(org: Organization) -> Organization:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/criterion/{id}')
def update_criterion(id: str, org: Organization) -> Organization:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
def add_evaluation(org: Evaluation) -> Evaluation:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/evaluation/{id}')
def update_evaluation(id: str, org: Evaluation) -> Evaluation:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
def add_person(org: Person) -> Person:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/person/{id}')
def update_person(id: str, org: Person) -> Person:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
def add_role(org: Role) -> Role:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/role/{id}')
def update_role(id: str, org: Role) -> Role:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
def add_outcome_template(org: OutcomeTemplate) -> OutcomeTemplate:
    res = linkMlDb.store(dump(org))
    linkMlDb.commit()
    return res

@api_router.patch('/outcome_template/{id}')
def update_outcome_template(id: str, org: OutcomeTemplate) -> OutcomeTemplate:
    if id != org.id:
        raise BadRequest("Do not change the Id")
    res = linkMlDb.update(dump(org))
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
