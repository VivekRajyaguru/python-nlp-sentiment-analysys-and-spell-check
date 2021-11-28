from logging import debug
from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from textblob import TextBlob, Word
import random
import time
import nltk

nltk.download('punkt')

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/checkspell', methods=["POST"])
def checkspell():
  if request.method == 'POST':
    start=time.time()
    rawText=request.form['rawText']
    blob = TextBlob(rawText)
    recieved_text = blob
    fixed_text = blob.correct()
    correct_flag = False
    if recieved_text == fixed_text:
      correct_flag = True
    end = time.time()
    final_time = time.time()
  
  return render_template('index.html', correct_flag=correct_flag, final_time=final_time, recieved_text=recieved_text, fixed_text=fixed_text)

@app.route('/analyze', methods=["POST"])
def analyze():
  start=time.time()
  print('Methods ', request.method)
  if request.method=='POST':
    rawText=request.form['rawText']
    blob = TextBlob(rawText)
    recieved_text = blob
    blob_sentiment, blob_subjectivity = blob.sentiment.polarity, blob.sentiment.subjectivity
    number_of_token = len(list(blob.words))
    nouns = []
    summary = list()
    final_time = None
    len_of_words = []
    for word, tag in blob.tags:
      if tag == 'NN':
        nouns.append(word.lemmatize())
        len_of_words = len(nouns)
        random_words = random.sample(nouns, len(nouns))
        final_word = list()
        for item in random_words:
          word = Word(item).pluralize()
          final_word.append(word)
          summary = final_word
    
    if blob_sentiment < 0:
      final_answer = 'Negative Comment'
    elif blob_sentiment == 0:
      final_answer = 'Neutral'
    else:
      final_answer = 'positive'
        
    end_time = time.time()
    final_time = end_time - start
  
  return render_template('index.html', recieved_text=recieved_text, number_of_token=number_of_token, blob_sentiment=blob_sentiment, blob_subjectivity=blob_subjectivity, summary=summary, final_time=final_time, len_of_words=len_of_words, final_answer=final_answer)


if __name__=='__main__':
  app.run(debug=True)