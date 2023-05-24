from bs4 import BeautifulSoup
import requests
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import sys
from selenium.webdriver.chrome.options import Options
from threading import Thread
from playwright.sync_api import sync_playwright
import time

test=[]
threadlist=[]
result_last=[]

config = configparser.ConfigParser()
config.read('config.cfg')
SCOPE_CHAINS = config['PROFITHUNTER']['SCOPE_CHAINS'] 
# amount_checker =config["PROFITHUNTER"]['AMOUNT_CHECKER']
# trade_checker=config["PROFITHUNTER"]['trade_checker']
# trade_value=config["PROFITHUNTER"]['trade_value']
# amount_value=config["PROFITHUNTER"]['AMOUNT_VALUE']


# #define part is DEBUGGED 
def walletchecker(x):
    try:   
        print("walletchecker started.....")
        counter=0
        arr= np.array([])
        walletlist=np.array([])
        final_walletlist=np.array([])
        driver=webdriver.Chrome(ChromeDriverManager().install())
        driver.get(f'https://www.coincarp.com/currencies/{x}/richlist/')

        # Wait 5 seconds for the page to load
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//td[@class="td4"]')))

        # Find the elements 
        elements = driver.find_elements_by_xpath('//td[@class="td4"]')
        wallets = driver.find_elements_by_xpath("//span[@class='mr-2']")

        for wallet in wallets:
            walletlist=np.append(walletlist,str(wallet.text))
        walletlist = list(filter(None, walletlist))
        #print(walletlist)


        #Get the text from the elements
        for element in elements:
            t=str(element.text)
            t1=float((t.replace("%","").strip()))
            t1=np.format_float_positional(t1,trim='-')
            arr= np.append(arr,t1)
        ##print(arr)

        for i in arr:
            i=float(i)
            if (1>i > 0.50):
                final_walletlist=np.append(final_walletlist,walletlist[counter])
            counter+=1
    
        driver.close()
        #print(final_walletlist)
        return(final_walletlist)
    except:
        print("error in checking wallets.. try again in a minute")


def method1(data):
    try:
        coin_name=data.text
        coin_name=coin_name.strip().replace(" ","-").lower()
                
        subpage=requests.get(f"https://www.coincarp.com/currencies/{coin_name}/").text
        #print(coin_name)
        soup1=BeautifulSoup(subpage,"lxml")
        buttons=soup1.find("img",class_="mr-1",alt=f"{SCOPE_CHAINS}")
        if buttons is not None:
            test= walletchecker(coin_name)
            t=history(test)
            result_last=result_last.append(t)
    except:
        pass
                    






#This part is debugged
html_text = requests.get("https://www.coincarp.com/gainers-losers/").text
soup=BeautifulSoup(html_text,"lxml")
gainers=soup.find("div",class_="col-lg-6")
all_data =gainers.find_all("span",class_="fullname")


def main():
    print("getting coin data.....")
    
    
    for data in all_data:
        try:
            M = Thread(target=method1,args=(data,))
            M.start()
            threadlist.append(M)
            
        except:
            print("main method error please try again later")
            continue
    for B in threadlist:
        B.join()
    config = configparser.ConfigParser()
    config['TRACKED_WALLET'] = {'wallets': f'{result_last}'}

    with open('config.conf', 'w') as configfile:
        config.write(configfile)
    sys.exit("Execution successful....")


#This section is debugged   
def history(i):
    result=[]
  
    for x in i:
        try:
            print("checking history....")
            driver=webdriver.Chrome(ChromeDriverManager().install())
            driver.get(f"https://app.zerion.io/{x}/history")
            if(day_year_toggle==1):#customziable amount check- define in config file
                l=day_year_checker(x)
                if l==0:
                    continue
            amount_money= WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="UIText-sc-96tl0y-0 BreakWordText-sc-1s64evs-0 doIpXm iHvGkp"]')))
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='shared__HStack-sc-1qg837v-1 iqVyxE']")))
            x=int(amount_money.text[1:6].replace(",",""))
            if  ((x<amount_value) and (amount_checker==1)) : #customziable amount check- define in config file
                continue
            text_attr = element.text
            text_attr = text_attr[:text_attr.index("(")]
            percentage = text_attr.replace("%", "").strip()
            p=float(percentage[1:])
            if (p > 5.0) and percentage[0]=="+" :
                tran = driver.find_elements_by_xpath("//div[@class='General__BalanceSenderReceiver-f4p87i-3 fhAA-DV']")
                count = len(tran)
                trades=WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='UIText-sc-96tl0y-0 efmSIO']")))
                trade_count=0
                for trade in trades:
                    if trade.text =="Trade":
                        trade_count +=1
                if (trade_count<trade_value) and (trade_checker==1):#customziable amount check- define in config file 
                    continue
                if count> 10:
                    result.append(x)
            driver.close()

        except:
            print("bad request")
            continue
    return(result)


def day_year_checker(x):
    with sync_playwright() as p:
        el=1
        browser= p.chromium.launch()
        page=browser.new_page()
        page.goto(f"https://app.zerion.io/{x}/overview")
        x=page.locator('xpath=//button[@class="UIText-sc-96tl0y-0 PillButton__PillButtonElement-uyxo0h-0 PzeMW dRIOyV" and text()="1Y"]')# change the text() into 1W for week,
        x.click()
        
        page.is_visible('div.shared__HStack-sc-1qg837v-1 iqVyxE')
        time.sleep(5)
        html = page.inner_html("//div[@class='nz4fo00 nz4fo01']")

        soup=BeautifulSoup(html,'html.parser')
        y =soup.find("div",{'class':'shared__HStack-sc-1qg837v-1 iqVyxE'})
        raw=y.text
        i=raw.index("%")
        year_value= float(raw[1:i].replace(",",""))
        if (year_value>1000) and raw[0]=="+" :#dummy value can be changed to variable
            el=1
        else:
            el=0

        #daycheck-reuses same vars to reserve memory
        day_value_button=page.locator('xpath=//button[@class="UIText-sc-96tl0y-0 PillButton__PillButtonElement-uyxo0h-0 PzeMW dRIOyV" and text()="1D"]')
        day_value_button.click()
        page.is_visible('div.shared__HStack-sc-1qg837v-1 iqVyxE')
        time.sleep(5)
        html = page.inner_html("//div[@class='nz4fo00 nz4fo01']")
        soup=BeautifulSoup(html,'html.parser')
        y =soup.find("div",{'class':'shared__HStack-sc-1qg837v-1 iqVyxE'})
        raw= y.text
        i=raw.index("%")
        day_value=float(raw[1:i].replace(",",""))
        if (day_value>1000) and raw[0]=="+" : #dummy value can be changed to variable
            el1=1
        else:
            el1=0
        if el==1 and el1== 1:
            return 1
        else :
            return 0

    
    
        



#Execution starts here------------- Scraper v1.0000


print("starting program......\n")
main()






    





  


    







    
  


    
