from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_owner_ids():
    url = "https://ninja.garden/api/rooms/new"
    response = requests.get(url)

    owner_ids = []

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            for room_data in data["data"]:
                owner_id = room_data["stats"]["owner_id"]
                owner_ids.append(owner_id)
        else:
            print("Gagal mendapatkan data dari API")
    else:
        print("Gagal melakukan permintaan ke API")

    return owner_ids

def validator(username):
    i = 1
    err = 1
    gagal = 1
    while True:
        print("================= VALIDATOR =================")
        init = 1
        with open("count2.txt", "w") as count_file:
             count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt
        try:
            
            first_button_xpath = '/html/body/main/div/div/div/div[1]/div[3]/div[2]/button'
            first_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, first_button_xpath)))
            first_button.click()
            print("first button clicked")
            with open("count2.txt", "w") as count_file:
                count_file.write(str(i-1))  # Menulis nilai terakhir i ke count2.txt
            

            second_button_xpath = '/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/button[1]'
            second_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, second_button_xpath)))
            second_button.click()
            print("second button clicked")


            third_button_xpath = '/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/button'
            third_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, third_button_xpath)))
            third_button.click()
            print(f"buy key {username}")
            with open("count2.txt", "w") as count_file:
                count_file.write(str(i+1))  # Menulis nilai terakhir i ke count2.txt
            buy = True


            while True:
                try:
                    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div')))
                    print("Element ditemukan.")
                    message = element.text

                    if "Failed to buy keys!" in message:
                        print("Transaksi gagal, menjalankan perform_action lagi.")
                        gagal +=1
                        
                        if gagal == 5:
                            with open("count2.txt", "w") as count_file:
                                count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt
                            visit_profiles_with_selenium(owners)
                        break
                    elif "Successfully bought keys!" in message:
                        print("Transaksi berhasil!")
                        visit_profiles_with_selenium(owners)
                        with open("user2.txt", "a", encoding='utf-8') as file:
                            file.write(username + "\n")
                except:
                    print(init)
                    print("mencari elemnt")
                    if init >= 3:
                        with open("count2.txt", "w") as count_file:
                            count_file.write(str(i-1))  # Menulis nilai terakhir i ke count2.txt
                        init = 1
                        visit_profiles_with_selenium(owners)
                    init += 1
                    continue
                
        except Exception as e:
            print(e)
            driver.refresh()
            if err ==20:
                visit_profiles_with_selenium(owners)
            err += 1
            continue

def visit_profiles_with_selenium(owner_ids):
    skip = 1
    print("=================visit==========================")
    base_url = "https://ninja.garden/profile/"
    i = 1
    for owner_id in owner_ids:
        profile_url = f"{base_url}{owner_id}"
        driver.get(profile_url)
        while True:
            try:
                keys_element_xpath = '/html/body/main/div/div/div/div[1]/div[2]'
                keys_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, keys_element_xpath)))
                keys_text = keys_element.text
                username_xpath = '/html/body/main/div/div/div/div[1]/div[3]/div[1]/div[2]'
                username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, username_xpath)))
                current_username = username_element.text
                price_xpath = '/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]'
                price_element = username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
                current_price = price_element.text
                print(f"{current_username}key price is {current_price}")
                
                with open("user.txt", "r", encoding='utf-8') as file:
                    usernames = [line.strip() for line in file.readlines()]
                if current_username not in usernames or (keys_text == "You hold 0 keys"):
                    i += 1
                    print(f"clicked {current_username}")
                    validator(current_username)
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
                    validator(current_username)
            except Exception as e:
                print(e)
                skip +=1
                print("Nenunggu element profil")
                if skip==5:
                    break
                time.sleep(5)
                continue



def perform_action(driver, error_count=0):
    print("================ PERFORM ==================")
    try:
        with open("count2.txt", "r") as count_file:
            i = int(count_file.read().strip())
    except FileNotFoundError:
        i = 2000  # Jika file count2.txt belum ada

    while i <= 5000:
        try:
            driver.get('https://ninja.garden/profil')
            time.sleep(3)
            transaction_element_xpath = f'/html/body/div[2]/div/div[1]/div[3]/div/a[{i}]'
            transaction_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, transaction_element_xpath)))
            transaction_element.click()
            
            print(f"rank {i}")
            skip = 0
            while True:
                try:
                    keys_element_xpath = '/html/body/main/div/div/div/div[1]/div[2]'
                    keys_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, keys_element_xpath)))
                    keys_text = keys_element.text
                    username_xpath = '/html/body/main/div/div/div/div[1]/div[3]/div[1]/div[2]'
                    username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, username_xpath)))
                    current_username = username_element.text
                    time.sleep(1)
                    price_xpath = '/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]'
                    price_element = username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
                    current_price = price_element.text
                    print(f"{current_username}key price is {current_price}")
                    

                    with open("user2.txt", "r", encoding='utf-8') as file:
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
                except:
                    skip +=1
                    print("Nenunggu element profil")
                    if skip==5:
                        break
                    time.sleep(5)
                    continue

        except Exception as e:
            print(e)
            with open("count2.txt", "w") as count_file:
                count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt
            
            # Limit jika terjadi kesalahan berulang
            if error_count >= 2:
                driver.refresh()  # Membuka kembali browser
                visit_profiles_with_selenium(owners)
                return False
            error_count += 1
            
            print(f"error terjadi sebanyak {error_count}\nRestart ")
            print(f"returned to number {i}")


chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\selenium")
driver = webdriver.Chrome(options=chrome_options)
# Mengambil owner IDs


owners = get_owner_ids()
# Mengunjungi profil masing-masing owner menggunakan Selenium
visit_profiles_with_selenium(owners)
