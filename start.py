from flask import Flask, render_template
import feedparser


app = Flask(__name__)

feeds = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
         'cnn': 'http://rss.cnn.com/rss/edition.rss',
         'fox': 'http://feeds.foxnews.com/foxnews/latest',}


@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(feeds[publication])
    return render_template('index.html',
                           articles=feed['entries'])


if __name__=="__main__":
    app.run(debug=True)