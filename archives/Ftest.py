from georead import *
import numpy
from pylab import *
import operator
from annot import annot
from scipy.stats import norm
import operator
ion()

show_classes(X)

def getByIndex2(L,inds):
	out = []
	for x in inds:
		out.append(L[x])
	return out

Psoriasis = 'geo/GDS3539_full.soft' #Psoriasis
Hepatitis = 'geo/GDS3282_full.soft' #Hepatitis
Pancreas_malaria = 'geo/GDS2822_full.soft' #Pancreas
colitis = 'geo/GDS3119_full.soft' #ulcerative colitis
X_pso = open(Psoriasis).readlines()
X_hep = open(Hepatitis).readlines()
X_pan = open(Pancreas_malaria).readlines()
X_col = open(colitis).readlines()

show_classes(X_pan)

#Define scoring kernel
def kernel(X):
	return var(X)

def mat_normalize(mat):
	mat = array(mat)
	return mat/mat.max()

# DATASETS

# 3539 Psoriasis	X_pso	'disease state'	'psoriasis'
# 3282 Hepatitis	X_hep	'specimen'	'non-tolarent'
# 2822 Pancreas	X_pan	X_pan'	'other'	'inflamed'
# 3119 Colitis	X_col	X_col	'specimen'	'inflamed'

# Platform: U133 | 54676 Markers

T_pso = numpy.array(ob_transform(X_pso, identifier='ID_REF',targetClass='disease state',targetCategory='psoriasis', enum=True))
T_hep = numpy.array(ob_transform(X_hep, identifier='ID_REF',targetClass='specimen',targetCategory='non-tolerant', enum=True))
T_pan = numpy.array(ob_transform(X_pan, identifier='ID_REF',targetClass='other',targetCategory='inflamed', enum=True))
T_col = numpy.array(ob_transform(X_col, identifier='ID_REF',targetClass='specimen',targetCategory='inflamed', enum=True))

controls = array(which(T[1],'0'))
cases = array(which(T[1],'1'))

M = MapGroups(X_pso,'psoriasis')

a = []
b = []

for x in T[2:]:
	caseVal = numpy.array(getByIndex2(x,cases)).astype(float)
	controlVal =  numpy.array(getByIndex2(x,controls)).astype(float)
	a.append(kernel(caseVal))
	b.append(kernel(controlVal))

a = array(a)
b = array(b)
c = a/b

mu = mean(log(c))
v = var(log(c))
sigma = sqrt(v)

# Plot between -10 and 10 with .001 steps.
#range = np.arange(-10, 10, 0.001)
#plot(range, norm.pdf(range,mu,sigma))

count = 2

index = []
for x in c:
	if abs(log(x)) >= 4 * sigma:
		index.append(count)
	count+=1

Ts = []
genes = {}

for x in index:
	genes[annot[T[x][0]]] = log(c[x-2])
	Ts.append(T[x])

Ds = array(Ts)[2:,1:].astype(float)
DsGenes = array(Ts)[2:,0]

DsSorted = []
for x in Ds:
	L = getByIndex2(x,controls-1)
	L += getByIndex2(x,cases-1)
	DsSorted.append(L)

DsSorted = array(DsSorted)

#PLOT!
total = len(T[0])-1
covar_samples=cov(transpose(DsSorted))
covar_genes=cov(DsSorted)
matshow(covar_samples)
ylim(0,total-1)
xlim(0,total-1)
axvline(len(controls),-10,10,c='red',lw=2)
axhline(len(controls),-10,10,c='red',lw=2)

covar = covar_samples
covar = covar_genes

#P2
#Dendrogram
import scipy.cluster.hierarchy as sch
F = figure()

#Left dendrogram
dendro = F.add_axes([0.09,0.1,0.2,0.8])
Y = sch.linkage(covar, method='centroid')
Z = sch.dendrogram(Y, orientation='right')
dendro.set_xticks([])
dendro.set_yticks([])

#Plot the matrix
I = Z['leaves']
covar = covar[I,:]
covar = covar[:,I]
axmatrix = F.add_axes([0.3,0.1,0.6,0.8])
im = axmatrix.matshow(covar, aspect='auto', origin='lower')
axmatrix.set_xticks([])
axmatrix.set_yticks([])


#pcolor(cov(DsSorted))

#plot(DsSorted[534][1:])

sortedGenes = sorted(genes.iteritems(), key=operator.itemgetter(1))
genes[Ts[index[x]]] = c[index[x]] for x in index]
geneNames = translateList(genes,annot)

#log(var(getByIndex2(Ds[0],(controls-1)))/var(getByIndex2(Ds[0],(cases-1))))


