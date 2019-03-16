import sqlite3 
from datetime import datetime, timedelta
from flask import Flask, g, jsonify

DATABASE = '../crowdcounting.db'
app = Flask(__name__)

def make_dicts(cursor, row):
  return dict((cursor.description[idx][0], value)
               for idx, value in enumerate(row))

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
  return db

# This makes working with the db a lot more pleasant that
# just using the raw cursor
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
  return 'Server Works!'
  
@app.route('/greet')
def say_hello():
  return 'Hello from Server'

@app.route('/count_vendor')
def requests():
  query = open('../sql_queries/count_by_vendor.sql').read()
  return jsonify(query_db(query))

@app.route('/last_registers/days/<days>')
def registers_last_days(days):
  query = open('../sql_queries/registers_x_last_minutes.sql').read()
  days_before = int(days)
  t1 = (datetime.now() - timedelta(days=days_before)).isoformat()
  t2 = datetime.now().isoformat()
  time_delta = (t1, t2,)
  return jsonify(query_db(query, time_delta))

@app.route('/last_registers/minutes/<minutes>')
def registers_last_minutes(minutes):
  query = open('../sql_queries/registers_x_last_minutes.sql').read()
  minutes_before = int(minutes)
  t1 = (datetime.now() - timedelta(minutes=minutes_before)).isoformat()
  t2 = datetime.now().isoformat()
  time_delta = (t1, t2,)
  return jsonify(query_db(query, time_delta))

@app.route('/total_probes')
def total_probes():
  query = open('../sql_queries/total_probes.sql').read()
  return jsonify(query_db(query))

@app.route('/unique_macs_vendor')
def unique_adress_vendor():
  query = open('../sql_queries/unique_addr_vendor_count.sql').read()
  return jsonify(query_db(query))

@app.route('/unique_macs')
def unique_adress():
  query = open('../sql_queries/unique_macaddr.sql').read()
  return jsonify(query_db(query))