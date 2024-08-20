# Bitbucket scanner

This application is to read all the projects and repos in Bitbucket server and generate a json that can be used for API-import tool to import the projects to Snyk

## Running
To run, install the dependencies using `poetry install`, and execute `poetry run python src/main.py`

Alternatively, use the provided *launch.json* to specify the command to run and execute in VS Code.