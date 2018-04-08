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
print data
print "* done"

stream.stop_stream()
stream.close()
p.terminate()


stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)
#samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

#stream.write(volume*samples)

correct=0
wrong=0
for i in range(10):
    print "try number:", i+0
    print "correct:", correct
    print "wrong:", wrong
    x=random.random()
    #print x
    if  x>0.5:
        f3=f2
    else:
        f3=f

    samples = (np.sin(2*np.pi*np.arange(fs*duration)*(f+20.0*np.sin(0.001*np.arange(fs*duration)))/fs)).astype(np.float32)
    samples = np.array([x if x<1.0/float(i+1) else 1.0/float(i+1) for x in samples ]).astype(np.float32)
    #samples2 = (np.sin(2*np.pi*np.arange(fs*duration)*f3/fs)).astype(np.float32)
    stream.write(data)
    stream.write(volume*samples)
    #stream.write(volume*samples2)

    z=raw_input( "Same? [y/n]:")

# play. May repeat with different volume values (if done interactively) 

    if ('y' in z and x<=0.5) or ('n' in z and x > 0.5):
        correct+=1
        print "right!"
    else:
        wrong+=1
        print "wrong!"

        


    



stream.stop_stream()


stream.close()

p.terminate()

print "Your score.  Correct:", correct, "wrong", wrong
