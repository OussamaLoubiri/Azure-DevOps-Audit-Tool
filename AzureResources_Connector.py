import subprocess
import json

def get_azure_resources(project_name):

    # Retrieve all resource groups with the project tag
    resource_groups = subprocess.run(["cmd.exe", "/c",'az', 'group', 'list', '--tag', f'project={project_name}', '--output', 'json'], capture_output=True)
    resource_groups = resource_groups.stdout.decode().strip()
    resource_groups = json.loads(resource_groups)

    azure_resources = []

    # Iterate through each resource group
    for resource_group in resource_groups:
        resource_group_name = resource_group['name']

        # Retrieve all resources inside the resource group
        resources = subprocess.run(["cmd.exe", "/c",'az', 'resource', 'list', '--resource-group', resource_group_name, '--output', 'json'], capture_output=True)
        resources = resources.stdout.decode().strip()
        resources = json.loads(resources)

        # Iterate through each resource
        for resource in resources:
            resource_name = resource['name']
            resource_type = resource['type']
            azure_resources.append({'name': resource_name,'type': resource_type,'group': resource_group_name})

    return azure_resources


