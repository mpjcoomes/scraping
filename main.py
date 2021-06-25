#!/usr/bin/env python3
# geckodriver https://github.com/mozilla/geckodriver/releases
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import asx_table


def skin(patt: str, soup_obj) -> int:
    match_obj = re.search(patt, soup_obj)
    if match_obj is not None:
        sub = re.sub(" +", " ", match_obj.group())
        sub = re.split(" ", re.sub("[$,]", "", sub))[-1]
        return sub


df_mi = pd.DataFrame()

for i in asx_table.df["CODE"]:
    # Market Index
    driver = webdriver.Firefox(executable_path="/home/user/geckodriver")
    driver.maximize_window()
    driver.get("https://www.marketindex.com.au/asx/" + i)
    time.sleep(5)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, "html.parser")
    flat = re.sub("[\n]", " ", soup.text)
    div_yield = skin("DIV YIELD [0-9.]+", flat)
    one_yr = skin("1 YR RETURN -*[0-9.]+", flat)
    cap = round(float(skin("Capitalisation \$[0-9,]+", flat)) / 10 ** 6)
    # ASX
    driver = webdriver.Firefox(executable_path="/home/user/geckodriver")
    driver.maximize_window()
    driver.get("https://www2.asx.com.au/markets/etp/" + i)
    time.sleep(5)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, "html.parser")
    frank = skin("Franking [0-9]+", soup.text)
    holdings = skin("Total fund holdings [0-9,]+", soup.text)
    us = skin("States\s{2}[0-9.]+", soup.text)
    chyna = skin("China\s{2}[0-9.]+", soup.text)
    hk = skin("Kong\s{2}[0-9.]+", soup.text)
    ind = skin("Industrials [0-9.]+", soup.text)
    mat = skin("Materials [0-9.]+", soup.text)
    ccy = skin("Consumer Cyclical [0-9.]+", soup.text)
    tec = skin("Technology [0-9.]+", soup.text)
    utl = skin("Utilities [0-9.]+", soup.text)
    cdf = skin("Consumer Defensive [0-9.]+", soup.text)
    egy = skin("Energy [0-9.]+", soup.text)
    fin = skin("Financial Services [0-9.]+", soup.text)
    hlc = skin("Healthcare [0-9.]+", soup.text)
    com = skin("Communication Services [0-9.]+", soup.text)
    rel = skin("Real Estate [0-9.]+", soup.text)
    df2 = pd.DataFrame(
        {
            "CODE": i,
            "FRK(%)": [frank],
            "HOLDS": [holdings],
            "US(%)": [us],
            "CH(%)": [chyna],
            "HK(%)": [hk],
            "CAP($M)": [cap],
            "YLD(%)": [div_yield],
            "1YR(%)": [one_yr],
            "CCY(%)": [ccy],
            "CDF(%)": [cdf],
            "COM(%)": [com],
            "EGY(%)": [egy],
            "FIN(%)": [fin],
            "HLC(%)": [hlc],
            "IND(%)": [ind],
            "MAT(%)": [mat],
            "REL(%)": [rel],
            "TEC(%)": [tec],
            "UTL(%)": [utl],
        }
    )
    df_mi = pd.concat([df_mi, df2])

df = asx_table.df.merge(df_mi, on="CODE", how="left")
df.to_csv("file1.csv", sep="\t")
