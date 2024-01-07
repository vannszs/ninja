from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
# Set opsi untuk mempertahankan data sesi
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\selenium")  # Ganti dengan direktori yang sesuai

# Inisialisasi WebDriver dengan opsi yang disetel
driver = webdriver.Chrome(options=chrome_options)  # Ganti dengan WebDriver yang sesuai

def cek_total(row):
    print("============ cek  row  ================")
    driver.get('https://ninja.garden/rooms')
    row_error = 1
    while True:
        try:
            user_xpath = f'/html/body/div[2]/div/div/div[2]/div[{1}]'
            row_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, user_xpath)))
            break
        except:
            if row_error > 10:
                cek_total(row)
            print(f"menuggu row muncul")
            

    while True:
        try:
            user_xpath = f'/html/body/div[2]/div/div/div[2]/div[{row}]'
            row_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, user_xpath)))
            row+=1
        except:
            print(f"ditemukan {row} room")
            return row


def tulis(driver):
    print("================ tulis =================")
    error = 1
    loop = cek_total(1)
    for found_username in range(1, loop):
        try:
            driver.get('https://ninja.garden/rooms')
            user_xpath = f'/html/body/div[2]/div/div/div[2]/div[{loop}]'
            loop -=1
            user_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, user_xpath)))
            user_element.click()
            time.sleep(0.5)

            form_xpath = '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/input'
            form_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, form_xpath)))
            form_element.click()
            form_element.send_keys("PLEASE BUY MY KEY :(")
            form_element.send_keys(Keys.ENTER)
            
            print(f"Username '{found_username}' ditemukan dan pesan dikirim!")
            driver.get('https://ninja.garden/rooms')
            
        except Exception as e:
            if error < 5:
                print("ga ketemu")
                error += 1
            else:
                error = 1
                time.sleep(120)
                tulis(driver)
        
        error = 1
        loop -= 1

loop = True
while loop == True:
    tulis(driver)

