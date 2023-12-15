import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from indicators import patterns
import plotly.graph_objects as go
import plotly.express as px
import requests
import os
import sys
import subprocess

# check if the library folder already exists, to avoid building everytime you load the pahe
if not os.path.isdir("/tmp/ta-lib"):

    # Download ta-lib to disk
    with open("/tmp/ta-lib-0.4.0-src.tar.gz", "wb") as file:
        response = requests.get(
            "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        )
        file.write(response.content)
    # get our current dir, to configure it back again. Just house keeping
    default_cwd = os.getcwd()
    os.chdir("/tmp")
    # untar
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    os.system("ls -la /app/equity/")
    # build
    os.system("./configure --prefix=/home/appuser")
    os.system("make")
    # install
    os.system("make install")
    # back to the cwd
    os.chdir(default_cwd)
    sys.stdout.flush()

# add the library to our current environment
from ctypes import *

lib = CDLL("/home/appuser/lib/libta_lib.so.0.0.0")
# import library
try:
    import talib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--global-option=build_ext", "--global-option=-L/home/appuser/lib/", "--global-option=-I/home/appuser/include/", "ta-lib"])
finally:
    import talib

option = st.sidebar.selectbox('Select Dashboard:', ('Technical', 'Social', 'Derivatives'))

st.header(option)

if option == 'Technical':
    st.subheader('Technical Dashboard logic')
    pattern =  st.sidebar.selectbox('Select Pattern:', patterns)

    #get crypto data
    btc = yf.download("BTC-USD", period='1y', end=None)
    eth = yf.download("ETH-USD", period='1y', end=None)
    bnb = yf.download("BNB-USD", period='1y', end=None)
    xrp = yf.download("XRP-USD", period='1y', end=None)
    sol = yf.download("SOL-USD", period='1y', end=None)
    ada = yf.download("ADA-USD", period='1y', end=None)
    dot = yf.download("DOT-USD", period='1y', end=None)
    avax = yf.download("AVAX-USD", period='1y', end=None)
    doge = yf.download("DOGE-USD", period='1y', end=None)
    tron = yf.download("TRX-USD", period='1y', end=None)
    matic = yf.download("MATIC-USD", period='1y', end=None)

    symbol = st.sidebar.text_input('Enter Symbol:' + "-USD", value='BTC-USD', max_chars=None, key=None, type='default')
    data = yf.download(symbol + '-USD', period='1y', end=None)

    #add momentum indicators to data 

    data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
    data['ADX'] = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=14)
    data['ADXR'] = talib.ADXR(data['High'], data['Low'], data['Close'], timeperiod=14)
    data['APO'] = talib.APO(data['Close'], fastperiod=12, slowperiod=26, matype=0)
    data['AROONOSC'] = talib.AROONOSC(data['High'], data['Low'], timeperiod=14)
    data['BOP'] = talib.BOP(data['Open'], data['High'], data['Low'], data['Close'])
    data['CCI'] = talib.CCI(data['High'], data['Low'], data['Close'], timeperiod=14)
    data['CMO'] = talib.CMO(data['Close'], timeperiod=14)
    data['DX'] = talib.DX(data['High'], data['Low'], data['Close'], timeperiod=14)
    data['MACD'], data['MACDsignal'], data['MACDhist'] = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    data['MFI'] = talib.MFI(data['High'], data['Low'], data['Close'], data['Volume'], timeperiod=14)
    data['MINUS_DI'] = talib.MINUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)
    data['MINUS_DM'] = talib.MINUS_DM(data['High'], data['Low'], timeperiod=14)
    data['MOM'] = talib.MOM(data['Close'], timeperiod=10)
    data['PLUS_DI'] = talib.PLUS_DI(data['High'], data['Low'], data['Close'], timeperiod=14)
    data['PLUS_DM'] = talib.PLUS_DM(data['High'], data['Low'], timeperiod=14)
    data['PPO'] = talib.PPO(data['Close'], fastperiod=12, slowperiod=26, matype=0)
    data['ROC'] = talib.ROC(data['Close'], timeperiod=10)
    data['ROCP'] = talib.ROCP(data['Close'], timeperiod=10)
    data['TRIX'] = talib.TRIX(data['Close'], timeperiod=30)
    data['ULTOSC'] = talib.ULTOSC(data['High'], data['Low'], data['Close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
    data['WILLR'] = talib.WILLR(data['High'], data['Low'], data['Close'], timeperiod=14)
    
    #add patterns to data

    data['Two Crows'] = talib.CDL2CROWS(data['Open'], data['High'], data['Low'], data['Close'])
    data['Three Black Crows'] = talib.CDL3BLACKCROWS(data['Open'], data['High'], data['Low'], data['Close'])
    data['Three Inside Up/Down'] = talib.CDL3INSIDE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Three-Line Strike'] = talib.CDL3LINESTRIKE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Three Outside Up/Down'] = talib.CDL3OUTSIDE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Three Stars In The South'] = talib.CDL3STARSINSOUTH(data['Open'], data['High'], data['Low'], data['Close'])
    data['Three Advancing White Soldiers'] = talib.CDL3WHITESOLDIERS(data['Open'], data['High'], data['Low'], data['Close'])
    data['Abandoned Baby'] = talib.CDLABANDONEDBABY(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
    data['Advance Block'] = talib.CDLADVANCEBLOCK(data['Open'], data['High'], data['Low'], data['Close'])
    data['Belt-hold'] = talib.CDLBELTHOLD(data['Open'], data['High'], data['Low'], data['Close'])
    data['Breakaway'] = talib.CDLBREAKAWAY(data['Open'], data['High'], data['Low'], data['Close'])
    data['Closing Marubozu'] = talib.CDLCLOSINGMARUBOZU(data['Open'], data['High'], data['Low'], data['Close'])
    data['Concealing Baby Swallow'] = talib.CDLCONCEALBABYSWALL(data['Open'], data['High'], data['Low'], data['Close'])
    data['Counterattack'] = talib.CDLCOUNTERATTACK(data['Open'], data['High'], data['Low'], data['Close'])
    data['Dark Cloud Cover'] = talib.CDLDARKCLOUDCOVER(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
    data['Doji'] = talib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
    data['Doji Star'] = talib.CDLDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'])
    data['Engulfing Pattern'] = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
    data['Evening Doji Star'] = talib.CDLEVENINGDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
    data['Evening Star'] = talib.CDLEVENINGSTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
    data['Gap Side-by-Side White Lines'] = talib.CDLGAPSIDESIDEWHITE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Gravestone Doji'] = talib.CDLGRAVESTONEDOJI(data['Open'], data['High'], data['Low'], data['Close'])
    data['Hammer'] = talib.CDLHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
    data['Hanging Man'] = talib.CDLHANGINGMAN(data['Open'], data['High'], data['Low'], data['Close'])
    data['Harami Pattern'] = talib.CDLHARAMI(data['Open'], data['High'], data['Low'], data['Close'])
    data['Harami Cross Pattern'] = talib.CDLHARAMICROSS(data['Open'], data['High'], data['Low'], data['Close'])
    data['High-Wave Candle'] = talib.CDLHIGHWAVE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Hikkake Pattern'] = talib.CDLHIKKAKE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Modified Hikkake Pattern'] = talib.CDLHIKKAKEMOD(data['Open'], data['High'], data['Low'], data['Close'])
    data['Homing Pigeon'] = talib.CDLHOMINGPIGEON(data['Open'], data['High'], data['Low'], data['Close'])
    data['Identical Three Crows'] = talib.CDLIDENTICAL3CROWS(data['Open'], data['High'], data['Low'], data['Close'])
    data['In-Neck Pattern'] = talib.CDLINNECK(data['Open'], data['High'], data['Low'], data['Close'])
    data['Inverted Hammer'] = talib.CDLINVERTEDHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
    data['Kicking'] = talib.CDLKICKING(data['Open'], data['High'], data['Low'], data['Close'])
    data['Kicking - Bull/Bear'] = talib.CDLKICKINGBYLENGTH(data['Open'], data['High'], data['Low'], data['Close'])
    data['Ladder Bottom'] = talib.CDLLADDERBOTTOM(data['Open'], data['High'], data['Low'], data['Close'])
    data['Long Legged Doji'] = talib.CDLLONGLEGGEDDOJI(data['Open'], data['High'], data['Low'], data['Close'])
    data['Long Line Candle'] = talib.CDLLONGLINE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Marubozu'] = talib.CDLMARUBOZU(data['Open'], data['High'], data['Low'], data['Close'])
    data['Matching Low'] = talib.CDLMATCHINGLOW(data['Open'], data['High'], data['Low'], data['Close'])
    data['Mat Hold'] = talib.CDLMATHOLD(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
    data['Morning Doji Star'] = talib.CDLMORNINGDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
    data['Morning Star'] = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'], penetration=0)
    data['On-Neck Pattern'] = talib.CDLONNECK(data['Open'], data['High'], data['Low'], data['Close'])
    data['Piercing Pattern'] = talib.CDLPIERCING(data['Open'], data['High'], data['Low'], data['Close'])
    data['Rickshaw Man'] = talib.CDLRICKSHAWMAN(data['Open'], data['High'], data['Low'], data['Close'])
    data['Rising/Falling Three Methods'] = talib.CDLRISEFALL3METHODS(data['Open'], data['High'], data['Low'], data['Close'])
    data['Separating Lines'] = talib.CDLSEPARATINGLINES(data['Open'], data['High'], data['Low'], data['Close'])
    data['Shooting Star'] = talib.CDLSHOOTINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
    data['Short Line Candle'] = talib.CDLSHORTLINE(data['Open'], data['High'], data['Low'], data['Close'])
    data['Spinning Top'] = talib.CDLSPINNINGTOP(data['Open'], data['High'], data['Low'], data['Close'])
    data['Stalled Pattern'] = talib.CDLSTALLEDPATTERN(data['Open'], data['High'], data['Low'], data['Close'])
    data['Stick Sandwich'] = talib.CDLSTICKSANDWICH(data['Open'], data['High'], data['Low'], data['Close'])
    data['Takuri'] = talib.CDLTAKURI(data['Open'], data['High'], data['Low'], data['Close'])
    data['Tasuki Gap'] = talib.CDLTASUKIGAP(data['Open'], data['High'], data['Low'], data['Close'])
    data['Thrusting Pattern'] = talib.CDLTHRUSTING(data['Open'], data['High'], data['Low'], data['Close'])
    data['Tristar Pattern'] = talib.CDLTRISTAR(data['Open'], data['High'], data['Low'], data['Close'])
    data['Unique 3 River'] = talib.CDLUNIQUE3RIVER(data['Open'], data['High'], data['Low'], data['Close'])
    data['Upside Gap Two Crows'] = talib.CDLXSIDEGAP3METHODS(data['Open'], data['High'], data['Low'], data['Close'])
    data['Upside/Downside Gap Three Methods'] = talib.CDLXSIDEGAP3METHODS(data['Open'], data['High'], data['Low'], data['Close'])

    #convert to dataframe
    btc_df = pd.DataFrame(btc)
    eth_df = pd.DataFrame(eth)
    bnb_df = pd.DataFrame(bnb)
    xrp_df = pd.DataFrame(xrp)
    sol_df = pd.DataFrame(sol)
    ada_df = pd.DataFrame(ada)
    dot_df = pd.DataFrame(dot)
    avax_df = pd.DataFrame(avax)
    doge_df = pd.DataFrame(doge)
    tron_df = pd.DataFrame(tron)
    matic_df = pd.DataFrame(matic)
    
    #bitcoin momentum indicators
    data_df = pd.DataFrame(data)
    btc_mom_df = []
    btc_mom_df = data_df['RSI']
    btc_mom_df = pd.merge(btc_mom_df, data_df['ADX'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['ADXR'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['APO'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['AROONOSC'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['BOP'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['CCI'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['CMO'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['DX'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['MACD'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['MACDsignal'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['MACDhist'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['MFI'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['MINUS_DI'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['MINUS_DM'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['MOM'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['PLUS_DI'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['PLUS_DM'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['PPO'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['ROC'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['ROCP'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['TRIX'], on='Date')
    btc_mom_df = pd.merge(btc_mom_df, data_df['ULTOSC'], on='Date')
    

    #clear blank rows
    btc_mom_df = btc_mom_df.dropna()

    #normalize to 1
    btc_mom_df['RSI'] = btc_mom_df['RSI']/btc_mom_df['RSI'].max()
    btc_mom_df['ADX'] = btc_mom_df['ADX']/btc_mom_df['ADX'].max()
    btc_mom_df['ADXR'] = btc_mom_df['ADXR']/btc_mom_df['ADXR'].max()
    btc_mom_df['APO'] = btc_mom_df['APO']/btc_mom_df['APO'].max()
    btc_mom_df['AROONOSC'] = btc_mom_df['AROONOSC']/btc_mom_df['AROONOSC'].max()
    btc_mom_df['BOP'] = btc_mom_df['BOP']/btc_mom_df['BOP'].max()
    btc_mom_df['CCI'] = btc_mom_df['CCI']/btc_mom_df['CCI'].max()
    btc_mom_df['CMO'] = btc_mom_df['CMO']/btc_mom_df['CMO'].max()
    btc_mom_df['DX'] = btc_mom_df['DX']/btc_mom_df['DX'].max()
    btc_mom_df['MACD'] = btc_mom_df['MACD']/btc_mom_df['MACD'].max()
    btc_mom_df['MACDsignal'] = btc_mom_df['MACDsignal']/btc_mom_df['MACDsignal'].max()
    btc_mom_df['MACDhist'] = btc_mom_df['MACDhist']/btc_mom_df['MACDhist'].max()
    btc_mom_df['MFI'] = btc_mom_df['MFI']/btc_mom_df['MFI'].max()
    btc_mom_df['MINUS_DI'] = btc_mom_df['MINUS_DI']/btc_mom_df['MINUS_DI'].max()
    btc_mom_df['MINUS_DM'] = btc_mom_df['MINUS_DM']/btc_mom_df['MINUS_DM'].max()
    btc_mom_df['MOM'] = btc_mom_df['MOM']/btc_mom_df['MOM'].max()
    btc_mom_df['PLUS_DI'] = btc_mom_df['PLUS_DI']/btc_mom_df['PLUS_DI'].max()
    btc_mom_df['PLUS_DM'] = btc_mom_df['PLUS_DM']/btc_mom_df['PLUS_DM'].max()
    btc_mom_df['PPO'] = btc_mom_df['PPO']/btc_mom_df['PPO'].max()
    btc_mom_df['ROC'] = btc_mom_df['ROC']/btc_mom_df['ROC'].max()
    btc_mom_df['ROCP'] = btc_mom_df['ROCP']/btc_mom_df['ROCP'].max()
    btc_mom_df['TRIX'] = btc_mom_df['TRIX']/btc_mom_df['TRIX'].max()
    btc_mom_df['ULTOSC'] = btc_mom_df['ULTOSC']/btc_mom_df['ULTOSC'].max()
    
    
    btc_mom_df = btc_mom_df.dropna()
    btc_mom_df['Total'] = btc_mom_df.sum(axis=1)
    btc_mom_df['Total'] = btc_mom_df['Total']/btc_mom_df['Total'].max()
    st.write(btc_mom_df)

    fig = px.imshow(btc_mom_df, color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True, size=1000)

# pattern dataframe
    pattern_df = []
    pattern_df = data_df['Two Crows']
    pattern_df = pd.merge(pattern_df, data_df['Three Black Crows'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Three Inside Up/Down'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Three-Line Strike'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Three Outside Up/Down'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Three Stars In The South'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Three Advancing White Soldiers'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Abandoned Baby'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Advance Block'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Belt-hold'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Breakaway'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Closing Marubozu'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Concealing Baby Swallow'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Counterattack'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Dark Cloud Cover'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Doji'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Doji Star'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Engulfing Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Evening Doji Star'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Evening Star'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Gap Side-by-Side White Lines'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Gravestone Doji'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Hammer'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Hanging Man'], on=['Date'])
    pattern_df = pd.merge(pattern_df, data_df['Harami Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Harami Cross Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['High-Wave Candle'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Hikkake Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Modified Hikkake Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Homing Pigeon'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Identical Three Crows'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['In-Neck Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Inverted Hammer'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Kicking'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Kicking - Bull/Bear'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Ladder Bottom'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Long Legged Doji'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Long Line Candle'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Marubozu'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Matching Low'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Mat Hold'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Morning Doji Star'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Morning Star'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['On-Neck Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Piercing Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Rickshaw Man'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Rising/Falling Three Methods'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Separating Lines'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Shooting Star'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Short Line Candle'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Spinning Top'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Stalled Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Stick Sandwich'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Takuri'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Tasuki Gap'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Thrusting Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Tristar Pattern'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Unique 3 River'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Upside Gap Two Crows'], on='Date')
    pattern_df = pd.merge(pattern_df, data_df['Upside/Downside Gap Three Methods'], on='Date')

#days since pattern

st.write("Most recent patterns (last 7 days")
last = pattern_df[-1:]
triggered_bullish = last.columns[(last.eq(100)).any()]
triggered_bearish = last.columns[(last.eq(-100)).any()]

st.dataframe(triggered_bullish[0:], width=500)
st.dataframe(triggered_bearish[0:], width=500)

st.write("Yesterday's Patterns (T-1)")
last = pattern_df[-2:]
triggered_bullish = last.columns[(last.eq(100)).any()]
triggered_bearish = last.columns[(last.eq(-100)).any()]

st.dataframe(triggered_bullish[0:], width=500)
st.dataframe(triggered_bearish[0:], width=500)

st.write("(T-2)")
last = pattern_df[-3:]
triggered_bullish = last.columns[(last.eq(100)).any()]
triggered_bearish = last.columns[(last.eq(-100)).any()]

st.dataframe(triggered_bullish[0:], width=500)
st.dataframe(triggered_bearish[0:], width=500)

st.write("(T-3)")
last = pattern_df[-4:]
triggered_bullish = last.columns[(last.eq(100)).any()]
triggered_bearish = last.columns[(last.eq(-100)).any()]

st.dataframe(triggered_bullish[0:], width=500)
st.dataframe(triggered_bearish[0:], width=500)

st.write("(T-4)")
last = pattern_df[-5:]
triggered_bullish = last.columns[(last.eq(100)).any()]
triggered_bearish = last.columns[(last.eq(-100)).any()]

st.dataframe(triggered_bullish[0:], width=500)
st.dataframe(triggered_bearish[0:], width=500)

st.write("(T-5)")
last = pattern_df[-6:]
triggered_bullish = last.columns[(last.eq(100)).any()]
triggered_bearish = last.columns[(last.eq(-100)).any()]

st.dataframe(triggered_bullish[0:], width=500)
st.dataframe(triggered_bearish[0:], width=500)

st.write("(T-6)")
last = pattern_df[-7:]
triggered_bullish = last.columns[(last.eq(100)).any()]
triggered_bearish = last.columns[(last.eq(-100)).any()]

st.dataframe(triggered_bullish[0:], width=500)
st.dataframe(triggered_bearish[0:], width=500)


if option == 'Social':
    st.subheader('Social Dashboard logic')

if option == 'Derivatives':
    st.subheader('Derivatives Dashboard logic')


#loop through csv files for price data
#def index():
#    pattern = request.arg.get('pattern', None) #get pattern from url
#    if pattern:
#        datafiles = os.listdir('datasets/daily')
#        for dataset in datafiles:
#            pd.read_csv('datasets/daily/{}'.format(filename))
#            print (df)
#            pattern_function = getattr(talib, pattern)
#            try:
#               result = talib.pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
#               last = result.tail(1).values[0]
#               print(last)
#               if last =! 0:
#               print("{} triggered {}".format(filename, pattern))
#            except:
#               pass
#    return render_template('index.html', patterns=patterns)    


# select a symbol symbol = st.sidebar.text_input('Enter Symbol:', value='BTC-USD', max_chars=None, key=None, type='default')
# create a candlestick chart in plotly     fig = go.Figure(data=[go.Candlestick(x=data.index,
#                    open=data['Open'],
#                   high=data['High'],
#                    low=data['Low'],
#                    close=data['Close'],
#                    name=symbol)])
#   fig.update_xaxes(type='category')
#    fig.update_layout(height=1000)

#   st.plotly_chart(fig, use_container_width=True)
#    st.write(data)
