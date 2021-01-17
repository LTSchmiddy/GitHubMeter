import github

from git_meter_module import settings

account: github.Github = None

def load_account():
    global account
    account = github.Github(settings.current['github']['user-token'])
    
    
def get_account() -> github.Github:
    global account
    return account


from .repo_monitors import gh_repo_list
from .repo_monitors import local_repo_list