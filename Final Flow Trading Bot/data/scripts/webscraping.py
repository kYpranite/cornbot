from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expConditions

import os
import time
import datetime
import data.scripts.contract as contract


def init():  # Function to login into unusualwhales
    driver.get("https://unusualwhales.com/login")
    print("Logging in!")
    username = driver.find_element(By.XPATH, '//*[@id="router-root"]/section/div/div/div/div/form/div[1]/input')  # XPATH of username box
    password = driver.find_element(By.XPATH, '//*[@id="router-root"]/section/div/div/div/div/form/div[2]/input')  # XPATH of password box
    button = driver.find_element(By.XPATH, '//*[@id="router-root"]/section/div/div/div/div/div/button')  # XPATH of button

    username.send_keys("USERNAME HERE")
    password.send_keys("PASSWORD HERE")
    button.click()
    print("Waiting for login!")
    time.sleep(10)
    driver.get("https://unusualwhales.com/alerts")
    print("Accessing results page")
    time.sleep(4)
    firstAlert = driver.find_elements(By.XPATH,
                                      '//*[@id="router-root"]/div[1]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[1]/a')  # tr normally 1
    firstAlert = firstAlert[0]  # for some reason can't search for single result, must search with array
    firstAlertHref = firstAlert.get_attribute("href")
    checkAlert.latestResult = firstAlert
    checkAlert.latestResultHref = firstAlertHref
    print("LATEST RESULT:")
    print(checkAlert.latestResult.text + "\n\n")


def checkAlert(count):  # Checks if theres a new alert by comparing title and running 3 previous 3 rows
    undetectedAlerts = dict()
    firstCheck = False
    driver.get("https://unusualwhales.com/alerts")
    print(str(count) + ": Refreshing alerts page")
    time.sleep(8)

    for i in range(1, 4):  # THIS IS NORMALLY 1, 4
        updatedResult = driver.find_elements(By.XPATH,
                                             '//*[@id="router-root"]/div[1]/div/div[3]/div[3]/div/table/tbody/tr[' + str(i) + ']/td[1]/a')
        priceColumn = driver.find_elements(By.XPATH,
                                           '//*[@id="router-root"]/div[1]/div/div[3]/div[3]/div/table/tbody/tr[' + str(i) + ']/td[11]')
        expDateColumn = driver.find_elements(By.XPATH,
                                             '//*[@id="router-root"]/div[1]/div/div[3]/div[3]/div/table/tbody/tr[' + str(i) + ']/td[3]')
        try:
            priceColumn = priceColumn[0]  # converts array to variable
            updatedResult = updatedResult[0]
            expDateColumn = expDateColumn[0]
        except IndexError:
            print("Skipped option due to index error, please contact developer")
            with open("log.txt", "a") as logfile:
                logfile.write(str(datetime.datetime.now()) + " - Skipped an option due to index error, please contact developer\n")
            raise

        updatedResultHref = updatedResult.get_attribute("href")
        if i == 1:
            if updatedResultHref != checkAlert.latestResultHref:
                print("First result is different!")
                print(updatedResultHref)
                print(checkAlert.latestResultHref)
                undetectedAlerts[updatedResult] = [priceColumn, expDateColumn, updatedResultHref]
                firstCheck = True  # to see if the first result is different or not
                continue
            else:
                break
        if firstCheck:
            if updatedResultHref == checkAlert.latestResultHref:  # using href since it is unique
                print("Found result at location " + str(i))
                checkAlert.latestResult = driver.find_elements(By.XPATH,
                                                               '//*[@id="router-root"]/div[1]/div/div[3]/div[3]/div/table/tbody/tr[1]/td[1]/a')
                checkAlert.latestResult = checkAlert.latestResult[0]
                checkAlert.latestResultHref = checkAlert.latestResult.get_attribute("href")
                break
            else:
                undetectedAlerts[updatedResult] = [priceColumn, expDateColumn, updatedResultHref]
        if i == 4:
            if updatedResultHref != checkAlert.latestResultHref:
                with open("log.txt", "a") as logfile:
                    logfile.write("New alerts did not match, resyncing")
                    print("New alerts did not match, resyncing\n\n")
                checkAlert.latestResult = driver.find_elements(By.XPATH, '//*[@id="router-root"]/div[1]/div/div[3]/div[3]/div/table/tbody/tr['+str(i)+']/td[1]/a')  # normally tr is 1
                checkAlert.latestResult = checkAlert.latestResult[0]
                checkAlert.latestResultHref = checkAlert.latestResult.get_attribute("href")
    return undetectedAlerts


def parseAlerts(alertElement, alertPrice, alertExpDate):
    returnedInformation = []
    textInfo = alertElement.text
    information = textInfo.split(' ')
    information[1] = information[1][1:]
    if str(information[2]) == "C":  # checks whether or not it is put or call
        information[2] = 'call'
    else:
        information[2] = 'put'
    returnedInformation += information
    returnedInformation.append(alertPrice.text[1:])
    parsedDate = alertExpDate.text.split('-')
    return returnedInformation, parsedDate


def createObjects(count):
    alerts = checkAlert(count)
    optionObjs = []
    for i in alerts:
        infoArray, dateArray = parseAlerts(i, alerts[i][0], alerts[i][1])
        website = alerts[i][2]
        expireDate = datetime.date(int(dateArray[0]), int(dateArray[1]), int(dateArray[2]))
        expireDate = expireDate - datetime.date.today()
        if expireDate.days >= 90:
            print(str(infoArray[0]) + " is not eligible because it is more than 90 days away!")
            continue
        else:
            for j in optionObjs:
                if j.href == website:
                    continue
            optionObjs.append(
                contract.Option(infoArray[1], infoArray[0], infoArray[2], infoArray[3], dateArray, website))
            print(str(infoArray[0]) + " has " + str(expireDate.days) + " days until it expires")
    return optionObjs


options = Options()
options.headless = True  # headless
options.add_argument('log-level=2')
directory = os.getcwd() + "\\data\\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=directory, options=options)
