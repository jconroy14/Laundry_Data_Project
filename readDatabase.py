import psycopg2
import os

DATABASE_URL = 'postgres://xjmgzqbovystmz:b59b93d8d13c724a530425e1e74b603b8ce3f7a2e56c98caa0156e7c7f5ca97e@ec2-107-22-221-60.compute-1.amazonaws.com:5432/djo19060qdtmp'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# Commands to uncomment: create table, add sample data, delete sample data, and view data
# cur.execute("CREATE TABLE dataTable (theTime integer, washers integer, dryers integer);")
# cur.execute("INSERT INTO dataTable (theTime, washers, dryers) VALUES (%s, %s, %s)",(100, 1,5))
# cur.execute("DELETE FROM dataTables;")
cur.execute("SELECT * FROM dataTable;")
print(cur.fetchall())

conn.commit()
cur.close()
conn.close()
