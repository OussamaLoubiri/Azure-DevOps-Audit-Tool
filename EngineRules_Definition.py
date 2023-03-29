from experta import *

# Maximum number of Repositories Rules
class Repositories(Fact):
    """Info about the repository"""
    pass

class RepositoriesChecker(KnowledgeEngine):

    @Rule(Repositories(names=P(lambda x: len(x) > 3)))
    def limit_exceeded(self):
        self.result = "Limit exceeded. More than 3 Pipelines.\n"

    @Rule(Repositories(names=P(lambda x: len(x) <= 3)))
    def limit_not_exceeded(self):
        self.result = "Limit not exceeded. 3 or less Pipelines.\n"

########################
# Maximum size of repositories Rules

class RepositorySize(Fact):
    """Info about the repository"""
    pass

class RepositorySizeChecker(KnowledgeEngine):

    @Rule(RepositorySize(name=MATCH.name, size=MATCH.size), 
          TEST(lambda size: size > 8 * 1024*1024)) # limit is 10 MB in bytes
    def size_exceeded(self, name, size):
        # size_mb = round(size / 1024/1024, 2)
        self.sizeResult = f"Repository {name} has exceeded the size limit.\n"
        self.Rulefired = True

########################
# Users Membership Rules

class Principal(Fact):
    pass

class MembershipRule(KnowledgeEngine):
    @Rule(Principal(Principal=MATCH.principal, Membership=MATCH.membership),
        TEST(lambda membership: "Project Collection Administrators" not in membership),
        TEST(lambda membership: "Project-Scoped Users" not in membership))
    def membership_compliance(self, principal):
        self.non_compliant_principals.append(principal)

    @Rule(Principal(Principal=MATCH.principal, Membership=MATCH.membership),
        TEST(lambda membership: "Project Collection Administrators" in membership),
        TEST(lambda membership: "Project-Scoped Users" in membership))
    def membership_compliant(self, principal):
        self.non_compliant_principals1.append(principal)
