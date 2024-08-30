# Bitbucket scanner

This application is to read all the projects and repos in Bitbucket server and generate a json that can be used for API-import tool to import the projects to Snyk

## Running
To run, install the dependencies using `poetry install`, and execute `poetry run python src/main.py <args>`

For Bitbucker Server; 
`poetry run python src/main.py server <args>`

### Arguments

workspace: Bitbucket Workspace to be mapped to Snyk Organization.

org_id: ID of Snyk Organization to be mapped to.

integration_id: ID of Snyk Bitbucket integration.

### Authentication Environment Variables

These environment variables need to be set when executing the script to authenticate with Bitbucket

BITBUCKET_CLOUD_USERNAME - User account to access the APIs.
BITBUCKET_CLOUD_PASSWORD - Password for user.

For Bitbucket Server use;
BITBUCKET_HOSTURL - Your Bitbucket url only
BITBUCKET_SERVER_TOKEN - Your Bibucket Server token

### Output

An import targets JSON file that can be directly fed to Snyk API Import Tool to import all repositories in the Bitbucket Workspace into a Snyk Org.