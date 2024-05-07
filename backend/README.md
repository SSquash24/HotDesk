# Hot Desking Backend

Mostly adapted from the [FastAPI SQL](https://fastapi.tiangolo.com/tutorial/sql-databases/) and [Security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) tutorials.

## Setup

1. Install [Python 3.12](https://www.python.org/) 
2. Install [Poetry](https://python-poetry.org/docs/) using the version of python you just installed (make sure `pipx` is installed with the correct version)
3. Run `poetry install` in the root directory
4. Run `poetry shell` to activate the virtual environment
5. Run `python -m scripts.init_db` to initialise the database with just the admin user.
6. (Optional) Run `python -m scripts.seed_db ./workspaces/example_seats.txt` to seed the database with dummy data.
7. Run `uvicorn app.main:app` in the virtual environment to start the app
8. You should see that `Uvicorn running on http://127.0.0.1:8000`. Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to be able to send requests to the server directly from the browser.
9. You can simulate logging in by clicking the green "Authorize" button at the top right. Note that the password needs to be non-empty (although we are not validating it for now)

## Scripts

- `python -m scripts.create_plan` to add a seating plan to the database, can specify output path for use with `seed_db`
  - `usage: create_plan.py [-h] [-n NAME] [-o OUTPUT_PATH] img_path num_desks`
- `python -m scripts.init_db` to initialise the database with just the admin user.
- `python -m scripts.seed_db` to seed the database with randomly generated data
  - `usage: seed_db.py [-h] [-e NUM_EMPLOYEES] [-d NUM_DEPTS] [-b NUM_BOOKINGS] [-a NUM_DAYS] seats_path`
- `python -m scripts.run_algo` to run the appropriate algorithm for a given date
  - `usage: run_algo.py [-h] [-d DATE] {k_furthest,simple}`

## Config

- `CURR_PLAN`: ID of plan in use for the algorithm
- `ALGO_METRIC`: `"euclidean"` denotes the euclidean metric, can add more in `algo.util`
- `CURR_ALGO`: `"k_furthest"` or `"simple"`, current algorithm in use for the API

## Testing

- `python -m pytest` to run all tests

## General Tips for Poetry

- To install a package, do `poetry add <package_name>` 
  - (DO NOT `pip install`, instead please do this whenever you use a new package and commit accordingly)
- To update all packages to their newest versions, do `poetry update`
- To run a command without activating the virtual environment, do `poetry run <command>`
