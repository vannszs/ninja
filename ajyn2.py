from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.common.exceptions import NoSuchElementException

username = ""
# import requests

# # Lakukan request ke API
# response = requests.get("https://ninja.garden/api/points/leaderboard")

# # Pastikan request berhasil dan responsenya valid
# if response.status_code == 200:
#     data = response.json()["data"]

#     # Ambil nilai id dari setiap objek dalam data
#     ids = [entry["user"]["id"] for entry in data]
# else:
#     print("Failed to fetch data from the API")

with open("leaderboard.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

ids = [item["user"]["id"] for item in json_data["data"]]


def validator(username, i):
    err = 1
    gagal = 1
    while True:
        print("================= VALIDATOR =================")
        init = 1
        with open("count2.txt", "w") as count_file:
            count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt
        try:
            price_xpath = "/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]"
            price_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, price_xpath))
            )
            current_price = str(price_element.text)
            trade_xpath = "/html/body/main/div/div/div/div[3]/div"
            trade_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, trade_xpath))
            )
            trade_text = trade_element.text

            with open("username.txt", "r", encoding="utf-8") as file:
                usernames = [line.strip() for line in file.readlines()]
            if (current_price == "0 INJ") or (trade_text == "No data found"):
                print(f"username  {username} the price is 0")
                with open("count2.txt", "w") as count_file:
                    count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt
                perform_action(driver)
            elif username in usernames:
                print(f"clicked {username}")
                print(f"username  {username} already on the list ")
                with open("count2.txt", "w") as count_file:
                    count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt

            first_button_xpath = (
                "/html/body/main/div/div/div/div[1]/div[3]/div[2]/button"
            )
            first_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, first_button_xpath))
            )
            first_button.click()
            print("first button clicked")
            with open("count2.txt", "w") as count_file:
                count_file.write(str(i - 1))  # Menulis nilai terakhir i ke count2.txt

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
            print(f"buy key {username}")
            with open("count2.txt", "w") as count_file:
                count_file.write(str(i + 1))  # Menulis nilai terakhir i ke count2.txt
            buy = True
            time.sleep(1)

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
                        gagal += 1
                        i += 1
                        if gagal == 5:
                            driver.refresh()
                            time.sleep(2)
                            if current_price == "0 INJ":
                                print(f"username  {username} the price is 0")
                                with open("count2.txt", "w") as count_file:
                                    count_file.write(
                                        str(i)
                                    )  # Menulis nilai terakhir i ke count2.txt
                                perform_action(driver)
                        break
                    elif "Successfully bought keys!" in message:
                        print("Transaksi berhasil!")
                        with open("username.txt", "a", encoding="utf-8") as file:
                            file.write(username + "\n")
                        perform_action(driver)

                except:
                    print(init)
                    print("mencari elemnt")
                    if init >= 3:
                        with open("count2.txt", "w") as count_file:
                            count_file.write(
                                str(i - 1)
                            )  # Menulis nilai terakhir i ke count2.txt
                        init = 1
                        perform_action(driver)
                    init += 1
                    continue

        except Exception as e:
            print(e)
            driver.refresh()
            if (current_price == "0 INJ") and (trade_text == "No data found"):
                print(f"username  {username} the price is 0")
                with open("count2.txt", "w") as count_file:
                    count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt
                perform_action(driver)
            if err == 20:
                perform_action(driver)
            err += 1
            continue


def perform_action(driver):
    print("================ PERFORM ==================")
    try:
        with open("count2.txt", "r") as count_file:
            i = int(count_file.read().strip())
    except FileNotFoundError:
        i = 2000

    while i <= 7000:
        try:
            base_url = "https://ninja.garden/profile/"
            profile_url = f"{base_url}{ids[i]}"
            driver.get(profile_url)
            time.sleep(1)
            username_xpath = "/html/body/main/div/div/div/div[1]/div[3]/div[1]/div[2]"
            username_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, username_xpath))
            )
            current_username = username_element.text

            print(f"rank {i}")
            skip = 0
            while True:
                try:

                    keys_element_xpath = "/html/body/main/div/div/div/div[1]/div[2]"
                    keys_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, keys_element_xpath))
                    )
                    keys_text = keys_element.text

                    time.sleep(2)
                    with open("username.txt", "r", encoding="utf-8") as file:
                        usernames = [line.strip() for line in file.readlines()]
                    price_xpath = (
                        "/html/body/main/div/div/div/div[1]/div[4]/div[1]/div[1]"
                    )
                    price_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, price_xpath))
                    )
                    current_price = str(price_element.text)
                    trade_xpath = "/html/body/main/div/div/div/div[3]/div"
                    trade_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, trade_xpath))
                    )
                    trade_text = trade_element.text
                    if (current_price == "0 INJ") or (trade_text == "No data found"):
                        print(f"username  {current_username} the price is 0")
                        with open("count2.txt", "w") as count_file:
                            count_file.write(
                                str(i + 1)
                            )  # Menulis nilai terakhir i ke count2.txt
                        perform_action(driver)
                    print(f"{current_username}key price is {current_price}")

                    if current_username not in usernames or (
                        keys_text == "You hold 0 keys"
                    ):
                        i += 1
                        print(f"clicked {current_username}")
                        validator(current_username, i)
                    elif current_username in usernames:
                        print(f"clicked {current_username}")
                        print(f"username  {current_username} already on the list ")
                        i += 1
                        break
                    else:
                        i += 1
                        validator(current_username, i)
                except:
                    skip += 1
                    print("Nenunggu element profil")
                    if skip == 5:
                        break
                    time.sleep(5)
                    continue

        except Exception as e:
            print(e)
            with open("count2.txt", "w") as count_file:
                count_file.write(str(i))  # Menulis nilai terakhir i ke count2.txt
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
chrome_options.add_argument(
    "--user-data-dir=D:\\selenium2"
)  # Ganti dengan direktori yang sesuai

# Inisialisasi WebDriver dengan opsi yang disetel
driver = webdriver.Chrome(options=chrome_options)  # Ganti dengan WebDriver yang sesuai

init = 0

while True:
    success = perform_action(driver)
    if not perform_action:
        print("kembali ke main")
        perform_action(driver)
        if success:
            continue
