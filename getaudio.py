import pyaudio 
import wave 
import time
from time import gmtime, strftime
import numpy as np
import scipy.signal

import subprocess
from subprocess import call 
from multiprocessing import Process
from getaudio import *


def record_arecord( _dir , _sec ): 
	subprocess.call(['arecord', '-vv','-fdat', _dir, '-d', str(_sec) ] )


def record(): 
	save_dir = "tmp/"
	chunk = 1024  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 1
	fs = 16000  # Record at 44100 samples per second
	seconds = 4
	filename = strftime("%Y%m%d%H%M%S.wav",gmtime())
	'''
	p = pyaudio.PyAudio()  # Create an interface to PortAudio
	print('Record in 2 sec')
	time.sleep(1)
	print('Record in 1 sec')
	time.sleep(1)
	print('Recording')

	stream = p.open(format=sample_format,
		        channels=channels,
		        rate=fs,
		        frames_per_buffer=chunk,
		        input=True)

	frames = []  # Initialize array to store frames

	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * seconds)):
	    data = stream.read(chunk)
	    frames.append(data)

	# Stop and close the stream 
	stream.stop_stream()
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()

	print('Finished recording')
	
	# Save the recorded data as a WAV file
	wf = wave.open(save_dir + filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()
	'''
	p = Process(target=record_arecord, args= ( save_dir + filename  , seconds))
	p.start()
	p.join()
	
	return save_dir + filename 


