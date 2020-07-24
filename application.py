import datetime
import sqlite3
from uuid import uuid4
import utiliy
from flask import Flask, request, g, jsonify, render_template
import pandas as pd

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=()):
    cur = get_db().cursor()
    cur.execute(query, args)

    rv = cur.fetchall()  # Retrive all rows
    cur.close()
    return rv
    # return (rv[0] if rv else None) if one else rv


def update_db(query, args=(), one=False):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()
    conn.close()
    return "DB updated"


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")  # take note of this decorator syntax, it's a common pattern
def home():
    return "API is up and running..."


@app.route('/update_case', methods=['GET', 'POST'])
def raise_case():
    country = request.args.get('country')
    confirmed_no = request.args.get('confirmed_no')
    icu_no = request.args.get('icu_no')
    death_no = request.args.get('death_no')

    time_stamp = str(datetime.datetime.now())
    # case_id = int(time.mktime(rpt_time.timetuple()))

    tmp_list = [country, confirmed_no, icu_no, death_no, time_stamp]

    update_db("INSERT INTO TB_CASE (COUNTRY, CONFIRMED_NO, ICU_NO, DEATH_NO, TIME_STAMP) VALUES (?,?,?,?,?);",
              tmp_list)

    return "Cases updated with time stamp as " + time_stamp


@app.route('/query_case', methods=['GET', 'POST'])
def search_case():
    search_country = request.args.get('country')

    tmp_list = [search_country]

    rows = query_db("SELECT * from TB_CASE WHERE COUNTRY = ?", tmp_list)

    return jsonify(rows)


@app.route('/init', methods=['GET', 'POST'])
def init_db():
    sql_create_table = """ CREATE TABLE IF NOT EXISTS TB_QUESTION (
                                          Q_NO text NOT NULL,
                                          TOPIC text NOT NULL,
                                          DIFFICULTY integer NOT NULL,
                                          QUESTION text NOT NULL,
                                          CHOICE text,
                                          ANSWER integer NOT NULL, 
                                          REMARK text,
                                          TIME_STAMP text NOT NULL
                                      ); """

    update_db(sql_create_table)
    return "DB created!"


@app.route('/load_excel', methods=['GET', 'POST'])
def load_excel_to_db():
    time_stamp = str(datetime.datetime.now())

    df = utiliy.load_excel()

    df.to_sql(name='TB_QUESTION_1', con=get_db())

    # for index, row in df.iterrows():
    #     tmp_list = [row['Q_NO'], row['TOPIC'], row['DIFFICULTY'], row['QUESTION'], row['CHOICE'], row['ANSWER'],
    #                 row['REMARK'], time_stamp]
    #
    #     update_db(
    #         "INSERT INTO TB_QUESTION (Q_NO, TOPIC, DIFFICULTY, QUESTION, CHOICE, ANSWER, REMARK, TIME_STAMP) VALUES (?,?,?,?,?,?,?,?);",
    #         tmp_list)


@app.route('/display_questions', methods=['GET', 'POST'])
def display_questions():

    # df = pd.read_sql_table(table_name='TB_QUESTION_1', con=get_db())
    rows = query_db("SELECT * from TB_QUESTION_1")

    return render_template('question_display.html', result=rows)


if __name__ == '__main__':
    DATABASE = "./db/demo.db"

    # Generate a globally unique address for this node
    node_identifier = str(uuid4()).replace('-', '')

    print(node_identifier)
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port, debug=True)
