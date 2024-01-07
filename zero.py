from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
import json

 
def Validator(i,id):
    print("========== THIS IS VALIDATOR PHASE ============")
    patient_zero = 0

    while True:
        try:
            if zero[i] in id:
                print(f"ID Found of rank {i}, Skip to Next User")
                break
            profile_url = "https://ninja.garden/profile/"
            url = f"{profile_url}{zero[i]}"
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
                Transaction(zero[i])
            break
        except Exception as e:
            print(e)
            print("Error Happened or fail to find xpath element")
            continue

def Transaction(idz):
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
        print(f"buy key of {idz}")
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
                                file.write(f"{idz}\n")
                        patient_zero += 1
                        success = True
                        break
                elif "Successfully bought keys!" in message:
                    success = True
                    print("Transaksi berhasil!")
                    with open("done.txt", "a", encoding="utf-8") as file:
                        file.write(f"{idz}\n")
                
                    # Remove ID from zero.txt if it exists
                    if idz in zero or idz in id:
                        with open("zero.txt", "r", encoding="utf-8") as file:
                            lines = file.readlines()
                        with open("zero.txt", "w", encoding="utf-8") as file:
                            for line in lines:
                                if line.strip() != id:
                                    file.write(line)
                        zero.remove(id)  # Remove ID from zero list in memory
                
                    break
                break
                success = False
            except:
                print("mencari elemnt")
                continue
        if success:
            break
        else:
            continue



username = ""
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\selenimu2")
driver = webdriver.Chrome(options=chrome_options)

with open("leaderboard.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)
ids = [item["user"]["id"] for item in json_data["data"]]


with open("done.txt", "r", encoding="utf-8") as file:
    id= [line.strip() for line in file.readlines()]
i = 1
total_ids = len(ids)

with open("zero.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    zero = [line.strip() for line in lines]



while i != total_ids:
    Validator(i,id)
    i+=1
    with open("count.txt", "w") as counter:
        counter.write(str(i))
driver.quit()