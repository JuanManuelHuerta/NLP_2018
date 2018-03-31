import sys
import json
import numpy
from nltk import sent_tokenize, word_tokenize, pos_tag
import unicodedata
import re

def custom_word_tokenize(my_string):
    s0=my_string
    s1=re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
    s2=re.sub(r'[;:\s \(\)\-]+',r' ',s1.lower())
    s3=re.sub(r'\. ',r' ',s2)
    words=s3.split(" ")
    return words




## Open the file, scan the data, keep review texts.




fp=open("../reviews_Automotive_5.json","rt")
all_data=[]
reviews_text=[]
products_count={}
for line in fp:
    review_data=json.loads(line)
    all_data.append(review_data)
    review_n=unicodedata.normalize('NFKD', review_data['reviewText']).encode('ascii','ignore')
    reviews_text.append(review_n)
    asin=review_data["asin"]
    if not asin  in products_count:
        products_count[asin]=0
    products_count[asin]+=1

## Let's compute some statistics
##  - Average Score
## -  Median score
##  - Total number of reviews
##  - Total number of reviewers
##  - Total number of products
print "Number of reviews",  len(reviews_text)
print "Number of products",  len(products_count)
print "Avg reviews per product",  numpy.mean(products_count.values())

only_scores=[]
for review in all_data:
    only_scores.append(review['overall'])
scores=numpy.array(only_scores)
print "Average score", numpy.mean(scores)
print "Median score", numpy.median(scores)

###  Take a peek at the data
for review in reviews_text:
    print review
    print "nltk tokenizer", word_tokenize(review)
    print "custom tokenizer", custom_word_tokenize(review)


## TEXT PREPROCESSING





