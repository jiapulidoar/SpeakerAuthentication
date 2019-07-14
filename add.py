# Save the voice features of the user in encoded form 

import time
import os
import sys
import numpy as np 
import configparser
import builtins
import json

import subprocess
from subprocess import call 
from multiprocessing import Process

path = os.path.abspath(__file__ +"/../") # get the absolute  current path 


def extract_features( i , count ): 
	subprocess.call(['./features_extractor', i ] )

if __name__ == "__main__":

	# The permanent file to store the encoded model in
	try:
		user = os.getlogin()
	except Exception:
		user = os.environ.get("SUDO_USER")
	
	enc_file = path + "/models/" + user + ".dat"
	# Known encodingss
	encodings = []

	# Make the ./models folder if it doesn't already exist
	if not os.path.exists(path + "/models"):
		print("No face model folder found, creating one")
		os.makedirs(path + "/models")

	# To try read a premade encodings file if it exists
	try:
		encodings = json.load(open(enc_file))
	except FileNotFoundError:
		encodings = []

	print("Adding face model for the user " + user)

	# Set the default label
	label = "Initial model"

	# If models already exist, set that default label
	if encodings:
		label = "Model #" + str(len(encodings) + 1)

	insert_model = {
		"time": int(time.time()),
		"label": label,
		"id": len(encodings),
		"data": []
	}

	# Extract the features to the model 

	## GETAUDIO 
	dir_audio = "audios/Yennylong1.wav" 
	## GETAUDIO 

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


	# Give let the user know how it went
	print("""Scan complete

	Added a new model to """ + user)
	print(path)






