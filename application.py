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

##
# now = datetime.datetime.now()
# Citi_US = pd.read_excel('IBRD_Benchmarks data/Citi_IBRD USD and Euro 28022018.xlsx',skiprows=[0],sheet_name="USD")
# Deutsche_US = pd.read_excel('IBRD_Benchmarks data/Deutsche_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="USD")
# MorganStanley_US = pd.read_excel('IBRD_Benchmarks data/MorganStanley_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="USD")
# JPMorgan_US = pd.read_excel('IBRD_Benchmarks data/JPMorgan_IBRD USD and Euro_Feb.xlsx',skiprows=[0],sheet_name="USD")
# a=Citi_US [Citi_US ['Maturity (years)']=='3m US$ Libor All-in (bps)']
# a=a.replace('3m US$ Libor All-in (bps)', 'Citi')
# b=Deutsche_US[Deutsche_US['Maturity (years)']=='3m US$ Libor All-in (bps)']
# b=b.replace('3m US$ Libor All-in (bps)', 'Deutsche')
# c=MorganStanley_US[MorganStanley_US['Maturity (years)']=='3m US$ Libor All-in (bps)']
# c=c.replace('3m US$ Libor All-in (bps)', 'MorganStanley')
# d=JPMorgan_US[JPMorgan_US['Maturity (years)']=='3m US$ Libor All-in (bps)']
# d=d.replace('3m US$ Libor All-in (bps)', 'JPMorgan')
# a.columns = map(str.lower, a.columns)
# b.columns = map(str.lower, b.columns)
# c.columns = map(str.lower, c.columns)
# d.columns = map(str.lower, d.columns)
# US_3m_Libot_result = pd.concat([a,b,c,d], ignore_index=True)
# US_3m_Libot_result.loc['Average'] = US_3m_Libot_result.mean()
# US_3m_Libot_result.loc['Average', 'maturity (years)'] = 'Average'
# US_3m_Libot_result=US_3m_Libot_result.round(2) 
# ##==================================================================================================
# a=Citi_US[Citi_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
# a=a.replace('6m US$ Libor All-in (bps)', 'Citi')
# b=Deutsche_US[Deutsche_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
# b=b.replace('6m US$ Libor All-in (bps)', 'Deutsche')
# c=MorganStanley_US[MorganStanley_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
# c=c.replace('6m US$ Libor All-in (bps)', 'MorganStanley')
# d=JPMorgan_US[JPMorgan_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
# d=d.replace('6m US$ Libor All-in (bps)', 'JPMorgan')
# a.columns = map(str.lower, a.columns)
# b.columns = map(str.lower, b.columns)
# c.columns = map(str.lower, c.columns)
# d.columns = map(str.lower, d.columns)
# US_6m_Libot_result = pd.concat([a,b,c,d], ignore_index=True)
# US_6m_Libot_result.loc['Average'] = US_6m_Libot_result.mean()
# US_6m_Libot_result.loc['Average', 'maturity (years)'] = 'Average'
# US_6m_Libot_result=US_6m_Libot_result.round(2) 
# #=========================================================================================================
# Deutsche_EURO = pd.read_excel('IBRD_Benchmarks data/Deutsche_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="EURO")
# MorganStanley_EURO = pd.read_excel('IBRD_Benchmarks data/MorganStanley_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="EURO")
# GS_EURO = pd.read_excel('IBRD_Benchmarks data/GS_IBRD Euro.xlsx',skiprows=[0],sheet_name="EURO")
# a=Deutsche_EURO[Deutsche_EURO['Maturity (years)']=='3m US$ Libor All-in (bps)']
# a=a.replace('3m US$ Libor All-in (bps)', 'Deutsche')

# b=MorganStanley_EURO[MorganStanley_EURO['Maturity (years)']=='3m US$ Libor All-in (bps)']
# b=b.replace('3m US$ Libor All-in (bps)', 'MorganStanley')

# c=GS_EURO[GS_EURO['Maturity (years)']=='3m US$ Libor All-in (bps)']
# c=c.replace('3m US$ Libor All-in (bps)', 'GS')

# a.columns = map(str.lower, a.columns)
# b.columns = map(str.lower, b.columns)
# c.columns = map(str.lower, c.columns)
# EURO_US_3m_Libot_result = pd.concat([a,b,c], ignore_index=True)
# EURO_US_3m_Libot_result.loc['Average'] = EURO_US_3m_Libot_result.mean()
# #=========================================================================================================
# a=Deutsche_EURO[Deutsche_EURO['Maturity (years)']=='3m EURIBOR All-in (bps)']
# a=a.replace('3m EURIBOR All-in (bps)', 'Deutsche')

