import pyaudio
import wave
import time
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import numpy
import math

# Goal: Implement a search algorithm to match a search query to closest reference entry


def viterbi(X,Y):
    self_transition = math.log(0.10)
    next_transition = math.log(0.80)
    skip_transition = math.log(0.10)
    # Cepstral mean normalization
    X=X-numpy.mean(X,axis=0)
    Y=Y-numpy.mean(Y,axis=0)
    # X: Reference 
    # Y: Hypothesis
    distance=0.0
    n=len(X)
    m=len(Y)
    T1=[]
    # T1 s per observations 
    for i in range(m):
        # Each vector is number of states
        T1.append([None]*n)       
    # First observation , state pair
    distance=math.exp(-0.5*numpy.linalg.norm(X[0]-Y[0]))
    T1[0][0]=math.log(distance)
    # Initialize State
    # For each input vector
    for i in range(1,m):
        for j in range(n):
            #distance=math.exp(-0.5*numpy.linalg.norm(X[j]-Y[i]))
            distance=(-0.5*numpy.linalg.norm(X[j]-Y[i]))
            same_state=None
            one_forward = None
            two_forward = None
            #
            if T1[i-1][j]!= None:
                same_state = T1[i-1][j]+self_transition+distance
            if j>0 and T1[i-1][j-1]!= None:
                one_forward = T1[i-1][j-1]+next_transition+distance
            if j>1 and T1[i-1][j-2]!= None:
                two_forward = T1[i-1][j-2]+skip_transition+distance
            
            if same_state is not None or one_forward is not None or two_forward is not None:
                T1[i][j]=max(same_state,one_forward,two_forward)
        #normalizer=numpy.max(T1[i])
        #T1[i]=[x/normalizer if x is not None else None for x in T1[i]]

#    for v1 in T1:
#        print v1

    total_distance = T1[m-1][n-1]
    return total_distance

# Define the domain:

reference={
"s1":("ok charlie, Read my email","reference.01.wav"),
"s2":("ok charlie, Play voice messages","reference.02.wav"),
"s3":("ok charlie, Let's Call home","reference.03.wav"),
"s4":("ok charlie, What's weather like today?","reference.04.wav"),
"s5":("ok charlie, How's the commute looking?","reference.05.wav")
}

print("Defined Domain")

# Load the reference data

vectors={}
for key in reference:
    (rate,sig) = wav.read(reference[key][1])
    mfcc_feat = mfcc(sig,rate)
    vectors[key]=mfcc_feat
print("Loaded vectorized Reference")


# Loop for audio
Record = False
if Record == True:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 11025
    RECORD_SECONDS = 3
#WAVE_OUTPUT_FILENAME = "output.wav"
#WAVE_OUTPUT_FILENAME = raw_input("Enter WAV file name, include extension: > ").rstrip()

    p = pyaudio.PyAudio()
    for i in range(3):
        print (3-i)
        time.sleep(1)
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open("test.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()




(rate,sig) = wav.read("test.wav")
mfcc_feat = mfcc(sig,rate)

for key in vectors:
    distance=viterbi(vectors[key],mfcc_feat)
    print key, (reference[key][0]+''.join([" "])*30)[:40], distance



