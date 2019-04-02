import data
import functions as f

# ============do NOT modify===========================
# configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.CRITICAL)
print("Press ctrl + c to quit.\n")

# driver
driver = webdriver.Chrome("./chromedriver.exe")
# login
f.login(driver)

# loop through the facility dict to perform the relevant downloading: the outmost loop=====================================================================================
for facility_jp_name, facility_en_name in data.FACILITY.items():
	# pass the 2 facilities whose downloading has completed
	if facility_jp_name == "継続支援トラビズ" or facility_jp_name == "継続支援コネクトワークス大通東":
		continue
	# click the facility link to proceed to the next page
	f.get_facility(facility_jp_name)

	# get into the post board, scroll down to the bottom and click the collecting link
	f.get_post_board(driver)

	# build the dict for the facility
	category_dict = f.construct_dict(driver)




# loop through the constructed dict to download each file
for categoryName, itemNum in categoryDict.items():
	fileIndex = 1
	if itemNum > 0:
		for i in range(1, itemNum + 1):
			# get parent element each time backed to the original page
			categoryElement = driver.find_element_by_css_selector(".gwBoardCollect__folder:nth-child(%s)" %str(categoryNames.index(categoryName) + 1))
			links = categoryElement.find_elements_by_css_selector(".gwBoardCollect__board")
			# get each anchor element
			while True:
				try:
					link = categoryElement.find_element_by_css_selector(".gwBoardCollect__board:nth-child(%s) a:nth-child(2)" %str(i))
				except:
					time.sleep(0.5)
				else:
					titleText = link.find_element_by_css_selector("span").text
					break
	
			# click the link 
			link.click()
			time.sleep(1)
			# press ctrl + s to save it 
			pyautogui.hotkey('ctrl', 's')
			time.sleep(1)
			# press delete to delete text in filename area
			pyautogui.press("delete")
			time.sleep(0.5)
# ==========================================================

			# type in new file name according to category
			# if the category is date-relevant, get the titleText using the regex and use the text to construct filenames

# =================modify the category names that are date-relevant==========================================
			if categoryName == "morning2019" or categoryName == "meeting2019":
				match = regex.findall(titleText)
				dates = match[0].split("/")
				dateString = "".join(dates)
# ================modify the filename constructor===========================================
				filename = "connect-%s-%s.html" %(categoryName, dateString)
			# otherwise use the following filename constructor
			else:
				filename = "connect-%s-%s.html" %(categoryName, str(fileIndex))

# ==========================do NOT modify===============================================
			pyautogui.typewrite(filename)
			time.sleep(1)
			# press return to ok 
			pyautogui.press('return')
			# log info of save file 
			logging.debug("%s: %s", str(categoryNames.index(categoryName) + 1), str(i))
			# wait until download is completed
			filepath = "c:\\Users\\user\\Downloads\\%s" %filename
			i = 0
			while not os.path.exists(filepath):
				time.sleep(1)
				logging.debug("saving...")
				i += 1
				if i == 10:
					# press ctrl + s to save it 
					pyautogui.hotkey('ctrl', 's')
					time.sleep(1)
					# press delete to delete text in filename area
					pyautogui.press("delete")
					time.sleep(0.5)
					# type in new file name 
					# type in new file name according to category

# =================modify the category names that are date-relevant==========================================
					if categoryName == "morning2019" or categoryName == "meeting2019":
						match = regex.findall(titleText)
						dates = match[0].split("/")
						dateString = "".join(dates)
# ================modify the filename constructor===========================================
						filename = "connect-%s-%s.html" %(categoryName, dateString)
					# otherwise use the following filename constructor
					else:
						filename = "connect-%s-%s.html" %(categoryName, str(fileIndex))

# =================================do NOT modify========================================
					pyautogui.typewrite(filename)
					time.sleep(1)
					# press return to ok 
					pyautogui.press('return')
					# log info of save file 
					logging.debug("%s: %s", str(categoryNames.index(categoryName) + 1), str(i))
			logging.debug("%s is saved as %s.\n" %(titleText, filename))

			fileIndex += 1
			# back
			driver.back()
			time.sleep(1)