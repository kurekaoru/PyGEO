import sys

sys.path.insert(0, '../PyUtils')
from sqlutils import *

goid = doQuery('select acc, term_type from GO.term where is_obsolete = 0 AND acc LIKE \'GO:%\'')

#L = {}

for x in goid:
	T = ''
	if x[1] == 'biological_process':
		T = 'GO_Process_id'
	if x[1] == 'molecular_function':
		T = 'GO_Function_id'
	if x[1] == 'cellular_component':
		T = 'GO_Component_id'
	if T != '':
		print ('select mid from xref.U133 where ' + T + ' like \'%' + x[0] +'%\'')
		ids = [y[0] for y in doQuery('select mid from xref.U133 where ' + T + ' like \'%' + x[0] +'%\'')]
		for a in ids:
			db.query('INSERT INTO xref.U133_GO(GOID, GOTYPE, MEMBER) VALUES (\'' + x[0] + '\',\'' + x[1] + '\',\'' + a + '\')')
		print x[0] + '\t' + repr(ids)


usedGOS = doQuery('select GOID, COUNT(*) c from xref.U133_GO where GOTYPE = \'biological_process \' GROUP BY GOID')

