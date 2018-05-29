# This is designed to verify that branches are ready to be merged into develop

import subprocess

master_branch = "origin/develop"  # the branch we are merging with will always be 'develop'

# get the name of the current branch
output = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                        stdout=subprocess.PIPE, encoding="utf-8")  # use PIPE to prevent subprocess from printing
current_branch = output.stdout.strip()  # select only stdout


def branch_builder(branch_1, branch_2):  # place two branch names together with '..' for git
    branch = branch_1 + '..' + branch_2
    return branch


def check_commits_before(current_branch):  # make sure that the checked out branch is based on the current branch
    branch_range = branch_builder(current_branch, master_branch)  # connect the two branch names with '..'
    output = subprocess.run(['git', 'rev-list', '--count', branch_range],
                            stdout=subprocess.PIPE, encoding="utf-8")  # using PIPE to prevent subprocess from printing
    if output.returncode != 0:
        print("git command was unsuccessful: return code", output.returncode)
    out_code = int(output.stdout.strip())  # select only stdout
    if out_code != 0:
        print("Not ready to be merged. There are", out_code,
              "commits after the current branch. You need to rebase")
        return False
    else:
        return True


def check_commits_after(current_branch):  # make sure that the checked out branch is only one commit ahead of develop
    branch_range = branch_builder(master_branch, current_branch)  # connect the two branch names with '..'
    output = subprocess.run(['git', 'rev-list', '--count', branch_range],
                            stdout=subprocess.PIPE, encoding="utf-8")  # using PIPE to prevent subprocess from printing
    if output.returncode != 0:
        print("git command was unsuccessful: return code", output.returncode)
    out_code = int(output.stdout.strip())
    if out_code > 2:
        print("Not ready to be merged. This branch is more than one commit ahead of develop")
        return False
    else:
        return True


def check_diff(current_branch):
    # run git diff
    output = subprocess.run(['git', 'diff', '--stat', master_branch, current_branch],
                            stdout=subprocess.PIPE, encoding="utf-8")
    if output.returncode != 0:
        print("git command was unsuccessful: return code", output.returncode)
    out_string = output.stdout.strip()  # select only stdout
    if not out_string:
        return True
    else:
        return False


if check_commits_before(current_branch) and check_commits_after(current_branch) and check_commits_after(current_branch):
    print("ready to merge")