# b=MorganStanley_EURO[MorganStanley_EURO['Maturity (years)']=='3m EURIBOR All-in (bps)']
# b=b.replace('3m EURIBOR All-in (bps)', 'MorganStanley')

# c=GS_EURO[GS_EURO['Maturity (years)']=='3m EURIBOR All-in (bps)']
# c=c.replace('3m EURIBOR All-in (bps)', 'GS')

# a.columns = map(str.lower, a.columns)
# b.columns = map(str.lower, b.columns)
# c.columns = map(str.lower, c.columns)

# EURO_US_3m_Euribor_result = pd.concat([a,b,c], ignore_index=True)
# EURO_US_3m_Euribor_result.loc['Average'] = EURO_US_3m_Euribor_result.mean()

# #=================================================
# a=Deutsche_EURO[Deutsche_EURO['Maturity (years)']=='6m EURIBOR All-in (bps)']
# a=a.replace('6m EURIBOR All-in (bps)', 'Deutsche')

# b=MorganStanley_EURO[MorganStanley_EURO['Maturity (years)']=='6m EURIBOR All-in (bps)']
# b=b.replace('6m EURIBOR All-in (bps)', 'MorganStanley')

# c=GS_EURO[GS_EURO['Maturity (years)']=='6m EURIBOR All-in (bps)']
# c=c.replace('6m EURIBOR All-in (bps)', 'GS')

# a.columns = map(str.lower, a.columns)
# b.columns = map(str.lower, b.columns)
# c.columns = map(str.lower, c.columns)

# EURO_US_6m_Euribor_result = pd.concat([a,b,c], ignore_index=True)
# EURO_US_6m_Euribor_result.loc['Average'] = EURO_US_6m_Euribor_result.mean()
# ##===========================================================
# Daiwa_JPY = pd.read_excel('IBRD_Benchmarks data/Daiwa_IBRD JPY levels.xls',skiprows=[0])
# Nomura_JPY = pd.read_excel('IBRD_Benchmarks data/Nomura_IBRD JPY levels - February 2018.xls',skiprows=[0])
# Nomura_JPY=Nomura_JPY.loc[:, ~Nomura_JPY.columns.str.contains('^Unnamed')]


# a=Daiwa_JPY[Daiwa_JPY['Maturity (years)']=='3m US$ Libor All-in (bps)']
# a=a.replace('3m US$ Libor All-in (bps)', 'Daiwa')

# b=Nomura_JPY[Nomura_JPY['Maturity (years)']=='3m US$ Libor All-in (bps)']
# b=b.replace('3m US$ Libor All-in (bps)', 'Nomura')

# a.columns = map(str.lower, a.columns)
# b.columns = map(str.lower, b.columns)

# JPY_US_3m_Libor_result = pd.concat([a,b], ignore_index=True)
# JPY_US_3m_Libor_result.loc['Average'] = JPY_US_3m_Libor_result.mean()
# #============================================================================
# a=Daiwa_JPY[Daiwa_JPY['Maturity (years)']=='6m JPY Libor All-in (bps)']
# a=a.replace('6m JPY Libor All-in (bps)', 'Daiwa')

# b=Nomura_JPY[Nomura_JPY['Maturity (years)']=='6m JPY Libor All-in (bps)']
# b=b.replace('6m JPY Libor All-in (bps)', 'Nomura')

# a.columns = map(str.lower, a.columns)
# b.columns = map(str.lower, b.columns)

# JPY_6m_JPY_Libor_result = pd.concat([a,b], ignore_index=True)
# JPY_6m_JPY_Libor_result.loc['Average'] = JPY_6m_JPY_Libor_result.mean()
# ##================================================================================

##=======================================================
app = Flask(__name__)
class ReusableForm(Form):
    Document = TextField('Document:',validators=[validators.required()])
#index/home
#@app.route('/home', methods=("POST", "GET"))
#def index():
#    return render_template('home.html',csv=US_3m_Libot_result,csv1=US_6m_Libot_result)

#@app.route('/IBRD_Benchmarks', methods=("POST", "GET"))
#def IBRD_Benchmarks():
#    return render_template('IBRD_Benchmarks.html',csv=US_3m_Libot_result,total_rows=len(US_3m_Libot_result.axes[0]),total_cols=len(US_3m_Libot_result.axes[1]))

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
    return render_template('nlp.html',form=form,summary=summary,a=a,b=b,nlpcsv=nlpcsv)
##
if __name__ == '__main__':
    app.run(debug=True)