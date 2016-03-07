import os
import git


class GitIntrerface(object):

    def __init__(self, repos_dir):
        self.repos_dir = os.path.expanduser(repos_dir)

    def get_repo(self, repo):
        """
        Returns the repo dir if exists, None o/w.
        :param repo: the repo to check
        :return:
        """
        if os.path.isabs(repo):
            repo_to_check = repo
        else:
            repo_to_check = os.path.join(self.repos_dir, repo)

        # if fun.is_git_dir(repo_to_check):
        return git.Repo(repo_to_check)
        # else:
        #     return None

    def get_log(self, repo, including_method, from_date):
        repo = self.get_repo(repo)
        return repo.git.log(S=including_method, since=from_date,
                            no_merges=True)

    def find_repos(self, containing=()):
        pass


