all: schema.svg processieve/models.py schema.png

processieve/models.py: schema.yaml
	.venv/bin/gen-pydantic schema.yaml > processieve/models.py

schema.puml: schema.yaml
	gen-plantuml schema.yaml> schema.puml

schema.svg: schema.puml
	plantuml -tsvg schema.puml

schema.png: schema.puml
	plantuml -tpng schema.puml

lint:
	linkml-lint --validate schema.yaml

run:
	uvicorn processieve.main:app
