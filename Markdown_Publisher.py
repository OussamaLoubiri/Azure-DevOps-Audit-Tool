import os
import git

REPO_URL = f"https://dev.azure.com/SES-Techcom/AVOBPADO/_git/audit-tool-wiki"
LOCAL_PATH = "audit_tool_wiki"
FILE_NAME = 'wiki/SES_Projects.md'

def clone_or_update_repo():
    if not os.path.exists(LOCAL_PATH):
        repo = git.Repo.clone_from(REPO_URL, LOCAL_PATH)
        os.chdir(LOCAL_PATH)
    else:
        os.chdir(LOCAL_PATH)
        repo = git.Repo.init()
    return repo

def save_markdown_to_file(markdown_output):
    with open(FILE_NAME, 'w') as file:
        file.write(markdown_output)
    print(f'Successfully saved the Azure DevOps report as markdown to "{FILE_NAME}"')

def commit_and_push_changes(repo):
    # Adding the markdown file to the repository
    repo.index.add(FILE_NAME)

    # Committing the changes to the repository
    repo.index.commit("Added SES ADO Markdown table Report")

    # Pushing the changes to the remote repository
    origin = repo.remote(name='origin')
    origin.push()