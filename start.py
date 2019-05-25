from flask import Flask
from flask import render_template
from flask import request
import feedparser
import requests
import json
import urllib.request
import urllib.parse


app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://RSS_FEEDS.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://RSS_FEEDS.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

RATES = 'https://openexchangerates.org/api/latest.json?app_id=24ea695da8fc45148ea0d8d6ec60ec8f'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2ed83ec7593c5df3c352a7c0870e699d'
DEFAULTS = {'publication': 'cnn',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'UAH'}


@app.route("/", methods=['GET', 'POST'])
def home():
    publication = request.form.get('publication')
    city = request.form.get('city')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.form.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    currency_from = request.form.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.form.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rete, currencies = get_rates(currency_from, currency_to)
    return render_template("index.html", articles=articles, weather=weather, rates=rete,
                           currency_from=currency_from, currency_to=currency_to, currensies=currencies)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    publication = feedparser.parse(RSS_FEEDS[publication])
    return publication['entries']


def get_weather(city):
    response = requests.get(WEATHER_URL.format(city)).json()
    weather = {
                'description': response['weather'][0]['description'],
                'temperature': response['main']['temp'],
                'country': response['sys']['country'],
                'city': response['name']
                }
    return weather


def get_rates(frm, to):
    rates = requests.get(RATES).json()
    frm_rate = rates['rates'][frm.upper()]
    to_rate = rates['rates'][to.upper()]
    return to_rate/frm_rate, rates['rates'].keys()








if __name__ == "__main__":
    app.run(port=5001, debug=True)
