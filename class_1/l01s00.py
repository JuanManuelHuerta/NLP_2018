import sys


print "Python refresher"


A=[]
A.append('hi')
A.append('hi')
print "This is an array", A

B=set(A)
print "This is a set", B
print "Add one more thing to the set", B.add('bye')

C={}
C['key1']='value1'
C['key3']='value2'
C['key2']='value3'


print "this is a dictionary", C

for key in C:
    print key, C[key]

print "Again"

for item in C.items():
    print item[0], item[1]

# List comprehension
D=[23,34,56,74]
E=[x*x for x in D]
print "List comprehension", E


