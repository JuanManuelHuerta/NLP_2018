import sys
import json
import numpy
from nltk import sent_tokenize, word_tokenize, pos_tag
import unicodedata
import re
import operator
import math
import gzip
import nltk

def custom_word_tokenize(my_string):
    s0=my_string
    s1=re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
    s2=re.sub(r'[;:\s \(\)\-\!\?]+',r' ',s1.lower())
    s3=re.sub(r'\. ',r' ',s2)
    words=s3.split(" ")
    return words




## Open the file, scan the data, keep review texts.


fp=open("stop_words.txt","rt")
stop_words=set()
for line in fp:
    stop_words.add(line.rstrip())
print "Loaded stop words"

#fp=gzip.open("../reviews_Movies_and_TV_5.json.gz")
#fp=gzip.open("../reviews_Beauty_5.json.gz")
fp=open("../reviews_Automotive_5.json")
master_dictionary={}
dictionary_per_product={}
revs_per_asin={}
for line in fp:
    review_data=json.loads(line)
    review=unicodedata.normalize('NFKD', review_data['reviewText']).encode('ascii','ignore')
    asin=review_data['asin']
    if not asin in dictionary_per_product:
        dictionary_per_product[asin]={}
        revs_per_asin[asin]=0
    revs_per_asin[asin]+=1
    words=nltk.word_tokenize(review)
    #words_pos = nltk.pos_tag(words)
    #for word in words_pos:
        #b_word=word[0].lower()
        #if b_word.lower() in stop_words or word[1] != 'JJ':
        #if b_word.lower() in stop_words or word[1] != 'VB':
        #if b_word.lower() in stop_words or word[1] != 'NN':
        #    continue
    for b_word in words:
        if b_word in stop_words:
            continue
        if not b_word in master_dictionary:
            master_dictionary[b_word]=0
        if not b_word in dictionary_per_product[asin]:
            dictionary_per_product[asin][b_word]=0
        master_dictionary[b_word]+=1
        dictionary_per_product[asin][b_word]+=1

top_words={}
InverseDocumentFrequency={}

for asin in dictionary_per_product:
    
    for word in dictionary_per_product[asin]:

        if not word in InverseDocumentFrequency:
            InverseDocumentFrequency[word]=0.0

        InverseDocumentFrequency[word]+=1.0


inverse_index={}

for asin in dictionary_per_product:
    top_words[asin]=[]

    for word in  dictionary_per_product[asin]:
        dictionary_per_product[asin][word]=dictionary_per_product[asin][word]*math.log(len(dictionary_per_product)/InverseDocumentFrequency[word])
    
        if not word in inverse_index:
            inverse_index[word]={}
        inverse_index[word][asin]=dictionary_per_product[asin][word]


while True:
    words=raw_input("Input query ").rstrip().split()
    results={}
    for word in words:
        if word in inverse_index:
            for asin in inverse_index[word]:
                if not asin in results:
                    results[asin]=inverse_index[word][asin]
                if inverse_index[word][asin] > results[asin]:
                    results[asin]=inverse_index[word][asin]
    sr=sorted(results.items(), key=operator.itemgetter(1), reverse=True)
    if len(sr)>10:
        sr=sr[:10]
    print sr




