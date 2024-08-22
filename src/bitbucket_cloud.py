import requests

class BitbucketCloud:
    auth = {}

    def __init__(self, username="", app_password="", token=""):
        if username != "" and app_password != "":
            self.set_auth_username_pw(username, app_password)
        else:
            self.set_auth_token(token)

    def set_auth_username_pw(self, username, app_password):
        self.auth = {
            username, app_password
        }

    def set_auth_token(self, token):
        self.auth = {"Authorization": f"Bearer {token}"}    

    def get_projects_and_repos(self, workspace):
        """Fetches all projects and repositories from a Bitbucket workspace and returns them as a list of dictionaries.

        Args:
            username (str): Bitbucket username.
            app_password (str): Bitbucket app password.
            workspace (str): Bitbucket workspace name.

        Returns:
            list: A list of dictionaries, each containing project and repository information.
        """

        base_url = "https://api.bitbucket.org/2.0/"

        headers = {"Accept": "application/json"}

        repos_url = f"{base_url}/repositories/{workspace}"
        next_page = None

        all_repos = []

        while True:
            url = repos_url
            if next_page:
                url += f"?next={next_page}"

            response = requests.get(url, auth=self.auth, headers=headers)
            
            if response.status_code != 200:
                print(f"Expected status code 200, received {response.status_code}")

            data = response.json()
            all_repos.extend(data["values"])

            next_page = data.get("next")
            if not next_page:
                break

        return all_repos

    def generate_import_structure(self, repos, workspace, orgId, integrationId, files=[], exclusionGlobs = ""):

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