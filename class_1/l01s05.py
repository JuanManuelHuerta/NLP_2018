import sys
import json
import numpy
from nltk import sent_tokenize, word_tokenize, pos_tag
import unicodedata
import re
import operator
import math
import gzip


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
    words=custom_word_tokenize(review)    
    for word in words:
        if not word in stop_words:
            if not word in master_dictionary:
                master_dictionary[word]=0
            if not word in dictionary_per_product[asin]:
                dictionary_per_product[asin][word]=0
            master_dictionary[word]+=1
            dictionary_per_product[asin][word]+=1

top_words={}
InverseDocumentFrequency={}

for asin in dictionary_per_product:
    
    for word in dictionary_per_product[asin]:

        if not word in InverseDocumentFrequency:
            InverseDocumentFrequency[word]=0.0

        InverseDocumentFrequency[word]+=1.0



for asin in dictionary_per_product:
    top_words[asin]=[]

    for word in  dictionary_per_product[asin]:
        dictionary_per_product[asin][word]=dictionary_per_product[asin][word]*math.log(len(dictionary_per_product)/InverseDocumentFrequency[word])

    dpp_sorted=sorted(dictionary_per_product[asin].items(),key=operator.itemgetter(1), reverse=True)

    for word in dpp_sorted:
        top_words[asin].append(word)
        if len(top_words[asin])>25:
            break
    if revs_per_asin[asin]>20:
        print "ASIN", asin
        print top_words[asin]
        



