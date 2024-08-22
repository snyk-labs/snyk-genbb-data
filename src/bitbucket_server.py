import requests

class BitbucketServer:
    base_url = ""

    auth = {}

    def __init__(self, tenant, username, app_password):
        self.base_url = f"https://bitbucket.{tenant}.com/rest/api/1.0/"

        self.auth.username = {username, app_password}
        pass
    
    def get_projects(self):
        url = self.base_url + "api/latest/projects"

        headers = {"Accept": "application/json"}

        last_page = False
        start = 0
        limit = 25

        params = {"start": start, "limit":limit}

        all_projects = []

        while not last_page:
            
            response = requests.get(url, params=params, auth=self.auth, headers=headers)

            if response.status_code != 200:
                print(f"Expected status code 200, received {response.status_code}")
            
            data = response.json()

            projects = data.get("values")

            all_projects.extend(projects)

            params("start") += limit

            last_page = data["isLastPage"]

        return all_projects


    def get_repos(self, project_key):
        url = self.base_url + f"api/latest/projects/{project_key}/repos"

        headers = {"Accept": "application/json"}

        last_page = False
        start = 0
        limit = 25

        params = {"start": start, "limit":limit}

        all_repos = []

        while not last_page:

            response = requests.get(url, params=params, auth=self.auth, headers=headers)

            if response.status_code != 200:
                print(f"Expected status code 200, received {response.status_code}")
            
            data = response.json()

            repos = data.get("values")
            
            all_repos.extend(repos)

        return all_repos

    def get_all_repos(self):
        projects = self.get_projects

        all_repos = []

        for project in projects:
            project_key = project("key")

            repos = self.get_repos(project_key=project_key)

            all_repos.extend(repos)

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