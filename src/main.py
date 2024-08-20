import typer
import requests
import json
import os

app = typer.Typer()

@app.command()
def test():
    print(f"Testing application. It works!")

@app.command()
def run(workspace: str, org_id: str, integration_id: str):
    username = os.getenv("BITBUCKET_CLOUD_USERNAME")
    app_password = os.getenv("BITBUCKET_CLOUD_PASSWORD")
    
    all_repos = get_projects_and_repos(username, app_password, workspace)

    import_object = generate_import_structure(all_repos, workspace, org_id, integration_id)

    with open("bitbucket_import_data.json", "w") as f:
        json.dump(import_object, f, indent=2)

def get_projects_and_repos(username, app_password, workspace):
    """Fetches all projects and repositories from a Bitbucket workspace and returns them as a list of dictionaries.

    Args:
        username (str): Bitbucket username.
        app_password (str): Bitbucket app password.
        workspace (str): Bitbucket workspace name.

    Returns:
        list: A list of dictionaries, each containing project and repository information.
    """

    base_url = "https://api.bitbucket.org/2.0/"

    auth = (username, app_password)
    headers = {"Accept": "application/json"}

    repos_url = f"{base_url}/repositories/{workspace}"
    next_page = None

    all_repos = []

    while True:
        url = repos_url
        if next_page:
            url += f"?next={next_page}"

        response = requests.get(url, auth=auth, headers=headers)
        
        if response.status_code != 200:
            print(f"Expected status code 200, received {response.status_code}")

        data = response.json()
        all_repos.extend(data["values"])

        next_page = data.get("next")
        if not next_page:
            break

    return all_repos

def generate_import_structure(repos, workspace, orgId, integrationId, files=[], exclusionGlobs = ""):

    targets = []

    for repo in repos:
        name = repo["name"]
        branch = repo["mainbranch"]["name"]

        target = {
            "orgId": orgId,
            "integrationId": integrationId,
            "target": {
                "owner": workspace,
                "name": name,
                "branch": branch
            }
        }

        if len(files) > 0:
            target["files"] = files
        
        if len(exclusionGlobs) > 0:
            target["exclusionGlobs"] = exclusionGlobs

        targets.append(target)
    
    import_object = {
        "targets": targets
    }

    return import_object

if __name__ == "__main__":
    app()