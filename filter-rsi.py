#! /bin/python3

import os
import pandas as pd
from indicator.rescale import prevMonth
from indicator.rsi import rsi

min_increase = 0.01

def check(emiten: str) -> bool:
    fileName = f"data/{emiten}.csv"
    if not os.path.exists(fileName):
        return

    ticker=pd.read_csv(fileName)
    lastIndex = ticker.index[-1]
    close = ticker.Close[lastIndex]
    RSI = rsi(ticker.Close, 2)
    if RSI[lastIndex] > 70:
        increase = (close / ticker.Close[ticker.index[-2]] - 1) * 100
        if increase > min_increase:
            print(f"{emiten}: +{increase:.2f}%, rsi: {RSI[lastIndex]:.2f}")

argv = os.sys.argv
argv.pop(0)
if len(argv) > 1 and argv[0] == '--min':
    argv.pop(0)
    min_increase = float(argv.pop(0))

if len(argv) > 0:
    emitenList = argv
else:
    emitenList = pd.read_csv('emiten.csv').emiten

for emiten in emitenList:
    check(emiten)
