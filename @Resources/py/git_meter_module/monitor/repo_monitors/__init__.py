from __future__ import annotations

import threading, sched, time
from git_meter_module import settings, monitor
from .repo_info import RepoInfo


class ReposMonitorBase:
    # Static
    _accessors: int = 0
    _instance: ReposMonitorBase = None
    
    # Instance
    repo_list: list[RepoInfo]
    # repo_count = settings.SettingRef[int]("github", "display-count")
    repo_count: settings.SettingRef[int]
    update_interval: settings.SettingRef[int]
    
    update_thread: threading.Thread
    update_event_loop_thread: threading.Thread
    
    update_sched: sched.scheduler
    update_event: sched.Event 
    
    kill_event_loop: bool = False
    
    @classmethod
    def get_instance(cls) -> ReposMonitorBase:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    @classmethod
    def set_instance(cls, p_instance: ReposMonitorBase):
        cls._instance = p_instance


    @classmethod
    def increase_accessors(cls):
        if cls._accessors == 0 and cls._instance is None:
            cls._instance = cls()
        cls._accessors += 1
        
    @classmethod
    def decrease_accessors(cls):
        cls._accessors -= 1
        
        if cls._accessors == 0:
            cls._instance.shutdown()
            cls._instance = None
    
    
    def __init__(self):
        # self.set_instance(self)
        self.update_thread = None
        
        self.repo_list = []
        for i in range(0, self.repo_count.val):
            self.repo_list.append(None)

        self.update_sched = sched.scheduler(time.time, time.sleep)
        self.on_update_event()
        
        self.update_event_loop_thread = threading.Thread(None, self.update_event_loop, f"{self.__class__.__name__}_Update_Event_Loop_{id(self)}")
        self.update_event_loop_thread.start()
    
    def on_update_event(self): 
        # print("update_event")
        self.update_async()
        self.update_event = self.update_sched.enter(
            self.update_interval.val * 60,
            1, 
            self.on_update_event
        )
        print(f"{self.__class__.__name__} will update again in {self.update_interval.val} minutes.")
    
    def update_event_loop(self):
        while not self.kill_event_loop:
            # print("checking")
            if not self.update_sched.empty():
                self.update_sched.run(False)
            
            time.sleep(1)
    
    def update_async(self):
        if self.update_thread is not None and self.update_thread.is_alive():
            print(f"Last update for {self.__class__.__name__} is still running...")
        else:
            self.update_thread = threading.Thread(None, self.update, f"{self.__class__.__name__}_Update_Thread_{id(self)}", daemon=True)
            self.update_thread.start()
    
    
    def update(self):
        print(f"{self.__class__.__name__} is updating...")
        # new_repo_list = sorted(self.account.get_user().get_repos(), key=lambda x: x.updated_at, reverse=True)
    
    
    def populate_repo_list(self, new_repo_list: list[RepoInfo], parser):
        for i in range(0, min(len(new_repo_list), self.repo_count.val)):
            self.repo_list[i] = parser(new_repo_list[i])
    
    def shutdown(self):
        print(f"Shutting down {self.__class__.__name__}...")
        self.kill_event_loop = True
        self.update_event_loop_thread.join()
        
        # if self.update_thread is not None and self.update_thread.is_alive():
        #     self.update_thread.join()

        self.update_sched.cancel(self.update_event)