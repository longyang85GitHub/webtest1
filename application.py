import pandas as pd
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import os
import numpy as np
import pandas as pd
import xlsxwriter
import datetime
import math
##
# NLP app
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired, Email
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import en_core_web_sm
nlp = en_core_web_sm.load()
# Build a List of Stopwords
stopwords = list(STOP_WORDS)


def text_summarizer(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency
  #  word.text is tokenization in spacy
    word_frequencies = {}  
    for word in docx:  
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Calculate Sentence Score and Ranking
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Find N Largest
    summary_sentences = nlargest(6, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w.text for w in summary_sentences ]
    summary = ' '.join(final_sentences)
    #print("Original Document\n")
    #print(raw_docx)
    #print("Total Length:",len(raw_docx))
    #print('\n\nSummarized Document\n')
    #print(summary)
    #print("Total Length:",len(summary))
    return summary
def create_text_analytics_table(text_string):
    text = []
    ORG =[]
    Date =[]
    EVENT=[]
    Money=[]
    GPE=[]
    doc = nlp(text_string)
    for ent in doc.ents:
        if ent.label_=="ORG":
            text.append(ent.text)
            ORG.append(ent.label_)
            Date.append("")
            EVENT.append("")
            Money.append("")
            GPE.append("")
        elif ent.label_=="DATE":
            text.append(ent.text)
            Date.append(ent.label_)
            ORG.append("")
            EVENT.append("")
            Money.append("")
            GPE.append("")
        elif ent.label_=="EVENT":
            text.append(ent.text)
            EVENT.append(ent.label_)
            Date.append("")
            ORG.append("")
            Money.append("")
            GPE.append("")
        elif ent.label_=="MONEY":
            text.append(ent.text)
            Money.append(ent.label_)
            Date.append("")
            ORG.append("")
            EVENT.append("")
            GPE.append("")
        elif ent.label_=="GPE":
            text.append(ent.text)
            Money.append("")
            Date.append("")
            ORG.append("")
            EVENT.append("")
            GPE.append(ent.label_)
    narr = np.array([text,ORG,Date,EVENT,Money,GPE],dtype = object)
    narr_t = np.transpose(narr)
    df = pd.DataFrame(narr_t,columns=['Text','lable:ORG','lable:Date','lable:Event','lable:Money','lable:GPE'])
    return df

##=======================================================
app = Flask(__name__)
class ReusableForm(Form):
    Document = TextField('Document:',validators=[validators.required()])

@app.route('/', methods=("POST", "GET"))
def nlptest():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        Document=request.form['Document']
        a=len(Document)
        if a == 0:
            Document="Please input text"
            summary=text_summarizer(Document)
            nlpcsv=create_text_analytics_table(Document)
            #print(csv)
            b=len(summary)
        else:
            summary=text_summarizer(Document)
            nlpcsv=create_text_analytics_table(Document)
            #print(csv)
            b=len(summary)
    #return "You entered: {}".format(text)
    else:
        a="0"
        b="0"
        Document="Please input text"
        summary="Please input text"
        data = [{'Text': "", 'lable:ORG': "", 'lable:Date':"", 'lable:Event':"", 'lable:Money':"", 'lable:GPE':""}] 
        nlpcsv = pd.DataFrame(data) 
    return render_template('home.html',form=form,summary=summary,a=a,b=b,nlpcsv=nlpcsv)
##
if __name__ == '__main__':
    app.run(debug=True)