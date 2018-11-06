from flask import Flask, render_template
import feedparser


app = Flask(__name__)
BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"


@app.route('/')
def get_news():
    return "OK"


if __name__=="__main__":
    app.run(debug=True)