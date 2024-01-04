from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

import json

# Try reading the file using UTF-8 encoding
with open('newmem.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Extracting IDs from the loaded JSON
ids = [item['user']['id'] for item in json_data]

def remove_id_from_newmem_and_append_to_leaderboard(id_to_remove):
    # Baca data dari newmem.json
    with open('newmem.json', 'r') as file:
        newmem_data = json.load(file)

    # Cari data yang sesuai dengan ID yang akan dihapus
    data_to_remove = None
    for item in newmem_data:
        if item["user"]["id"] == id_to_remove:
            data_to_remove = item
            break

    if data_to_remove:
        # Hapus data dari newmem.json
        newmem_data.remove(data_to_remove)

        # Baca data dari leaderboard.json
        with open('leaderboard.json', 'r') as file:
            leaderboard_data = json.load(file)

        # Tambahkan data yang akan dihapus ke leaderboard.json
        leaderboard_data.append(data_to_remove)

        # Simpan kembali leaderboard.json dengan data baru
        with open('leaderboard.json', 'w') as file:
            json.dump(leaderboard_data, file)

        # Simpan kembali newmem.json tanpa data yang dihapus
        with open('newmem.json', 'w') as file:
            json.dump(newmem_data, file)

def validator(username,i):
    err = 1
    gagal = 1
    while True:
        print("================= VALIDATOR =================")
        init = 1
        try:
            
            first_button_xpath = '/html/body/main/div/div/div/div[1]/div[3]/div[2]/button'
            first_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, first_button_xpath)))
            first_button.click()
            print("first button clicked")

            

            second_button_xpath = '/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/button[1]'
            second_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, second_button_xpath)))
            second_button.click()
            print("second button clicked")


            third_button_xpath = '/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/button'
            third_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, third_button_xpath)))
            third_button.click()
            print(f"buy key {username}")
            buy = True


            while True:
                try:
                    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div')))
                    print("Element ditemukan.")
                    message = element.text

                    if "Failed to buy keys!" in message:
                        print("Transaksi gagal, menjalankan perform_action lagi.")
                        gagal +=1
                        i+=1
                        if gagal == 5:
                            visit_profiles_with_selenium(ids,i)
                        break
                    elif "Successfully bought keys!" in message:
                        print("Transaksi berhasil!")
                        with open("username.txt", "a", encoding='utf-8') as file:
                            file.write(username + "\n")
                        visit_profiles_with_selenium(ids,i)
                except:
                    print(init)
                    print("mencari elemnt")
                    if init >= 3:
                        init = 1
                        i+=1
                        visit_profiles_with_selenium(ids,i)
                    init += 1
                    continue
                
        except Exception as e:
            print(e)
            driver.refresh()
            if err ==3:
                visit_profiles_with_selenium(ids,i)
            err += 1
            continue

def visit_profiles_with_selenium(owner_ids,i):
    skip = 1
    print("=================visit==========================")
    base_url = "https://ninja.garden/profile/"

    for owner_id in owner_ids:
        profile_url = f"{base_url}{owner_ids[i]}"
        driver.get(profile_url)
        while True:
            try:
                keys_element_xpath = '/html/body/main/div/div/div/div[1]/div[2]'
                keys_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, keys_element_xpath)))
                keys_text = keys_element.text
                username_xpath = '/html/body/main/div/div/div/div[1]/div[3]/div[1]/div[1]'
                username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, username_xpath)))
                current_username = username_element.text
                price_xpath = '/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]'
                price_element = username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
                current_price = price_element.text
                print(f"{current_username}key price is {current_price}")
                
                with open("username.txt", "r", encoding='utf-8') as file:
                    usernames = [line.strip() for line in file.readlines()]
                if current_username not in usernames or (keys_text == "You hold 0 keys"):
                    i += 1
                    print(f"clicked {current_username}")
                    validator(current_username,i)
                elif current_username in usernames :
                    print(f"clicked {current_username}")
                    print(f"username  {current_username} already on the list ")
                    i += 1
                    break
                elif (current_price == "0 INJ"):
                    print(f"username  {current_username} the price is 0")
                    i += 1
                    break
                else:
                    i += 1
                    validator(current_username,i)
            except Exception as e:
                print(e)
                if (e) == "list index out of range":
                    break
                skip +=1
                print("Nenunggu element profil")
                if skip==5:
                    break
                time.sleep(5)
                continue
        pass



chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\selenium")
driver = webdriver.Chrome(options=chrome_options)
# Mengambil owner IDs


# Mengunjungi profil masing-masing owner menggunakan Selenium
visit_profiles_with_selenium(ids,1)
