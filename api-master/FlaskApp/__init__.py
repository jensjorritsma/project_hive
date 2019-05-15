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
        temp1 = float(content.get("temp1"))
        humidity1 = float(content.get("humidity1"))
        broodtemp1 = float(content.get("broodtemp1"))
        #broodtemp2 = float(content.get("broodtemp2"))
        photocell1 = content.get("photocell1")
        pir1 = content.get("pir1")
        weight = float(content.get("weight"))
        datetime = content.get("datetime")
        device_id = content.get("device_id")
        account_id = content.get("account_id")
        cursor.execute("INSERT INTO temperatures (temp1, humidity1, broodtemp1, photocell1, pir1, datetime, weight, device_id, account_id, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())", (temp1, humidity1, broodtemp1, photocell1, pir1, datetime, weight, device_id, account_id))
        #cursor.execute("INSERT INTO temperatures (temp1, humidity1, broodtemp1, broodtemp2, datetime, weight, device_id, account_id, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())", (temp1, humidity1, broodtemp1, broodtemp2, datetime, weight, device_id, account_id))
        conn.commit()
        conn.close()
        return "POST request completed."
    elif request.method == 'GET':
        cursor.execute("select temp1, humidity1, broodtemp1, photocell1, pir1, weight, datetime, CONVERT_TZ(updated_at,'+00:00','-05:00'), device_id, account_id from temperatures")
        #cursor.execute("select temp1, humidity1, broodtemp1, broodtemp2, weight, datetime, updated_at, device_id, account_id from temperatures")
        data = cursor.fetchall()
        conn.close()
        return render_template('db.html', data=data)
    else:
        return "Access denied"
        conn.close()
    conn.close()


@app.route("/dev_metrics", methods=['GET', 'POST'])
def dev_beepeeker():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        content = request.get_json(silent=True)
        print(content)
        temp1 = float(content.get("temp1"))
        humidity1 = float(content.get("humidity1"))
        broodtemp1 = float(content.get("broodtemp1"))
        #broodtemp2 = float(content.get("broodtemp2"))
        photocell1 = content.get("photocell1")
        pir1 = content.get("pir1")
        weight = float(content.get("weight"))
        datetime = content.get("datetime")
        device_id = content.get("device_id")
        account_id = content.get("account_id")
        cursor.execute("INSERT INTO dev_temperatures (temp1, humidity1, broodtemp1, photocell1, pir1, datetime, weight, device_id, account_id, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())", (temp1, humidity1, broodtemp1, photocell1, pir1, datetime, weight, device_id, account_id))
        #cursor.execute("INSERT INTO temperatures (temp1, humidity1, broodtemp1, broodtemp2, datetime, weight, device_id, account_id, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())", (temp1, humidity1, broodtemp1, broodtemp2, datetime, weight, device_id, account_id))
        conn.commit()
        conn.close()
        return "POST request completed."
    elif request.method == 'GET':
        cursor.execute("select temp1, humidity1, broodtemp1, photocell1, pir1, weight, datetime, CONVERT_TZ(updated_at,'+00:00','-05:00'), device_id, account_id from dev_temperatures")
        #cursor.execute("select temp1, humidity1, broodtemp1, broodtemp2, weight, datetime, updated_at, device_id, account_id from temperatures")
        data = cursor.fetchall()
        conn.close()
        return render_template('db.html', data=data)
    else:
        return "Access denied"
        conn.close()
    conn.close()


if __name__ == "__main__":
    app.run()
