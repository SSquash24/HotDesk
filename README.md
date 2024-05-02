# Hot Desking Backend

Currently contains a login mechanism, and some boilerplate in preparation for the DB implementation. 

Mostly adapted from the [FastAPI SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/) and [Security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) tutorials.

## Setup

1. Install [Python 3.12](https://www.python.org/) 
2. Install [Poetry](https://python-poetry.org/docs/) using the version of python you just installed (make sure `pipx` is installed with the correct version)
3. Run `poetry install` in the root directory
4. Run `poetry shell` to activate the virtual environment
5. Run `python -m scripts.init_db` to initialise the database with just the admin user.
6. Run `uvicorn app.main:app` in the virtual environment to start the app
7. You should see that `Uvicorn running on http://127.0.0.1:8000`. Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to be able to send requests to the server directly from the browser.
8. You can simulate logging in by clicking the green "Authorize" button at the top right. Note that the password needs to be non-empty (although we are not validating it for now)

## Scripts

- `python -m scripts.workspace` to add a seating plan to the database
- `python -m scripts.init_db` to initialise the database with just the admin user.

## Testing

- `python -m pytest` to run all tests

## General Tips for Poetry

- To install a package, do `poetry add <package_name>` 
  - (DO NOT `pip install`, instead please do this whenever you use a new package and commit accordingly)
- To update all packages to their newest versions, do `poetry update`
- To run a command without activating the virtual environment, do `poetry run <command>`
