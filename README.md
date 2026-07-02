# ProcesSieve

A DSPy-powered business process evaluation engine. Given a situation description, ProcesSieve evaluates it against a library of program templates using an LLM backbone and returns confidence-ranked matches. Built with FastAPI, LinkML, and Neo4j.

## What it does

Organizations accumulate cases — real situations with context, constraints, and goals. ProcesSieve sieves each case against a set of structured program templates (SOPs, frameworks, KPI structures) and scores how well each template applies, using DSPy for LLM-backed inference with a calibrated confidence field.

Use cases: process audit, SOP matching, organizational assessment, framework recommendation.

## Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| LLM inference | DSPy (`dspy.Predict`) |
| Schema + DB | LinkML → Neo4j |
| Document I/O | Google Drive API (service account) |
| Env | `uv`, `config.ini` |

## Data Model

Core entities (defined in `schema.yaml`):

- **Organization** — the actor; has roles, skills, objectives
- **ProgramTemplate** — a reusable process schema with criteria and rules
- **SituationSchema** — structured description of a context/problem
- **Case** — a real instance: org + situation
- **Evaluation** — DSPy-scored match between a case and a template
- **Report / ReportTemplate** — structured output of an evaluation pass
- **Narrative** — supporting context attached to cases or evaluations

## Setup

### Local

```bash
# Requires: Neo4j, uv
uv sync --all-extras
cp config.ini.template config.ini   # add Cohere key
uvicorn processieve.main:app --reload
```

### Google Drive integration

1. Create a GCP project → IAM → Service Accounts → create with Edit permissions
2. Share your target Drive folder with the service account email
3. Download the private key as `service-account.json` → place in project root
4. Enable Google Docs and Google Drive APIs

## API

REST endpoints under `/api`. Key routes:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/organization` | List all organizations |
| `POST` | `/case` | Submit a new case |
| `GET` | `/program_template` | List program templates |
| `POST` | `/evaluate/{case_id}` | Run sieve — score case against all active templates |
| `GET` | `/report/{id}` | Retrieve evaluation report |

Full schema in `schema.yaml` / `schema.svg`.
