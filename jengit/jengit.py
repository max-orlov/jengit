import json
import os

import argh
from argh.decorators import arg
from datetime import date, timedelta

import je_interface as je
from configuration import configuration as conf
from git_interface import GitIntrerface

app = argh.EntryPoint('jit')
command = app


class JenGit(object):

    def __init__(self, repos_dir='~/dev/repos'):
        self.repos_dir = repos_dir
        self.git = GitIntrerface(self.repos_dir)

    def cross_ref(self, job, build, since=None):
        yesterday = date.today() - timedelta(1)
        since = since or yesterday.strftime("%Y-%m-%d")

        failed_tests = je.get_failed_tests_files(job, build)

        check_list = {}

        for test_name, values in failed_tests.iteritems():
            appearances = []
            for trace in values:
                method = trace[je.METHOD_KEY]
                file_path = trace[je.FILE_KEY]
                appearance = self.git.get_log(file_path[0], method, since)
                if appearance:
                    commit_info = [c.strip() for c in appearance.split('\n')
                                   if c.strip()]
                    appearances.append({je.METHOD_KEY: method,
                                        je.FILE_KEY: os.path.join(*file_path),
                                        'commit_info': commit_info})
            check_list[test_name] = appearances

        return check_list

    @staticmethod
    def get_date(year, month, date):
        return "{0}-{1}-{2}".format(year, month, date)

jit = JenGit(conf.root_repos_dir)


@command
@arg('--reset')
def init(repos_dir, reset=False):
    conf.save(repos_dir, reset)


@command
@arg('-since')
# @arg('-to_file')
@arg('--stdout')
def cross(job, build, since=None, to_file='', stdout=True):
    result = jit.cross_ref(job, build, since)
    json_result = json.dumps(result, separators=(',', ':'), indent=4)
    print os.path.dirname(to_file)
    if stdout:
        print json_result
    if to_file:
        if not os.path.isabs(to_file):
            to_file = os.path.join(os.getcwd(), to_file)
        if not os.path.exists(os.path.dirname(to_file)):
            os.mkdir(os.path.dirname(to_file))

        with open(os.path.join(os.getcwd(), to_file), 'a') as f:
            f.write(json_result)
