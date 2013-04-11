from georead import *
import operator
from annot import annot
from kfuncs import *
from dataproc import *

def readDataset(filename):
	from numpy import array
	return array([ x.rstrip().split('\t') for x in open(filename).readlines()])

def alterLabel(dataset,targetCategory):	
	L = ['']
	for x in dataset[1][1:]:
		if x == targetCategory:
			L.append('1')
		else:
			L.append('0')
	dataset[1] = L

def readOB(filename, targetCategory):
	from numpy import array
	x = readDataset(filename)
	alterLabel(x,targetCategory)
	return array(x)


fat = readOB('/run/media/kurekaoru/SILVER/Inflammation/geo/GSEct27916.data','female')

fat_m = ob2moses(fat)

writecsv('/run/media/kurekaoru/SILVER/Inflammation/geo/GSEct27916.moses',fat_m)
