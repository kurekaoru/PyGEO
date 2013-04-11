from sqlutils import *
from kfuncs import *

def SQL_translateList(IDS):
	return doQuery('SELECT Gene_title FROM xref.U133 WHERE mid IN (\"'+'\",\"'.join(IDS)+'\")')

def SQL_translateMarker(ID):
	return doQuery('SELECT Gene_symbol FROM xref.U133 WHERE mid = \''+ID+'\'')

def SQL_translateList(IDS):
	return doQuery('SELECT Gene_symbol FROM xref.U133 WHERE mid IN (\"'+'\",\"'.join(IDS)+'\")')

def SQL_translateList2(IDS):
	res = [x[0] for x in doQuery('SELECT Gene_symbol FROM xref.U133 WHERE mid IN (\"'+'\",\"'.join(IDS)+'\")')]
	for i in range(0,len(res)):
		if res[i] == '':
			res[i] = IDS[i]
	return res
