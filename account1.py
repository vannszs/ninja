from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
import json

 
def Validator(i,id,ids):
    print("========== THIS IS VALIDATOR PHASE ============")
    patient_zero = 0

    while True:
        try:
            if ids[i] in id:
                print(f"ID Found of rank {i}, Skip to Next User")
                break
            profile_url = "https://ninja.garden/profile/"
            url = f"{profile_url}{ids[i]}"
            print(f"Visit Rank {i}")
            driver.get(url)

            price_xpath = ( "/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]")
            price_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
            current_price = str(price_element.text)
            
            if ("0 INJ" in  current_price) and (patient_zero <= 5):
                patient_zero += 1
                continue
            elif patient_zero >= 5:
                i+=1
                continue
            else:
                Transaction(ids[i])
            break
        except Exception as e:
            print(e)
            print("Error Happened or fail to find xpath element")
            continue

def Transaction(id):
     patient_zero = 0
     
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
                        if id not in zero:
                            with open("zero.txt", "a", encoding="utf-8") as file:
                                file.write(f"{id}\n")
                        patient_zero += 1
                        break

                    elif patient_zero >5:
                        break
                elif "Successfully bought keys!" in message:
                    print("Transaksi berhasil!")
                    with open("done.txt", "a", encoding="utf-8") as file:
                        file.write(f"{id}\n")
                    break
                pass
            except:
                print("mencari elemnt")
                continue
        break



username = ""
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\selenium")
driver = webdriver.Chrome(options=chrome_options)

with open("leaderboard.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)
ids = [item["user"]["id"] for item in json_data["data"]]


try:
    with open("count.txt", "r") as count_file:
        i = int(count_file.read().strip())
except FileNotFoundError:
    i = 2000

total_ids = len(ids)

with open("done.txt", "r", encoding="utf-8") as file:
    id = [line.strip() for line in file.readlines()]

with open("zero.txt", "r", encoding="utf-8") as file:
    zero = [line.strip() for line in file.readlines()]

while i != total_ids:
    Validator(i,id,ids)
    i+=1
    with open("count.txt", "w") as counter:
        counter.write(str(i))