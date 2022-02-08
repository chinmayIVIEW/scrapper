
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import concurrent.futures
import os


ROOT = os.getcwd()

url = 'https://nrfbigshow.nrf.com/exhibitors'
s=Service(f'{ROOT}/driver/chromedriver')

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get(url)

company_names = list(driver.find_elements(By.XPATH,'//table[@class="views-table views-view-table cols-2 responsive-enabled"]/tbody/tr/td[1]/a'))

company_details = []

def Scrap(name):
    driver = webdriver.Chrome(service=s, options=chrome_options)
    company_name = name.text
    company_url = name.get_attribute("href")
    driver.get(company_url)
    company_country_elem = driver.find_element(By.CLASS_NAME,'company_country')
    company_country = company_country_elem.text
    try:
        company_linkedin_elem = driver.find_element(By.XPATH,'//*[@id="block-nrf-d8-content"]/div/div/div[2]/div[1]/div[1]/div[3]/div[3]/a')
        company_linkedin = company_linkedin_elem.get_attribute("href")
        company_website_elem = driver.find_element(By.XPATH,'//*[@id="block-nrf-d8-content"]/div/div/div[2]/div[1]/div[1]/div[3]/div[2]/a')
        company_website = company_website_elem.get_attribute("href")
    except:
        company_linkedin = "No Data Present"
        company_website = "No Data Present"
    print("company_name: ", company_name)
    details = {
        "company name": company_name,
        "country":company_country,
        "linkedin link": company_linkedin,
        "website link":company_website
    }
    company_details.append(details)
    print(len(company_details))
    driver.close()

# for company in company_names:
#     print(">", company)
#     Thread(target=Scrap, name="T1" , kwargs={'name': company}, daemon=False)
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(Scrap, company_names)

# for name in company_names[:5]:
#     print(name.text)
#     Scrap(name)

dataframe = pd.DataFrame(company_details)
file_name = 'compnay_details.xlsx'
dataframe.to_excel(file_name)
print("Data Extraction Completed !!!")

driver.close()