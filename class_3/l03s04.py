
# Goal: Implement string edit distance (Levenshtein)

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



def  sed(x,y):
	x_l=len(x)
	y_l=len(y)
	Z=[[0.0]*(y_l+1) for i in range(x_l+1)]
	for i in range(y_l+1):
		Z[0][i]=i
	for i in range(x_l+1):
		Z[i][0]=i
	for i in range(y_l):
		ii=i+1
		for j in range(x_l):
			jj=j+1
			if x[j]==y[i]:
				Z[jj][ii]=Z[jj-1][ii-1]
			else:
				Z[jj][ii]=min(Z[jj-1][ii]+1,Z[jj][ii-1]+1,Z[jj-1][ii-1]+1)
	return Z[-1][-1]



s="AABC"
t="AADCF"
while True:
	x=raw_input("String A>").rstrip()
	y=raw_input("String B>").rstrip()
	print levenshtein(x,y)
	print sed(x,y)

