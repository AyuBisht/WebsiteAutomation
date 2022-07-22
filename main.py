from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

s=Service('path-to-chromedriver.exe')
driver = webdriver.Chrome(service=s)
  
#navigate to the website
driver.get("https://www1.nseindia.com/products/content/equities/equities/fii_dii_market_today.htm")

#get the data
matches = driver.find_elements(By.XPATH, "//tr[@class='alt']")

category = []
date = []
buy = []
sell = []
net_value = []


for match in matches: 
    category.append(match.find_element(By.XPATH,'./td[1]').text)
    date.append(match.find_element(By.XPATH,'./td[2]').text)
    buy.append(match.find_element(By.XPATH,'./td[3]').text)
    sell.append(match.find_element(By.XPATH,'./td[4]').text)
    net_value.append(match.find_element(By.XPATH,'./td[5]').text)

driver.quit()

#transfer  to a csv file
df = pd.DataFrame({
    'Category': category,
    'Date': date,
    'Buy Value': buy,
    'Sell Value':sell,
    'Net Value': net_value
})
print(df)

# connect to Google sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]
cred = {
  "type": "service_account",
  "project_id": "automation-356709",
  "private_key_id": "private_key_id",
  "private_key": "private_key",
  "client_email": "client_email",
  "client_id": "client_id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/automation%40automation-356709.iam.gserviceaccount.com"
}

credentials=ServiceAccountCredentials.from_json_keyfile_dict(cred,
scope)
client = gspread.authorize(credentials)

#Open a spreadsheet:
sheet = client.open("DailyFII/DII")
wksh = sheet.sheet1
for i in range(len(df)):
    new = []
    for j in df.loc[i]:
        new.append(j)
    wksh.append_row(new)
