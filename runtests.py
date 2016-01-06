#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import subprocess

import pytest
from flake8.main import main as flake8_main


def main():
    try:
        sys.argv.remove('--nolint')
    except ValueError:
        run_lint = True
    else:
        run_lint = False

    try:
        sys.argv.remove('--lintonly')
    except ValueError:
        run_tests = True
    else:
        run_tests = False

    if run_tests:
        exit_on_failure(tests_main())

    if run_lint:
        exit_on_failure(run_flake8())
        exit_on_failure(run_isort())
        exit_on_failure(run_setup_py_check())


def tests_main():
    return pytest.main()


def run_flake8():
    print('Running flake8 code linting')
    try:
        original_argv = sys.argv
        sys.argv = ['flake8', 'bin', 'tests']
        did_fail = False
        flake8_main()
    except SystemExit:
        did_fail = True
    finally:
        sys.argv = original_argv

    print('flake8 failed' if did_fail else 'flake8 passed')
    return did_fail


def run_isort():
    print('Running isort check')
    return subprocess.call([
        'isort', '--recursive', '--check-only', '--diff',
        'bin', 'tests'
    ])


def run_setup_py_check():
    print('Running setup.py check')
    return subprocess.call([
        'python', 'setup.py', 'check',
        '-s', '--restructuredtext', '--metadata'
    ])


def exit_on_failure(ret, message=None):
    if ret:
        sys.exit(ret)


if __name__ == '__main__':
    main()
