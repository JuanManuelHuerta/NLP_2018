import sys
import json
import unicodedata
import numpy

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


print "Number of reviews", len(all_data)
print "Number of products", len(products_count)
print "Average review per product", numpy.mean(products_count.values())






