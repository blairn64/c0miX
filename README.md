# c0miX — Comic Collection & Run Tracker

A personal software project for organising comic reading runs, issue order and collection data.

## Project goals

- Model comic series and issues in a structured database
- Track reading and ownership state
- Identify missing issues in a run
- Handle issue ordering and reprints/variants without losing the canonical run
- Provide a small API and a usable interface for exploring the collection

## Technical direction

The project is designed around a Python application with a relational data layer and a clean separation between data ingestion, domain logic and presentation.

```text
Comic data
    ↓
Canonical data model
    ↓
Database
    ↓
Application/API
    ↓
Run tracking + collection views
```

## Portfolio status

This repository is being developed as a documented personal software project. Design notes and implementation decisions will be recorded in `docs/` so the repository shows both the finished application and the engineering reasoning behind it.

## Safety

No customer, employer or production information is required for this project. External datasets should be used in accordance with their licensing terms.
