from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
# from win10toast import ToastNotifier
import schedule

#Initiate notifier
# toaster = ToastNotifier()
print('*** OPENING FIREFOX BROWSER ', flush=True)

#Initiate variables
go_date = '08:35'
back_date = '17:54'
card_id = '610179321001547'
sleep_duration = 2
schedule_timer = "04:00" #heroku uses UTC, UTC = GMT, but Morocco has GMT+1 so UTC is morrocan time -1h


def reserve_ticket(date=go_date):
    ################### STEP 0
    # Chrome webdriver for heroku:
    gChromeOptions = webdriver.ChromeOptions()
    gChromeOptions.add_argument("window-size=1920x1480")
    gChromeOptions.add_argument("--headless")
    gChromeOptions.add_argument("--disable-dev-shm-usage")
    gChromeOptions.add_argument("--no-sandbox")
    gChromeOptions.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install())
    # Chrome webdriver for local
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    link = "https://www.oncf-voyages.ma/"
    driver.get(link)
    time.sleep(sleep_duration)
    print(driver.page_source)
    time.sleep(sleep_duration)
    ################### STEP 1 
    # click reserve tab
    try:
        a = driver.find_elements_by_xpath('/html/body/div/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[1]/div[3]').click()
        time.sleep(sleep_duration)
        print(driver.page_source)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[1]/div[3]'))).click()
        # enter card type
        time.sleep(sleep_duration)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div"))).click()
        # click right card type
        time.sleep(sleep_duration)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[9]"))).click()
        # enter card code 
        time.sleep(sleep_duration)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchDataCode-0"]'))).send_keys(card_id)
        # click on départ
        time.sleep(sleep_duration)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div"))).click()
        # choose départ
        time.sleep(sleep_duration)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[39]"))).click()
        # click on arrivée
        time.sleep(sleep_duration)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div/div"))).click()
        # choose arrivée
        time.sleep(sleep_duration)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div/ul/li[26]'))).click()
        time.sleep(sleep_duration)
        # open calendar
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.sc-EHOje:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)'))).click()
        time.sleep(sleep_duration)
        # chose après midi
        element = driver.find_element(By.CSS_SELECTOR, ".option-group-filter > label:nth-child(3) > span:nth-child(1) > input:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)
        # click on confirm
        time.sleep(sleep_duration)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]'))).click()
        # click on search 
        time.sleep(sleep_duration)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/button'))).click()
    except NoSuchElementException:
        pass
    
    ################### STEP 2
    Status = False
    increment = 1
    #wait for page to load:
    try:
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/button')))
    except:
        print("PAGE STILL NOT LOADED", flush=True)
    time.sleep(sleep_duration)

    while Status == False & increment < 5:
        time.sleep(5)
        # Check date label associated to Div
        found_time = ''
        print("--------- increment: " + str(increment), flush=True)
        try:
            found_time = driver.find_element(By.XPATH, '//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[1]/div[1]/div/div[3]/div[1]/div/label[2]').text
            print(found_time, flush=True)
        except NoSuchElementException:
            print("error found", flush=True)
        if found_time == go_date:
            try:
                # Click on "Réserver"
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[1]/div[2]/div/button'))).click()
                # Click on "Selectioner"
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[2]/div/div/div[2]/div/div/div[1]/div/div/button'))).click()
                # Click on "Ajouté au panier"
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[2]/div/div/div[2]/div/div[2]/div/div[2]/button'))).click()
                # Click on "Continuer"
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[2]/div/footer/a/button'))).click()
                # Fill contact info forms
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/input'))).send_keys('Hamza')
                time.sleep(sleep_duration)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div/input'))).send_keys('Dellam')
                time.sleep(sleep_duration)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div/input'))).send_keys('hamzadellam@hotmail.com')
                time.sleep(sleep_duration)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[5]/div/input'))).send_keys('hamzadellam@hotmail.com')
                time.sleep(sleep_duration)
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input'))).click()
                element = driver.find_element(By.XPATH, "/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(sleep_duration)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[3]/button'))).click()
                time.sleep(30)
                print("Train ticket reservation has completed, check email in your phone.", flush=True)
            except NoSuchElementException:
                print("error found", flush=True)
            #end operations
            # time.sleep(15)
            # toaster.show_toast("Train Ticket Script","Train ticket reservation has completed, check email in your phone.", duration=10)
            # driver.quit()
            Status = True
        elif increment == 4:
            increment +=1
            # toaster.show_toast("Train Ticket Script","[N] Date check is unsuccessfull, operation halted !", duration=10)
        else:
            increment += 1


# schedule.every().day.at(schedule_timer).do(reserve_ticket)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


reserve_ticket()




















        # #aller
        # time.sleep(5)
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + int(increment) + ']/div[1]/div[2]/div/button'))).click()
        # time.sleep(sleep_duration)
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + int(increment) + ']/div[2]/div/div/div[2]/div/div/div[1]/div/div/button'))).click()
        # time.sleep(sleep_duration)
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + int(increment) + ']/div[2]/div/div/div[2]/div/div[2]/div/div[2]/button'))).click()
        # #retour (disabled ftm)
        # # time.sleep(3)
        # # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[6]/div[2]/div[5]/div[1]/div[2]/div/button'))).click()
        # # time.sleep(sleep_duration)
        # # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[6]/div[2]/div[5]/div[2]/div/div/div[2]/div/div/div[1]/div/div/button'))).click()
        # # time.sleep(sleep_duration)
        # # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[6]/div[2]/div[5]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/button'))).click()
        # #continuer
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[2]/div/footer/a/button'))).click()

        
        # #check if the times are correct
        # import datetime
        # import re
        # from bs4 import BeautifulSoup

        # time.sleep(3)
        # html = driver.page_source
        # soup = BeautifulSoup(html, 'html.parser')

        # if result[0] == go_date:
        #     print('[Y] Date check successful !')
        #     toaster.show_toast("Train Ticket Script","[Y] Date check successful !", duration=10)
        #     #fill info
        #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/input'))).send_keys('Hamza')
        #     time.sleep(sleep_duration)
        #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div/input'))).send_keys('Dellam')
        #     time.sleep(sleep_duration)
        #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div/input'))).send_keys('hamzadellam@hotmail.com')
        #     time.sleep(sleep_duration)
        #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[5]/div/input'))).send_keys('hamzadellam@hotmail.com')
        #     time.sleep(sleep_duration)
        #     # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input'))).click()
        #     element = driver.find_element(By.XPATH, "/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input")
        #     driver.execute_script("arguments[0].click();", element)
        #     time.sleep(sleep_duration)
        #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[3]/button'))).click()
        #     #end operations
        #     time.sleep(15)
        #     if result[1] == back_date:
        #         toaster.show_toast("Train Ticket Script","Train ticket reservation has completed, check email in your phone.", duration=10)
        #     if result[1] != back_date:    
        #         toaster.show_toast("Train Ticket Script","Train ticket reservation has completed, evening ticket doesn't match recommended time. Check email in your phone.", duration=10)
        #     driver.quit()
        #     Status = True
        # else: 
        #     print('[N] Date check is unsuccessfull, operation halted !')
        #     toaster.show_toast("Train Ticket Script","[N] Date check is unsuccessfull, operation halted !", duration=10)
        #     time.sleep(15)

