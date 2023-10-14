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
    if now > now.replace(hour=15, minute=30):
        return formatDate(now + timedelta(days=1))
    else:
        return formatDate(now)

def append(output: str, emiten: str):
    data = pd.read_csv(output)

    lastDate = data.Date[data.index[-1]]
    nextDate = add2date(lastDate, 1)
    if nextDate == endDate:
        print(f"Skipping {emiten}... already has latest data")
        return
    print(f"Updating {emiten}...")
    data = yf.download(emiten + ".JK", progress=False, start=nextDate, end=endDate)

    # either network problem or emiten is delisted
    if data.index.size == 0:
        print(f"Skipping {emiten}... due to no data")
        return
    elif formatDate(data.index[0]) == lastDate:
        print(f"Skipping {emiten}... already has latest data")
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

endDate = getCurrentDate()
for emiten in emitenList:
    fileOutput = f"data/{emiten.lower()}.csv"
    if os.path.exists(fileOutput):
        append(fileOutput, emiten.upper())
    else:
        download(fileOutput, emiten.upper())