# Remove a encoding from the models file

# Import required modules
import sys
import os
import json
import builtins
import gnupg

# Get the absolute path and the username
path = os.path.dirname(os.path.realpath(__file__))  + "/.."
user = builtins.howdy_user
uid = builtins.howdy_uid

# Check if enough arguments have been passed
if builtins.howdy_args.argument == None:
	print("Please add the ID of the model you want to remove as an argument")
	print("You can find the IDs by running:")
	print("\n\thowdy list\n")
	sys.exit(1)

# Check if the models file has been created yet
if not os.path.exists(path + "/models"):
	print("Face models have not been initialized yet, please run:")
	print("\n\thowdy add\n")
	sys.exit(1)

# Path to the models file
enc_file = path + "/models/" + user + ".dat"


'''#########################################'''
### Directory of gnupg 
gpg = gnupg.GPG(gnupghome='/home/'+user+'/.howdy')

'''#########################################'''
# To try read a premade encodings file if it exists
try:
	with open(enc_file, 'rb') as d:
    		status = gpg.decrypt_file(d, passphrase= uid, 
			output=enc_file+'.dec')
	encodings = json.load(open(enc_file+'.dec'))
	os.remove(enc_file+'.dec')


except FileNotFoundError:
	print("No speaker model known for the user " + user + ", please run:")
	print("\n\thowdy add\n")
	sys.exit(1)

# Tracks if a encoding with that id has been found
found = False

# Loop though all encodings and check if they match the argument
for enc in encodings:
	if str(enc["id"]) == builtins.howdy_args.argument:
		# Only ask the user if there's no -y flag
		if not builtins.howdy_args.y:
			# Double check with the user
			print('This will remove the model called "' + enc["label"] + '" for ' + user)
			ans = input("Do you want to continue [y/N]: ")

			# Abort if the answer isn't yes
			if (ans.lower() != "y"):
				print('\nInerpeting as a "NO"')
				sys.exit()

			# Add a padding empty  line
			print()

		# Mark as found and print an enter
		found = True
		break

# Abort if no matching id was found
if not found:
	print("No model with ID " + builtins.howdy_args.argument + " exists for " + user)
	sys.exit()

# Remove the entire file if this encoding is the only one
if len(encodings) == 1:
	os.remove(path + "/models/" + user + ".dat")
	print("Removed last model, howdy disabled for user")
else:
	# A place holder to contain the encodings that will remain
	new_encodings = []

	# Loop though all encodin and only add thos that don't need to be removed
	for enc in encodings:
		if str(enc["id"]) != builtins.howdy_args.argument:
			new_encodings.append(enc)

	# Save this new set to disk
	with open(enc_file, "w") as datafile:
		json.dump(new_encodings, datafile)

	# Encrypt file 
	''' #########################Changes '''


	with open(enc_file, 'rb') as f:
	    status = gpg.encrypt_file(
		f, recipients=[user+'@local'], # Fingerprint
		output= enc_file)
	print(status)

	print("Removed model " + builtins.howdy_args.argument)
