#!/usr/bin/python3
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
import typing

CHANNEL = 'wsbu/stable'


def run() -> None:
    root = os.path.dirname(__file__)
    directories = [os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(d)]
    conan_dirs = [os.path.abspath(d) for d in directories if os.path.exists(os.path.join(d, 'conanfile.py'))]

    for d in conan_dirs:
        completed_process = subprocess.run(['conan', 'info', d, '--only', 'None'], stdout=subprocess.PIPE)
        package = completed_process.stdout.decode().split()[0].split('@')[0]

        execute(['conan', 'create', CHANNEL, '--build', 'missing', '--build', 'outdated', '--update', '--cwd', d])
        execute(['conan', 'upload', '--force', '--confirm', '--remote', 'ci', '--all', package + '@' + CHANNEL])


def execute(args: typing.List, echo: bool=True) -> None:
    if echo:
        print(' '.join(args))
        sys.stdout.flush()
    subprocess.check_call(args)


run()
