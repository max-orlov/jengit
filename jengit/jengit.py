import json
import os
from datetime import date, timedelta

from git_interface import GitIntrerface
import je_interface as je


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
                method_call = trace[je.METHOD_KEY]
                method_file = trace[je.FILE_KEY]
                appearance = self.git.get_log(method_file[0],
                                              method_call,
                                              since)
                if appearance:
                    appearances.append({je.METHOD_KEY: method_call,
                                        je.FILE_KEY: os.path.join(*method_file)})
            check_list[test_name] = appearances

        return check_list

    @staticmethod
    def get_date(year, month, date):
        return "{0}-{1}-{2}".format(year, month, date)


jg = JenGit('~/dev/tmp')

x = jg.cross_ref('system-tests', 83)

print json.dumps(x, separators=(',', ':'), indent=4, )
