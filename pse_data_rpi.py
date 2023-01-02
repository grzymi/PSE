from selenium import webdriver
from selenium.webdriver.chrome.service import Service# as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from pyvirtualdisplay import Display

lista = ['date', 'zapotrzebowanie-mw', "generacja-mw", 'el-cieplne', 'el-wodne', 'el-wiatrowe', 'el-fotowoltaiczne', 'el-inne', 'saldo-wymiany', 'czestotliwosc']

x=0
while x==0:
    try:
        print('Service start.')
        display = Display(visible=0, size=(1024,768))
        display.start()
        print('Display ON')
        opts = webdriver.ChromeOptions()
        opts.add_argument('--no-sandbox')
        service = Service('usr/lib/chromedriver')
        #browser = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        browser = webdriver.Chrome(service=service, options=opts)
        browser.implicitly_wait(0.5)
        print('Browser run...')
        browser.get('https://www.pse.pl/dane-systemowe')
        print('Webpage open...')
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
        display.stop()
        print('Data saved successfully!')
    except:
        print('Data not saved!')
        with open('log.dat', 'a') as log:
            log.write(f'{datetime.now()}, Access denied\n')
    
    print('Waiting for next session...')
    sleep(290)
