import typer
import requests
import json
import os

from bitbucket_cloud import BitbucketCloud
from bitbucket_server import BitbucketServer

app = typer.Typer()

@app.command()
def test():
    print(f"Testing application. It works!")

@app.command()
def cloud(workspace: str, org_id: str, integration_id: str):
    username = os.getenv("BITBUCKET_CLOUD_USERNAME")
    app_password = os.getenv("BITBUCKET_CLOUD_PASSWORD")

    bb_cloud = BitbucketCloud(username=username, app_password=app_password)
    
    all_repos = bb_cloud.get_projects_and_repos(workspace)

    import_object = bb_cloud.generate_import_structure(all_repos, workspace, org_id, integration_id)

    with open("bitbucket_cloud_import_data.json", "w") as f:
        json.dump(import_object, f, indent=2)

@app.command()
def server(org_id: str, integration_id: str):
    bitbucketurl =  os.getenv("BITBUCKET_HOSTURL")
    token = os.getenv("BITBUCKET_SERVER_TOKEN")

    bb_server = BitbucketServer(bitbucketurl=bitbucketurl, token=token)
    
    """
    project_key = bb_server.get_all_projects()

    print(repos)"""

    repos = bb_server.get_all_repos()
    with open("bitbucket_server_sample_data.json", "w") as f:
        json.dump(repos, f, indent=2)

    """
    import_object = bb_server.generate_import_structure(repos, org_id, integration_id)

    with open("bitbucket_server_import_data.json", "w") as f:
        json.dump(import_object, f, indent=2)
    """


if __name__ == "__main__":
    app()