from datetime import datetime

from neo4j.exceptions import ConstraintError
from orjson import dumps, loads

from processieve import linkMlDb
from processieve.models import *
from processieve.sieve import evaluate_one
from processieve.utils import dump

# If necessary, run on first time
# from processieve.storage import clear_database
# clear_database()

p = Person(id="maparent", name="Marc-Antoine Parent", email="maparent@conversence.com")
n = Narrative(
    authors=["maparent"],
    id="n1",
    title="Center-Led, Guild-Driven Model Applicability Assessment",
    when=datetime.now(),
)
a = '{\n  "$schema": "http://json-schema.org/draft-07/schema#",\n  "title": "Center-Led, Guild-Driven Model Applicability Assessment",\n  "description": "Parameters to determine suitability for a Center-Led, Guild-Driven Automation Development Model",\n  "type": "object",\n  "properties": {\n    "numberOfBusinessUnits": {\n      "type": "integer",\n      "description": "Number of distinct business units or departments with independent process ownership.",\n      "minimum": 2,\n      "maximum": 100,\n      "notes": "A single business unit can often use more centralized approaches."\n    },\n    "geographicDistribution": {\n      "type": "string",\n      "description": "How distributed are the business units geographically?",\n      "enum": ["Centralized", "Regional", "Global"],\n      "notes": "More distributed units necessitate greater local autonomy within guilds."\n    },\n    "automationProjectVolume": {\n      "type": "string",\n      "description": "Approximate number of automation projects anticipated in the next 12 months.",\n      "enum": ["Low", "Medium", "High"],\n      "notes": "High volume often necessitates a structured, scalable approach like Guilds."\n    },\n    "processComplexity": {\n      "type": "string",\n      "description": "Overall complexity of processes to be automated (consider cross-functional dependencies, data transformations).",\n      "enum": ["Low", "Medium", "High"],\n      "notes": "High complexity suggests benefits from specialized guild expertise."\n    },\n    "existingAutomationSkills": {\n      "type": "string",\n      "description": "Level of existing automation skills and expertise within the client organization.",\n      "enum": ["Low", "Medium", "High"],\n      "notes": "Low skills suggest a stronger initial need for central guidance, even with Guilds."\n    },\n    "organizationalCulture": {\n      "type": "string",\n      "description": "General organizational culture regarding collaboration and autonomy.",\n      "enum": ["Hierarchical", "Collaborative", "Decentralized"],\n      "notes": "Decentralized cultures are generally more receptive to a Guild-driven model."\n    },\n    "currentDevelopmentProcess": {\n      "type": "string",\n      "description": "How are automation solutions currently developed?",\n      "enum": ["Ad-hoc", "Centralized", "Decentralized"],\n      "notes": "If development is currently \'Ad-hoc\', the move to a structured Guild model will require significant change management."\n    },\n    "willingnessToShareKnowledge": {\n      "type": "boolean",\n      "description": "Is there a willingness across business units to share automation knowledge and best practices?",\n      "notes": "Critical for Guild success – resistance indicates potential roadblocks."\n    },\n    "anticipatedChangeResistance": {\n      "type": "integer",\n      "description": "Estimated level of resistance to change regarding the proposed development model (1-10, 1 being low resistance, 10 being high).",\n      "minimum": 1,\n      "maximum": 10,\n      "notes": "High resistance necessitates greater investment in change management and communication."\n    }\n  },\n  "required": [\n    "numberOfBusinessUnits",\n    "willingnessToShareKnowledge"\n  ]\n}'
sso = SituationSchema(id="a1111", schema_def=a, narrative="n1")


for ob in (p, n, sso):
    try:
        linkMlDb.insert(dump(ob))
    except ConstraintError:
        pass
linkMlDb.commit()
eg = """This client is a small local company, with no automation expertise, and their processes are very ad hoc."""
x = await evaluate_one(eg, "a1111", "SituationSchema")
print(x)
