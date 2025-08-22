from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
import pandas as pd
 
 
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
#Seçenekler menüsü
def menu():
    print(Fore.CYAN + "Bir seçenek seçin: \n")
    print(Fore.GREEN + "1) USD/TRY - Amerikan Doları Türk Lirası ")
    print("2) EUR/TRY - Euro Türk Lirası")
    print("3)Altın")
    print(Style.RESET_ALL)
#Tablonun satırlarını çekmek 
def fetch_data(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tr")))
    price_data = driver.find_elements(By.TAG_NAME, "tr")
    return price_data
 
def  save_data(price_data, filename):
    data_list = []
    for x in price_data[1:]: 
        try:
            date = x.find_element(By.XPATH, "./td[1]").text
            now = x.find_element(By.XPATH, "./td[2]").text
            open_ = x.find_element(By.XPATH, "./td[3]").text 
            high =x.find_element(By.XPATH, "./td[4]").text
            low =x.find_element(By.XPATH, "./td[5]").text
            data_list.append({'Tarih     ': date ,'Şimdi    ': now,'Açılış   ': open_,'Yüksek   ': high,'Düşük     ': low})
        except:
            continue
         
#Verileri csv dosyasına kaydetmek 
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False, encoding='utf-8')
   

def main():
    print(Fore.CYAN + "Hoş geldiniz! \n")
    menu()
    choice = input("Seçiminizi girin (1-3): ")

    urls = {
        "1": ("https://tr.investing.com/currencies/usd-try-historical-data", "USD_TRY.csv"),
        "2": ("https://tr.investing.com/currencies/eur-try-historical-data", "EUR_TRY.csv"),
        "3": ("https://tr.investing.com/commodities/gold-historical-data", "Gold_TRY.csv")
    }

    try:
     if choice in urls:
             
            url, filename = urls[choice]
            price_data = fetch_data(url)
            save_data(price_data, filename)
            print(Fore.GREEN + f"Veriler {filename} doasyasına kaydedildi.")
     else:
            print(Fore.RED + "Geçersiz seçim. Lütfen 1 ile 3 arasında bir sayı girin.")
    finally:
     driver.quit()


main()
