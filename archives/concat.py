#RFTEST
from kfuncs import *
from sqlutils import *
import _mysql
from numpy import *
from pylab import *
from georead import *
from Test4 import *
ion()


L_car = T_car[1,1:].astype(float)
D_car = T_car[2:,1:].astype(float)
#D_car = log(D_car)

features = T_car[2:,0]

o = []
oo = []
for x in D_car:
	#o.append(stats.ttest_ind(x[L_car==1],x[L_car==0]))
	o.append(stats.ttest_ind(x[L_car==1],x))
	oo.append(sum(x[L_car==1])/sum(x[L_car==0]))

o = array(o)
oo = array(oo)
pval = o[:,1]

#L = []
#for i in range(0,len(pval)):
#	if pval[i] < 0.1:	
#		L.append(i)

L = []
for i in range(0,len(oo)):
	if oo[i] > 8:	
		L.append(i)

res_car = getByIndex(D_car,L)
feat_car = getByIndex(features,L)
SQL_translateList2(feat_car)


for i in range(len(L)):
	#print ('INSERT INTO S300 VALUES(\''+feat_car[i]+'\','+'2154'+',\''+SQL_translateMarker(feat_car[i])[0][0]+'\','+str(oo[i])+','+str(o[i][0])+','+str(o[i][1])+')')
	db.query('INSERT INTO randomForest.S300 VALUES(\''+feat_car[i]+'\','+'2154'+',\''+SQL_translateMarker(feat_car[i])[0][0]+'\','+str(oo[L[i]])+','+str(o[L[i]][0])+','+str(o[L[i]][1])+')')

#CREATE TABLE randomForest.S300(gene varchar(128) not null, dataset int(10), name varchar(128), diff float, tstat float, pval float);



#####################sar
L_sar = T_sar[1,1:].astype(float)
D_sar = T_sar[2:,1:].astype(float)
D_sar = exp(D_sar)

o = []
oo = []
for x in D_sar:
	o.append(stats.ttest_ind(x[L_sar==1],x))
	oo.append(sum(x[L_sar==1])/sum(x[L_sar==0]))

o = array(o)
pval = o[:,1]


L = []
for i in range(0,len(oo)):
	if oo[i] > 5:	
		L.append(i)

#L = []
#for i in range(0,len(pval)):
#	if pval[i] < 0.1:	
#		L.append(i)

res_sar = getByIndex(D_sar,L)
feat_sar = getByIndex(features,L)
SQL_translateList(feat_sar)

for i in range(len(L)):
	db.query('INSERT INTO randomForest.S300 VALUES(\''+feat_sar[i]+'\','+'3580'+',\''+SQL_translateMarker(feat_sar[i])[0][0]+'\','+str(oo[L[i]])+','+str(o[L[i]][0])+','+str(o[L[i]][1])+')')

#####################sar


def binarize(data,metric='median'):
	from numpy import array
	data = array(data).astype(float)
	if metric == 'median':
		return (data < median(data)).astype(int)

def binarizeDataset(dataset, metric='median'):
	return [binarize(x) for x in dataset]

def concatDatasets(ListOfDatasets,index, binarize=False):
	try:
		import progressbar as P
		pbar_exists = True
	except ImportError: 
		pbar_exists = False
	from numpy import array, nan, nanmax
	out = []
	Ind = index [:]
	#Convert everything to float and normalize!
	D = []
	for x in ListOfDatasets:
		Dataset = array(x)[2:,1:]
		removeNull(Dataset,nan)
		Dataset = Dataset.astype(float)
		##################################################NORMALIZATION STEP (CRUCIAL)
		if binarize:
			Dataset = array(binarizeDataset(Dataset)).astype(int)
			D.append(Dataset)
		else:
			Dataset /= nanmax(Dataset)
			D.append(Dataset)
		##################################################NORMALIZATION STEP (CRUCIAL)
	header = [""]
	classifier = [""]
	for x in ListOfDatasets:
		header+=x[0][1:]
		classifier+=x[1][1:]
	out.append(header)
	out.append(classifier)
	for x in Ind:
		L = [ListOfDatasets[0][x][0]]
		for y in D:
			L+=y[x-2]
		out.append(L)
	return array(out)

def ob2moses(dataset):
	from numpy import array, transpose
	out = []
	T = transpose(dataset)
	features = T[0][1:]
	features[0] = 'out'
	out.append(features)
	for x in T[1:]:
		out.append(array(x[1:]).astype(int))
	return array(out)

db=_mysql.connect("localhost","kaoru","rbdWK2uk")

F = array([x[0] for x in (doQuery('select distinct gene from randomForest.R300'))])
F2 = array([x[0] for x in (doQuery('select distinct gene from randomForest.S300'))])

F = list(F)+list(F2)

ALL = array(extractFeatures(T_pso))

def which2(E,L):
	c = 0
	for x in L:
		if E == x:
			return c
		c+=1

I = []
for x in F:
	I.append(which2(x,ALL))


T_INF = concatDatasets([T_sar,T_pso,T_col,T_pan,T_car],I,binarize=True)

MT_INF = ob2moses(T_INF)

writecsv('O100.ob',array(T_INF).astype(str))
writecsv('MF.moses',array(MT_INF).astype(str))

