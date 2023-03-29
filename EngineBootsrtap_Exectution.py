from EngineRules_Definition import RepositoriesChecker, Repositories
from EngineRules_Definition import MembershipRule, Principal
from EngineRules_Definition import RepositorySize,RepositorySizeChecker
import re

def check_repository_size(repo_data):
    engine_repos_size = RepositorySizeChecker()
    engine_repos_size.Rulefired = False
    for Repo in repo_data:
        engine_repos_size.reset()  # reset the engine before each iteration
        engine_repos_size.declare(RepositorySize(name=Repo[0], size=Repo[1]))  # declare the repository as a fact
        engine_repos_size.run()  # run the engine to check the repository information

    if engine_repos_size.Rulefired:
        return engine_repos_size.sizeResult
    else:
        return "All repositories meet the size limit.\n"


def check_number_of_pipelines(pipelines_data):
    engine_pip = RepositoriesChecker()

    pip_names = [pip for pip in pipelines_data]
    engine_pip.reset()
    engine_pip.declare(Repositories(names=pip_names))
    engine_pip.run()
    return engine_pip.result

def Check_UserMemberships(project_name, markdown_output):

    engine_users = MembershipRule()
    data = []
    flag = False
    markdown_output1 = ""
    for line in markdown_output.split("\n"):
        if f"## {project_name}: Users" in line:
            flag = True
        elif f"## {project_name}:" in line and "Users" not in line:
            flag = False
        if flag:
            match = re.search("^\| (.*?) \| (.*?) \|", line)
            if match and match.group(1) != "Principal":
                data.append({"Principal": match.group(1), "Membership": match.group(2).split(", ")})

    engine_users.non_compliant_principals = []
    engine_users.non_compliant_principals1 = []

    for item in data:
        engine_users.reset() 
        engine_users.declare(Principal(Principal=item["Principal"], Membership=item["Membership"]))
        engine_users.run()
    
    if engine_users.non_compliant_principals:
        markdown_output1 += "The following users are not compliant:\nThey don't have neither Project Collection Administrators or Project-Scoped Users membership:\n"
        for principal in engine_users.non_compliant_principals:
            markdown_output1 += (f"- {principal}\n")
            
    if engine_users.non_compliant_principals1:
        markdown_output1 += "\nThe following users are not compliant:\nThey have both memberships Project Collection Administrators and Project-Scoped Users:\n"
        for principal in engine_users.non_compliant_principals1:
            markdown_output1 += (f"- {principal}\n")
    
    if not engine_users.non_compliant_principals and not engine_users.non_compliant_principals1 :
        markdown_output1 += "All users are compliant.\n"
    
    return markdown_output1