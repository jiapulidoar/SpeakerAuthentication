# Compare incomming Audio with known models
# Running in a local python instance to get around PATH issues

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


# Make sure we were given an username to tast against
try:
	if not isinstance(sys.argv[1], str):
		sys.exit(1)
except IndexError:
	sys.exit(1)

# Get the absolute path to the current directory
PATH = os.path.abspath(__file__ + "/../")
# The username of the user being authenticated
audio = ''
user = sys.argv[1]
if len(sys.argv )> 2:
	audio = sys.argv[2]
result = subprocess.run(['id', '-u', user], stdout=subprocess.PIPE)
uid =  result.stdout.decode('utf-8')[:-1]


print(uid)

# The model file contents
models = []
# Encoded face models
encodings = []

enc_file = os.path.dirname(os.path.abspath(__file__)) + "/models/" + user + ".dat"
gpg = gnupg.GPG(gnupghome='/home/'+user+'/.howdy')

def extract_features( i , count ): 
	subprocess.call(['./features_extractor', i ] )

if __name__ == "__main__":
	# Try to load the speaker model from the models folder
	try:
		with open(enc_file, 'rb') as d:
    			status = gpg.decrypt_file(d, passphrase=uid, 
				output=enc_file+'.dec')
		print()
		models = json.load(open(enc_file+'.dec'))
		#os.remove(enc_file+'.dec')	

	except FileNotFoundError:
		sys.exit(10)

	# Check if the file contains a model
	if len(models) < 1:
		sys.exit(10)
	
	
	for model in models:
		encodings += model["data"]
	## GETAUDIO5
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

	for i in models:
		# Extract the model features 
		model_features = np.reshape(np.array(i["data"], dtype=np.dtype("f4")), (-1))
	
		cos_score = np.dot( features ,model_features) / ( np.linalg.norm(features) * np.linalg.norm(model_features) )

		print("\n" + str( cos_score))
		if (cos_score >= 0.8):
			print("Winning model: " + str(i['id']) + " (\"" + i["label"] + "\")")
			sys.exit(0)
	print("Speaker not recognised!!!!!")
	sys.exit(10)
	

	






	
