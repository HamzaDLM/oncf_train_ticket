from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from win10toast import ToastNotifier
import schedule
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Initiate notifier
toaster = ToastNotifier()

# Initiate variables
ALLER_DATE = os.environ('ALLER_DATE')
RETOUR_DATE = os.environ('RETOUR_DATE')
CARD_ID = os.environ('CARD_ID')
SLEEP_DURATION = os.environ('SLEEP_DURATION')
CRON_START_TIME = os.environ('CRON_START_TIME') #heroku uses UTC, UTC = GMT, but Morocco has GMT+1 so UTC is morrocan time -1h
FIRST_NAME = os.environ('FIRST_NAME')
LAST_NAME = os.environ('LAST_NAME')
EMAIL = os.environ('EMAIL')


def reserve_ticket(date=ALLER_DATE):
    ################### STEP 0
    # Chrome webdriver for heroku:
    toaster.show_toast("Train Ticket Script","Script will run.", duration=10)
    print('*** OPENING DRIVER', flush=True)
    gChromeOptions = webdriver.ChromeOptions()
    gChromeOptions.add_argument("window-size=1920x1480")
    # gChromeOptions.add_argument("--headless")
    gChromeOptions.add_argument("--disable-dev-shm-usage")
    gChromeOptions.add_argument("--no-sandbox")
    gChromeOptions.add_argument("--disable-gpu")
    driver = webdriver.Chrome(chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install())
    # Chrome webdriver for local
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    link = "https://www.oncf-voyages.ma/"
    driver.get(link)
    time.sleep(SLEEP_DURATION)
    print(driver.page_source)
    time.sleep(SLEEP_DURATION)

    #test if elements are found
    a = driver.find_elements_by_xpath('//*[@id="root"]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[1]/div[3]')
    print("-----------------------", flush=True)
    print(a, flush=True)
    b = driver.find_elements_by_css_selector("#root > section > div.ant-row > div.ant-col > main > div.b_homeBanner > div > div > div > div > div.SearchWidget_form.home > div > div.sc-bwzfXH.cbJdAM > div:nth-child(3)")
    print("-----------------------", flush=True)
    print(b, flush=True)
    c = driver.find_elements_by_class_name("sc-bxivhb")
    print("-----------------------", flush=True)
    print(c, flush=True)

    ################### STEP 1 
    # click reserve tab
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[1]/div[3]'))).click()
        # enter card type
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div"))).click()
        # click right card type
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[9]"))).click()
        # enter card code 
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchDataCode-0"]'))).send_keys(CARD_ID)
        # click on départ
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div"))).click()
        # choose départ
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[39]"))).click()
        # click on arrivée
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div/div"))).click()
        # choose arrivée
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div/ul/li[26]'))).click()
        time.sleep(SLEEP_DURATION)
        # open calendar
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.sc-EHOje:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)'))).click()
        time.sleep(SLEEP_DURATION)
        # chose après midi
        element = driver.find_element(By.CSS_SELECTOR, ".option-group-filter > label:nth-child(3) > span:nth-child(1) > input:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)
        # click on confirm
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]'))).click()
        # click on search 
        time.sleep(SLEEP_DURATION)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/button'))).click()
    except NoSuchElementException:
        pass

    print("---------------------------------------", flush=True)
    time.sleep(SLEEP_DURATION)
    print(driver.page_source, flush=True)
    ################### STEP 2
    Status = False
    increment = 1
    #wait for page to load:
    try:
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/button')))
    except:
        print("PAGE STILL NOT LOADED", flush=True)
    time.sleep(SLEEP_DURATION)

    while Status == False & int(increment) < 5:
        time.sleep(5)
        # Check date label associated to Div
        found_time = ''
        print("--------- increment: " + str(increment), flush=True)
        try:
            found_time = driver.find_element(By.XPATH, '//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[1]/div[1]/div/div[3]/div[1]/div/label[2]').text
            print(found_time, flush=True)
        except NoSuchElementException:
            print("error found", flush=True)
        if found_time == ALLER_DATE:
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
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/input'))).send_keys(FIRST_NAME)
                time.sleep(SLEEP_DURATION)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div/input'))).send_keys(LAST_NAME)
                time.sleep(SLEEP_DURATION)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div/input'))).send_keys(EMAIL)
                time.sleep(SLEEP_DURATION)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[5]/div/input'))).send_keys(EMAIL)
                time.sleep(SLEEP_DURATION)
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input'))).click()
                element = driver.find_element(By.XPATH, "/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(SLEEP_DURATION)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[3]/button'))).click()
                time.sleep(30)
                print("Train ticket reservation has completed, check email in your phone.", flush=True)
            except NoSuchElementException:
                print("error found", flush=True)
            #end operations
            time.sleep(15)
            toaster.show_toast("Train Ticket Script","Train ticket reservation has completed, check email in your phone.", duration=10)

            Status = True
        else:
            increment += 1
    driver.quit()


schedule.every().day.at(CRON_START_TIME).do(reserve_ticket)

while True:
    schedule.run_pending()
    time.sleep(1)