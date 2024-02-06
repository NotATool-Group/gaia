# Gaia
Source code for gAIa, the AI social media manager.

## Project setup
- Install Poetry for dependency management: [Installation guide](https://python-poetry.org/docs/#installing-with-pipx) (use pipx!)
- Install dependencies: `poetry install`
- Setup the local environment variable: `cp .env.template .env` and fill in the values
- Create a local Postgres database: `createdb gaia`
- Run the migrations: `poetry run python manage.py migrate`
- Run the server: `poetry run python manage.py runserver`