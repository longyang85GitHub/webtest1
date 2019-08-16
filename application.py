import pandas as pd
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import os
import numpy as np
import pandas as pd
import xlsxwriter
import datetime
import math
now = datetime.datetime.now()
Citi_US = pd.read_excel('IBRD_Benchmarks data/Citi_IBRD USD and Euro 28022018.xlsx',skiprows=[0],sheet_name="USD")
Deutsche_US = pd.read_excel('IBRD_Benchmarks data/Deutsche_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="USD")
MorganStanley_US = pd.read_excel('IBRD_Benchmarks data/MorganStanley_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="USD")
JPMorgan_US = pd.read_excel('IBRD_Benchmarks data/JPMorgan_IBRD USD and Euro_Feb.xlsx',skiprows=[0],sheet_name="USD")
a=Citi_US [Citi_US ['Maturity (years)']=='3m US$ Libor All-in (bps)']
a=a.replace('3m US$ Libor All-in (bps)', 'Citi')
b=Deutsche_US[Deutsche_US['Maturity (years)']=='3m US$ Libor All-in (bps)']
b=b.replace('3m US$ Libor All-in (bps)', 'Deutsche')
c=MorganStanley_US[MorganStanley_US['Maturity (years)']=='3m US$ Libor All-in (bps)']
c=c.replace('3m US$ Libor All-in (bps)', 'MorganStanley')
d=JPMorgan_US[JPMorgan_US['Maturity (years)']=='3m US$ Libor All-in (bps)']
d=d.replace('3m US$ Libor All-in (bps)', 'JPMorgan')
a.columns = map(str.lower, a.columns)
b.columns = map(str.lower, b.columns)
c.columns = map(str.lower, c.columns)
d.columns = map(str.lower, d.columns)
US_3m_Libot_result = pd.concat([a,b,c,d], ignore_index=True)
US_3m_Libot_result.loc['Average'] = US_3m_Libot_result.mean()
US_3m_Libot_result.loc['Average', 'maturity (years)'] = 'Average'
US_3m_Libot_result=US_3m_Libot_result.round(2) 
##==================================================================================================
a=Citi_US[Citi_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
a=a.replace('6m US$ Libor All-in (bps)', 'Citi')
b=Deutsche_US[Deutsche_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
b=b.replace('6m US$ Libor All-in (bps)', 'Deutsche')
c=MorganStanley_US[MorganStanley_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
c=c.replace('6m US$ Libor All-in (bps)', 'MorganStanley')
d=JPMorgan_US[JPMorgan_US['Maturity (years)']=='6m US$ Libor All-in (bps)']
d=d.replace('6m US$ Libor All-in (bps)', 'JPMorgan')
a.columns = map(str.lower, a.columns)
b.columns = map(str.lower, b.columns)
c.columns = map(str.lower, c.columns)
d.columns = map(str.lower, d.columns)
US_6m_Libot_result = pd.concat([a,b,c,d], ignore_index=True)
US_6m_Libot_result.loc['Average'] = US_6m_Libot_result.mean()
US_6m_Libot_result.loc['Average', 'maturity (years)'] = 'Average'
US_6m_Libot_result=US_6m_Libot_result.round(2) 
#=========================================================================================================
Deutsche_EURO = pd.read_excel('IBRD_Benchmarks data/Deutsche_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="EURO")
MorganStanley_EURO = pd.read_excel('IBRD_Benchmarks data/MorganStanley_IBRD USD and Euro.xlsx',skiprows=[0],sheet_name="EURO")
GS_EURO = pd.read_excel('IBRD_Benchmarks data/GS_IBRD Euro.xlsx',skiprows=[0],sheet_name="EURO")
a=Deutsche_EURO[Deutsche_EURO['Maturity (years)']=='3m US$ Libor All-in (bps)']
a=a.replace('3m US$ Libor All-in (bps)', 'Deutsche')

b=MorganStanley_EURO[MorganStanley_EURO['Maturity (years)']=='3m US$ Libor All-in (bps)']
b=b.replace('3m US$ Libor All-in (bps)', 'MorganStanley')

c=GS_EURO[GS_EURO['Maturity (years)']=='3m US$ Libor All-in (bps)']
c=c.replace('3m US$ Libor All-in (bps)', 'GS')

a.columns = map(str.lower, a.columns)
b.columns = map(str.lower, b.columns)
c.columns = map(str.lower, c.columns)
EURO_US_3m_Libot_result = pd.concat([a,b,c], ignore_index=True)
EURO_US_3m_Libot_result.loc['Average'] = EURO_US_3m_Libot_result.mean()
#=========================================================================================================
a=Deutsche_EURO[Deutsche_EURO['Maturity (years)']=='3m EURIBOR All-in (bps)']
a=a.replace('3m EURIBOR All-in (bps)', 'Deutsche')

b=MorganStanley_EURO[MorganStanley_EURO['Maturity (years)']=='3m EURIBOR All-in (bps)']
b=b.replace('3m EURIBOR All-in (bps)', 'MorganStanley')

c=GS_EURO[GS_EURO['Maturity (years)']=='3m EURIBOR All-in (bps)']
c=c.replace('3m EURIBOR All-in (bps)', 'GS')

a.columns = map(str.lower, a.columns)
b.columns = map(str.lower, b.columns)
c.columns = map(str.lower, c.columns)

EURO_US_3m_Euribor_result = pd.concat([a,b,c], ignore_index=True)
EURO_US_3m_Euribor_result.loc['Average'] = EURO_US_3m_Euribor_result.mean()

#=================================================
a=Deutsche_EURO[Deutsche_EURO['Maturity (years)']=='6m EURIBOR All-in (bps)']
a=a.replace('6m EURIBOR All-in (bps)', 'Deutsche')

b=MorganStanley_EURO[MorganStanley_EURO['Maturity (years)']=='6m EURIBOR All-in (bps)']
b=b.replace('6m EURIBOR All-in (bps)', 'MorganStanley')

c=GS_EURO[GS_EURO['Maturity (years)']=='6m EURIBOR All-in (bps)']
c=c.replace('6m EURIBOR All-in (bps)', 'GS')

a.columns = map(str.lower, a.columns)
b.columns = map(str.lower, b.columns)
c.columns = map(str.lower, c.columns)

EURO_US_6m_Euribor_result = pd.concat([a,b,c], ignore_index=True)
EURO_US_6m_Euribor_result.loc['Average'] = EURO_US_6m_Euribor_result.mean()
##===========================================================
Daiwa_JPY = pd.read_excel('IBRD_Benchmarks data/Daiwa_IBRD JPY levels.xls',skiprows=[0])
Nomura_JPY = pd.read_excel('IBRD_Benchmarks data/Nomura_IBRD JPY levels - February 2018.xls',skiprows=[0])
Nomura_JPY=Nomura_JPY.loc[:, ~Nomura_JPY.columns.str.contains('^Unnamed')]


a=Daiwa_JPY[Daiwa_JPY['Maturity (years)']=='3m US$ Libor All-in (bps)']
a=a.replace('3m US$ Libor All-in (bps)', 'Daiwa')

b=Nomura_JPY[Nomura_JPY['Maturity (years)']=='3m US$ Libor All-in (bps)']
b=b.replace('3m US$ Libor All-in (bps)', 'Nomura')

a.columns = map(str.lower, a.columns)
b.columns = map(str.lower, b.columns)

JPY_US_3m_Libor_result = pd.concat([a,b], ignore_index=True)
JPY_US_3m_Libor_result.loc['Average'] = JPY_US_3m_Libor_result.mean()
#============================================================================
a=Daiwa_JPY[Daiwa_JPY['Maturity (years)']=='6m JPY Libor All-in (bps)']
a=a.replace('6m JPY Libor All-in (bps)', 'Daiwa')

b=Nomura_JPY[Nomura_JPY['Maturity (years)']=='6m JPY Libor All-in (bps)']
b=b.replace('6m JPY Libor All-in (bps)', 'Nomura')

a.columns = map(str.lower, a.columns)
b.columns = map(str.lower, b.columns)

JPY_6m_JPY_Libor_result = pd.concat([a,b], ignore_index=True)
JPY_6m_JPY_Libor_result.loc['Average'] = JPY_6m_JPY_Libor_result.mean()
##================================================================================

##=======================================================
app = Flask(__name__)
#index/home
@app.route('/')
def index():
    return render_template('home.html',csv=US_3m_Libot_result,csv1=US_6m_Libot_result)
@app.route('/IBRD_Benchmarks', methods=("POST", "GET"))
def IBRD_Benchmarks():
    return render_template('IBRD_Benchmarks.html',csv=US_3m_Libot_result,total_rows=len(US_3m_Libot_result.axes[0]),total_cols=len(US_3m_Libot_result.axes[1]))
##
if __name__ == '__main__':
    app.run(debug=True)