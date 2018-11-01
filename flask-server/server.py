from flask import Flask
import psycopg2

app = Flask(__name__)

# Catch all requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='172.20.0.2' password='password'")
    except:
        print("Can't connect to database!")

    curr = conn.cursor()
    curr.execute("INSERT INTO pathcount (path, count) VALUES (%s, 1) ON CONFLICT (path) DO UPDATE SET count = pathcount.count + 1 RETURNING count;", (path,))
    conn.commit()

    curr.execute("SELECT path, count from pathcount ORDER BY path ASC;")
    rows = curr.fetchall()
    print("\nShow me the databases:\n")

    pathcount_result = ''
    for row in rows:
        pathcount_result += 'Path "/' + str(row[0]) + '": ' + str(row[1]) + '\n'

    return pathcount_result
