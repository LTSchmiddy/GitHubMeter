import os
from datetime import datetime, timezone

from github.Repository import Repository
from github.Commit import Commit as ghCommit

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
        
        commit: ghCommit = repo.get_commits()[0]
        
        retVal.last_update = datetime(
            repo.updated_at.year,
            repo.updated_at.month,
            repo.updated_at.day,
            repo.updated_at.hour,
            repo.updated_at.minute,
            repo.updated_at.second,
            repo.updated_at.microsecond,
            tzinfo=timezone.utc
        )
        
        retVal.last_commit_message = commit.commit.message
        retVal.last_commit_author = commit.commit.author.name
        
        retVal.content_address = repo.contents_url
        
        return retVal
    
    @classmethod
    def from_local_path(cls, p_repo):
        import git
        from git.objects.commit import Commit as lCommit
        from git.remote import Remote
        repo: git.Repo = p_repo
        
        retVal = cls()
        retVal.name = os.path.basename(repo.working_dir)
        
        commit: lCommit = repo.head.commit
        use_date = commit.committed_datetime
        use_tz = commit.committer_tz_offset
        
        retVal.last_update = datetime(
            use_date.year,
            use_date.month,
            use_date.day,
            use_date.hour,
            use_date.minute,
            use_date.second,
            use_date.microsecond,
            # tzinfo=timezone.utc()
        )
        
                
        retVal.last_commit_message = commit.message
        retVal.last_commit_author = commit.author.name
        
        retVal.content_address = None
        
        # for i in repo.remotes:
        #     r: Remote = i
        #     if r.name == 'origin':
        #         retVal.content_address = r.urls[0]

        return retVal