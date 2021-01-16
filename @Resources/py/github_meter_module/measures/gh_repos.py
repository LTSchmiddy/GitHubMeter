import pathlib
from datetime import datetime, timezone

import github
from tzlocal import get_localzone
import pytz

from PythonLoaderUtils.rm_stub import RainmeterW
from PythonLoaderUtils.meaure_type import MeasureBase

from github_meter_module.monitor.gh_repo_list import GHUserReposMonitor



class GHLatestReposMeasure(MeasureBase):
    
    sPath: str
    rm: RainmeterW
    
    login_name: str
    
    def __init__(self):
        super().__init__()
        GHUserReposMonitor.increase_accessors()
        GHUserReposMonitor.get_instance().update_async()

        self.sPath = None
        
        
    def Reload(self, rm: RainmeterW, maxValue: float):
        self.rm = rm
        
        # self.sPath = pathlib.Path(rm.RmReplaceVariables("#CURRENTPATH#")).joinpath(rm.RmReplaceVariables("#CURRENTFILE#"))
        # print(self.sPath)
        
        
    def Update(self):        
        return 1.0

    def GetString(self):
        # return UserReposMonitor.get_instance().account.get_user().login
        return f"Latest Repos for {GHUserReposMonitor.get_instance().login_name}"

    def ExecuteBang(self, args):
        pass

    def Finalize(self):
        super().Finalize()
        GHUserReposMonitor.decrease_accessors()
    
    
    def RepoName(self, p_index: str):
        index = int(p_index)
        repo = GHUserReposMonitor.get_instance().repo_list[index]
        if repo == None:
            return "None"
        
        return repo.name
    
    def RepoUpdatedAt(self, p_index: str):
        index = int(p_index)
        repo = GHUserReposMonitor.get_instance().repo_list[index]
        if repo == None:
            return "None"
        
        as_utc = datetime(
            repo.last_update.year,
            repo.last_update.month,
            repo.last_update.day,
            repo.last_update.hour,
            repo.last_update.minute,
            repo.last_update.second,
            repo.last_update.microsecond,
            tzinfo=timezone.utc)
        # return str(repo.updated_at)
        return str(as_utc.astimezone(get_localzone()).strftime("%a, %b %d %Y - %I:%M %p"))
    
    def RepoLastCommitMessage(self, p_index: str):
        index = int(p_index)
        repo = GHUserReposMonitor.get_instance().repo_list[index]
        if repo == None:
            return "None"
        
        # return str(repo.updated_at)
        return str(repo.last_commit_message)
    
    def RepoLastCommitAuthor(self, p_index: str):
        index = int(p_index)
        repo = GHUserReposMonitor.get_instance().repo_list[index]
        if repo == None:
            return "None"
        
        # return str(repo.updated_at)
        return str(repo.last_commit_author)
    
    def RepoContentAddress(self, p_index: str):
        index = int(p_index)
        repo = GHUserReposMonitor.get_instance().repo_list[index]
        if repo == None:
            return "None"
        
        # return str(repo.updated_at)
        return str(repo.content_address)
    