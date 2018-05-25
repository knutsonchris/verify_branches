#This is designed to verify that banches are ready to be merged into develop
#Chris Knutson

import subprocess
from argparse import ArgumentParser


parser = ArgumentParser() #create an argument parsing object
parser.add_argument("current_branch", help="the branch we are currently in")
args = parser.parse_args() #grab the arguments and store them in args (a Namespace object)

master_branch = "..origin/develop"#the branch we are merging with will always be 'develop'



#check to make sure that the branch we are working on is based on the current branch
output = subprocess.run(['git', 'rev-list', '--count', args.current_branch, master_branch], stdout=subprocess.PIPE) #using PIPE to prevent subprocess from printing git's output
out_code = int(output.stdout.decode("ascii").strip())
if (out_code != 0):
	print("Not ready to be merged. There are", output.returncode, "commits after the current branch. You need to rebase")
else: test1 = True


#check to make sure that the branch we are working on is only one commit ahead of origin/develop
output = subprocess.run(['git', 'rev-list', '--count', master_branch, args.current_branch], stdout=subprocess.PIPE) #using PIPE to prevent subprocess from printing git's output
out_code = int(output.stdout.decode("ascii").strip())
if (out_code > 1):
	print("Not ready to be merged. This branch is more than one commit ahead of develop")
else: test2 = True


if (test1 and test2 == True):
	print("ready to merge")