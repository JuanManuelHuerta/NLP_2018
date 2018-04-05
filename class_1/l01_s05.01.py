import sys
import json
import unicodedata
import numpy
from nltk import sent_tokenize, word_tokenize, pos_tag
import re
import operator
import math

def custom_word_tokenize(my_string):
	s0=my_string
	s1=re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
	s2=re.sub(r'[;\,\:\s \(\)\-\!\?]',r' ',s1.lower())
	s3=re.sub(r'\. ',r' ',s2)
	words=s3.split(" ")
	return words



fp=open("stop_words.txt","rt")
stop_words=set()
for line in fp:
	stop_words.add(line.rstrip())
print "Loaded stop words!"



fp=open("../reviews_Automotive_5.json","rt")
all_data = []
reviews_text=[]
products_count={}

for line in fp:
	review_data = json.loads(line)
	all_data.append(review_data)
	review_n = unicodedata.normalize('NFKD',review_data["reviewText"]).encode('ascii','ignore')
	reviews_text.append(review_n)
	asin = review_data["asin"]
	if not asin in products_count:
		products_count[asin]=0
	products_count[asin]+=1


#print "Number of reviews", len(all_data)
#print "Number of products", len(products_count)
#print "Average review per product", numpy.mean(products_count.values())

#for review in reviews_text:
#	print "Original Review", review
#	print "nltk tokenizer", word_tokenize(review)
#	print "custom tokenizer", custom_word_tokenize(review)


master_dictionary={}
dictionary_per_score={}


for review_data in all_data:
	review = unicodedata.normalize('NFKD',review_data["reviewText"]).encode('ascii','ignore')
	score = review_data["asin"]
	if not score in dictionary_per_score:
		dictionary_per_score[score]={}
	words = custom_word_tokenize(review)
	for word in words:
		if not word in stop_words:
			if not word in master_dictionary:
				master_dictionary[word]=0
			if not word in dictionary_per_score[score]:
				dictionary_per_score[score][word]=0
			master_dictionary[word]+=1
			dictionary_per_score[score][word]+=1


top_words={}
InverseDocumentFrequency={}

for asin in dictionary_per_score:
	for word in dictionary_per_score[asin]:
		if not word  in InverseDocumentFrequency:
			InverseDocumentFrequency[word]=0
		InverseDocumentFrequency[word]+=1


for score in dictionary_per_score:
	print "ASIN", score

	for word in dictionary_per_score[score]:
		dictionary_per_score[score][word]=dictionary_per_score[score][word]*math.log(len(dictionary_per_score)/InverseDocumentFrequency[word])


	dps_sorted = sorted(dictionary_per_score[score].items(),key=operator.itemgetter(1),reverse=True)[0:25]
	for word in zip(range(len(dps_sorted)),dps_sorted):
		print score, word









