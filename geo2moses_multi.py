from georead import *
from kfuncs import *
import numpy
import operator
import sys
import getopt

def pvalFilter(Data, cutoff):
	from operator import itemgetter
	rkey = range(2,len(Data))
	M = {}
	rank = featureRank(Data,'1')
	for i in range(len(rkey)):
		if rank[i] < float(cutoff):
			M[rkey[i]] = rank[i]
	X = list(Data[0:2])
	for x in M.keys():
		X.append(Data[x])
	print '[p-value filter] on, cutoff = '+str(cutoff)
	print 'Removed '+str(len(Data)-len(M)-2) +' features'
	return numpy.array(X)

def binarizeMoses(mosesObj):
	labels = numpy.array([eval(x) for x in mosesObj[1:,0]]).astype(int)
	dat = mosesObj[1:,1:].astype(float)
	datB = binarizeDataset(dat)
	out = list([mosesObj[0]])
	for i in range(len(labels)):
		out.append([labels[i]]+list(datB[i]))
	return numpy.array(out)

def main(argv):
	binarize = True
	ifile = ''
	ofile = ''
	p_cutoff = 0
	idf = 'IDENTIFIER'
	try:
		opts, args = getopt.getopt(argv,"hi:o:d:p:b",["ifile=","ofile=","identifier=","pval=","binarize="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			ifile = arg
		elif opt in ("-o", "--ofile"):
			ofile = arg
		elif opt in ("-d", "--identifier"):
			idf = arg
		elif opt in ("-p", "--pval"):
			p_cutoff = arg
		elif opt in ("-b", "--binarize"):
			binarize = arg
			print binarize
	D = ifile
	if ofile == '':
		ofile = ifile+'.moses'
	D_Obj = open(D).readlines()
	OB = ob_transform(D_Obj, identifier=idf, enum=True)
	print 'Detected ' + str(len(D_Obj)-2) + ' features'
	if idf != 'IDENTIFIER':
		print '[identifier] flag on, overriding identifier as '+idf
	if p_cutoff != 0:
		OB = pvalFilter(OB,p_cutoff)
	M_ob = ob2moses(OB)
	if binarize == (True or 1):
		print '[binarize] flag on, Binarizing dataset'
		M_ob = binarizeMoses(M_ob)
	outfile = open(ofile,'w')
	outfile.write('\t'.join(list(M_ob[0]))+'\n')
	for x in M_ob[1:]:
		outfile.write(str(int(eval(x[0])))+'\t'+'\t'.join(x[1:])+'\n')
	outfile.close()
	print 'PREPROCESSING COMPLETE, CREATED MOSES FILE '+ofile
	print str(M_ob.shape[0]-1) + ' Samples, ' + str(M_ob.shape[1]) + ' Features'

if __name__ == "__main__":
	main(sys.argv[1:])
