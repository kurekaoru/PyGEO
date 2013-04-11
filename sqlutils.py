import _mysql

db=_mysql.connect("localhost","kaoru","rbdWK2uk")

def doQuery(query):
	db.query(query)
	r=db.store_result()
	return r.fetch_row(0)
