from georead import *
from pylab import *
import numpy
import operator
from annot import annot
from kfuncs import *
from dataproc import *
ion()

Psoriasis = 'geo/GDS3539_full.soft' #Psoriasis
sarcoidosis = 'geo/GDS3580_full.soft' #sarcoidosis
Pancreas_malaria = 'geo/GDS2822_full.soft' #Pancreas
colitis = 'geo/GDS3119_full.soft' #ulcerative colitis
Myocarditis = 'geo/GDS2154_full.soft' #inflammatory dilated cardiomyopathy

X_pso = open(Psoriasis).readlines()
X_sar = open(sarcoidosis).readlines()
X_pan = open(Pancreas_malaria).readlines()
X_col = open(colitis).readlines()
X_car = open(Myocarditis).readlines()

#Define scoring kernel
def kernel(X):
	return var(X)

# DATASETS
# geoId	Describtion	VarName	Class	targetCategory	
# 3539	Psoriasis	X_pso	'disease state'	'psoriasis' 21 61
# 2822	Pancreas	X_pan	X_pan'	'other'	'inflamed'
# 3119	Colitis	X_col	X_col	'specimen'	'inflamed'
# 3580	sarcoidosis	X_sar	'disease state'	'sarcoidosis'
# 2154	Myocarditis	X_car	'disease state'	'inflammatory dilated cardiomyopathy'

# Platform: U133 | 54676 Markers

T_pso = numpy.array(ob_transform(X_pso, identifier='ID_REF',targetClass='disease state',targetCategory='psoriasis', enum=True))
T_sar = numpy.array(ob_transform(X_sar, identifier='ID_REF',targetClass='disease state',targetCategory='sarcoidosis', enum=True))
T_car = numpy.array(ob_transform(X_car, identifier='ID_REF',targetClass='disease state',targetCategory='inflammatory dilated cardiomyopathy', enum=True))
T_col = numpy.array(ob_transform(X_col, identifier='ID_REF',targetClass='specimen',targetCategory='inflamed', enum=True))
T_pan = numpy.array(ob_transform(X_pan, identifier='ID_REF',targetClass='other',targetCategory='inflamed', enum=True))

sargenes = readMap('out/GDS3580sd2.txt')
psogenes = readMap('out/GDS3539sd2.txt')
colgenes = readMap('out/GDS3119sd2.txt')
myogenes = readMap('out/GDS2154sd2.txt')
pangenes = readMap('out/GDS2822sd2.txt')

C11111 = intersection(intersection(intersection(intersection(psogenes,sargenes),pangenes),colgenes),myogenes)
C11110 = intersection(intersection(intersection(psogenes,sargenes),pangenes),colgenes)
C11101 = intersection(intersection(intersection(psogenes,sargenes),pangenes),myogenes)
C11011 = intersection(intersection(intersection(psogenes,sargenes),colgenes),colgenes)
C10111 = intersection(intersection(intersection(myogenes,psogenes),pangenes),colgenes)
C01111 = intersection(intersection(intersection(myogenes,sargenes),pangenes),colgenes)
C11100 = intersection(intersection(psogenes,sargenes),pangenes)
C11010 = intersection(intersection(psogenes,sargenes),colgenes)
C11001 = intersection(intersection(psogenes,sargenes),myogenes)
C10011 = intersection(intersection(psogenes,colgenes),myogenes)
C10101 = intersection(intersection(psogenes,pangenes),myogenes)
C10110 = intersection(intersection(psogenes,pangenes),colgenes)
C01011 = intersection(intersection(sargenes,colgenes),myogenes)
C01101 = intersection(intersection(sargenes,pangenes),myogenes)
C01110 = intersection(intersection(sargenes,pangenes),colgenes)
C00111 = intersection(intersection(myogenes,pangenes),colgenes)

GL = [C11111,C11110,C11101,C11011,C10111,C01111,C11100,C11010,C11001,C10011,C10101,C10110,C01011,C01101,C01110,C00111]

U = unique(union(union(union(union(psogenes,sargenes),pangenes),colgenes),myogenes))

index = whichIn(U, extractFeatures(T_pso))

#Override: use everything

index = range(2,len(T_pso))

T_INF = array(concatDatasets([T_sar,T_pso,T_col,T_pan,T_car],index))


