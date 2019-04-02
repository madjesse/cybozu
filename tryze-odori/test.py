import selenium, pyautogui, time, os.path, logging, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import data, functions

# driver = webdriver.Chrome("./chromedriver.exe")
# functions.login(driver)
# functions.get_facility(driver, "継続支援プラスタ")
# functions.get_post_board(driver)

# categories = driver.find_elements_by_css_selector(".gwBoardCollect__folder")
# for category in categories:
# 	items = category.find_elements_by_css_selector(".gwBoardCollect__board")
# 	print(len(items))

d = {"a": 1, "b": 2}
print(list(d.items()))
