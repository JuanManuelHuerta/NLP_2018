import pyaudio
import numpy as np
import random
p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 12.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float
f = 100.0        # sine frequency, Hz, may be float
f2 = 443.0        # sine frequency, Hz, may be float



chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1, 
                rate=fs, 
                input=True,
                output=True,
                frames_per_buffer=chunk)
data=np.array([])
print "* recording"

for i in range(0, 44100 / chunk * RECORD_SECONDS):
    data2 = stream.read(chunk)
    data=np.append(data,data2)
    # check for silence here by comparing the level with 0 (or some threshold) for 
    # the contents of data.
    # then write data or not to a file
print "* done"

stream.stop_stream()
stream.close()
p.terminate()

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

stream.write(data)

