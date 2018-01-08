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
    conan_dirs = [d for d in directories if os.path.exists(os.path.join(d, 'conanfile.py'))]

    for d in conan_dirs:
        execute(['conan', 'create', CHANNEL, '--build', 'missing', '--update'], cwd=d)

        completed_process = subprocess.run(['conan', 'info', d, '--only', 'None'], stdout=subprocess.PIPE)
        package = completed_process.stdout.decode().split()[0].split('@')[0]
        execute(['conan', 'upload', '--force', '--confirm', '--remote', 'ci', package + '@' + CHANNEL], cwd=d)


def execute(args: typing.List, cwd: str, echo: bool=True) -> None:
    if echo:
        print('cd ' + cwd + ' && ' + ' '.join(args))
        sys.stdout.flush()
    subprocess.check_call(args, cwd=cwd)


run()
