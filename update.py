#! /bin/python3

import os
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

def formatDate(x: datetime):
	return x.strftime("%Y-%m-%d")

def add2date(start: str, days: int):
	return formatDate(datetime.fromisoformat(start) + timedelta(days))

def getCurrentDate():
    now = datetime.now()
    if now.hour >= 15 and now.minute > 30:
        return add2date(formatDate(now), 1)
    else:
        return formatDate(now)

def append(output: str, emiten: str):
    data = pd.read_csv(output)
    lastDate = add2date(data.Date[data.index[-1]], 1)
    if lastDate == currentDate:
        print(f"Skipping {emiten}... already latest data")
        return
    print(f"Updating {emiten}...")
    data = yf.download(emiten + ".JK", progress=False, start=lastDate, end=currentDate)

    # either network problem or emiten is delisted
    if data.index.size == 0:
        print(f"Skipping {emiten}... due to no data")
        return

    # save result
    data.to_csv(output, mode='a', header=False)

def download(output: str, emiten: str):
    print(f"Downloading {emiten}...")
    data = yf.download(emiten + ".JK", progress=False)
    if data.index.size == 0:
        print(f"Skipping {emiten}... due to no data")
        return
    data.to_csv(output)

if len(os.sys.argv) > 1:
    emitenList = os.sys.argv[1:]
else:
    emitenList = pd.read_csv('emiten.csv').emiten

currentDate = getCurrentDate()
for emiten in emitenList:
    fileOutput = f"data/{emiten.lower()}.csv"
    if os.path.exists(fileOutput):
        append(fileOutput, emiten.upper())
    else:
        download(fileOutput, emiten.upper())