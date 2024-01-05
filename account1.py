from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
import json

 
def Validator(i,usernames):
    print("========== THIS IS VALIDATOR PHASE ============")
    
    while True:
        try:
            profile_url = "https://ninja.garden/profile/"
            url = f"{profile_url}{ids[i]}"
            print(f"Visit Rank {i}")
            driver.get(url)

            username_xpath = "/html/body/main/div/div/div/div[1]/div[3]/div[1]/div[1]"
            username_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, username_xpath)))
            current_username = username_element.text

            if current_username in usernames:
                with open("done.txt", "a") as id_user:
                    id_user.write(f"{ids[i]}\n")  # Menulis ID ke file
                print("Username Found and wrote the ID")


            break
            # elif current_username in username:
            #     with open("done.txt","W") as id_user:
            #         id_user.write(f"ids{i}")
                


        except Exception as e:
            print(e)
            print("Error Happened or fail to find xpath element")


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

with open("username.txt", "r", encoding="utf-8") as file:
    usernames = [line.strip() for line in file.readlines()]

while True:
    Validator(i,usernames)
    i+=1
    with open("count.txt", "w") as counter:
        counter.write(str(i))