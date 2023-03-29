import subprocess
from Markdown_Publisher import clone_or_update_repo, commit_and_push_changes, save_markdown_to_file
from AzureDevOps_Connector import get_projects, get_repositories, get_feeds, get_Pipelines, get_memberships
from EngineBootsrtap_Exectution import check_repository_size, check_number_of_pipelines, Check_UserMemberships
from AzureResources_Connector import get_azure_resources

def generate_markdown_output(projects):

    # Loging in to Azure using the az login command
    subprocess.run(["cmd.exe", "/c","az", "login"], stdout=subprocess.DEVNULL)
    # Initialize the markdown output string
    markdown_output = '[[_TOC_]]\n'

    for project in projects:
        project_name = project["name"]
        project_id = project['id']

        repo_data = get_repositories(project_name)

        # Adding the project name and repository names to the markdown output
        markdown_output += f'# {project_name}\n\n'
        markdown_output += f'## {project_name}: Repositories\n\n'
        markdown_output += '| Name | Size |\n'
        markdown_output += '|------|------|\n'
        for repo_name, size in repo_data:
            markdown_output += f'| {repo_name} | {size/1024/1024 : .2f}MB |\n'
        
        #Loading Repo Data to the rule engine
        markdown_output += check_repository_size(repo_data)

        feed_data = get_feeds(project_name)

        # Add the project name and feed names to the markdown output
        markdown_output += f'## {project_name}: Feeds\n\n'
        markdown_output += '| Name | URL | Upstream Source |\n'
        markdown_output += '|------|-----|-----------------|\n'
        for feed_name, url, upstream_sources in feed_data:
            markdown_output += f'|{feed_name} | {url} | {upstream_sources}\n'

        pipelines_data = get_Pipelines(project_name)
     
        # Adding the project name and pipeline names to the markdown table
        markdown_output += f'## {project_name}: Pipelines\n\n'
        markdown_output += '| Name |\n'
        markdown_output += '|------|\n'
        for pipeline_name in pipelines_data:
            markdown_output += f'| {pipeline_name} |\n'

        #Loading Pipelines Data to the rule engine
        markdown_output += check_number_of_pipelines(pipelines_data)

        user_groups = get_memberships(project_name, project_id)

        markdown_output += f'## {project_name}: Users\n\n'
        markdown_output += '| Principal | Membership |\n'
        markdown_output += '|--|--|\n'
        for user, groups in user_groups.items():
            markdown_output += f"| {user} | {', '.join(groups)} |\n"

        #Loading memberships Data to the rule engine
        markdown_output += Check_UserMemberships(project_name, markdown_output)

        azure_resources = get_azure_resources(project_name)

        # Adding Azure resources to markdown output
        markdown_output += f'## {project_name}: Azure Resources\n\n'
        markdown_output += '| Name | Type | Resource Group |\n'
        markdown_output += '|------|------|----------------|\n'
        for resource in azure_resources:
            markdown_output += f'| {resource["name"]} | {resource["type"]} | {resource["group"]} |\n'

    return markdown_output

repo = clone_or_update_repo()

projects = get_projects()

markdown_output = generate_markdown_output(projects)
            
save_markdown_to_file(markdown_output)

commit_and_push_changes(repo)
