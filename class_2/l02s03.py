import sys
import json
import gzip
import unicodedata
import numpy 
import re
import operator
import math

def custom_word_tokenizer(my_string):
    s0= my_string
    s1= re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
    s2= re.sub(r'[;:,!\? \-\$\*\%]+',r' ',s1.lower())
    s3= re.sub(r'\.$',r'',s2)
    s4 = re.sub(r'[\.]+ ',r' ',s3)
    words = s3.split(' ')
    return words



fp1=open('stop_words.txt','rt')
stop_words=set()
for line in fp1:
    word=line.rstrip()
    stop_words.add(word)

def entropy(X):
    entropy=0.0
    for z in X:
        if z !=0.0:
            entropy+=z*math.log(z)
    return -1.0*entropy

fp=gzip.open("../reviews_Beauty_5.json.gz")
all_data=[]
reviews_text=[]
products_count={}
only_scores=[]

all_counts={}
word_counts={}
for line in fp:
    review_data=json.loads(line)
    review_n=unicodedata.normalize('NFKD',review_data['reviewText']).encode('ascii','ignore')
    words= custom_word_tokenizer(review_n)
    rating=review_data['overall']
    if not rating in all_counts:
        all_counts[rating]={}
    for word in words:
        if word in stop_words:
            continue
        if not word in word_counts:
            word_counts[word]=0
        if not word in all_counts[rating]:
            all_counts[rating][word]=0
        all_counts[rating][word]+=1
        word_counts[word]+=1

# Computing Entropy of the Posterior probabilities P[Y | x] = P[Y] P[x|Y]/P[x]

entropy_value={}
prob_vectors={}
for score in all_counts:
    Tot_words = numpy.sum([all_counts[score][x] for x in all_counts[score]])
    for word in all_counts[score]:
        all_counts[score][word]/=float(Tot_words)

for word in word_counts:
    if word_counts[word]>200.0:
        p=[]
        for r in all_counts:
            if word in all_counts[r]:
                p.append(all_counts[r][word])
        prob_vectors[word]=p
        entropy_value[word]=entropy(p)

sorted_words=sorted(entropy_value.items(), key=operator.itemgetter(1), reverse=False)
for i in range(30):
    print sorted_words[i], prob_vectors[sorted_words[i][0]]
