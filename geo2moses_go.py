from georead import *
from kfuncs import *
import numpy
import operator
import sys

sys.path.insert(0, '../PyUtils')
from sqlutils import *

#D = sys.argv[1]
D = '../data/GDS3688R.soft'

D_Obj = open(D).readlines()

idf = 'ID_REF'

try:
	idf = sys.argv[2]
	print 'IDENTIFIER flag overridden as '+idf
except:
	pass

DAT = ob_transform(D_Obj, identifier=idf, enum=True)

M = {}
c = 0
for x in DAT[:,0][2:]:
	M[x] = c
	c+=1

usedGOS = [x[0] for x in doQuery('select distinct GOID from xref.U133_GO where GOTYPE = \'biological_process \'')]

def xmean(mat):
	out = []
	for i in range(len(mat[0])):
		out.append(numpy.mean(mat[:,i].astype(float)))
	return out

GO_mat = list(DAT[0:2])
c = 0
for x in usedGOS:
	MEMBERS = [y[0] for y in doQuery('SELECT MEMBER FROM xref.U133_GO WHERE GOID = \''+x+'\'')]
	linelist = []
	for y in MEMBERS:
		try:
			linelist.append(M[y])
		except:
			pass
	if linelist != []:
		entry = xmean(extractOB(DAT,linelist))
		entry.insert(0,x)
		GO_mat.append(entry)
		print entry
	print 'STEP '+ repr(c) +'/'+repr(len(usedGOS))
	c+=1

GO_mat = numpy.array(GO_mat)

M_ob = ob2moses(GO_mat)
X = binarizeMoses(M_ob)

outfile = open(D+'.GO.moses','w')
outfile.write('\t'.join(list(X[0]))+'\n')
for x in X[1:]:
	outfile.write(str(int(eval(x[0])))+'\t'+'\t'.join(x[1:])+'\n')

outfile.close()
