import psycopg2.extras

def connect():
	connection = 'dbname=tesnames user=tes password=tes host=localhost'
	try:
		return psycopg2.connect(connection)
	except:
		print("Cannot connect to database")
		raise
