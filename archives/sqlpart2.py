#RFTEST
from kfuncs import *
from sqlutils import *
import _mysql
from numpy import *
from pylab import *
#from Test4 import *
ion()

db=_mysql.connect("localhost","kaoru","rbdWK2uk")

#scores = array(doQuery('SELECT score FROM randomForest.genes')).astype(float)
#hist(log(scores),1000)

def genR300(LIMIT):
	db.query('DROP TABLE IF EXISTS randomForest.R300;')
	print 'DROP TABLE OK'
	db.query('CREATE TABLE randomForest.R300 SELECT gene, dataset, count(gene) c FROM randomForest.genes WHERE dataset = 2822 GROUP BY randomForest.genes.gene ORDER BY c DESC LIMIT '+str(LIMIT)+';')
	#db.query('INSERT INTO randomForest.R300 SELECT gene, dataset, count(gene) c FROM randomForest.genes WHERE dataset = 2154 GROUP BY randomForest.genes.gene ORDER BY c DESC LIMIT '+str(LIMIT)+';')
	db.query('INSERT INTO randomForest.R300 SELECT gene, dataset, count(gene) c FROM randomForest.genes WHERE dataset = 3119 GROUP BY randomForest.genes.gene ORDER BY c DESC LIMIT '+str(LIMIT)+';')
	db.query('INSERT INTO randomForest.R300 SELECT gene, dataset, count(gene) c FROM randomForest.genes WHERE dataset = 3539 GROUP BY randomForest.genes.gene ORDER BY c DESC LIMIT '+str(LIMIT)+';')
	#db.query('INSERT INTO randomForest.R300 SELECT gene, dataset, count(gene) c FROM randomForest.genes WHERE dataset = 3580 GROUP BY randomForest.genes.gene ORDER BY c DESC LIMIT '+str(LIMIT)+';')
	print 'CREATE TABLE OK'
	db.query('alter table randomForest.R300 add name LONGTEXT;')
	db.query('alter table randomForest.R300 add AV float;')
	print 'ALTER TABLE OK'
	db.query('update randomForest.R300 set name = (select distinct(xref.U133.Gene_symbol) from xref.U133 where xref.U133.mid = randomForest.R300.gene);')
	print 'CROSS REFERENCE GENENAME OK'
	db.query('update randomForest.R300 set AV = (select avg(score) from randomForest.genes where randomForest.genes.gene = randomForest.R300.gene);')
	print 'CALCULATE MEAN OK'
	print 'FINISHED'

genR300(200)



a = array(doQuery('SELECT c,AV FROM randomForest.R300')).astype(float)
scatter(a[:,0],log(a[:,1]),c='red')
scatter(a[:,0],log(a[:,2]),c='blue')
scatter(a[:,0],log(a[:,3]),c='green')

create table randomForest.RES select gene, dataset, count(gene) c from randomForest.genes group by randomForest.genes.dataset, randomForest.genes.gene order by c desc limit 200;

select *, count(*) c from genes where dataset = 2154 group by gene order by c desc limit 100;
select *, count(*) c from genes where dataset = 2822 group by gene order by c desc limit 100;
select *, count(*) c from genes where dataset = 3119 group by gene order by c desc limit 100;
select *, count(*) c from genes where dataset = 3539 group by gene order by c desc limit 100;
select *, count(*) c from genes where dataset = 3580 group by gene order by c desc limit 100;
