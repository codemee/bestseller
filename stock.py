# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:10:06 2026

@author: Admin
"""

import requests
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.flag.com.tw/test/books_list.php'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
books = soup.find_all("div")

for book in books:
    time.sleep(random.randint(25,30))
    bokno = book.find('strong', class_='bokno').text.strip() 
    bookid = book.find('strong', class_='url').text.strip()     
    pt = book.find('strong', class_='bookspt').text.strip()   

    meta="https://www.books.com.tw/products/"+bookid
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 無頭模式，背景執行
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'--user-agent={my_user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(meta)
    driver.implicitly_wait(5)
    
    try:
        elements = driver.find_elements(By.CLASS_NAME, 'no')
        print(f'書號: {bokno}') 
        print(f'網址: {meta}')  
        for element in elements:
            value = element.text
        print(f"數量: {value}")            
        localtime = time.localtime()
        result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
        print(f"時間: {result}") 
        print('=============================')           
    except requests.RequestException as e:
        print(f"error msg：{e}")        
driver.quit()        