from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #com2

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")



@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})



@app.route('/commits/')
def commit_graph():
    
    url = "https://api.github.com/repos/NaderMR/5MCSI_Metriques/commits"
    response = urlopen(url, context=context)
    data = json.loads(response.read())

    commits = [{'date': commit['commit']['author']['date'], 'message': commit['commit']['message']} for commit in data]

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Commit Graph</title>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {'packages':['corechart']});
            google.charts.setOnLoadCallback(drawChart);

            function drawChart() {
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Date');
                data.addColumn('number', 'Commits');

                data.addRows({{ commit_data }});

                var options = {
                    title: 'Commits Over Time',
                    curveType: 'function',
                    legend: { position: 'bottom' }
                };

                var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

                chart.draw(data, options);
            }
        </script>
    </head>
    <body>
        <div id="curve_chart" style="width: 900px; height: 500px"></div>
    </body>
    </html>
    """.replace("{{ commit_data }}", str([list(item.values()) for item in commits]))

    return render_template_string(html)

  


if __name__ == "__main__":
  app.run(debug=True)
