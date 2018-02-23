from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests
import json
from datetime import datetime

f = open('druidconn')
(hostn,portn,path,queryurl) = f.read().splitlines()

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/dashboard")
def dashboard():
    headers = {'Content-Type': 'application/json'}

    averages_query_file = open('../druid/queries/averages_list_past_hour.json', 'r')
    averages_query_one_hour = averages_query_file.read()
    averages_query_file.close()

    averages_query_one_hour = averages_query_one_hour.replace('<<now>>', datetime.now().isoformat())
    r = requests.post(queryurl, headers=headers, data=averages_query_one_hour)
    one_hour_data = json.loads(r.content)

    day_query_count_file = open('../druid/queries/count_average_errors_past_day.json', 'r')
    day_query_count = day_query_count_file.read()
    day_query_count_file.close()

    day_query_count = day_query_count.replace('<<now>>', datetime.now().isoformat())
    r = requests.post(queryurl, headers=headers, data=day_query_count)
    past_day_count = json.loads(r.content)[0]['result'][0]['count']

    alert_data = []
    recent_count = len(one_hour_data[0]['result']['events'])
    for event in one_hour_data[0]['result']['events']:
        alert_row = []
        event_json = event['event']
        alert_row.append(event_json['timestamp'])
        alert_row.append(event_json['part_type'])
        alert_row.append(event_json['violation_type'])
        alert_row.append(event_json['threshold'])
        alert_row.append(event_json['average_val'])
        alert_data.append(alert_row)
    return render_template('dashboard.html', recent_alert_count = recent_count, alerts_count = past_day_count, alert_data = alert_data)

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port=5000)

