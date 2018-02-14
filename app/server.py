from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pyhs2

f = open('hs2conn')
(hostn,portn,username,password) = f.read().splitlines()

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/dashboard")
def dashboard():
    with pyhs2.connect(host=hostn, port=int(portn), authMechanism="PLAIN", user=username, password=password, database="default") as conn:
        with conn.cursor() as cur:
            cur.execute("select count(*) From errors.averages_errors")
            alert_count = cur.fetchone()[0]
            cur.execute("select * from errors.averages_errors order by violation_time desc limit 25")
            alert_data = cur.fetchall()
    return render_template('dashboard.html', recent_alert_count = len(alert_data), alerts_count = alert_count, alert_data = alert_data)

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port=5000)

