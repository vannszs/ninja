from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
import json
import requests

 
def Validator(i,id,ids):
    print("========== THIS IS VALIDATOR PHASE ============")
    patient_zero = 0
    if ids[i] in id:
        print(f"ID Found of rank {i}, Skip to Next User")
        return i
    profile_url = "https://ninja.garden/profile/"
    url = f"{profile_url}{ids[i]}"
    driver.get(url)
    while True:
        try:
            price_xpath = ( "/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]")
            price_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
            current_price = str(price_element.text)
            first_button_xpath = (
                "/html/body/main/div/div/div/div[1]/div[3]/div[2]/button"
        )
            trade_xpath = "/html/body/main/div/div/div/div[3]/div"
            trade_elm  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, trade_xpath)))
            trade_stat = trade_elm.text
            print(f"Visit Rank {i}  with {current_price} Price")
            
            if ("0 INJ" in  current_price) and (patient_zero <= 5):
                patient_zero += 1
                continue
            elif patient_zero >= 5 and ("No data found" in trade_stat):
                break
            else:
                Transaction(ids[i])
            break
        except Exception as e:
            # if patient_zero == 20:
            #     break
            print("Error Happened or fail to find xpath element")
            continue

def Transaction(id):
     patient_zero = 0
     success = False
     
     while True:
        print("================= TRANSACTION PHASE =================")
        first_button_xpath = (
                "/html/body/main/div/div/div/div[1]/div[3]/div[2]/button"
        )
        first_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, first_button_xpath))
        )
        first_button.click()
        print("first button clicked")
        second_button_xpath = "/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/button[1]"
        second_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, second_button_xpath))
        )
        second_button.click()
        print("second button clicked")

        third_button_xpath = "/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/button"
        third_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, third_button_xpath))
        )
        third_button.click()
        print(f"buy key of {id}")
        price_xpath = ( "/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]")
        price_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
        current_price = str(price_element.text)

        while True:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "/html/body/div[3]/div/div")
                    )
                )
                print("Element ditemukan.")
                message = element.text
                if "Failed to buy keys!" in message:
                    print("Transaksi gagal, menjalankan perform_action lagi.")
                    if ("0 INJ" in  current_price) and (patient_zero <= 5):
                        print("Zero Price Detected")
                        patient_zero += 1
                        success = True
                        break
                elif "Successfully bought keys!" in message:
                    success = True
                    print("Transaksi berhasil!")
                    with open("done3.txt", "a", encoding="utf-8") as file:
                        file.write(f"{id}\n")
                    break
                break
                success = False
            except:
                print("mencari elemnt")
                patient_zero +=1
                if patient_zero == 10:
                    driver.refresh
                    Transaction(id)
                continue
        if success:
            break
        else:
            continue



username = ""
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\selenium3")
driver = webdriver.Chrome(options=chrome_options)

# with open("leaderboard.json", "r", encoding="utf-8") as file:
#     json_data = json.load(file)
# ids = [item["user"]["id"] for item in json_data["data"]]

response = requests.get("https://ninja.garden/api/points/leaderboard")

# Pastikan request berhasil dan responsenya valid
if response.status_code == 200:
    data = response.json()["data"]

    # Ambil nilai id dari setiap objek dalam data
    ids = [entry["user"]["id"] for entry in data]


try:
    with open("count3.txt", "r") as count_file:
        i = int(count_file.read().strip())
except FileNotFoundError:
    i = 2000

total_ids = len(ids)

with open("done3.txt", "r", encoding="utf-8") as file:
    id = [line.strip() for line in file.readlines()]


while i != total_ids:
    Validator(i,id,ids)
    i+=1
    with open("count3.txt", "w") as counter:
        counter.write(str(i))

driver.quit()