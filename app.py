from flask import Flask, render_template, request, redirect, url_for
from textblob import TextBlob
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form", methods=['POST', 'GET'])
def form():
    if request.method == "POST":
        url = request.form['nm']
        data = ur.urlopen(url).read()
        soup_url= BeautifulSoup(data,'lxml')
        li = []
        for i in soup_url.find("div", {"class":"story-body__inner"}).findAll('p'):
            li.append(i.string)
        lis = list(filter(None,li))
        sr = ''
        for i in lis:
          sr = sr + ' ' + i

        sia = SentimentIntensityAnalyzer()
        user = sia.polarity_scores(sr)['compound']

        return render_template("form.html", score = user)
    else:
        return render_template("form.html")


if __name__ == "__main__":
    app.run(debug = True)
