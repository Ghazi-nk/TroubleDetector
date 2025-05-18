import os
import requests
from pathlib import Path
import load_dotenv
# ======== CONFIGURATION ========

load_dotenv.load_dotenv()  # Load environment variables from .env file
#repo_full_name = "ghazi-nk/heybot"  # Format: owner/repo
api_token = os.getenv("GITHUB_PAT")
destination_folder = Path("project")  # Folder to save files


# ===============================

def get_default_branch(repo_full_name, headers):
    url = f"https://api.github.com/repos/{repo_full_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("default_branch", "main")


def get_all_file_paths(repo_full_name, branch, headers):
    url = f"https://api.github.com/repos/{repo_full_name}/git/trees/{branch}?recursive=1"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    tree = response.json().get("tree", [])
    return [item["path"] for item in tree if item["type"] == "blob"]


def download_and_save_file(repo_full_name, branch, file_path, headers):
    raw_url = f"https://raw.githubusercontent.com/{repo_full_name}/{branch}/{file_path}"
    response = requests.get(raw_url, headers=headers)
    response.raise_for_status()
    save_path = destination_folder / file_path
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)
    print(f"✓ Saved: {file_path}")


def retrieve_repo(repo_full_name):
    headers = {"Authorization": f"token {api_token}"} if api_token else {}
    print(f"📦 Cloning {repo_full_name} into '{destination_folder}'")

    branch = get_default_branch(repo_full_name, headers)
    print(f"🌿 Default branch: {branch}")

    file_paths = get_all_file_paths(repo_full_name, branch, headers)
    print(f"📄 Files to download: {len(file_paths)}")

    for path in file_paths:
        download_and_save_file(repo_full_name, branch, path, headers)

    print("✅ All files downloaded!")


# Run the script
if __name__ == "__main__":
    retrieve_repo("ghazi-nk/heybot")
