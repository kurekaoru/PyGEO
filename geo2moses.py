from georead import *
from kfuncs import *
import numpy
import operator
import sys

D = sys.argv[1]

D_Obj = open(D).readlines()

idf = ID_REF

try:
	idf = sys.argv[2]
	print 'IDENTIFIER flag overridden as '+idf
except:
	pass

#M_ob = ob2moses(numpy.array(ob_transform(D_Obj, identifier='ID_REF', enum=True)))
M_ob = ob2moses(numpy.array(ob_transform(D_Obj, identifier=idf, enum=True)))

def binarizeMoses(mosesObj):
	labels = numpy.array([eval(x) for x in mosesObj[1:,0]]).astype(int)
	dat = mosesObj[1:,1:].astype(float)
	datB = binarizeDataset(dat)
	out = list([M_ob[0]])
	for i in range(len(labels)):
		out.append([labels[i]]+list(datB[i]))
	return numpy.array(out)

X = binarizeMoses(M_ob)

outfile = open(sys.argv[1]+'.moses','w')
outfile.write('\t'.join(list(X[0]))+'\n')
for x in X[1:]:
	outfile.write(str(int(eval(x[0])))+'\t'+'\t'.join(x[1:])+'\n')

outfile.close()
