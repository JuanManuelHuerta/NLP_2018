import sys
import json
import unicodedata
import operator
import math
import gzip
import nltk


##  STEP A. LOAD THE STOP WORDS
fp=open("stop_words.txt","rt")
stop_words=set()
for line in fp:
    stop_words.add(line.rstrip())
print "Loaded stop words"


## STEP B:  FIND THE MOST COMMON PRODUCTS

fp=gzip.open("../reviews_Beauty_5.json.gz")
master_dictionary={}
dictionary_per_product={}
product_count={}
words_per_product={}
for line in fp:
    review_data=json.loads(line)
    asin=review_data['asin']
    if not asin in product_count:
        product_count[asin]=0
    product_count[asin]+=1

## STEP c:  BUild word dictionaries  for most common products, and keep track of words per product
fp=gzip.open("../reviews_Beauty_5.json.gz")        
for line in fp:
    review_data=json.loads(line)
    asin=review_data['asin']
    if product_count[asin]<40:
        continue
    review=unicodedata.normalize('NFKD', review_data['reviewText']).encode('ascii','ignore')
    if not asin in dictionary_per_product:
        dictionary_per_product[asin]={}
        words_per_product[asin]=0.0
    words=nltk.word_tokenize(review)    

    for word_r in words:
        word=word_r.lower()
        if not word in stop_words:
            if not word in master_dictionary:
                master_dictionary[word]=0
            if not word in dictionary_per_product[asin]:
                dictionary_per_product[asin][word]=0
            master_dictionary[word]+=1
            dictionary_per_product[asin][word]+=1
            words_per_product[asin]+=1.0

top_words={}
InverseDocumentFrequency={}
## Step d.:Keep track of the IDF
for asin in dictionary_per_product:
    for word in dictionary_per_product[asin]:
        if not word in InverseDocumentFrequency:
            InverseDocumentFrequency[word]=0.0
        InverseDocumentFrequency[word]+=1.0

# Step e: for each product, foreach word calculate its TFIDF and keep those abovea threshold
for asin in dictionary_per_product:
    top_words[asin]=set()
    for word in  dictionary_per_product[asin]:
        if dictionary_per_product[asin][word]>=10.0:

            tf_idf=((float(dictionary_per_product[asin][word])/words_per_product[asin])*math.log(len(dictionary_per_product)/InverseDocumentFrequency[word]))
            if tf_idf>=0.0001:
                top_words[asin].add((word,tf_idf))
    print asin, top_words[asin]
        



