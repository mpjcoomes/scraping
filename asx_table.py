#!/usr/bin/env python3
import requests
import numpy as np
import pandas as pd
from datetime import datetime

url = "https://www2.asx.com.au/markets/trade-our-cash-market/asx-investment-products-directory/etps"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64)",
    "X-Requested-With": "XMLHttpRequest",
}
r = requests.get(url, headers=header)
df = pd.read_html(r.text, header=0)[0]
df = df.assign(ASX_CAT="Equity - Australia")
names = [
    "Equity - Australian Small/Mid Cap",
    "Equity - Australian Sectors",
    "Equity - Australia Strategy",
    "Equity - Global",
    "Equity - Global Sectors",
    "Equity - Global Strategy",
    "Equity - Global Factors",
    "Equity - Emerging Markets",
    "Equity - Asia",
    "Equity - China",
    "Equity - Europe",
    "Equity - Japan",
    "Equity - South Korea",
    "Equity - United Kingdom",
    "Equity - USA",
    "Equity - India",
    "Equity - Infrastructure",
    "Property - Australia",
    "Property - Global",
    "Currency",
    "Fixed Income - Australian Dollar",
    "Fixed Income - Global",
    "Cash",
    "Mixed Asset",
    "Commodity",
]

for i, j in enumerate(names, start=1):
    df2 = pd.read_html(r.text, header=0)[i]
    df2 = df2.assign(ASX_CAT=j)
    df = pd.concat([df, df2])

df = df[
    [
        "ASX_CAT",
        "ASX Code",
        "Type",
        "Exposure",
        "Benchmark",
        "Management Cost %",
        "Outperf' Fee",
        "Admission Date",
    ]
]
df.columns = ["ASX_CAT", "CODE", "TYP", "NAME", "BENCHMARK", "MER%", "OF", "AGE(Y)"]
df["AGE(Y)"] = datetime.now() - pd.to_datetime(df["AGE(Y)"], format="%d/%m/%Y")
df["AGE(Y)"] = (df["AGE(Y)"] / np.timedelta64(1, "Y")).round(1)

df.reset_index(drop=True, inplace=True)
df.to_csv("file0.csv", sep="\t")
