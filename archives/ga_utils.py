from kutils import *

def divideDataset(Data,testSize=0.1):
	numOfCases = len(Data[1][1:])
	Size = int(numOfCases*testSize)
	tests = random.sample(xrange(numOfCases), Size)
	tests.sort()
	trains = complement(tests, range(numOfCases))
	return [tests,trains]

def randsamp(sampleSize,fraction):
	from random import sample
	if fraction > 1:
		print '[ERROR] Fraction must be in the range 0<=F<=1!'
	else:
		R = range(sampleSize)
		out = sample(R, int(fraction*sampleSize))
		out.sort()
		return out

def bootstrap(D,fraction = 0.1):
	x = randsamp(len(D),fraction)
	return getByIndex(D,x)

def info(classes):
	sumOfClass = 0
	Nt = float(sum(classes.values()))
	for V in classes.values():
		print [V, Nt]
		sumOfClass+=(float(V)/Nt)*log(float(V)/Nt)
	return -sumOfClass

def mapIndex(dat, offset = 0):
	out = {}
	for i in range(len(dat)):
		out[dat[i]] = i+offset
	return out

def zippedSort(V,cat):
	Z = zip(cat,V)
	Z.sort()
	return Z

def sortSplit(V,Cat):
	sList = zippedSort(V,Cat)
	print sList

def medianSplit(V):
	M = median(V)
	out = {}
	c = 0
	for x in V:
		if x < M:
			out[c] = 0
		else:
			out[c] = 1
		c+=1
	return out

def C4_5(trainDat):
	from numpy import array
	#Check for base classes:
	#A: All the samples in the list belong to the same class. When this happens, it simply creates a leaf node for the decision tree saying to choose that class.
	#B: None of the features provide any information gain. In this case, C4.5 creates a decision node higher up the tree using the expected value of the class.
	#C: Instance of previously-unseen class encountered. Again, C4.5 creates a decision node higher up the tree using the expected value.
	#Fro each attribute a:
	Fmap = mapIndex(trainDat[:,0][2:],2)
	print Fmap
	for x in Fmap.keys():
		values = trainDat[Fmap[x]][1:].astype(float)
		print values


C4_5(T_pso[0:5])

#step(range(len(yd)),yd)

def sortMap(Map):
	K = []
	V = []
	S = sorted(Map.iteritems(), key=operator.itemgetter(1))
	for x in S:
		K.append(x[0])
		V.append(x[1])
	return array([K,V])

def evaluate(List, cutoff):
	from numpy import array
	out = []
	for x in List:
		if x < cutoff:
			out.append(0)
		else:
			out.append(1)
	return array(out)


def forest(M, F):
	for x in range(M):
		Dk = bootstrap(D)


#1: Let the number of training cases be N, and the number of variables in the classifier be M.
#2: We are told the number m of input variables to be used to determine the decision at a node of the tree; m should be much less than M.
#3: Choose a training set for this tree by choosing n times with replacement from all N available training cases (i.e., take a bootstrap sample). Use the rest of the cases to estimate the error of the tree, by predicting their classes.
#4: For each node of the tree, randomly choose m variables on which to base the decision at that node. Calculate the best split based on these m variables in the training set.
#5: Each tree is fully grown and not pruned (as may be done in constructing a normal tree classifier).


# Random forest fseudo code
#	M:No of trees on forest
# 	f:Num of features in original space
#	F:Num of features desired in induced space
#	Bootstrap: builds training set by sampling w replacement
#	NodesOnPath : Returns nodes on path from root to leaf for a fiven instance and tree
#	GetNodeID : Returns a node identifier ID in forest
#
# Pseudocode:
# for k ⇐ 1 to M do
#	Dk ⇐ Bootstrap(D)
#	hk ⇐ RandomTree(Dk , √f )
# Forest ⇐ hk
# for each hk ∈ Forest do
#	for each xi ∈ D do
#		Phk(xi) ⇐ NodesOnPath(xi , hk )
#		for each n ∈ Phk (xi ) do
#			node id ⇐ GetNodeID(n)
#			feature id ⇐ Hash(node id, F )
#			xi,feature id ⇐ xi,feature id + 1
# return D ⇐ xi

a=[7.965,7.888,7.74, 6.655,7.621,6.806,6.13, 5.17, 5.916,7.306,7.194,7.632,6.72, 7.4,7.474,7.74, 7.119,7.554,8.14, 7.012,7.623,7.714,7.007,6.552,6.216,7.075,6.973,7.76, 7.149,6.585,7.257,7.892,6.947,7.425,7.045,7.338,7.412,7.94, 6.555,6.842,7.661,7.835,7.227,6.747,7.172,5.957,7.265,6.446,6.327,6.178,6.989,6.869,7.306,7.873,7.611,7.676,6.899,7.431,7.839,7.139,7.153,6.799,6.949,7.396,7.397,7.456,7.764,7.058,7.699,6.731,6.704,7.138,7.462,6.391,7.086,7.182,3.92, 6.68, 7.572,7.245,7.523,6.759]








#def forest(Data, Nsamples, testSize = 0.1, mfrac = 0.001):
#	N = len(Data[1][1:])
#	M = len(Data[2:,1])
#	print [N,M]
#	#Create N bootstrap samples
#	for x in range(Nsamples):		
#		indeces = divideDataset(Data, testSize)
#		for y in range(Nsamples):
#			print randsamp(M,mfrac)
#	print indeces
#forest(T_pso,1)

