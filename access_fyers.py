
import configparser
import re
from bs4 import BeautifulSoup
from fyers_api import fyersModel
from fyers_api import accessToken
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import urllib.parse as urlparse
import pandas as pd
import requests
import re
import datetime
import numpy as np

# Fetching values for Keys
config = configparser.ConfigParser()
config.read('.credentials.ini')
app_id = config['fyers']['app_id']
secret_id = config['fyers']['secret_id']
redirect_url = config['fyers']['redirect_url']
user_id = config['fyers']['user_id']
password = config['fyers']['password']
two_fa = config['fyers']['two_fa']

class Fyers:
    def __init__(self, app_id, secret_id, redirect_url, user_id, password, two_fa):
        self.app_id = app_id
        self.secret_id = secret_id
        self.redirect_url = redirect_url
        self.user_id = user_id
        self.password = password
        self.two_fa = two_fa
        self.set_token()

    def get_session_url(self):
        self.session=accessToken.SessionModel(client_id=app_id,secret_key=secret_id,redirect_uri=redirect_url,response_type="code", grant_type="authorization_code")
        self.url = self.session.generate_authcode()
    
    def login_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='C:\\Users\\Raghu Veera Reddy\\Desktop\\chromedriver.exe',options=options)
        driver.get(self.url)
        form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="container login-main-start"]')))
        driver.find_element_by_xpath("//input[@id='fyers_id']").send_keys(user_id)
        driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
        driver.find_element_by_xpath("//input[@id='pancard']").send_keys(two_fa)
        driver.find_element_by_xpath("//button[@id='btn_id']").click()
        sleep(2)        
        return driver
    
    def get_auth_code(self,driver):
        current_url = driver.current_url
        driver.close()
        print(current_url)
        parsed = urlparse.urlparse(current_url)
        auth_code = urlparse.parse_qs(parsed.query)['auth_code'][0]
        return auth_code
    
    def set_token(self):
        self.get_session_url()
        driver = self.login_driver()
        auth_code = self.get_auth_code(driver)
        self.session.set_token(auth_code)
        response = self.session.generate_token()
        access_token = response['access_token']
        self.fyers = fyersModel.FyersModel(client_id=app_id, token=access_token,log_path="C:\\Users\\Raghu Veera Reddy\\fyers")
  
fyers = Fyers(app_id, secret_id, redirect_url, user_id, password, two_fa)

