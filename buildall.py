#!/usr/bin/python
# @file    buildall.py
# @author  David Zemon
#
# Created with: PyCharm

"""
@description:
"""

import json
import os
import subprocess
import sys

PACKAGE_OPTIONS_FILE_NAME = 'options.json'

try:
    from shutil import which
except ImportError:
    def which(file_name):
        for path in os.environ["PATH"].split(os.pathsep):
            full_path = os.path.join(path, file_name)
            if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                return full_path
        return None

CHANNEL = 'wsbu/stable'


def run():
    assert __file__, '__file__ value should be defined and not empty'
    assert os.path.isfile(__file__), '__file__ should be a path to a file'
    root = os.path.dirname(os.path.abspath(__file__))
    directories = [os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(d)]
    conan_dirs = [os.path.abspath(d) for d in directories if os.path.exists(os.path.join(d, 'conanfile.py'))]

    conan_exe_args = get_conan_exe_args()

    for d in conan_dirs:
        print('#' * 80)
        print('### Building {0}'.format(os.path.basename(d)))
        print('#' * 80)

        args = conan_exe_args + ['info', d, '--only', 'None']
        print(args)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        return_code = p.wait()
        if 0 != return_code:
            if p.stdout:
                print(p.stdout.read().decode())
            if p.stderr:
                sys.stderr.write(p.stderr.read().decode() + os.linesep)
            raise Exception('Process exited with non-zero return code: {0}'.format(return_code))
        else:
            lines = p.stdout.read().decode().split()
            this_project = [line for line in lines if line.endswith('@PROJECT')][0]
            package = this_project.split('@')[0]

            for config in get_options(d):
                execute(conan_exe_args + ['create', d, CHANNEL, '--build', 'missing', '--build', 'outdated', '--update']
                        + config + sys.argv[1:])
            execute(conan_exe_args + ['upload', '--force', '--confirm', '--remote', 'ci', '--all', package + '@' +
                                      CHANNEL])


def get_conan_exe_args():
    conan_exe = which('conan')
    with open(conan_exe, 'r') as f:
        first_line = f.readline().strip()
        return [first_line[2:], '-u', conan_exe]


def get_options(d):
    options_filename = os.path.join(d, PACKAGE_OPTIONS_FILE_NAME)
    if os.path.exists(options_filename):
        with open(options_filename, 'r') as options_file:
            json_content = json.loads(options_file.read())
        build_configs = []
        for config in json_content:
            extra_args = []
            for k, v in config.items():
                extra_args += ['--options', '{0}:{1}={2}'.format(d, k, v)]
            build_configs.append(extra_args)
        return build_configs
    else:
        return [[]]


def execute(args, echo=True):
    """
    :type args list
    :type echo bool
    :rtype None
    """
    if echo:
        print(' '.join(args))
        sys.stdout.flush()
    subprocess.check_call(args)


run()
