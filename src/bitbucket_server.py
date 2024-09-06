import requests

class BitbucketServer:
    base_url = ""

    headers = {}

    def __init__(self, username="", app_password="", bitbucketurl="", token=""):
        self.base_url = f"{bitbucketurl}rest/api/1.0/"
        self.set_auth_token(token)


    def set_auth_token(self, token):
        self.headers = {"content-type": "application/json",
                     "Authorization": f"Bearer {token}"}
    
    def get_projects(self):
        url = f"{self.base_url}projects"

        headers = self.headers

        last_page = False
        start = 0
        limit = 25

        params = {"start": start, "limit":limit}

        print(url)

        all_projects = []

        while not last_page:
            
            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                print(f"Expected status code 200, received {response.status_code}")
            
            data = response.json()

            projects = data.get("values")

            all_projects.extend(projects)

            params["start"] += limit

            last_page = data["isLastPage"]

        return all_projects


    def get_repos(self, project_key):
        url = f"{self.base_url}projects/{project_key}/repos"

        headers = self.headers

        last_page = False
        start = 0
        limit = 25

        params = {"start": start, "limit":limit}

        all_repos = []

        while not last_page:

            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                print(f"Expected status code 200, received {response.status_code}")
            
            data = response.json()

            repos = data.get("values")
            
            all_repos.extend(repos)
            last_page = data["isLastPage"]

        return all_repos

    def get_all_repos(self):
        print("Fetching all Projects")
        projects = self.get_projects()

        print(f"Found {len(projects)} projects")

        all_repos = []

        print("Fetching all Repos")
        numberofProjects = 0
        for project in projects:
            project_key = project["key"]

            repos = self.get_repos(project_key=project_key)

            all_repos.extend(repos)
            numberofProjects+=1
            if numberofProjects == 5:
                break

            

        return all_repos

    def generate_import_structure(self, repos, orgId, integrationId):
        targets = []

        for repo in repos:
            name = repo["name"]
            branch = repo["defaultBranch"]
            project = repo["project"]["key"]

            target = {
                "orgId": orgId,
                "integrationId": integrationId,
                "target": {
                    "owner": project,
                    "name": name,
                    "branch": branch
                }
            }

            targets.append(target)
        
        import_object = {
            "targets": targets
        }