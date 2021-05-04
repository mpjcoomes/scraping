#!/usr/bin/env python3
# geckodriver https://github.com/mozilla/geckodriver/releases
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import asx_table

df_mi = pd.DataFrame()

for i in asx_table.df["CODE"][1:3]:
    driver = webdriver.Firefox(executable_path="/home/user/geckodriver")
    driver.maximize_window()
    time.sleep(5)
    driver.get("https://www.marketindex.com.au/asx/" + i)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    div_yield = re.sub('[%]', '', soup.text.split('\n')[49].split(' ')[17])
    one_yr = re.sub('[%]', '', soup.text.split('\n')[49].split(' ')[28])
    cap = re.sub('[$,]', '', soup.text.split('\n')[291])
    cap = cap if cap != "Market Capitalisation" else re.sub('[$,]', '', soup.text.split('\n')[292])
    cap = round(float(cap) / 10 ** 6)
    df2 = pd.DataFrame({"CODE": i, "CAP($M)": [cap], "YIELD(%)": [div_yield], "1YR(%)": [one_yr]})
    df_mi = pd.concat([df_mi, df2])
    driver.close()

asx_table.df.merge(df_mi, on="CODE", how='left').to_csv('file1.csv', sep='\t')
