from numpy import *
from sqlutils import *

F = array([x.replace('\n','').split('\t') for x in open('utilization.csv').readlines()][1:])

def SQL_getGOdesc(ID):
	N = doQuery('SELECT name FROM ontology.term WHERE id = '+repr(ID.replace('GO:','')))
	if len(N) > 0:
		return N[0][0]
	else:
		return 'NA'

def SQL_getTermType(ID):
	N = doQuery('SELECT term_type FROM ontology.term WHERE id = '+repr(ID.replace('GO:','')))
	if len(N) > 0:
		return N[0][0]
	else:
		return 'NA'

uniprot = [[x[0],x[1]] for x in doQuery('SELECT DISTINCT GENE, UNIPROT FROM workspace.MATCHING3')]

def insertOrCount(M,K):
	if K in M:
		M[K] = M[K]+1
	else:
		M[K] = 1

def SQL_getPathwayByUniprot(UID):
	N = doQuery('SELECT pName FROM pathways.pathway_homo_sapien WHERE UNIPROT LIKE \'%'+UID+'%\'')
	if len(N) > 0:
		return [x[0] for x in N]
	else:
		return 'NA'

pwy = []

for x in uniprot:
	if x[1] != None:
		pwy.append([x[0],x[1],SQL_getPathwayByUniprot(x[1])])

pwys = {}
for x in pwy:
	for y in x[2]:
		insertOrCount(pwys,y)

spwy = sortMap(pwys)

path = open('pathway.txt','w')

for i in range(len(spwy[0])):
	path.write(spwy[0][i]+'\t'+spwy[1][i]+'\n')

path.close()


GO1 = {}
GO2 = {}
GO3 = {}
GO = {}

for x in F:
	go1 = x[3].split('///')
	for y in go1:
		insertOrCount(GO,y)
		if y in GO1:
			GO1[y] = GO1[y]+1
		else:
			GO1[y] = 1
	#################
	go2 = x[4].split('///')
	for y in go2:
		insertOrCount(GO,y)
		if y in GO2:
			GO2[y] = GO2[y]+1
		else:
			GO2[y] = 1
	#################
	go3 = x[5].split('///')
	for y in go3:
		insertOrCount(GO,y)
		if y in GO3:
			GO3[y] = GO3[y]+1
		else:
			GO3[y] = 1

func = open('GO_func.txt','w')

proc = open('GO_proc.txt','w')

loc = open('GO_loc.txt','w')

go = open('GO.txt','w')

for x in GO1:
	func.write(str(GO1[x])+'\t'+x+'\t'+SQL_getGOdesc(x)+'\n')

for x in GO2:
	loc.write(str(GO2[x])+'\t'+x+'\t'+SQL_getGOdesc(x)+'\n')

for x in GO3:
	proc.write(str(GO3[x])+'\t'+x+'\t'+SQL_getGOdesc(x)+'\n')

sGO = sortMap(GO)

for i in range(len(sGO[0])):
	go.write(sGO[0][i]+'\t'+sGO[1][i]+'\t'+SQL_getGOdesc(sGO[0][i])+'\n')

func.close()
proc.close()
loc.close()
go.close()
