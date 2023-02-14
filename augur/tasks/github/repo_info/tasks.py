from augur.tasks.github.util.github_task_session import GithubTaskManifest
from augur.application.db.session import DatabaseSession
from augur.tasks.github.repo_info.core import *
from augur.tasks.init.celery_app import celery_app as celery
from augur.application.db.util import execute_session_query
import traceback

@celery.task()
def collect_repo_info(repo_git: str):

    logger = logging.getLogger(collect_repo_info.__name__)

    with GithubTaskManifest(logger) as manifest:
        query = manifest.session.query(Repo).filter(Repo.repo_git == repo_git)
        repo = execute_session_query(query, 'one')
        repo_info_model(manifest.key_auth, repo, logger, manifest.augur_db_engine)
    
