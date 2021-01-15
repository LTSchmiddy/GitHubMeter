from datetime import datetime

from github.Repository import Repository
from github.Commit import Commit

class RepoInfo:
    name: str = None
    last_update: datetime = None
    last_commit_message: str = None
    last_commit_author: str = None
    content_address: str = None
    
    
    @classmethod
    def from_github_Repository(cls, repo: Repository):
        retVal = cls()
        
        retVal.name = repo.name
        retVal.last_update = repo.updated_at
        commit: Commit = repo.get_commits()[0]
        
        retVal.last_commit_message = commit.commit.message
        retVal.last_commit_author = commit.commit.author.name
        
        retVal.content_address = repo.contents_url
        
        return retVal