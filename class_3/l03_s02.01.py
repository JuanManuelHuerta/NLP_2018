import sys
import json
import unicodedata
#import numpy
#from nltk import sent_tokenize, word_tokenize, pos_tag
import re
import operator

def custom_word_tokenize(my_string):
	s0=my_string
	s1=re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
	s2=re.sub(r'[;\,\:\s \(\)\-\!\?]',r' ',s1.lower())
	s3=re.sub(r'\. ',r' ',s2)
	words=s3.split(" ")
	return words

def cosine_similarity(dict1, dict2):
	numerator=0.0
	norm1=0.0
	norm2=0.0
	for word in dict1:
		norm1+=dict1[word]**2.0
	norm1=norm1**0.5
	for word in dict2:
		norm2+=dict2[word]**2.0
	norm2=norm2**0.5

	for word in set(dict1.keys()).intersection(set(dict2.keys())):
		numerator+=(dict1[word]*dict2[word])
	return numerator/(norm1*norm2)


## Open the file, scan the data, keep review texts.
fp=open("stop_words.txt","rt")
stop_words=set()
for line in fp:
    stop_words.add(line.rstrip())


fp=open("../reviews_Automotive_5.json","rt")
all_data = []
reviews_text=[]
products_count={}

reviews_per_product={}

for line in fp:
	review_data = json.loads(line)
	all_data.append(review_data)
	review_n = unicodedata.normalize('NFKD',review_data["reviewText"]).encode('ascii','ignore')
	asin = review_data["asin"]
	if not asin in reviews_per_product:
		reviews_per_product[asin]={}
	words=custom_word_tokenize(review_n)
	for word in words:
		if word in stop_words:
			if not word in reviews_per_product[asin]:
				reviews_per_product[asin][word]=0.0
			reviews_per_product[asin][word]+=1.0


nodes=set()
links=[]
threshold =.975
for asin1 in reviews_per_product:
	for asin2 in reviews_per_product:
		cs= cosine_similarity(reviews_per_product[asin1],reviews_per_product[asin2])
		if cs > threshold:
			nodes.add(asin1)
			nodes.add(asin2)
			links.append((asin1, asin2, cosine_similarity(reviews_per_product[asin1],reviews_per_product[asin2])))
		if len(links)>300:
			break
fp=open("nodes.csv","wt")
fp.write("node,group\n")
for node in nodes:
	fp.write(node+",class1\n")
fp.close()
fp=open("links.csv","wt")
fp.write("source,target,type\n")
for link in links:
	fp.write(link[0]+','+link[1]+',type1\n')
fp.close()



				    

		       






