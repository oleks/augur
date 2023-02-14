from augur.tasks.github.util.github_task_session import GithubTaskManifest
from augur.tasks.github.detect_move.core import *
from augur.tasks.init.celery_app import celery_app as celery
from augur.application.db.util import execute_session_query
import traceback



@celery.task()
def detect_github_repo_move(repo_git : str) -> None:

    logger = logging.getLogger(detect_github_repo_move.__name__)

    logger.info(f"Starting repo_move operation with {repo_git}")
    with GithubTaskManifest(logger) as manifest:
        #Ping each repo with the given repo_git to make sure
        #that they are still in place. 
        query = manifest.session.query(Repo).filter(Repo.repo_git == repo_git)
        repo = execute_session_query(query, 'one')
        logger.info(f"Pinging repo: {repo_git}")
        ping_github_for_repo_move(manifest.session, repo, logger, manifest.key_auth, manifest.augur_db_engine)