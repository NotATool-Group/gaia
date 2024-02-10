# Gaia
Source code for gAIa, the AI social media manager.

## Project setup
- Install Poetry for dependency management: [Installation guide](https://python-poetry.org/docs/#installing-with-pipx) (use pipx!)
- Create and join a python virtual envinronment. Poetry has such feature, i.e. `poetry shell`
- Install dependencies: `poetry install --no-root`
- Create a local Postgres database: `createdb gaia`
- Setup the local environment variable: `cp .env.template .env` and fill in the values
- Run the migrations: `python3 manage.py migrate`
- Run the server: `python3 manage.py runserver`

## Troubleshoot

### Database PostgreSQL

If issues arise with role of the user for postgres, see this links:
- [role "username" does not exist](https://stackoverflow.com/questions/65222869/how-do-i-solve-this-problem-to-use-psql-psql-error-fatal-role-postgres-d)
- remember to [change your postgres user password](https://stackoverflow.com/questions/12720967/how-can-i-change-a-postgresql-user-password)

Generally, for local testing, create a postgres user with the same name as your local OS username for using ident authentication.

