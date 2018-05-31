#! /usr/bin/python3
# Verify that branches are ready to be merged into develop by checking that there have been no commits to the base
# since the current branch was checked out, that the current branch is only one branch ahead of the base, and that
# there are no differences between the local current branch and the origin current branch

import subprocess
import sys
import logging

# the branch we are merging with will always be 'develop'
base_branch = "origin/develop"

# get the name of the current branch
results = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                         stdout=subprocess.PIPE, encoding="utf-8")
current_branch = results.stdout.strip()


def check_commits_before(current_branch):
    """
    :param current_branch: The branch that is currently checked out in git
    :return: Boolean indicating that there have been no commits after current working branch (True) or that there have been commits after the current branch (False)
    """
    # connect branch names with '..' revision selector
    branch_range = f'{current_branch}..{base_branch}'
    results = subprocess.run(['git', 'rev-list', '--count', branch_range],
                             stdout=subprocess.PIPE, encoding="utf-8")

    if results.returncode != 0:
        logging.info("git command was unsuccessful: return code", results.returncode)
    num_commits = int(results.stdout.strip())

    if num_commits != 0:
        logging.info("Not ready to be merged. There are", num_commits,
                     "commits after the current branch. You need to rebase")
        return False
    else:
        return True


def check_commits_after(current_branch):
    """
    :param current_branch: The branch that is currently checked out in git
    :return: Boolean indicating whether current branch is one (True) or more than one (False) commit ahead of the base
    """
    # connect the two branch names with '..'
    branch_range = f'{base_branch}..{current_branch}'
    results = subprocess.run(['git', 'rev-list', '--count', branch_range],
                             stdout=subprocess.PIPE, encoding="utf-8")

    if results.returncode != 0:
        logging.info("git command was unsuccessful: return code", results.returncode)
    out_code = int(results.stdout.strip())
    if out_code > 2:
        logging.info("Not ready to be merged. This branch is more than one commit ahead of its base")
        return False
    else:
        return True


def check_diff(current_branch):
    """
    :param current_branch: The branch that is currently checked out in git
    :return: Boolean indicating if there is a difference (False) between current branch and the base, or not (True)
    """
    origin_of_current_branch = f'origin/{current_branch}'
    output = subprocess.run(['git', 'diff', '--stat', origin_of_current_branch, current_branch],
                            stdout=subprocess.PIPE, encoding="utf-8")

    if output.returncode != 0:
        logging.info("git command was unsuccessful: return code", output.returncode)
    out_string = output.stdout.strip()

    if not out_string:
        return True
    else:
        return False


if check_commits_before(current_branch) and check_commits_after(current_branch) and check_diff(current_branch):
    print("ready to merge")
    sys.exit(0)
else:
    print("not ready to merge")
    sys.exit(1)
