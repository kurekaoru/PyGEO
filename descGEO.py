#GEOreader
import re
import numpy as np
from kfuncs import *
import sys

def show_classes(FileObj,listCases = False):
	from numpy import array
	subsetTypes = {}
	subsetTypeLines = which(FileObj,'!subset_type')
	for i in subsetTypeLines:
		subsetTypes[FileObj[i].strip().split(' = ')[1]] = True
	for x in subsetTypes.keys():
		subsetChildLines = which(FileObj,'!subset_type = '+x)
		print 'Class: '+x
		for y in subsetChildLines:
			print '\tCategory: '+FileObj[y-2].strip().split(' = ')[1]+' | '+repr(len(FileObj[y-1].strip().split(' = ')[1].split(','))) + ' cases'
			if listCases:
				subsetCases = FileObj[y-1].strip().split(' = ')[1].split(',')
				for z in subsetCases:
					print '\t\tCase:'+z

if __name__ == '__main__':
	try:
		FO = open(sys.argv[1]).readlines()
		show_classes(FO,listCases=False)
	except:
		print 'Error: File not specified'
