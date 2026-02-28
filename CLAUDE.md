# Project: StatApp

## Who I Am

Statistician learning full-stack deployment. Strong in Python and stats,
new to Docker and cloud.

## Stack

- App: Streamlit
- Stats: statsmodels, pandas
- Plots: matplotlib / seaborn
- File support: openpyxl (Excel), csv

## Coding Rules

- Simple and readable over clever
- One file to start (app.py) — no premature splitting
- Add comments explaining the "why", not just the "what"

## Teaching Rules

- Explain each step: what it does and why it's needed
- Flag common failure points before they happen
- When I hit an error, explain the cause before the fix

## Git Rules

- Commit after each working milestone, never broken code
- Commit messages must be descriptive: what works and what was added
- Milestones: app runs locally → docker works → tests pass → deployed

## Testing Rules

- Write tests before marking anything as done
- Unit tests: pytest, one file per module (test_app.py to start)
- Integration test: simulate a full user flow (upload CSV → run OLS → check output)
- App must pass all tests before any commit
- If a test fails, fix the code not the test

## Project Goals (in order)

1. Working Streamlit app locally
2. All tests passing
3. Dockerized and running on localhost
4. Deployed to Render (free tier)
