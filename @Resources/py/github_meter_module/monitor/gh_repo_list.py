from __future__ import annotations

import threading, sched, time

from github.MainClass import Github
from github.Repository import Repository

from github_meter_module import settings, monitor

from .repo_info import RepoInfo

class GHUserReposMonitor:
    _accessors: int = 0
    _instance: GHUserReposMonitor = None
    # Static
    repo_count: int = 5
    
    # Instance
    account: Github
    login_name: str
    repo_list: list[RepoInfo]
    
    update_thread: threading.Thread
    update_event_loop_thread: threading.Thread
    
    update_sched: sched.scheduler
    update_event: sched.Event 
    
    kill_event_loop: bool = False
    
    @classmethod
    def get_instance(cls) -> GHUserReposMonitor:
        if cls._instance is None:
            cls._instance = cls(monitor.get_account())
        return cls._instance


    @classmethod
    def set_instance(cls, p_instance: GHUserReposMonitor):
        cls._instance = p_instance


    @classmethod
    def increase_accessors(cls):
        if cls._accessors == 0 and cls._instance is None:
            cls._instance = cls(monitor.get_account())
        cls._accessors += 1
        
    @classmethod
    def decrease_accessors(cls):
        cls._accessors -= 1
        
        if cls._accessors == 0:
            cls._instance.shutdown()
            cls._instance = None
    
    
    
    def __init__(self, p_account: Github):
        # self.set_instance(self)
        self.account = p_account
        
        self.login_name = "Loading..."
        self.update_thread = None
        
        self.repo_list = []
        for i in range(0, self.repo_count):
            self.repo_list.append(None)

        self.update_sched = sched.scheduler(time.time, time.sleep)
        self.on_update_event()
        
        self.update_event_loop_thread = threading.Thread(None, self.update_event_loop, f"ReposMonitor_Update_Event_Loop_{id(self)}")
        self.update_event_loop_thread.start()
    
    def on_update_event(self): 
        # print("update_event")
        self.update_async()
        self.update_event = self.update_sched.enter(
            settings.current['general']['update-interval-min'] * 60,
            1, 
            self.on_update_event
        )
        print(f"GHUserReposMonitor will update again in {settings.current['general']['update-interval-min']} minutes.")
    
    def update_event_loop(self):
        while not self.kill_event_loop:
            # print("checking")
            if not self.update_sched.empty():
                self.update_sched.run(False)
            
            time.sleep(1)
    
    def update_async(self):
        if self.update_thread is not None and self.update_thread.is_alive():
            print("Last update is still running...")
        else:
            self.update_thread = threading.Thread(None, self.update, f"ReposMonitor_Update_Thread_{id(self)}")
            self.update_thread.start()
    
    def update(self):
        print("GHUserReposMonitor is updating...")
        self.login_name = self.account.get_user().login
        new_repo_list = sorted(self.account.get_user().get_repos(), key=lambda x: x.updated_at, reverse=True)
        
        for i in range(0, min(len(new_repo_list), self.repo_count)):
            self.repo_list[i] = RepoInfo.from_github_Repository(new_repo_list[i])
    
    def shutdown(self):
        print("Shutting down GHUserReposMonitor...")
        self.kill_event_loop = True
        self.update_event_loop_thread.join()
        
        # if self.update_thread is not None and self.update_thread.is_alive():
        #     self.update_thread.join()

        self.update_sched.cancel(self.update_event)
        