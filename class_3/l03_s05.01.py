import sys
import json
import unicodedata
#import numpy
#from nltk import sent_tokenize, word_tokenize, pos_tag
import re
import operator
import random

def custom_word_tokenize(my_string):
	s0=my_string
	s1=re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
	s2=re.sub(r'[;\,\:\s \(\)\-\!\?]',r' ',s1.lower())
	s3=re.sub(r'\. ',r' ',s2)
	words=s3.split(" ")
	return words

def sed(x,y):
	lx=len(x)
	ly=len(y)
	D=[[0.0]*(ly+1) for i in range(lx+1)]
	for i in range(lx+1):
		D[i][0]=i
	for i in range(ly+1):
		D[0][i]=i
	for i in range(ly):
		ii=i+1
		for j in range(lx):
			jj=j+1
			if x[j]==y[i]:
				D[jj][ii]=D[jj-1][ii-1]
			else:
				D[jj][ii]=min(D[jj-1][ii]+1.0,D[jj][ii-1]+1.0,D[jj-1][ii-1]+1.0)
	
	return D[-1][-1]

fp=open("../reviews_Automotive_5.json","rt")
all_data = []
reviews_text=[]
products_count={}

reviews_per_product={}
master_dictionary={}

for line in fp:
	review_data = json.loads(line)
	all_data.append(review_data)
	review_n = unicodedata.normalize('NFKD',review_data["reviewText"]).encode('ascii','ignore')
	words=custom_word_tokenize(review_n)
	for word in words:
		if not word in master_dictionary:
			master_dictionary[word]=0
		master_dictionary[word]+=1
sd=sorted(master_dictionary.items(),key=operator.itemgetter(1), reverse=True)[:300]


while True:
	input=raw_input("Enter word> ").rstrip()
	results =sorted( [(x[0],sed(x[0],input)) for x in sd],key=operator.itemgetter(1))[:10]
	for r in results:
		print r

	
		       






