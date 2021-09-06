import os, json

from . import settings
settings.load_settings()
settings.save_settings()


from . import monitor
monitor.load_account()

from .measures.latest_repos import gh_repos, local_repos
from .measures.config import regen_dynamic_includes


