#system libraries
import asyncio
import os
import random
import sys
import threading
import time
import winsound
from datetime import datetime

import requests
#selenium libraries
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

asmens_kodas = '55555555555'
vardas = 'John'
pavarde = 'Doe'


teorijosId = '22222222'
mobilusisTelefonas = '11111111'
elektroninisPastas = '123123@gmail.com'

targetCity = 'Vilnius'

API_KEY = "KEY" 
data_sitekey = 'KEY'
page_url ='https://vp.regitra.lt/#/'

#scanningMonth2 = 'Liepos mėn.'
scanningMonth1 = 'Birželio mėn.'

refreshLoop = True

totalRefreshCount = 0
refreshTime = 20

def delay ():
    time.sleep(random.randint(2,3))

try:
    #create chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options, executable_path=r"webdriver\chromedriver.exe")

    delay()
    #go to website
    driver.get("https://vp.regitra.lt/#/")
    delay()
    driver.execute_script('document.body.style.zoom="90%";')   
except:
    print("[-] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")


def restartAll():
    print("RESTARTING")
    driver.get("https://www.google.com/")
    driver.delete_all_cookies()
    driver.execute_script('localStorage.clear();')
    delay()
    driver.get("https://vp.regitra.lt/#/")
    time.sleep(10)
    login()  




def Solver(many=0):
    u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}"
    r1 = requests.get(u1)
    
    print(r1.text)
    rid = r1

    u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid.text[3:])}&json=1"
    time.sleep(5)
    while True:
        r2 = requests.get(u2)
        print(r2.json())
        if r2.json().get("status") == 1:
            form_tokon = r2.json().get("request")
            break
        if r2.json().get("request") != 'CAPCHA_NOT_READY':
            raise Exception('An error occurre, Captcha request unknown')
        time.sleep(5)

        
    wirte_tokon_js = f'document.getElementsByClassName("g-recaptcha-response")[0].innerHTML="{form_tokon}";'

    submitCallback = f"___grecaptcha_cfg.clients['{many}']['B']['B']['callback']('{form_tokon}');"




#//h4[text()='Rugpjūčio mėn.']/parent::*//button[@ng-click="add(vieta.p3.id)"]
#//h4[text()='Rugpjūčio mėn.']
#ng-click="endRegistration()"
#ng-click="ok()"

    driver.execute_script(wirte_tokon_js)
    print('Token is in innerHTML')

    time.sleep(2)
    driver.execute_script(submitCallback)
    print('Callback Submitted')

    time.sleep(2)

time.sleep(2)

def beepSound():
    for i in range(1, 3):
        frequency = 2000
        duration = 500
        winsound.Beep(frequency, duration)

def checkCaptcha():
    try:
        btnView = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@ng-click='add(vieta.p2.id)']"))
        )
    except:
        driver.refresh()
        Solver()

def checkSpot(ngClick, month, day):
    if driver.find_element(By.XPATH, f"//h4[text()='{month}']/parent::*//b[@class='ng-binding' and contains(text(), '{day}')]/ancestor::div[2]//button[contains(@ng-click, 'add(vieta.{ngClick}.id)') and not(contains(@disabled, 'disabled'))]"):

        elem = driver.find_element(By.XPATH, f"//h4[text()='{month}']/parent::*//b[@class='ng-binding' and contains(text(), '{day}')]/ancestor::div[2]//button[contains(@ng-click, 'add(vieta.{ngClick}.id)') and not(contains(@disabled, 'disabled'))]")
        driver.execute_script("arguments[0].click();", elem)
        
        try:
            spotBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@ng-click="ok()"]'))
            )
            element1 = spotBtn
    
            driver.execute_script("arguments[0].click();", element1)
        except:
            print("Error submitting free spot")
        try:
            finalBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//button[@ng-click="endRegistration()"]'))
            )
            element2 = finalBtn
    
            driver.execute_script("arguments[0].click();", element2)
            print(f"SPOT CLCIKED {month}, {ngClick}")    
        except:
            print("Error ending place registration")

        time.sleep(5)
        if len(driver.find_elements_by_xpath("//div[text()='Jūsų pasirinktas laikas jau užimtas, prašome pasirinkti kitą egzamino laiką']")) == 0:
            input("SPOT IS FINALLY TAKEN, PRESS TO CONTINUE")


        againBtn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/mainframe/div[3]/div[2]/div[2]/div[1]/p/button'))
        )
        driver.execute_script("arguments[0].click();", againBtn)

        Solver()

  #//h4[text()='Liepos mėn.']/parent::*//b[@class='ng-binding' and contains(text(), '30 d.')]


def takeFreeSpot(month, day):

    for i in range(1, 8):
        try:
            checkSpot(f'p{i}', month, day)
        except:
            pass


#//h4[text()='Rugpjūčio mėn.']/parent::*//button[contains(@ng-click, 'add(vieta.p6.id)') and not(contains(@disabled, 'disabled'))]




def monthScan(month):
    try:
        day_number = driver.find_elements_by_xpath(f"//h4[text()='{scanningMonth1}']/parent::*//b[@class='ng-binding']")
        today = int(str(datetime.date(datetime.now()))[-2:])
        print(today)
        print(datetime.date(datetime.now()))

        for el in day_number:
            day_number_string = el.get_attribute('innerHTML')
            print(day_number_string)



            nums = [s for s in day_number_string if s.isdigit()]
            num = ""
            for number in nums:
                num += str(number)


            num = int(num)
            print(num)

            if num < today+7:
                beepSound()
                day = f"{num} d."
                print(day)
                takeFreeSpot(month, day)
    except:
        print(f"Nera vietu {month}")



