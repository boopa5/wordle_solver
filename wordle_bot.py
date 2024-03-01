from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import wordle_logic

class Color:
    GRAY = 0
    YELLOW = 1
    GREEN = 2

driver = webdriver.Chrome()

driver.get("https://www.nytimes.com/games/wordle/")
driver.maximize_window()

play_button = driver.find_element(By.CLASS_NAME, "Welcome-module_button__ZG0Zh")
play_button.click()

x_button = driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb")
x_button.click()

input_field = driver.find_element(By.TAG_NAME, "body")

time.sleep(2)
best_guess = "crane"

for i in range(6):

    input_field.send_keys(best_guess)
    input_field.send_keys(Keys.ENTER)
    time.sleep(5)

    tiles = driver.find_elements(By.CLASS_NAME, "Tile-module_tile__UWEHN")
    tiles_of_interest = tiles[5*i : 5*(i+1)]

    pattern = []
    for tile in tiles_of_interest:
        result = tile.get_attribute("aria-label")
        if result[15] == "a": pattern.append(Color.GRAY)
        elif result[15] == "p": pattern.append(Color.YELLOW)
        else: pattern.append(Color.GREEN)

    

    
    
    time.sleep(5)

driver.quit()