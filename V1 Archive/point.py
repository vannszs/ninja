from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
import random
username = ''
def validator(username,i):
    err = 1
    gagal = 1
    while True:
        print("================= VALIDATOR =================")
        init = 1
        with open("count.txt", "w") as count_file:
             count_file.write(str(i))  # Menulis nilai terakhir i ke count.txt
        try:
            
            first_button_xpath = '/html/body/main/div/div/div/div[1]/div[3]/div[2]/button'
            first_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, first_button_xpath)))
            first_button.click()
            print("first button clicked")
            with open("count.txt", "w") as count_file:
                count_file.write(str(i-1))  # Menulis nilai terakhir i ke count.txt
            

            second_button_xpath = '/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/button[1]'
            second_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, second_button_xpath)))
            second_button.click()
            print("second button clicked")


            third_button_xpath = '/html/body/div[5]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/button'
            third_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, third_button_xpath)))
            third_button.click()
            print(f"buy key {username}")
            with open("count.txt", "w") as count_file:
                count_file.write(str(i+1))  # Menulis nilai terakhir i ke count.txt
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
                            with open("count.txt", "w") as count_file:
                                count_file.write(str(i))  # Menulis nilai terakhir i ke count.txt
                            perform_action(driver)
                        break
                    elif "Successfully bought keys!" in message:
                        print("Transaksi berhasil!")
                        perform_action(driver)
                        with open("user.txt", "a", encoding='utf-8') as file:
                            file.write(username + "\n")
                except:
                    print(init)
                    print("mencari elemnt")
                    if init >= 3:
                        with open("count.txt", "w") as count_file:
                            count_file.write(str(i-1))  # Menulis nilai terakhir i ke count.txt
                        init = 1
                        perform_action(driver)
                    init += 1
                    continue
                
        except Exception as e:
            print(e)
            driver.refresh()
            if err ==20:
                perform_action(driver)
            err += 1
            continue


def perform_action(driver, error_count=0):
    print("================ PERFORM ==================")
    try:
        with open("count.txt", "r") as count_file:
            i = int(count_file.read().strip())
    except FileNotFoundError:
        i = 2000  # Jika file count.txt belum ada

    while i <= 7000:
        try:
            driver.get('https://ninja.garden/leaderboard')
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
                    price_xpath = '/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]'
                    price_element = username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
                    current_price = str(price_element.text)
                    print(f"{current_username}key price is {current_price}")
                    

                    with open("user.txt", "r", encoding='utf-8') as file:
                        usernames = [line.strip() for line in file.readlines()]
                    if current_username not in usernames or keys_text == "You hold 0 keys":
                        i += 1
                        print(f"clicked {current_username}")
                        validator(current_username,i)
                    elif current_username in usernames :
                        print(f"clicked {current_username}")
                        print(f"username  {current_username} already on the list ")
                        i += 1
                        break
                    elif current_price == "0 INJ":
                        print(f"clicked {current_username}")
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
            with open("count.txt", "w") as count_file:
                count_file.write(str(i))  # Menulis nilai terakhir i ke count.txt
            
            # Limit jika terjadi kesalahan berulang
            if error_count >= 2:
                driver.refresh()
  # Membuka kembali browser
                perform_action(driver)
                return False

            error_count += 1
            
            print(f"error terjadi sebanyak {error_count}\nRestart ")
            print(f"returned to number {i}")

            



        

# Set opsi untuk mempertahankan data sesi
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=D:\\selenium")  # Ganti dengan direktori yang sesuai

# Inisialisasi WebDriver dengan opsi yang disetel
driver = webdriver.Chrome(options=chrome_options)  # Ganti dengan WebDriver yang sesuai

init = 0

# if perform_action == False:
#     driver.quit()

while True:
    success = perform_action(driver)
    if not perform_action:
        print("kembali ke main")
        perform_action(driver)
        if success:
            continue

        






