for btc in [btc, eth, bnb, xrp, sol, ada, dot, avax, doge, tron, matic]:
    pattern_function = getattr(talib, patterns[pattern])
    try:
        result = talib.pattern_function(btc['Open'], btc['High'], btc['Low'], btc['Close'])
        last = result.tail(1).values[0]
        print(last)
        if last != 0:
            st.write("{} triggered {}".format(btc, pattern))
    except:
        pass

for eth in [btc, eth, bnb, xrp, sol, ada, dot, avax, doge, tron, matic]:
    pattern_function = getattr(talib, patterns[pattern])
    try:
        result = talib.pattern_function(eth['Open'], eth['High'], eth['Low'], eth['Close'])
        last = result.tail(1).values[0]
        print(last)
        if last != 0:
            st.write("{} triggered {}".format(btc, pattern))
    except:
        pass


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

RSI_df = []
    RSI_df['Bitcoin'] = talib.RSI(btc['Close'], timeperiod=14)
    RSI_df['Ethereum'] = talib.RSI(eth['Close'], timeperiod=14)
    RSI_df['BNB'] = talib.RSI(bnb['Close'], timeperiod=14)
    RSI_df['XRP'] = talib.RSI(xrp['Close'], timeperiod=14)
    RSI_df['Solana'] = talib.RSI(sol['Close'], timeperiod=14)  
    RSI_df['Cardano'] = talib.RSI(ada['Close'], timeperiod=14)
    RSI_df['Polkadot'] = talib.RSI(dot['Close'], timeperiod=14)
    RSI_df['Avalanche'] = talib.RSI(avax['Close'], timeperiod=14)
    RSI_df['Dogecoin'] = talib.RSI(doge['Close'], timeperiod=14)
    RSI_df['Tron'] = talib.RSI(tron['Close'], timeperiod=14)
    RSI_list['Polygon'] = talib.RSI(matic['Close'], timeperiod=14)