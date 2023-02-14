import logging 
import traceback
from augur.tasks.github.pull_requests.commits_model.core import *
from augur.tasks.github.util.github_task_session import GithubTaskManifest

from augur.tasks.init.celery_app import celery_app as celery
from augur.application.db.util import execute_session_query


@celery.task()
def process_pull_request_commits(repo_git: str) -> None:

    logger = logging.getLogger(process_pull_request_commits.__name__)

    with GithubTaskManifest(logger) as manifest:

        query = manifest.session.query(Repo).filter(Repo.repo_git == repo_git)
        repo = execute_session_query(query, 'one')
        pull_request_commits_model(repo.repo_id, logger, manifest.session, manifest.augur_db_engine, manifest.key_auth)