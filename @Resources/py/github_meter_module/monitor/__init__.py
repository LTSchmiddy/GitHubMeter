import github

from github_meter_module import settings

account: github.Github = None

def load_account():
    global account
    account = github.Github(settings.current['user']['token'])
    # account = github.Github("thewiseguyalex@gmail.com", password="Xxeellaa!!1")
    
    
def get_account() -> github.Github:
    global account
    return account


from . import gh_repo_list