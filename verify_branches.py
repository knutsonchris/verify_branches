#This is designed to verify that branches are ready to be merged into develop

import subprocess

master_branch = "..origin/master"#the branch we are merging with will always be 'develop'

#get the name of the current branch
output = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE) #use PIPE to prevent subprocess from printing git's output
current_branch = output.stdout.decode("ascii").strip() #select only stdout


#check to make sure that the branch we are working on is based on the current branch
output = subprocess.run(['git', 'rev-list', '--count', current_branch, master_branch], stdout=subprocess.PIPE)
out_code = int(output.stdout.decode("ascii").strip()) #select only stdout
if out_code != 0:
	print("Not ready to be merged. There are", output.returncode, "commits after the current branch. You need to rebase")
else: test1 = True


#check to make sure that the branch we are working on is only one commit ahead of origin/develop
output = subprocess.run(['git', 'rev-list', '--count', master_branch, current_branch], stdout=subprocess.PIPE) #using PIPE to prevent subprocess from printing git's output
out_code = int(output.stdout.decode("ascii").strip())
if out_code > 1:
	print("Not ready to be merged. This branch is more than one commit ahead of develop")
else: test2 = True


if test1 and test2 == True:
	print("ready to merge")

output = subprocess.run(['git', 'diff', '--stat', master_branch, current_branch], stdout=subprocess.PIPE)
out_string = output.stdout.decode("ascii").strip() #select only stdout

if not out_string:
	print ('no diff')
else: print (out_string)

	
