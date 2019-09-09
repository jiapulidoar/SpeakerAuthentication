# Save the voice features of the user in encoded form 

import time
import os
import sys
import numpy as np 
import configparser
import builtins
import json
import gnupg

import subprocess
from subprocess import call 
from multiprocessing import Process
from getaudio import *

path = os.path.abspath(__file__ +"/../") # get the absolute  current path 


def extract_features( i , count ): 
	subprocess.call(['./features_extractor', i ] )

user = builtins.howdy_user
uid = builtins.howdy_uid
audio = builtins.howdy_audio

### Directory of gnupg 

if not os.path.exists("/home/"+user+"/.howdy"):
	import generate.key
gpg = gnupg.GPG(gnupghome='/home/'+user+'/.howdy')


def add(): 
	# The permanent file to store the encoded model in
	
	
	enc_file = path + "/../models/" + user + ".dat"
	# Known encodingss
	encodings = []

	# Make the ./models folder if it doesn't already exist
	if not os.path.exists(path + "/../models"):
		print("No face model folder found, creating one")
		os.makedirs(path + "/../models")

	# To try read a premade encodings file if it exists
	try:
		with open(enc_file, 'rb') as d:
    			status = gpg.decrypt_file(d, passphrase= uid, 
				output=enc_file+'.dec')
		encodings = json.load(open(enc_file+'.dec'))
		os.remove(enc_file+'.dec')

	except FileNotFoundError:
		encodings = []

	

	print("Adding face model for the user " + user)

	# Set the default label
	label = "Initial model"

	# If models already exist, set that default label
	if encodings:
		label = "Model #" + str(len(encodings) + 1)
	
	# Keep de default name if we can't ask questions
	if builtins.howdy_args.y:
		print("Using default label \"" + label + "\" because of -y flag")
	else:
		# Ask the user for a custom label
		label_in = input("Enter a label for this new model [" + label + "]: ")

		# Set the custom label (if any) and limit it to 24 characters
		if label_in != "":
			label = label_in[:24]

	# Prepare the metadata for insertion

	insert_model = {
		"time": int(time.time()),
		"label": label,
		"id": len(encodings),
		"data": []
	}

	# Extract the features to the model 

	## GETAUDIO 

	if len(audio) > 0:
		dir_audio = audio
	else: 
		dir_audio = record()
	## GETAUDIO 

	print(dir_audio)
	p = Process(target=extract_features, args= ( dir_audio , 0))
	p.start()
	p.join()

	features = np.fromfile("./tmp/features.data", dtype=np.dtype("f4"))
	os.remove("./tmp/features.data")

	#Insert the model to the metadata

	
	insert_model["data"].append(features.tolist())
	
	encodings.append(insert_model)
	
	# Save the new encodings to disk
	with open(enc_file, "w") as datafile:
		json.dump(encodings, datafile)

	# Encrypt file 

	with open(enc_file, 'rb') as f:
    		status = gpg.encrypt_file(
        		f, recipients=[user+'@local'], # Fingerprint
        		output= enc_file)
	print(status)


	# Give let the user know how it went
	print("""Scan complete

	Added a new model to """ + user)
	print(path)






