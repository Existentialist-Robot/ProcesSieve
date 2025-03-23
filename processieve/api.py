from typing import List, Dict, Any, Union

from pydantic import BaseModel
from fastapi import HTTPException, status

from .models import Organization
from .main import api_router
from . import linkMlDb


class NotFound(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)

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

@api_router.patch('/organization')
def update_organization(org: Organization) -> Organization:
    res = linkMlDb.update(dump(org))
    linkMlDb.commit()
    return res
