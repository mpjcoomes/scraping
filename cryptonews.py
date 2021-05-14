#!/usr/bin/env python3
import requests
import pandas as pd
import time
import re

url = "https://cryptonews.com.au/cryptos?page=1"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64)",
    "X-Requested-With": "XMLHttpRequest",
}
r = requests.get(url, headers=header)
df = pd.read_html(r.text, header=0)[0]

for i in range(2, 11):
    url = "https://cryptonews.com.au/cryptos?page=" + str(i)
    time.sleep(1)
    r = requests.get(url, headers=header)
    df2 = pd.read_html(r.text, header=0)[0]
    df = pd.concat([df, df2])

df["Name"] = df.apply(lambda row: re.sub("[()]", "", row["Name"]), axis=1)
df = pd.concat([df, df["Name"].str.rsplit(n=1, expand=True)], axis=1)
df["Market cap"] = df.apply(
    lambda row: round(float(re.sub("[$,]", "", row["Market cap"])) / 10 ** 6), axis=1
)
df = df[[1, 0, "Market cap"]]
df.columns = ["CODE", "NAME", "CAP($M)"]

# AU Coinbase supported, 58 as of 14-05-2021, Celo is CGLD on Coinbase, CELO elsewhere.
coinbaseAU = [
    "1INCH",
    "AAVE",
    "ADA",
    "ALGO",
    "ANKR",
    "ATOM",
    "BAL",
    "BAND",
    "BAT",
    "BCH",
    "BNT",
    "BTC",
    "CELO",
    "COMP",
    "CRV",
    "CTSI",
    "CVC",
    "DAI",
    "DASH",
    "DNT",
    "ENJ",
    "EOS",
    "ETC",
    "ETH",
    "FIL",
    "FORTH",
    "GRT",
    "ICP",
    "KNC",
    "LINK",
    "LRC",
    "LTC",
    "MANA",
    "MATIC",
    "MIR",
    "MKR",
    "NKN",
    "NMR",
    "NU",
    "OGN",
    "OMG",
    "OXT",
    "REN",
    "REP",
    "RLC",
    "SKL",
    "SNX",
    "STORJ",
    "SUSHI",
    "TRB",
    "UMA",
    "UNI",
    "WBTC",
    "XLM",
    "XTZ",
    "YFI",
    "ZEC",
    "ZRX",
]

df2 = df.loc[df["CODE"].isin(coinbaseAU)]
df2.reset_index(drop=True, inplace=True)

# Read in and join your own buy transactions, supports 1-to-1 only.
df3 = pd.read_csv("Coinbase.csv", skiprows=7)
df3.columns = [
    "DATE_TIME",
    "TYPE",
    "CODE",
    "QUANTITY",
    "SPOT($)",
    "COIN($)",
    "TOTAL($)",
    "FEE($)",
    "NOTES",
]

df4 = df2.merge(df3, on="CODE", how="left")
df4 = df4.sort_values(by="CAP($M)", ascending=False)
df4.to_csv("file4.csv", sep="\t", index=False)
