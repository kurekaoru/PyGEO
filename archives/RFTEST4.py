#RFTEST
from kfuncs import *
from sklearn.ensemble import RandomForestClassifier
from sqlutils import *
import _mysql
from Test4 import *

db=_mysql.connect("localhost","kaoru","rbdWK2uk")
db.query('CREATE DATABASE IF NOT EXISTS randomForest')
db.query('CREATE TABLE IF NOT EXISTS randomForest.genes (id INT(10) PRIMARY KEY auto_increment, gene VARCHAR(100) NOT NULL, ntrees INT(10) NOT NULL, score FLOAT NOT NULL, dataset INT(10) NOT NULL, step INT(5) NOT NULL)')

def SQL_insertObesrvation(gene,score,NTREES,dataset, step):
	db.query('INSERT INTO randomForest.genes(gene, score, ntrees, dataset, step) VALUES(\''+gene+'\','+str(score)+','+str(NTREES)+','+str(dataset)+','+str(step)+')')


def SQL_translateList(IDS):
	return doQuery('SELECT Gene_title FROM xref.U133 WHERE mid IN (\"'+'\",\"'.join(IDS)+'\")')

a = doQuery('SELECT c,AV FROM randomForest.TEMP1')

MT_pso = ob2moses(T_pso)
labels = MT_pso[:,0][1:].astype(float).astype(int)
data = MT_pso[:,1:][1:].astype(float)

##################################

dataset = 3539
NTREES = 500

#c=686
c=723

feats = MT_pso[0][1:]

for x in range(77):
	from decimal import Decimal
	model = RandomForestClassifier(
		bootstrap=True, 
		compute_importances=True,
		criterion='gini',
		max_depth=None,
		max_features='auto',
		min_density=0.1,
		min_samples_leaf=1,
		min_samples_split=1,
		n_estimators=NTREES, 
		n_jobs=-1,		# -1 to use all CPUs
		oob_score=True,
		verbose=0)
	model.fit(data, labels)
	O = zip(feats,model.feature_importances_)
	for x in O:
		if x[1] > 0:
			SQL_insertObesrvation(x[0],round(Decimal(x[1]),10),NTREES, dataset, c)
	c+=1
	print c



