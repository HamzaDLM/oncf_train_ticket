from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time
from win10toast import ToastNotifier
import schedule

# Initiate notifier
toaster = ToastNotifier()

# Initiate variables
go_date = '08:35'
back_date = '17:54'
sleep_duration = 2 # takes in consideration case of slow network
schedule_timer = '02:00' # Note: Heroku uses UTC, UTC = GMT, but Morocco has GMT+1 so UTC is Morrocan time -1h
driver_sleep = 30

# Sensitive data
card_id = '610179321001547'
firstname = 'Hamza'
lastname = 'Dellam'
email = 'hamzadellam@hotmail.com'


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
    time.sleep(sleep_duration) # wait page to load (in case of slow network)

    #### STEP 1 

    try:
        # click reserve tab
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[1]/div[3]'))).click()
        # enter card type (deuxième class)
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div"))).click()
        # click right card type
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[9]"))).click()
        # enter card code 
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchDataCode-0"]'))).send_keys(card_id)
        # click on départ
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div"))).click()
        # choose départ
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div/div/ul/li[39]"))).click()
        # click on arrivée
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div/div"))).click()
        # choose arrivée
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div/ul/li[26]'))).click()
        # open calendar
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.sc-EHOje:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)'))).click()
        # chose après midi
        element = driver.find_element(By.CSS_SELECTOR, ".option-group-filter > label:nth-child(3) > span:nth-child(1) > input:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)
        # click on confirm
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]'))).click()
        # click on search 
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div[1]/div/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div/button'))).click()
    except NoSuchElementException as e:
        print("Element not found: ", e)

    print("---------------------------------------", flush=True)
    time.sleep(sleep_duration)
    print(driver.page_source, flush=True)
    ################### STEP 2
    Status = False
    increment = 1
    #wait for page to load:
    try:
        WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/button')))
    except:
        print("PAGE STILL NOT LOADED", flush=True)
    time.sleep(sleep_duration)

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
                # Click on "Réserver"
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[1]/div[2]/div/button'))).click()
                # Click on "Selectioner"
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[2]/div/div/div[2]/div/div/div[1]/div/div/button'))).click()
                # Click on "Ajouté au panier"
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[5]/div[2]/div[' + str(increment) + ']/div[2]/div/div/div[2]/div/div[2]/div/div[2]/button'))).click()
                # Click on "Continuer"
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section/div[1]/div[2]/main/div/div/div/div[2]/div/footer/a/button'))).click()
                # Fill contact info forms
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/input'))).send_keys(firstname)
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div/input'))).send_keys(lastname)
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div/input'))).send_keys(email)
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[5]/div/input'))).send_keys(email)
                time.sleep(sleep_duration)
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input'))).click()
                element = driver.find_element(By.XPATH, "/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[10]/label/span[1]/input")
                driver.execute_script("arguments[0].click();", element)
                time.sleep(sleep_duration)
                WebDriverWait(driver, driver_sleep).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/section/div[1]/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[3]/button'))).click()
                time.sleep(driver_sleep)
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