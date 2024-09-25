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
    close = ticker.Close[lastIndex]
    RSI = rsi(ticker.Close, 2)
    if RSI[lastIndex] > 70:
        print(f"{emiten}: +{(close / ticker.Close[ticker.index[-2]] - 1) * 100:.2f}%, rsi: {RSI[lastIndex]:.2f}")

if len(os.sys.argv) > 1:
    emitenList = os.sys.argv[1:]
else:
    emitenList = pd.read_csv('emiten.csv').emiten

for emiten in emitenList:
    check(emiten)
