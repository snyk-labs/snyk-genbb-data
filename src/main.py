import typer
import requests
import json
import os

from bitbucket_cloud import BitbucketCloud
from bitbucket_server import BitbucketServer

from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def test():
    print(f"Testing application. It works!")

@app.command()
def run_bb_cloud(workspace: str, org_id: str, integration_id: str):
    username = os.getenv("BITBUCKET_CLOUD_USERNAME")
    app_password = os.getenv("BITBUCKET_CLOUD_PASSWORD")

    bb_cloud = BitbucketCloud(username=username, app_password=app_password)
    
    all_repos = bb_cloud.get_projects_and_repos(username, app_password, workspace)

    import_object = bb_cloud.generate_import_structure(all_repos, workspace, org_id, integration_id)

    with open("bitbucket_cloud_import_data.json", "w") as f:
        json.dump(import_object, f, indent=2)

def run_bb_server(workspace: str, org_id: str, integration_id: str, project_key: Annotated[str, typer.Argument()] = ""):
    username = os.getenv("BITBUCKET_CLOUD_USERNAME")
    app_password = os.getenv("BITBUCKET_CLOUD_PASSWORD")

    bb_server = BitbucketServer(username=username, app_password=app_password)
    
    repos = []

    if project_key == "":
        repos = bb_server.get_repos(project_key)
    else:
        repos = bb_server.get_all_repos()

    import_object = bb_server.generate_import_structure(repos, workspace, org_id, integration_id)

    with open("bitbucket_server_import_data.json", "w") as f:
        json.dump(import_object, f, indent=2)

if __name__ == "__main__":
    app()