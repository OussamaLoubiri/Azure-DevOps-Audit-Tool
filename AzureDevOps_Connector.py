import requests
from collections import defaultdict

AZURE_DEVOPS_ORG = "Organization Name"
AZURE_DEVOPS_AUTH = ("", "xriw6ah6xn6kbtouyt7jq6yvebq345hpc2oonwokhw7prkbulnuq")

def get_projects():
    # Sending a GET request to the Azure DevOps REST API to get the list of projects
    response = requests.get(f'https://dev.azure.com/{AZURE_DEVOPS_ORG}/_apis/projects?api-version=7.0', auth=AZURE_DEVOPS_AUTH)

    # Check the status code of the response
    if response.status_code != 200:
        print('Error: API request was not successful')
        return []

    # Geting the JSON response
    projects = response.json()["value"]
    return projects

def get_repositories(project_name):
    # Sending a GET request to the Azure DevOps REST API to get the list of repositories
    response = requests.get(f'https://dev.azure.com/{AZURE_DEVOPS_ORG}/{project_name}/_apis/git/repositories?api-version=7.0', auth=AZURE_DEVOPS_AUTH)

    # Check the status code of the response
    if response.status_code != 200:
        print(f'Error: API request for project "{project_name}" was not successful')
        return []

    # Geting the JSON response
    repositories = response.json()

    # Check if the JSON response is valid
    if 'value' in repositories:
        # Extract the repository names and sizes from the JSON response
        repo_data = [(repo['name'], repo['size']) for repo in repositories['value']]
        return repo_data

    print(f'Error: JSON response for project "{project_name}" is invalid')
    return []

def get_feeds(project_name):
        # Sending a GET request to the Azure DevOps REST API to get the list of Feeds
        response = requests.get(f'https://feeds.dev.azure.com/{AZURE_DEVOPS_ORG}/%s/_apis/packaging/Feeds?api-version=7.0'%(project_name), auth=AZURE_DEVOPS_AUTH)

        # Check the status code of the response
        if response.status_code != 200:
            print(f'Error: API request for project "{project_name}" was not successful')
        else:
            # Getting the JSON response
            feeds = response.json()

            # Check if the JSON response is valid
            if 'value' in feeds:
                # Extract the repository names from the JSON response
                feed_data =  [(feed['name'], feed['url'], feed['upstreamSources']) for feed in feeds['value']]
                return feed_data

            print(f'Error: JSON response for project "{project_name}" is invalid')
            return []

def get_Pipelines(project_name):
        # Sending a GET request to the Azure DevOps REST API to get the list of Pipelines
        response = requests.get(f'https://dev.azure.com/{AZURE_DEVOPS_ORG}/%s/_apis/pipelines?api-version=7.0'%(project_name), auth=AZURE_DEVOPS_AUTH)

        # Check the status code of the response
        if response.status_code != 200:
            print(f'Error: API request for project "{project_name}" was not successful')
        else:
            # Get the JSON response
            pipelines = response.json()

            # Checking if the JSON response is valid
            if 'value' in pipelines:
                # Extract the repository names from the JSON response
                pipline_data = [(pipeline['name']) for pipeline in pipelines['value']]
                return pipline_data

            print(f'Error: JSON response for project "{project_name}" is invalid')
            return[]

def get_memberships(project_name, project_id):

        # Getting the scope descriptor for the project
        response = requests.get(f"https://vssps.dev.azure.com/{AZURE_DEVOPS_ORG}/_apis/graph/descriptors/{project_id}", auth=AZURE_DEVOPS_AUTH)

        if response.status_code == 200:
            scope_descriptor = response.json()["value"]
            
            # Use the scope descriptor and storage key to get the list of users in the project
            response = requests.get(f"https://vssps.dev.azure.com/{AZURE_DEVOPS_ORG}/_apis/graph/users?scopeDescriptor={scope_descriptor}&api-version=6.0-preview.1", auth=AZURE_DEVOPS_AUTH)
            
            if response.status_code == 200:
                users = response.json()["value"]
                user_groups = defaultdict(set)
                for user in users:
                    if '_links' in user:
                        if 'memberships' in user['_links']:
                            memberships_href = user['_links']['memberships']['href']
                            response = requests.get(f"{memberships_href}", auth=AZURE_DEVOPS_AUTH)
                            if response.status_code == 200:
                                memberships = response.json()["value"]
                                for membership in memberships:
                                    if '_links' in membership:
                                        if 'container' in membership['_links']:
                                            container_href = membership['_links']['container']['href']
                                            response = requests.get(f"{container_href}", auth=AZURE_DEVOPS_AUTH)
                                            group = response.json()
                                            user_groups[user["displayName"]].add(group["displayName"])
                return user_groups

            print(f"Failed to get list of users for project {project_name}. Status code: {response.status_code}")
            return[]
