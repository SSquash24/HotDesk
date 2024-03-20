# Hot Desking Test

Currently this code has no real database, just a basic login system and a way for a user to request a desk for a day and see their booking for today.

## Setup

1. Install [Python 3.12](https://www.python.org/) 
2. Install [Poetry](https://python-poetry.org/docs/) using the version of python you just installed (make sure `pipx` is installed with the correct version)
3. Run `poetry install` in the root directory
4. Run `poetry shell` to activate the virtual environment
5. Run `uvicorn backend:app --reload` in the virtual environment to start the app

## General Tips for Poetry

- To install a package, do `poetry add <package_name>` 
  - (DO NOT `pip install`, instead please do this whenever you use a new package and commit accordingly)
- To update all packages to their newest versions, do `poetry update`
- To run a command without activating the virtual environment, do `poetry run <command>`
