# Audit Tool Architecture

This Audit Tool is a Python-based tool that can evaluate the compliance of Azure DevOps projects and Azure resources to specific policies. It consists of six Python files, each responsible for a specific functionality. 

## Components

![C4-final-Page-2](https://user-images.githubusercontent.com/74933380/228666251-24cd3424-91e4-4ce6-bf51-56575766badd.png)


The following is a brief description of each component:

1. `Orchestrator.py`: This Python file orchestrates the execution of the functions defined in the other Python files. It generates a Markdown output that summarizes information about Azure DevOps projects, Azure resources, and their compliance to the policies.

2. `AzureDevOps_Connector.py`: This Python file makes API calls to Azure DevOps to extract all the information related to the projects.

3. `AzureResource_Connector.py`: This Python file uses Azure CLI to extract the computing resources that are utilized by each Azure DevOps project.

4. `Engine_Rules_Definition.py`: This file contains the predefined rules that are going to be evaluated based on the extracted data.

5. `Engine_Bootstrap_and_Execution.py`: This file contains the inference engine, which is Experta. In this file, the extracted data from Azure DevOps is loaded into the engine along with the rules defined in the `Engine_Rules_Definition.py` file. After that, the engine is run, and the results are added to the generated Markdown output by the `Orchestrator.py` file.

6. `Markdown_Publisher.py`: This file is responsible for saving and committing the changes to publish them to a remote wiki repository in Azure DevOps where the Markdown file is going to be hosted.

## How to Run

To run the Audit Tool, follow these steps:

1. Open the `AzureDevOps_Connector.py` file and specify the following variables:

- `AZURE_DEVOPS_ORG`: Organization name.
- `AZURE_DEVOPS_AUTH`: Personal Access Token.

2. Open the `Markdown_Publisher.py` file and specify the following variable:

- `REPO_URL`: URL of the remote repository where you want to save the generated report.

3. Run the `Orchestrator.py` file to execute the Audit Tool. After running the `Orchestrator.py` file, a prompt will pop up asking you to log in using your username and password to authenticate with Azure.
