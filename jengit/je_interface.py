import os
import re
from je import commands as je_commands

JE_ROOT_DIR = os.path.expanduser('~/.je')
JE_WORK_DIR = 'work'
JE_FAILED_DIR = 'failed'

METHOD_KEY = 'method'
FILE_KEY = 'file'


def get_failed_tests_files(job, build):

    tests_log_dir_path = os.path.join(JE_ROOT_DIR,
                                      JE_WORK_DIR,
                                      '{0}-{1}'.format(job, build),
                                      JE_FAILED_DIR)
    logs = {}

    if not os.path.isdir(tests_log_dir_path):
        je_commands.report(job, build, failed=True)

    for log_name in os.listdir(tests_log_dir_path):
        log_path = os.path.join(tests_log_dir_path, log_name)
        with open(log_path, 'rb') as l:
            logs[log_name[:log_name.rindex('.')]] = \
                _extract_cloudify_files_and_functions_from_trace(l.read())

    return logs


def _extract_cloudify_files_and_functions_from_trace(log):
    # TODO: move from working with the str log to json log (cache)
    start_index = log.index('error stacktrace:')
    end_index = log.index('stdout')
    stack_trace = \
        log[start_index: end_index].split('\n')[1:]

    tracing = []

    for line in stack_trace:
        if line.strip().startswith('File'):
            affecting_file = re.search('\".*\"', line).group(0).replace('"', '')
            affecting_method = line[line.rindex(','):].strip().split()[2]
            if affecting_file.startswith('/env/cloudify-'):
                tracing.append({FILE_KEY: affecting_file.replace('/env/', '').split('/'),
                                METHOD_KEY: affecting_method})

    return tracing

# logs = get_failed_tests_files('system-tests', 80)
#
# print logs