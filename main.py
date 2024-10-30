import requests
import json

with open("config.json") as config_file:
    config = json.load(config_file)

print(config)

gh_user = config["github"]["user"]
gh_token = config["github"]["token"]
gitea_url = config["gitea"]["url"]
gitea_user = config["gitea"]["user"]
gitea_token = config["gitea"]["token"]

gh_repo_list = requests.get(
    f"https://api.github.com/users/{gh_user}/repos",
    headers={"Authorization": f"Bearer {gh_token}"},
).json()
gh_repo_list = [repo["name"] for repo in gh_repo_list]
gitea_repo_list = requests.get(
    f"{gitea_url}/api/v1/users/{gitea_user}/repos",
    headers={"Authorization": f"token {gitea_token}"},
).json()
gitea_repo_list = [repo["name"] for repo in gitea_repo_list]
repos_to_migrate = [repo for repo in gh_repo_list if repo not in gitea_repo_list]

for repo in repos_to_migrate:
    print(f"Migrating {repo}...")
    migrate_request = requests.post(
        f"{gitea_url}/api/v1/repos/migrate",
        headers={"Authorization": f"token {gitea_token}"},
        json={
            "auth_password": gh_token,
            "auth_username": gh_user,
            "clone_addr": f"https://github.com/{gh_user}/{repo}",
            "repo_name": repo,
            "mirror": True,
            "repo_owner": gitea_user,
        },
    )
    print(
        "Migrated",
        "successfully!" if migrate_request.status_code == 201 else "unsuccessfully!",
    )
