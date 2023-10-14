#! /bin/python3

import os
import pandas as pd
from indicator.rescale import prevMonth
from indicator.rsi import rsi

def check(emiten: str) -> bool:
    fileName = f"data/{emiten}.csv"
    if not os.path.exists(fileName):
        return

    ticker=pd.read_csv(fileName)
    lastIndex = ticker.index[-1]
    open = ticker.Open[lastIndex]
    close = ticker.Close[lastIndex]
    if close < open:
        return False
    pm = prevMonth(ticker)
    prevMonthLow = pm.Low
    prevMonthHigh = pm.High
    prevMonthMid = (prevMonthLow + prevMonthHigh) / 2
    RSI = rsi(ticker.Close, 2)
    if (
        (open < prevMonthLow[lastIndex] < close) or
        (open < prevMonthMid[lastIndex] < close) or
        (open < prevMonthHigh[lastIndex] < close)
    ) and RSI[lastIndex] > 70:
        print(f"{emiten}: +{(close / ticker.Close[ticker.index[-2]] - 1) * 100:.2f}%, rsi: {RSI[lastIndex]:.2f}")

if len(os.sys.argv) > 1:
    emitenList = os.sys.argv[1:]
else:
    emitenList = pd.read_csv('emiten.csv').emiten

for emiten in emitenList:
    check(emiten)
