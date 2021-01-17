from typing import TypeVar, Generic

from datetime import datetime, timezone
from git_meter_module.monitor.repo_monitors import ReposMonitorBase

from tzlocal import get_localzone

from PythonLoaderUtils.rm_stub import RainmeterW
from PythonLoaderUtils.meaure_type import MeasureBase

def LatestReposMeasureBaseType(set_base: ReposMonitorBase = ReposMonitorBase):
    class LatestReposMeasureBase(MeasureBase):
        monitor_base: ReposMonitorBase = ReposMonitorBase
        
        sPath: str
        rm: RainmeterW
        
        login_name: str
        
        def __init__(self):
            super().__init__()
            self.monitor_base.increase_accessors()
            self.monitor_base.get_instance().update_async()

            self.sPath = None
            
            
        def Reload(self, rm: RainmeterW, maxValue: float):
            self.rm = rm
            
            # self.sPath = pathlib.Path(rm.RmReplaceVariables("#CURRENTPATH#")).joinpath(rm.RmReplaceVariables("#CURRENTFILE#"))
            # print(self.sPath)
            
            
        def Update(self):        
            return 1.0

        def GetString(self):
            return f"Latest Repos: "
            # return f"Latest Repos for {T.get_instance().login_name}"

        def ExecuteBang(self, args):
            pass

        def Finalize(self):
            super().Finalize()
            self.monitor_base.decrease_accessors()
        
        
        def RepoName(self, p_index: str):
            index = int(p_index)
            repo = self.monitor_base.get_instance().repo_list[index]
            if repo == None:
                return "None"
            
            return repo.name
        
        def RepoUpdatedAt(self, p_index: str):
            index = int(p_index)
            repo = self.monitor_base.get_instance().repo_list[index]
            if repo == None:
                return "None"
            
            # return str(repo.updated_at)
            return str(repo.last_update.astimezone(get_localzone()).strftime("%a, %b %d %Y - %I:%M %p"))
        
        def RepoLastCommitMessage(self, p_index: str):
            index = int(p_index)
            repo = self.monitor_base.get_instance().repo_list[index]
            if repo == None:
                return "None"
            
            # return str(repo.updated_at)
            return str(repo.last_commit_message)
        
        def RepoLastCommitAuthor(self, p_index: str):
            index = int(p_index)
            repo = self.monitor_base.get_instance().repo_list[index]
            if repo == None:
                return "None"
            
            # return str(repo.updated_at)
            return str(repo.last_commit_author)
        
        def RepoContentAddress(self, p_index: str):
            index = int(p_index)
            repo = self.monitor_base.get_instance().repo_list[index]
            if repo == None:
                return "None"
            
            # return str(repo.updated_at)
            return str(repo.content_address)
    
    LatestReposMeasureBase.monitor_base = set_base
    return LatestReposMeasureBase