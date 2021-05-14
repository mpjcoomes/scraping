#!/usr/bin/env python3
# geckodriver https://github.com/mozilla/geckodriver/releases
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import asx_table

df_mi = pd.DataFrame()

for i in asx_table.df["CODE"]:
    driver = webdriver.Firefox(executable_path="/home/user/geckodriver")
    driver.maximize_window()
    time.sleep(5)
    driver.get("https://www.marketindex.com.au/asx/" + i)
    time.sleep(5)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, "html.parser")
    flat = re.sub("[\n]", " ", soup.text)
    div_yield = re.split(" ", re.search("DIV YIELD [0-9.]*", flat).group())[2]
    one_yr = re.split(" ", re.search("1 YR RETURN -*[0-9.]*", flat).group())[3]
    cap = re.split(
        " ",
        re.sub("[$,]", "", re.search("Market Capitalisation \$[0-9,]*", flat).group()),
    )[2]
    cap = round(float(cap) / 10 ** 6)
    driver = webdriver.Firefox(executable_path="/home/user/geckodriver")
    driver.maximize_window()
    time.sleep(5)
    driver.get("https://www2.asx.com.au/markets/etp/" + i)
    time.sleep(5)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, "html.parser")
    frank = re.split(" ", re.search("Franking [0-9]*", soup.text).group())[1]
    companies = re.split(
        " ",
        re.sub("[,]", "", re.search("Total fund holdings [0-9,]*", soup.text).group()),
    )[3]
    us = re.search("United States\s{2}[0-9.]*", soup.text)
    if us is not None:
        us = re.split(" ", us.group())[3]
    chyna = re.search("China\s{2}[0-9.]*", soup.text)
    if chyna is not None:
        chyna = re.split(" ", chyna.group())[2]
    hk = re.search("Hong Kong\s{2}[0-9.]*", soup.text)
    if hk is not None:
        hk = re.split(" ", hk.group())[3]
    df2 = pd.DataFrame(
        {
            "CODE": i,
            "FRANK(%)": [frank],
            "HOLDS": [companies],
            "US(%)": [us],
            "CH(%)": [chyna],
            "HK(%)": [hk],
            "CAP($M)": [cap],
            "YIELD(%)": [div_yield],
            "1YR(%)": [one_yr],
        }
    )
    df_mi = pd.concat([df_mi, df2])

df = asx_table.df.merge(df_mi, on="CODE", how="left")
df.to_csv("file1.csv", sep="\t")
