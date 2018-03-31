import sys
import json
import gzip
import unicodedata
import numpy 
import re
import operator
import nltk




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




fp=gzip.open("../reviews_Beauty_5.json.gz")
all_data=[]
reviews_text=[]
products_count={}
only_scores=[]

all_counts={}
max_reviews=20000

for line in fp:
    if max_reviews==0:
        break
    max_reviews-=1
    review_data=json.loads(line)
    review_n=unicodedata.normalize('NFKD',review_data['reviewText']).encode('ascii','ignore')
    words = nltk.word_tokenize(review_n)
    words_pos = nltk.pos_tag(words)
    #print words_pos

    rating=review_data['overall']
    if not rating in all_counts:
        all_counts[rating]={}
    for word in words_pos:
        b_word=word[0].lower()
        #if b_word.lower() in stop_words or word[1] != 'JJ':
        if b_word.lower() in stop_words or word[1] != 'NN':
            continue
        if not b_word in all_counts[rating]:
            all_counts[rating][b_word]=0
        all_counts[rating][b_word]+=1


# Compute:  P[ word_i | Class_j ]


for score in all_counts:
    print "SCORE", score
    sortedx=sorted(all_counts[score].items(), key=operator.itemgetter(1),reverse=True)
    Tot_words = numpy.sum([x[1] for x in sortedx])
    Probabilities=[(x[0],float(x[1])/Tot_words) for x in sortedx]
    print Probabilities[:20]


