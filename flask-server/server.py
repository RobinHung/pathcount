from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@171.20.0.2:5432/pathcount'
# db = SQLAlchemy(app)

# def connect_to_DB():
#     connectionString = 'dbname=pg-db user=postgres password=password host=172.20.0.2'
#     try:
#         psycopg2.connect("dbname='postgres' user='postgres' host='172.20.0.2' password='password'")
#     except:
#         print("Can't connect to database")

# if db is None:
#     @app.route('/')
#     def index():
#         return "DB not found!"
# else:
#     class URLPath(db.Model):
#         __tablename__ = "url_path_count"
#         url_path = db.Column('url_path', db.String())
#         path_count = db.Column('path_count', db.Integer)
#
#     # @app.route('/'):
#
#
#     @app.route('<path>'):
#     def queryDB(path):
#         # Exists
#         if URLPath.query.filterby(url_path = path) != None:
#             URLPath.path_count += 1
#         # Not Exists, Create new row!
#         else:



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

    curr.execute("SELECT path, count from pathcount ORDER BY count DESC;")
    rows = curr.fetchall()
    print("\nShow me the databases:\n")

    pathcount_result = ''
    for row in rows:
        pathcount_result += 'Path "/' + str(row[0]) + '": ' + str(row[1]) + '\n'

    return pathcount_result
