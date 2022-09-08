import os

import git

TEST_REPO = "git@github.com:socar-inc/socar-data-mlops-dags.git"


def test_git_clone_from_remote_repo(tmpdir):
    repo = git.Repo.clone_from(TEST_REPO, to_path=os.path.join(tmpdir, "test"), branch="main")
    assert str(repo.active_branch) == "main"
