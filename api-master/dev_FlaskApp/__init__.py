#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from flaskext.mysql import MySQL

import json


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''
mysql.init_app(app)


@app.route("/")
def hello():
    return "yeah ... no"


@app.route("/metrics", methods=['GET', 'POST'])
def beepeeker():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        content = request.get_json(silent=True)
        print(content)
	mysql_field = []
	mysql_input = []
        for line, payload in content.items():
	    temp1 = payload["temp1"]
            humidity1 = float(payload["humidity1"])
            broodtemp1 = float(payload["broodtemp1"])
            photocell1 = payload["photocell1"]
            pir1 = payload["pir1"]
            weight = float(payload["weight"])
            datetime = payload["datetime"]
            device_id = payload["device_id"]
            account_id = payload["account_id"]
	    cursor.execute("INSERT INTO temperatures (temp1, humidity1, broodtemp1, photocell1, pir1, datetime, weight, device_id, account_id, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())", (temp1, humidity1, broodtemp1, photocell1, pir1, datetime, weight, device_id, account_id))
        conn.commit()
        conn.close()
        return "POST request completed."
    elif request.method == 'GET':
        cursor.execute("select temp1, humidity1, broodtemp1, photocell1, pir1, weight, datetime, CONVERT_TZ(updated_at,'+00:00','-05:00'), device_id, account_id from temperatures")
        data = cursor.fetchall()
        conn.close()
        return render_template('db.html', data=data)
    else:
        return "Access denied"
        conn.close()
    conn.close()

if __name__ == "__main__":
    app.run()
