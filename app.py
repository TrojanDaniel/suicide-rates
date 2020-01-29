from flask import Flask, render_template
from flask import redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def basic():
    response = requests.get(url='https://web-project-59451.firebaseio.com/suicide-statistics.json')
    # response.json() is a list
    return render_template("table.html", data=response.json())

@app.route('/description')
def description():
    return render_template("description.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/filterOnNum/<attribute>/<start>/<end>')
def filterOnNum(attribute: str, start: str, end: str):
    response = requests.get(url='https://web-project-59451.firebaseio.com/suicide-statistics.json?orderBy="' + attribute + '"&startAt=' + start + '&endAt=' + end)
    # an example url is
    # 'https://web-project-59451.firebaseio.com/suicide-statistics.json?orderBy="year"&startAt=2009&endAt=2010'
   
    # response.json() is a dict
    return render_template("table.html", data=response.json().values())

@app.route('/filterOnCountry/<country>')
def filterOnCountry(country: str):
    print("2333")
    print(country)
    print(type(country))
    response = requests.get(url='https://web-project-59451.firebaseio.com/index-country/' + country + '.json')
    # an example url is
    # 'https://web-project-59451.firebaseio.com/index-country/France.json'
   
    data = requests.get(url='https://web-project-59451.firebaseio.com/suicide-statistics.json').json()
    # response.json() is a list of int
    # data is a list of dict
    
    res = [data[i] for i in response.json()]

    return render_template("table.html", data=res)



@app.route('/sort/<attribute>/<reverse>')
def sort(attribute: str, reverse: str):
    data = requests.get(url='https://web-project-59451.firebaseio.com/suicide-statistics.json').json()

    # data is a list of dict
    data.sort(key=lambda entry: entry[attribute], reverse=(reverse == 'True'))
    return render_template("table.html", data=data)


if __name__ == '__main__':
    app.run()
