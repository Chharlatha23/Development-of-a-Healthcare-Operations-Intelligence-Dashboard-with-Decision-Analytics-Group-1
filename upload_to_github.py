import urllib.request
import json
import base64
import os
import sys

REPO_OWNER = "Chharlatha23"
REPO_NAME = "Development-of-a-Healthcare-Operations-Intelligence-Dashboard-with-Decision-Analytics-Group-1"

def push_file(file_path, repo_path, token):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    
    with open(file_path, "rb") as f:
        content = f.read()
    
    encoded_content = base64.b64encode(content).decode("utf-8")
    
    # Check if file exists to get sha
    sha = None
    req = urllib.request.Request(url, headers={"Authorization": f"token {token}", "User-Agent": "Python"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            sha = data.get("sha")
    except Exception:
        pass

    payload = {
        "message": f"Upload {repo_path} via API",
        "content": encoded_content
    }
    if sha:
        payload["sha"] = sha
        
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, method="PUT", headers={
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
        "User-Agent": "Python"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Successfully uploaded: {repo_path}")
    except Exception as e:
        print(f"Error uploading {repo_path}: {e}")

if __name__ == "__main__":
    token = input("Enter your GitHub Personal Access Token (PAT): ").strip()
    if not token:
        print("Token is required to push to GitHub.")
        sys.exit(1)
        
    print("\nUploading project files to GitHub...")
    push_file("README.md", "README.md", token)
    push_file("Raw Dataset/Admissions_filled.csv", "Raw Dataset/Admissions_filled.csv", token)
    print("\nFinished! Check your repository at:")
    print(f"https://github.com/{REPO_OWNER}/{REPO_NAME}")
