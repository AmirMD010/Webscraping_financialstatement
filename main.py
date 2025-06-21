from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service

import pandas as pd



def scraping_financial_statement(ticker):
    options = Options()
    options.add_experimental_option("detach", True)
    service = Service(r"C:\Users\Zone\Downloads\chromedriver-win32\chromedriver.exe")
    driver = Chrome(service=service, options=options)

    driver.get('https://www.amarstock.com/stock/' + ticker)

    products = driver.find_elements(By.XPATH, '//div[@class="box bgg0"]')

    data = []

    for product in products:
        ratio = product.find_element(By.XPATH, './/div[@class="name"]').text
        value = product.find_element(By.XPATH, './/div[@class="value"]').text

        data.append({
            "Ratio": ratio,
            "Value": value
        })

    df = pd.DataFrame(data=data)
    df.to_csv('csv/Ratios.csv',index=False)
    print(df)
    print("----------------------------------")

    for financial_statement in range(2,6):
        tab = driver.find_element(By.XPATH, f'//*[@id="tab-cont"]/div[1]/ul/li[{financial_statement}]')
        tab.click()

        headers = [th.text.strip() for th in driver.find_elements(By.XPATH, f'//*[@id="tab{financial_statement}"]/div/div/table/thead/tr/th')]

        rows = driver.find_elements(By.XPATH, f'//*[@id="tab{financial_statement}"]/div/div/table/tbody/tr')

        data1 =[]
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text.strip() for cell in cells]
            data1.append(row_data)

        
        df1 = pd.DataFrame(data=data1, columns=headers)
        df1.to_csv(f'csv/Financial{financial_statement}.csv', index=False)
        
        print(df1)
        print("----------------------------------------------------")
    

scraping_financial_statement('SQURPHARMA')