import sys

sys.path.insert(0, '..')

from sqlutils import *
from kfuncs import *
from numpy import array, insert

db.query('CREATE TABLE workspace.MATCHING (MARKER VARCHAR(64),GENE VARCHAR(128),UNIPROT VARCHAR(48),COMPOUND VARCHAR(128), HERBS VARCHAR(128));')

inFile = 'moses_out/O100_utils.txt'

F = array([x.strip().split('\t') for x in open(inFile).readlines()])

markers = F[:,0]

def getCompound(ID, name='Name'):
	return doQuery('SELECT '+name+' FROM TCMID.compounds WHERE ID = '+repr(ID))[0][0]

def getHerb(ID, name='cName'):
	herbs = doQuery('SELECT '+name+' FROM TCMID.herbs WHERE ID = '+repr(ID))
	if len(herbs) == 0:
		return 'NULL'
	else:
		return herbs

def getHerbByCompound(cid, name='name'):
	if type(cid) == int:
		cid = repr(cid)
	herbs = doQuery('SELECT '+name+' FROM TCMID.herbs WHERE compounds LIKE \'%'+cid+',E|%\'')
	#print ('SELECT '+name+' FROM TCMID.herbs WHERE compounds LIKE \'%'+repr(cid)+',E|%\'')
	if len(herbs) == 0:
		return 'NULL'
	else:
		return [x[0] for x in herbs]

M2G = {}
G2U = {}
X = open('../curate2.txt').readlines()
for x in X:
	L = x.strip().split('\t')
	uniprot = L[2].split('///')
	G2U[L[1]] = uniprot
	M2G[L[0]] = True

markers = M2G.keys()

#db.query('TRUNCATE workspace.MATCHING')
for m in markers:
    db.query('DELETE FROM workspace.MATCHING WHERE MARKER = \''+m+'\'')
    genes = [x[0] for x in doQuery('SELECT Gene_symbol FROM xref.U133 WHERE mid = \''+m+'\'')][0].split('///')
    for y in genes:
            print [m,y]
            uniprot = G2U[y]
            if len(uniprot) == 0:
                    print [m, y, 'NA']
                    #db.query('INSERT INTO workspace.MATCHING(MARKER, GENE) VALUES(\''+m+'\',\''+y+'\');')
            else:
                    for z in uniprot:
                            compounds = [t[0] for t in doQuery('SELECT cID FROM TCMID.interactions WHERE protein = \''+z[0]+'\'')]
                            for a in compounds:
                                    compoundName = getCompound(a)
                                    herbs = getHerbByCompound(a)
                                    if type(herbs) == list:
                                           for b in herbs:
                                                   db.query('INSERT INTO workspace.MATCHING(MARKER, GENE, UNIPROT, COMPOUND, HERBS) VALUES(\''+m+'\',\''+y+'\',\''+z[0]+'\',\''+compoundName+'\',\''+b+'\');')
                                    else:
                                           db.query('INSERT INTO workspace.MATCHING(MARKER, GENE, UNIPROT, COMPOUND) VALUES(\''+m+'\',\''+y+'\',\''+z[0]+'\',\''+compoundName+'\');')

