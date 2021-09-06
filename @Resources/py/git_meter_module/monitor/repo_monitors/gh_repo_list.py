from __future__ import annotations

import threading, sched, time

from github.MainClass import Github
from github.Repository import Repository

from git_meter_module import settings, monitor

from . import ReposMonitorBase
from .repo_info import RepoInfo

class GHUserReposMonitor(ReposMonitorBase):
    # Static
    repo_count = settings.SettingRef[int]("github", "display-count")
    update_interval = settings.SettingRef[int]("github", "update-interval-min")
    
    # Instance
    account: Github
    login_name: str   
    
    def __init__(self):
        self.account = monitor.get_account()
        self.login_name = "Loading..."
        settings.load_settings()
        super().__init__()
        
    
    def update(self):
        super().update()
        self.login_name = self.account.get_user().login
        self.populate_repo_list(
            sorted(self.account.get_user().get_repos(), key=lambda x: x.updated_at, reverse=True),
            RepoInfo.from_github_Repository
        )
        


        