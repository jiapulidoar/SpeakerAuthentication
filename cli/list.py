# List all models for a user

# Import required modules
import sys
import os
import json
import time
import builtins
import gnupg
from pprint import * 
# Get the absolute path and the username
path = os.path.dirname(os.path.realpath(__file__))  + "/.."
user = builtins.howdy_user
uid = builtins.howdy_uid

# Check if the models file has been created yet
if not os.path.exists(path + "/models"):
	print("Face models have not been initialized yet, please run:")
	print("\n\thowdy " + user + " add\n")
	sys.exit(1)

# Path to the models file
enc_file = path + "/models/" + user + ".dat"

'''#########################################'''
### Directory of gnupg 
gpg = gnupg.GPG(gnupghome='/home/'+user+'/.howdy')

'''#########################################'''
# To try read a premade encodings file if it exists
try:
	print(uid)
	with open(enc_file, 'rb') as d:
    		status = gpg.decrypt_file(d, passphrase= uid, 
			output=enc_file+'.dec')
	encodings = json.load(open(enc_file+'.dec'))
	os.remove(enc_file+'.dec')


except FileNotFoundError:
	print("No face model known for the user " + user + ", please run:")
	print("\n\thowdy " + user + " add\n")
	sys.exit(1)

# Print a header
print("Known face models for " + user + ":")
print("\n\t\033[1;29mID  Date                 Label\033[0m")

# Loop through all encodings and print info about them
for enc in encodings:
	# Start with a tab and print the id
	print("\t" + str(enc["id"]), end="")
	# Print padding spaces after the id
	print((4 - len(str(enc["id"]))) * " ", end="")
	# Format the time as ISO in the local timezone
	print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(enc["time"])), end="")
	# End with the label
	print("  " + enc["label"])

# Add a closing enter
print()
