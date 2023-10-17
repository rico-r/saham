#! /bin/python3

import os
import pandas as pd
import yfinance as yf

def append(output: str, emiten: str):
    data = pd.read_csv(output).set_index('Date')
    data.index = pd.to_datetime(data.index)

    print(f"Updating {emiten}...")
    newData = yf.download(emiten + ".JK", progress=False, start=data.index[-1], prepost=True)

    # either network problem or emiten is delisted
    if data.index.size == 0:
        print(f"Skipping {emiten}... due to no data")
        return

    # update old data
    data.update(newData)
    data = data.combine_first(newData)

    # save result
    data.to_csv(output)

def download(output: str, emiten: str):
    print(f"Downloading {emiten}...")
    data = yf.download(emiten + ".JK", progress=False, prepost=True)
    if data.index.size == 0:
        print(f"Skipping {emiten}... due to no data")
        return
    data.to_csv(output)

if len(os.sys.argv) > 1:
    emitenList = os.sys.argv[1:]
else:
    emitenList = pd.read_csv('emiten.csv').emiten

for emiten in emitenList:
    fileOutput = f"data/{emiten.lower()}.csv"
    if os.path.exists(fileOutput):
        append(fileOutput, emiten.upper())
    else:
        download(fileOutput, emiten.upper())