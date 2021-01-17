from __future__ import annotations

import os, pathlib, traceback

from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from threading import Thread

from git_meter_module import settings
from . import ReposMonitorBase
from .repo_info import RepoInfo

class LocalReposMonitor(ReposMonitorBase):
    # Static
    repo_count = settings.SettingRef[int]("local", "display-count")
    
    # Instance  
    
    def __init__(self):
        self.login_name = "Loading..."
        
        super().__init__()
        
    
    def update(self):
        os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = settings.current["local"]["git-path"]
        super().update()
        
        parent, child = Pipe(True)
        
        scan_proc = Process(None, update_mp, args=(child,), name="LocalReposMonitor_scanning_multiprocessing")
        # scan_proc = Thread(None, update_mp, args=(child,), name="LocalReposMonitor_scanning_thread")
        scan_proc.start()
        
        result = parent.recv()
        
        self.populate_repo_list(result, RepoInfo.from_local_path)
        


def update_mp(return_pipe: Connection):
    import git
    # from git.objects.commit import Commit
    
    paths = settings.current["local"]["paths"]
    depth = settings.current["local"]["search-depth"]
    display_count = settings.current["local"]["display-count"]
    
    found_repos: list[git.Repo] = []
    
    def search_dir(repos: list[git.Repo], path: pathlib.Path, current_depth: int):
        print(path)
        if not path.joinpath(".git").exists():
            
            current_depth -= 1
            if current_depth < 0:
               return 
                
            for i in os.listdir(path):
                fullpath = path.joinpath(i)
                
                if not (fullpath.is_dir() or fullpath.is_symlink()):
                    continue

                search_dir(repos, fullpath, current_depth)
            
        else:
            try:
            # This is a git repo. Time to process it:
                # rinfo = RepoInfo.from_local_path(git.Repo(str(path.joinpath(".git"))))
                repo = git.Repo(str(path.joinpath(".git")))
                
                inserted = False
                for i in range(0, len(repos)):
                    if repos[i].head.commit.committed_datetime < repo.head.commit.committed_datetime:
                        inserted = True
                        repos.insert(i, repo)
                        break
                
                if inserted:
                    while len(repos) > display_count:
                        repos.pop()
                        
                elif len(repos) < display_count:
                    repos.append(repo)
            except Exception as e:
                print(f"Repo @ {path} could not be parsed.")
                traceback.print_exception(type(e), e, e.__traceback__)
                
    for i in paths:
        search_dir(found_repos, pathlib.Path(i), depth)
    print(found_repos)
    return_pipe.send(found_repos)
            