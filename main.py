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
credentials=ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
scope)
client = gspread.authorize(credentials)

#Open a spreadsheet:
sheet = client.open("sheet-name")
#create a new worsheet
wsh = sheet.add_worksheet(date[0],100,100)
#enter the values from the dataframe
wsh.update([df.columns.values.tolist()] + df.values.tolist())





