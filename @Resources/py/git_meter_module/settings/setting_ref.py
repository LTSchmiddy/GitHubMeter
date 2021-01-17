from typing import TypeVar, Generic

from git_meter_module import settings


T = TypeVar('T')
class SettingRef(Generic[T]):
    
    def __init__(self, *setting_path):
        self.setting_path = setting_path
        
    @property
    def val(self) -> T:
        s_pos = settings.current
        for i in self.setting_path:
            s_pos = s_pos[i]
        
        return s_pos
    
    @val.setter
    def val(self, value: T):
        s_pos = settings.current
        for i in self.setting_path[:-1]:
            s_pos = s_pos[i]
        
        s_pos[self.setting_path[-1]] = value