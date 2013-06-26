import numpy


import sys

from sqlutils import *
from kfuncs import *
#from geo_sql import *
from numpy import array, insert

def getCompound(ID, name='Name'):
	return doQuery('SELECT '+name+' FROM TCMID.compounds WHERE ID = '+repr(ID))[0][0]

def getUniprotByGeneName(geneName):
	return [x[0] for x in doQuery('SELECT identifier FROM uniprot.uniprot_homo_sapien WHERE entryName = \''+geneName+'\' and identifier not like \'%-%\'')]

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

#-----------------------------------------------------------Main

#inFile = sys.argv[1]
inFile = '../PyMOSES/obesity.tab'

F = array([x.strip().split('\t') for x in open(inFile).readlines()])

Genes = [x[0] for x in F]

def printmap(M):
	for x in M:
		print [x,M[x]]

db.query('DROP TABLE workspace.OBESITY;')
db.query('CREATE TABLE workspace.OBESITY (GENE VARCHAR(128),SCORE INT(10), UNIPROT VARCHAR(48),COMPOUND VARCHAR(512), HERBS VARCHAR(128));')

for y in F:
	#print y
	g = y[0]
	score = y[1]
	uniprot = getUniprotByGeneName(g)
	#print score+' '+g+ ' '+repr(uniprot)
	if len(uniprot) == 0:
		print 'INSERT INTO workspace.OBESITY(GENE, SCORE) VALUES(\''+g+'\','+score+');'	#OK
		db.query('INSERT INTO workspace.OBESITY(GENE, SCORE) VALUES(\''+g+'\','+score+');')
	else:
		for z in uniprot:
			compounds = [t[0] for t in doQuery('SELECT cID FROM TCMID.interactions WHERE protein = \''+z+'\'')]
			if len(compounds) == 0:
				print 'INSERT INTO workspace.OBESITY(GENE, SCORE, UNIPROT) VALUES(\''+g+'\','+score+',\''+z+'\');'
				db.query('INSERT INTO workspace.OBESITY(GENE, SCORE, UNIPROT) VALUES(\''+g+'\','+score+',\''+z+'\');')
			else:
				for a in compounds:
					compoundName = getCompound(a).replace('\'','_')
					herbs = getHerbByCompound(a)
					if type(herbs) == str:
						print 'INSERT INTO workspace.OBESITY(GENE, SCORE, UNIPROT, COMPOUND) VALUES(\''+g+'\','+score+',\''+z+'\',\''+compoundName+'\');'
						db.query('INSERT INTO workspace.OBESITY(GENE, SCORE, UNIPROT, COMPOUND) VALUES(\''+g+'\','+score+',\''+z+'\',\''+compoundName+'\');')
					else:
						for hb in herbs:
							print 'INSERT INTO workspace.OBESITY(GENE, SCORE, UNIPROT, COMPOUND, HERBS) VALUES(\''+g+'\','+score+',\''+z+'\',\''+compoundName+'\',\''+hb+'\');'
							db.query('INSERT INTO workspace.OBESITY(GENE, SCORE, UNIPROT, COMPOUND, HERBS) VALUES(\''+g+'\','+score+',\''+z+'\',\''+compoundName+'\',\''+hb+'\');')

