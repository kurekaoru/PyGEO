#affy.py
from kfuncs import *

X = open('geo/GPL570.annot').readlines() #CHANGE ANNOTATION FILE!!!

def translateList(List,Map,permissive = True):
	out = []
	if permissive:
		for x in List:
			if x in Map and Map[x] != '':
				out.append(Map[x])
			elif Map[x] == '':
				out.append(x)
			else:
				out.append(x)
	else:
		for x in List:
			if x in Map:
				out.append(Map[x])
			else:
				print 'Key error, abort!'
				return
	return out

def annotMap(File):
	startLine = which(X,'!platform_table_begin\n')[0]+1
	M = {}
	for x in File[startLine:-1]:
		O = x.strip().split('\t')
		#print O
		M[O[0]] = O[2]	#CHOOSE WHICH COLUNM TO USE AS VALUES!!!
	return M

annot = annotMap(X)

if __name__ == '__main__':
	annot = annotMap(X)
	translateList(genes,annot)
