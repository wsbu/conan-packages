#!/usr/bin/python
# @file    buildall.py
# @author  David Zemon
#
# Created with: PyCharm

"""
@description:
"""

import os
import sys
import subprocess

CHANNEL = 'wsbu/stable'


def run():
    assert __file__, '__file__ value should be defined and not empty'
    assert os.path.isfile(__file__), '__file__ should be a path to a file'
    root = os.path.dirname(os.path.abspath(__file__))
    directories = [os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(d)]
    conan_dirs = [os.path.abspath(d) for d in directories if os.path.exists(os.path.join(d, 'conanfile.py'))]

    for d in conan_dirs:
        p = subprocess.Popen(['conan', 'info', d, '--only', 'None'], stdout=subprocess.PIPE)
        return_code = p.wait()
        if 0 != return_code:
            raise Exception('Process exited with non-zero return code: ' + return_code)
        else:
            lines = p.stdout.read().decode().split()
            this_project = [line for line in lines if line.endswith('@PROJECT')][0]
            package = this_project.split('@')[0]

            execute(['conan', 'create', d, CHANNEL, '--build', 'missing', '--build', 'outdated', '--update'])
            execute(['conan', 'upload', '--force', '--confirm', '--remote', 'ci', '--all', package + '@' + CHANNEL])


def execute(args, echo=True):
    """
    :type args list
    :type echo bool
    :rtype None
    """
    if echo:
        print(' '.join(args))
        sys.stdout.flush()
    # subprocess.check_call(args)


run()
