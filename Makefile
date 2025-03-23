all: schema.svg processieve/models.py

processieve/models.py: schema.yaml
	.venv/bin/gen-pydantic schema.yaml > processieve/models.py

schema.puml: schema.yaml
	gen-plantuml schema.yaml> schema.puml

schema.svg: schema.puml
	plantuml -tsvg schema.puml

lint:
	linkml-lint --validate schema.yaml
