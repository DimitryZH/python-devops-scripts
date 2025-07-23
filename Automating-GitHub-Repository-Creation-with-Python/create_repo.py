from github import Github
import os

# === 1. USER SETTINGS ===
GITHUB_TOKEN = "your_personal_access_token_here"
REPO_NAME = "python-datadog-monitoring-automation"
REPO_DESCRIPTION = "Automation for monitoring with Datadog using Python."
PRIVATE = False  # Set to True if you want the repo to be private

# === 2. INITIAL FILE STRUCTURE ===
files = {
    "README.md": "# Python Datadog Monitoring Automation\n\nThis project automates monitoring checks using the Datadog API.",
    "requirements.txt": "datadog\nPyYAML",
    "config/secrets.yaml": "# Secrets file\napi_key: YOUR_API_KEY\napp_key: YOUR_APP_KEY\nslack_webhook: YOUR_WEBHOOK_URL",
    "scripts/monitor_checker.py": "# Main monitoring script\n\nprint('Running Datadog monitor check...')",
    "logs/execution.log": "",  # Optional empty log file
}


# === 3. CREATE GITHUB REPO AND FILES ===
def create_github_repo():
    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    # Check if repo already exists
    for repo in user.get_repos():
        if repo.name == REPO_NAME:
            print(f"Repository '{REPO_NAME}' already exists.")
            return repo

    repo = user.create_repo(
        name=REPO_NAME, description=REPO_DESCRIPTION, private=PRIVATE, auto_init=False
    )
    print(f"Repository '{REPO_NAME}' created.")
    return repo


def create_files_in_repo(repo):
    for path, content in files.items():
        repo.create_file(path, f"Add {path}", content)
        print(f"Added: {path}")


if __name__ == "__main__":
    repo = create_github_repo()
    if repo:
        create_files_in_repo(repo)
