from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe',options=options)
from selenium.webdriver.support.ui import WebDriverWait
import urllib
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

def translate(sentence):
  url_encoded = urllib.parse.quote(sentence)
  url = f"https://translate.google.com/?hl=vi&sl=auto&tl=vi&text={url_encoded}&op=translate"
  
  driver.get(url)
  # print(BeautifulSoup(driver.page_source, 'lxml').body.text)
  delay = 2
  output_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'JLqJ4b')))
  soup = BeautifulSoup(driver.page_source, 'lxml')
  input_class = "er8xn"
  input_element = soup.select_one(f'.{input_class}')
  output_class = "JLqJ4b"
  output_element = soup.select_one(f'.{output_class}')

  result = ""
  for chil in output_element.findChildren():
    result = chil.text
    break
  return result