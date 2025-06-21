# == ACTION: Bootstrap recruiting-agency automation project ==
## Goal
Generate all modules, tests, Dockerfile, and rule scaffolding for the Recruiting-Agency Automation Stack.

## Deliverables
- folders:  
  - src/  
  - tests/  
  - docs/  
  - .cursor/rules/
- in src/, add empty files:  
  jobs_scraper.py        (RapidAPI fetch + LinkedIn filters)  
  contacts.py            (decision-maker lookup + 30-day cache)  
  drive_ingest.py        (résumé extractor → pgvector)  
  vector_matcher.py      (pgvector search + GPT-4o rerank)  
  messaging.py           (template + guard-rails)  
  sheet_writer.py        (Google Sheets writer)  
  scheduler.py           (APScheduler cron jobs, MYT zone)  
  main.py                (FastAPI entrypoint)  
  __init__.py
- in tests/, add placeholder test files mirroring each module plus:  
  conftest.py            (dummy fixture)  
  __init__.py
- in .cursor/rules/, add:  
  recruiting-automation.mdc  
  senior-engineer.mdc
- project root files:  
  Dockerfile  
  .dockerignore  
  requirements.txt
- commit everything.

## Next actions
1. Scaffold folders and __init__.py
2. Stub each module with type-annotated signatures only
3. Generate tests with external calls mocked
4. Stop – wait for my review

## Finish
- Append a TODO list with “Critical Review & Suggestions” items.
- Reply with a concise summary: files created and the next recommended command (e.g. “Implement jobs_scraper.py”).
