import selenium, pyautogui, time, os.path, logging, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.CRITICAL)
print("Press ctrl + c to quit.\n")
# login
loginUrl = "https://cybozulive.com/login?dummy=1552289327620"
driver = webdriver.Chrome("./chromedriver.exe")
driver.get(loginUrl)
try:
	userName = driver.find_element_by_name('loginMailAddress')
	userName.send_keys('c.wei@yokazu.co.jp')
	password = driver.find_element_by_name('password')
	password.send_keys('wei880830')
except:
	raise Exception("login failed.\n")
else:
	password.send_keys(Keys.RETURN)
time.sleep(1)

# click 継続支援トラビズ
linkElement = driver.find_element_by_xpath("//a[@class='groupwareList__groupwareName '][@title='継続支援トラビズ']")
linkElement.click()
time.sleep(1)

# click 掲示板
infoElement = driver.find_element_by_xpath("//a[@title='掲示板']")
infoElement.click()
time.sleep(1)

# scroll to the bottom
pyautogui.moveTo(100, 500, duration=0.25)
time.sleep(1)
pyautogui.scroll(-4000)
time.sleep(1)

# click　まとめ
listElement = driver.find_element_by_css_selector(".collectLink")
listElement.click()
time.sleep(1)

# this is the main part
# basic data
# get category names
categoryNames = ["morning2019", "morning2018", "confirm2019", "confirm2018", "meeting2019", "meeting2018", "info2019", "info2018", "infosharing", "report2019", "report2018", "training", "others"]
# create a list to store names and item numbers
categoryDict = {}
# create a regex to get date string
regex = re.compile('^\d.+\d')

# loop through each category to get its item number
for j in range(7, len(categoryNames) + 1):
	# get the number of items in each category
	items = driver.find_elements_by_css_selector(".gwBoardCollect__folder:nth-child(%s) .gwBoardCollect__board" %str(j))
	itemNum = len(items)
	# get category name and build the dict 
	categoryName = categoryNames[j - 1]
	categoryDict[categoryName] = itemNum

for categoryName, itemNum in categoryDict.items():
	fileIndex = 1
	for i in range(1, itemNum + 1):
		# get parent element each time backed to the original page
		categoryElement = driver.find_element_by_css_selector(".gwBoardCollect__folder:nth-child(%s)" %str(categoryNames.index(categoryName) + 1))
		links = categoryElement.find_elements_by_css_selector(".gwBoardCollect__board")
		if len(links) == 0:
			break
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
		# type in new file name according to category
		if categoryName == "morning2019" or categoryName == "morning2018" or categoryName == "meeting2019" or categoryName == "meeting2018":
			match = regex.findall(titleText)
			dates = match[0].split("/")
			dateString = "".join(dates)
			filename = "trbiz-%s-%s.html" %(categoryName, dateString)
		else:
			filename = "trbiz-%s-%s.html" %(categoryName, str(fileIndex))
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
				if categoryName == "morning2019" or categoryName == "morning2018" or categoryName == "meeting2019" or categoryName == "meeting2018":
					match = regex.findall(titleText)
					dates = match[0].split("/")
					dateString = "".join(dates)
					filename = "trbiz-%s-%s.html" %(categoryName, dateString)
				else:
					filename = "trbiz-%s-%s.html" %(categoryName, str(fileIndex))
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