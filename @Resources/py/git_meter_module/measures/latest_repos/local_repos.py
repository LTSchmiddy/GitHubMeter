from . import LatestReposMeasureBaseType
from git_meter_module.monitor.repo_monitors.local_repo_list import LocalReposMonitor

class LocalLatestReposMeasure(LatestReposMeasureBaseType(LocalReposMonitor)):
    def GetString(self):
        return f"Latest Repos on Disk"