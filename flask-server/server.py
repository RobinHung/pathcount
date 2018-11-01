from flask import Flask
import psycopg2
import os

app = Flask(__name__)

# Catch all requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    POSTGRES = {
        'user': os.environ['POSTGRES_USER'],
        'pw': os.environ['POSTGRES_PASSWORD'],
        'db': os.environ['POSTGRES_DATABASE'],
        'host': os.environ['POSTGRES_HOST'],
        'port': os.environ['POSTGRES_PORT'],
    }

    try:
        conn = psycopg2.connect("dbname=%(db)s user=%(user)s password=%(pw)s host=%(host)s port=%(port)s" % POSTGRES)
        # conn = psycopg2.connect("dbname='postgres' user='postgres' host='172.20.0.2' password='password'")
    except:
        print("Can't connect to database!")

    curr = conn.cursor()
    curr.execute("INSERT INTO pathcount (path, count) VALUES (%s, 1) ON CONFLICT (path) DO UPDATE SET count = pathcount.count + 1 RETURNING count;", (path,))
    conn.commit()

    curr.execute("SELECT path, count from pathcount ORDER BY path ASC;")
    rows = curr.fetchall()

    pathcount_result = ''
    for row in rows:
        pathcount_result += 'Path "/' + str(row[0]) + '": ' + str(row[1]) + '\n'

    return pathcount_result