def citySelect():
    time.sleep(10)
    btnSchedule = WebDriverWait(driver,25).until(
        EC.presence_of_element_located((By.XPATH, "//button[@id='schedule']"))
    )
    element = btnSchedule
    
    driver.execute_script("arguments[0].click();", element)
    delay()
    btnSchedule = WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{targetCity}']"))
    )
    element = btnSchedule
    
    driver.execute_script("arguments[0].click();", element)


def frontLogin():
    time.sleep(5)
    #CLICK LOGIN ICON
    ButtonPrisijungti = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/mainframe/div[2]/div/div[1]/div[1]/div[2]"))
    )
    element = ButtonPrisijungti
    
    driver.execute_script("arguments[0].click();", element)

    time.sleep(2)


    #SUBMIT LOGIN CREDENTIALS
    asmens_kodasInput = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="asmens_kodas"]'))
    )
    vardasInput = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="vardas"]'))
    )
    pavardeInput = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="pavarde"]'))
    )

    asmens_kodasInput.send_keys(asmens_kodas)
    vardasInput.send_keys(vardas)
    pavardeInput.send_keys(pavarde)

    if __name__ == "__main__":
        Solver()

    time.sleep(5)
    submitInput = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/form/div[3]/button[1]'))
    )
    element = submitInput
    
    driver.execute_script("arguments[0].click();", element)

    print("FrontLogin Successfull")


def midLogin():
    time.sleep(2)
    #CLICK ACCEPT BUTTON
    btnSuccess = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/mainframe/div[3]/div[4]/div/div[3]/button"))
    )
    element = btnSuccess
    
    driver.execute_script("arguments[0].click();", element)
    print("MidLogin Successfull")


def backLogin():
    time.sleep(3)
    driver.refresh()

    time.sleep(5)

    #CLICK ON ICON
    if len(driver.find_elements_by_xpath("/html/body/div/mainframe/div[3]/div/div[2]/div/h4")) !=0:

        btnView = WebDriverWait(driver, 40).until(
             EC.element_to_be_clickable((By.XPATH, "/html/body/div/mainframe/div[3]/div/div[2]/div/h4"))
        )
        element = btnView
        
        driver.execute_script("arguments[0].click();", element)
     

        time.sleep(2)

        #CHANGE SCHEDULE TIME

        teorijaInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="prasymoNumeris"]'))
        )
        telInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="mobilusisTelefonas"]'))
        )
        emailInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="elektroninisPastas"]'))
        )
        teorijaInput.send_keys(teorijosId)
        telInput.send_keys(mobilusisTelefonas)
        emailInput.send_keys(elektroninisPastas)

        if __name__ == "__main__":
            Solver()


        delay()

        submitInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/form/div[2]/button[1]'))
        )
        element = submitInput
        
        driver.execute_script("arguments[0].click();", element)



        time.sleep(5)


        #CLICK ON ICON
        btnView = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/mainframe/div[3]/div[3]/div/div[5]/label"))
        )
        element = btnView
        driver.execute_script("arguments[0].click();", element)

        
        btnView2     = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-click='ok()']"))
        )
        element = btnView2
        
        driver.execute_script("arguments[0].click();", element)
        print("submit-clicked")



        delay()

        driver.refresh()

        citySelect()
        print("Backlogin citySelect")

        time.sleep(2)



        if __name__ == "__main__":
            Solver()


        print("Backlogin captcha Successfull")
    else:
        print("Backlogin failed")


def login():

    time.sleep(3)


    if len(driver.find_elements( By.XPATH, ("//div[@ng-click='asduom()']") )) !=0:
        while True:
            try:
                frontLogin()
                break
            except:
                time.sleep(10)
                print("Restarting front login")
                driver.refresh()
                driver.get("https://vp.regitra.lt/#/")
                time.sleep(10)

    time.sleep(30)
        
    if len(driver.find_elements( By.XPATH, ("//button[@ng-click='taip()']") )) != 0:
        while True:
            try:
                midLogin()
                break
            except:
                print("Restarting mid login")
                driver.refresh()
                time.sleep(10)
                driver.get("https://vp.regitra.lt/#/")
                time.sleep(10)  
 
    time.sleep(30)
        
    if len(driver.find_elements( By.XPATH, ("//h4[text()='Registruotis į praktikos egzaminą']") )) != 0:
        while True:
            try:
                backLogin()
                break
            except:
                print("Restarting back login")
                driver.refresh()
                time.sleep(10)
                driver.get("https://vp.regitra.lt/#/")
                time.sleep(10)


    time.sleep(5)




    #checkCaptcha()

###############################################################################


if __name__ == '__main__':
    login()

refreshCount = 0


while refreshLoop:

    monthScan(scanningMonth1)

    #monthScan(scanningMonth2)

    #TIMER0
    time.sleep(1)

    for i in range(1, refreshTime):
        print(i)
        time.sleep(1)   

    print("No dates found, refreshing")
    refreshCount += 1

    print(refreshCount)

    driver.refresh()

    delay()
    try:
        driver.find_element(By.XPATH, "//button[@id='schedule']")
        citySelect()

        delay()
        Solver()

        #checkCaptcha()

        time.sleep(7)
    except:
        driver.get("https://vp.regitra.lt/#/")
        login()
        totalRefreshCount += refreshCount
        refreshCount = 0
        print(f"Total refresh count - {totalRefreshCount}")
