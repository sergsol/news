from flask import Flask
from flask import render_template
from flask import request
import feedparser
import requests
import datetime
from flask import make_response


app = Flask(__name__)


RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/world/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

RATES = 'https://openexchangerates.org/api/latest.json?app_id=24ea695da8fc45148ea0d8d6ec60ec8f'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2ed83ec7593c5df3c352a7c0870e699d'
DEFAULTS = {'publication': 'cnn',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'UAH'}


@app.route("/", methods=['GET', 'POST'])
def home():
    publication = get_input_cookie('publication')
    if not publication:
            publication = DEFAULTS['publication']
    articles, company = get_news(publication)
    city = get_input_cookie('city')
    if not city:
        city = DEFAULTS['city']
    if get_weather(city):
        weather = get_weather(city)
    else:
        weather = None
    currency_from = get_input_cookie('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = get_input_cookie('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rete, currencies = get_rates(currency_from, currency_to)
    response = make_response(render_template("index.html", articles=articles, weather=weather, rates=rete,
                           currency_from=currency_from, currency_to=currency_to, currensies=currencies, feeds=RSS_FEEDS,
                           company=company))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    if weather:
        response.set_cookie("city", city, expires=expires)
    response.set_cookie("company", company, expires=expires)
    response.set_cookie("publication", publication, expires=expires)
    return response


def get_input_cookie(key):
    if request.form.get(key):
        return request.form.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)


def get_news(query):
    publication = query.lower()
    publication = feedparser.parse(RSS_FEEDS[publication])
    return publication['entries'], query.lower()


def get_weather(city):
    response = requests.get(WEATHER_URL.format(city)).json()
    try:
        weather = {
                'description': response['weather'][0]['description'],
                'temperature': response['main']['temp'],
                'country': response['sys']['country'],
                'city': response['name']
                }
    except KeyError:
        return False
    else:
        return weather


def get_rates(frm, to):
    rates = requests.get(RATES).json()
    frm_rate = rates['rates'][frm.upper()]
    to_rate = rates['rates'][to.upper()]
    return round(to_rate/frm_rate, 2), rates['rates'].keys()


if __name__ == "__main__":
    app.run(port=5001, debug=True)
