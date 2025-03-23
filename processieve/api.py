from typing import List

from pydantic import BaseModel

from .models import Organization
from .main import api_router
from . import linkMlDb

def dump(m: BaseModel) -> dict:
    d = m.model_dump()
    d['category'] = org.schema()['title']
    return d

@api_router.get('/organizations')
def get_organizations() -> List[Organization]:
    rows = linkMlDb.find({"category": "Organization"}).rows
    for row in rows:
        row.pop('category', None)
    return rows
