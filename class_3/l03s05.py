import sys
import json
import unicodedata
import numpy
import re
import operator

def custom_word_tokenize(my_string):
	s0=my_string
	s1=re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
	s2=re.sub(r'[;\,\:\s \(\)\-\!\?]',r' ',s1.lower())
	s3=re.sub(r'\. ',r' ',s2)
	words=s3.split(" ")
	return words

def levenshtein(s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(t)]





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
print "IMHERE"

print "Number of reviews", len(all_data)
print "Number of products", len(products_count)
print "Average review per product", numpy.mean(products_count.values())

#for review in reviews_text:
#	print "Original Review", review
#	print "nltk tokenizer", word_tokenize(review)
#	print "custom tokenizer", custom_word_tokenize(review)


master_dictionary={}
dictionary_per_score={}


for review_data in all_data:
	review = unicodedata.normalize('NFKD',review_data["reviewText"]).encode('ascii','ignore')
	score = review_data["overall"]
	if not score in dictionary_per_score:
		dictionary_per_score[score]={}
	words = custom_word_tokenize(review)
	for word in words:
		if not word in master_dictionary:
			master_dictionary[word]=0
		if not word in dictionary_per_score[score]:
			dictionary_per_score[score][word]=0
		master_dictionary[word]+=1
		dictionary_per_score[score][word]+=1


md_sorted = sorted(master_dictionary.items(),key=operator.itemgetter(1),reverse=True)[:3000]
md_dict={}
for item in md_sorted:
	md_dict[item[0]]=item[1]
while True:
	candidate = raw_input("Enter candidate word: >").rstrip()
	if candidate in md_dict:
		print "Spelling fond"
	else:
		corrections={}
		for key_w in md_dict:
			corrections[key_w]=levenshtein(candidate,key_w)
		c_sorted=sorted(corrections.items(),key=operator.itemgetter(1),reverse=False)[:10]
		for matches in c_sorted:
			print matches









