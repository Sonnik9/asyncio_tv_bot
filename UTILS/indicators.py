import talib

def calculate_adx(data, period=14):
    adx = None
    try:
        adx = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=period)
        adx = adx.to_numpy()[-1]
    except Exception as ex:
        print(f"34 indicatorss:___{ex}")
    return adx

def calculate_sma(data, period=20):
    sma = None
    num_std = 2
    try:
        _, sma, _ = talib.BBANDS(data['Close'], timeperiod=period, nbdevup=num_std, nbdevdn=num_std)
        sma = sma.to_numpy()[-1]
    except Exception as ex:
        print(ex)
    return sma

def calculate_bollinger_bands(data, period=20, num_std=2):
    upper_band, _, lower_band = None, None, None
    try:
        upper_band, _, lower_band = talib.BBANDS(data['Close'], timeperiod=period, nbdevup=num_std, nbdevdn=num_std)
        upper_band = upper_band.to_numpy()[-1]
        lower_band = lower_band.to_numpy()[-1]
    except Exception as ex:
        print(f"Error in calculate_bollinger_bands: {ex}")
    return upper_band, lower_band

def calculate_rsi(data, period=14):
    rsi = None
    try:
        rsi = talib.RSI(data['Close'], timeperiod=period)
        rsi.interpolate(method='linear', inplace=True)
        rsi = rsi.to_numpy()[-1]
    except Exception as ex:
        print(f"Error in calculate_rsi: {ex}")
    return rsi

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    macd, signal = None, None
    try:
        macd, signal, _ = talib.MACD(data['Close'], fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
        macd = macd.to_numpy()[-1]
        signal = signal.to_numpy()[-1]
    except Exception as ex:
        print(f"Error in calculate_macd: {ex}")
    return macd, signal

def calculate_atr(data, period=14):
    atr = None
    try:
        atr = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=period)
        atr = atr.to_numpy()[-1]
        # atr = atr[-1]
    except Exception as ex:
        print(f"Error in calculate_atr: {ex}")
    return atr

def calculate_engulfing_patterns(data):
    engulfing = None
    try:
        engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
        engulfing = engulfing.to_numpy()[-1]
    except Exception as ex:
        print(f"Error in calculate_engulfing_patterns: {ex}")
    return engulfing

def calculate_doji(data):
    doji = None
    try:
        doji = talib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
        doji = doji.to_numpy()[-1]
    except Exception as ex:
        print(f"Error in calculate_doji: {ex}")
    return doji

def calculate_stochastic_oscillator(data, k_period=14, d_period=3):
    slow_k, slow_d = None, None
    try:
        slow_k, slow_d = talib.STOCH(data['High'], data['Low'], data['Close'], fastk_period=k_period, slowk_period=k_period, slowd_period=d_period)
        slow_k = slow_k.to_numpy()[-1]
        slow_d = slow_d.to_numpy()[-1]
    except Exception as ex:
        print(f"Error in calculate_stochastic_oscillator: {ex}")
    return slow_k, slow_d

