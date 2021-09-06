from git_meter_module import settings
from git_meter_module.dynamic_inc_gen import repo_list_view

from PythonLoaderUtils.meaure_type import MeasureBase

class RegenControlMeasure(MeasureBase):
    def __init__(self):
        super().__init__()
        print("REGEN CONTROL")
        
    def ExecuteBang(self, args):
        settings.load_settings()
        repo_list_view.generate_repo_list_meters("local_repo_list", settings.current["local"]["display-count"])
        repo_list_view.generate_repo_list_meters("github_repo_list", settings.current["github"]["display-count"])
        