from georead import *
from kfuncs import *
import numpy
import operator
import sys

sys.path.insert(0, '../PyUtils')
from sqlutils import *

#D = sys.argv[1]
D = '../data/MF.moses'

D_Obj = [x.strip().split('\t') for x in open(D).readlines()]

MARKERS = D_Obj[0][1:]

M = {}
c = 1
for x in MARKERS:
	M[x] = c
	c+=1

usedGOS = [x[0] for x in doQuery('select distinct GOID from xref.U133_GO where GOTYPE = \'biological_process \'')]

def xmean(mat):
	out = []
	for i in range(len(mat[0])):
		out.append(numpy.mean(numpy.array(mat)[:,i].astype(float)))
	return out

def ymean(mat):
	out = []
	for i in range(len(mat)):
		out.append(numpy.mean(numpy.array(mat)[i,:].astype(float)))
	return out

def getXbyLines(mdata, lines):
	out = []
	for x in lines:
		out.append(numpy.array(mdata)[:,x][1:])
	return numpy.array(out)

xmean(getXbyLines(D_Obj,[1,2,3,4,5]))

GO_mat = []#list([D_Obj[0]])

c = 0
for x in usedGOS:
	MEMBERS = [y[0] for y in doQuery('SELECT MEMBER FROM xref.U133_GO WHERE GOID = \''+x+'\'')]
	linelist = []
	for y in MEMBERS:
		try:
			linelist.append(M[y])
		except:
			pass
	print linelist
	#if linelist != []:
	if len(linelist) > 1:
		entry = xmean(getXbyLines(D_Obj,linelist))
		#Binarize
		entry = list(binarize(entry))
		entry.insert(0,x)
		GO_mat.append(entry)
		print entry
	if len(linelist) == 1:
		entry = list(getXbyLines(D_Obj,linelist)[0].astype(int))
		entry.insert(0,x)
		print entry
	print 'STEP '+ repr(c) +'/'+repr(len(usedGOS))
	c+=1

D_Obj = numpy.array(D_Obj)
GO_mat.insert(0,list(D_Obj[:,0]))

GO_mat = numpy.array(GO_mat)
GO_mat = numpy.transpose(GO_mat)

X = GO_mat

outfile = open(D+'.GO.moses','w')
outfile.write('\t'.join(list(X[0]))+'\n')
for x in X[1:]:
	outfile.write(str(int(eval(x[0])))+'\t'+'\t'.join(x[1:])+'\n')

outfile.close()
