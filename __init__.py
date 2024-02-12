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
@app.route("/commits/")
def mescommits():
import requests
url = "https://api.github.com/repos/NaderMR/5MCSI_Metriques/commits"
response = requests.get(url)
commits = response.json()
from collections import defaultdict
from datetime import datetime
# Organiser les commits par date
commits_per_day = defaultdict(int)
for commit in commits:
    date_str = commit['commit']['committer']['date']
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').date()
    commits_per_day[date] += 1
import matplotlib.pyplot as plt

# Dates et nombres de commits
dates = list(commits_per_day.keys())
commit_counts = [commits_per_day[date] for date in dates]

# Créer le graphique
plt.figure(figsize=(10, 6))
plt.plot(dates, commit_counts, marker='o')
plt.title('Commits par Jour')
plt.xlabel('Date')
plt.ylabel('Nombre de Commits')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
return 0




if __name__ == "__main__":
  app.run(debug=True)
