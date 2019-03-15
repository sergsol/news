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

DEFAULTS = {'publication': 'cnn',
            'city': 'London,UK'}


@app.route("/", methods=['GET', 'POST'])
def home():
    publication = request.form.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.form.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("index.html", articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    publication = feedparser.parse(RSS_FEEDS[publication])
    return publication['entries']

def get_weather(city):
    API_KEY = '2ed83ec7593c5df3c352a7c0870e699d'
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city, API_KEY)
    response = requests.get(api_url).json()
    print(response['sys']['country'])
    return response






if __name__ == "__main__":
    app.run(port=5000, debug=True)
