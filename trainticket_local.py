from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
from win10toast import ToastNotifier
from dotenv import load_dotenv

# Load environment variables
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


def reserve_ticket(date=go_date):
    """
    1- Open chrome driver
    2- Fill in card info
    3- Search and select designated ticket
    4- Fill contact info
    5- Submit
    """
    #### STEP 0

    toaster.show_toast("Train Ticket Script","Script will run.", duration=10)
    
    gChromeOptions = webdriver.ChromeOptions()
    gChromeOptions.add_argument("window-size=1920x1480")
    # gChromeOptions.add_argument("--headless") # Activate when hosting the app
    gChromeOptions.add_argument("--disable-dev-shm-usage")
    gChromeOptions.add_argument("--no-sandbox")
    gChromeOptions.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install())
    
    link = "https://www.oncf-voyages.ma/"
    driver.get(link)
    time.sleep(SLEEP_DURATION) # wait page to load (in case of slow network)

    #### STEP 1 

    try:
        # click reserve tab
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[1]/div[3]'))).click()
        # enter card type (deuxi??me class)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div"))).click()
        # click right card type
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[9]"))).click()
        # enter card code 
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchDataCode-0"]'))).send_keys(card_id)
        # click on d??part
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div"))).click()
        # choose d??part
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[39]"))).click()
        # click on arriv??e
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div/div"))).click()
        # choose arriv??e
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div/ul/li[26]'))).click()
        # open calendar
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.sc-EHOje:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)'))).click()
        # chose apr??s midi
        element = driver.find_element(By.CSS_SELECTOR, ".option-group-filter > label:nth-child(3) > span:nth-child(1) > input:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)
        # click on confirm
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]'))).click()
        # click on search 
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/button'))).click()
    except NoSuchElementException as e:
        print("Element not found: ", e)

    print("---------------------------------------", flush=True)
    time.sleep(SLEEP_DURATION)
    print(driver.page_source, flush=True)
    ################### STEP 2
    Status = False
    increment = 1
    #wait for page to load:
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/button')))
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
        if found_time == go_date:
            try:
                # Click on "R??server"
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[1]/div[2]/div/button'))).click()
                # Click on "Selectioner"
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[2]/div/div/div[2]/div/div/div[1]/div/div/button'))).click()
                # Click on "Ajout?? au panier"
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[2]/div/div/div[2]/div/div[2]/div/div[2]/button'))).click()
                # Click on "Continuer"
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[2]/div/footer/a/button'))).click()
                # Fill contact info forms
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/input'))).send_keys(FIRST_NAME)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div/input'))).send_keys(LAST_NAME)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div/input'))).send_keys(EMAIL)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[5]/div/input'))).send_keys(EMAIL)
                time.sleep(SLEEP_DURATION)
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input'))).click()
                element = driver.find_element(By.XPATH, "/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(SLEEP_DURATION)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[3]/button'))).click()
                time.sleep(30)
                print("Train ticket reservation has completed, check email in your phone.", flush=True)
            except NoSuchElementException:
                print("error found", flush=True)
            #end operations
            # time.sleep(15)
            toaster.show_toast("Train Ticket Script","Train ticket reservation has completed, check email in your phone.", duration=10)

            Status = True
        else:
            increment += 1
    driver.quit()


if __name__ == "__main__":
    reserve_ticket()