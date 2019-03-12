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


@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather(location='London,UK')
    return render_template("index.html", articles=feed['entries'], weather=weather)


def get_weather(location="Kyiv"):
    API_KEY = '2ed83ec7593c5df3c352a7c0870e699d'
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(location, API_KEY)
    response = requests.get(api_url).json()
    print(response)
    return response

get_weather()


if __name__ == "__main__":
    app.run(port=5000, debug=True)
