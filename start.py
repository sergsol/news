from flask import Flask, render_template
import feedparser


app = Flask(__name__)
BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
feeds = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
         'cnn': 'http://rss.cnn.com/rss/edition.rss',
         'fox': 'http://feeds.foxnews.com/foxnews/latest',
         'IOL': 'http://www.iol.co.za/cmlink/1.640'}

@app.route("/")
@app.route("/bbc")
def bbc():
    # return render_template('index.html')
    return get_news('bbc')

@app.route("/cnn")
def cnn():
    return get_news('cnn')

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(feeds[publication])
    first_article = feed['entries'][0]
    return """
    <body>
    <h1> Headlines </h1>
    <b>{}</b>
    <br>
    <i>{}</i>
    <p>{}</p>
    </body>
    """.format(first_article.get('title'),
               first_article.get('published'),
               first_article.get('summary'),
               )


if __name__=="__main__":
    app.run(debug=True)