import typer
import requests
import json

app = typer.Typer()

@app.command()
def test():
    print(f"Testing application. It works!")

def get_projects_and_repos(username, app_password, workspace):
    """Fetches all projects and repositories from a Bitbucket workspace and returns them as a list of dictionaries.

    Args:
        username (str): Bitbucket username.
        app_password (str): Bitbucket app password.
        workspace (str): Bitbucket workspace name.

    Returns:
        list: A list of dictionaries, each containing project and repository information.
    """

    base_url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}"
    auth = (username, app_password)
    headers = {"Accept": "application/json"}

    projects = []
    next_page = None

    while True:
        url = f"{base_url}/projects"
        if next_page:
            url += f"?next={next_page}"

        response = requests.get(url, auth=auth, headers=headers)
        response.raise_for_status()

        data = response.json()
        projects.extend(data["values"])

        next_page = data.get("next")
        if not next_page:
            break

    all_repos = []
    for project in projects:
        project_key = project["key"]
        repos_url = f"{base_url}/projects/{project_key}/repos"
        next_page = None

        while True:
            url = repos_url
            if next_page:
                url += f"?next={next_page}"

            response = requests.get(url, auth=auth, headers=headers)
            response.raise_for_status()

            data = response.json()
            all_repos.extend(data["values"])

            next_page = data.get("next")
            if not next_page:
                break

    return all_repos

@app.command()
def run():
    username = "your_username"
    app_password = "your_app_password"
    workspace = "your_workspace"

    all_repos = get_projects_and_repos(username, app_password, workspace)

    with open("bitbucket_data.json", "w") as f:
        json.dump(all_repos, f, indent=2)

if __name__ == "__main__":
    app()