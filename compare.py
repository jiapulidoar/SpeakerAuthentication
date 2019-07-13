# Compare incomming Audio with known models
# Running in a local python instance to get around PATH issues

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

# Make sure we were given an username to tast against

if len(sys.argv) < 2:
	sys.exit(12)

# Get the absolute path to the current directory
PATH = os.path.abspath(__file__ + "/../")
# The username of the user being authenticated
user = sys.argv[1]
# The model file contents
models = []
# Encoded face models
encodings = []


def extract_features( i , count ): 
	subprocess.call(['./features_extractor', i ] )

if __name__ == "__main__":
	# Try to load the speaker model from the models folder
	print(PATH)
	try:
		models = json.load(open(PATH + "/models/" + user + ".dat"))
		for model in models:
			encodings += model["data"]

	except FileNotFoundError:
		sys.exit(10)

	# Check if the file contains a model
	if len(models) < 1:
		sys.exit(10)
	
	# Extract the model features 
	model_features = np.reshape(np.array(models[-1]["data"], dtype=np.dtype("f4")), (-1))

	## GETAUDIO 
	dir_audio = "audios/Jimmy3.wav" 
	## GETAUDIO 


	p = Process(target=extract_features, args= ( dir_audio , 0))
	p.start()
	p.join()

	features = np.fromfile("./tmp/features.data", dtype=np.dtype("f4"))

	print(features, model_features )
	
	cos_score = np.dot( features ,model_features) / ( np.linalg.norm(features) * np.linalg.norm(model_features) )

	print(cos_score)

	






	
