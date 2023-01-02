from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime

lista = ['date', 'zapotrzebowanie-mw', "generacja-mw", 'el-cieplne', 'el-wodne', 'el-wiatrowe', 'el-fotowoltaiczne', 'el-inne', 'saldo-wymiany', 'czestotliwosc']

x=0
while x==0:
    try:
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        browser.get('https://www.pse.pl/dane-systemowe')
        with open('dane_systemowe.txt', 'a') as file:
            for index, value in enumerate(lista):
                if index == 0:
                    nav = browser.find_element(By.ID, value)
                    file.write(f'{nav.text},')
                if index>0 and index<8:
                    nav = browser.find_element(By.ID, value)
                    data = int(nav.text.replace(' ',''))
                    file.write(f'{data},')
                if index == 8:
                    nav = browser.find_element(By.ID, value)
                    if 'EKSPORT' in nav.text:
                        data = -int(nav.text.replace(' EKSPORT', ''))
                        file.write(f'{data},')
                    elif 'IMPORT' in nav.text:
                        data = int(nav.text.replace(' IMPORT', ''))
                        file.write(f'{data},')
                if index == 9:
                    nav = browser.find_element(By.ID, value)
                    data = float(nav.text.replace(',','.'))
                    file.write(f'{data}\n')

        browser.quit()
    except:
        with open('log.dat', 'a') as log:
            log.write(f'{datetime.now()}, Access denied\n')
            
    sleep(60)
