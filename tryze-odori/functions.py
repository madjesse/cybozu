import selenium, pyautogui, time, os.path, logging, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import data

# ===================basic css selectors===============
# the logo
# th.globalNavi__logo a

# the container of each category:
# div.gwBoardCollect__folder

# the category name container:
# div.gwBoardCollect__folder__name

# the category name:
# (div.gwBoardCollect__folder__name a).text

# the container of each item:
# div.gwBoardCollect__board

# the a tag of each item to be clicked:
# div.gwBoardCollect__board a:nth-child(2)
# =====================================================

# the regex for getting the date string
regex_date = re.compile('\d.*\d')

def login(driver):
	"""to login to the cybozu live system"""
	loginUrl = "https://cybozulive.com/login?dummy=1552289327620"
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

def get_facility(driver, facility_name):
	"""get the facility link and click it"""
	linkElement = driver.find_element_by_xpath("//a[@class='groupwareList__groupwareName '][@title='" + facility_name + "']")
	# click it and wait 1s before the following actions
	linkElement.click()
	time.sleep(1)

def get_post_board(driver):
	"""to get into the post board, scroll down to the bottom and click the collecting link"""
	# get into the post board
	infoElement = driver.find_element_by_xpath("//a[@title='掲示板']")
	infoElement.click()
	time.sleep(1)
	# scroll to the bottom
	pyautogui.moveTo(100, 500, duration=0.25)
	time.sleep(1)
	pyautogui.scroll(-4000)
	time.sleep(1)
	# click　collecting link
	listElement = driver.find_element_by_css_selector(".collectLink")
	listElement.click()
	time.sleep(1)

def construct_dict(driver):
	"""to make the dictionary for looping to download"""
	category_dict = {}
	# get all category names 
	categories = driver.find_elements_by_css_selector(".gwBoardCollect__folder")
	# loop through each category to compare its text with the target string, construct a proper english name, get its item number and set up the dict
	for category in categories:
		# get category names and item numbers
		category_name = ""
		# displayed category name 
		displayed_name = category.find_element_by_css_selector(".gwBoardCollect__folder__name a").text
		for jp_str, en_str in data.CATEGORY.items():
			if jp_str in displayed_name:
# convert each jp name into a proper english name
				category_name_base = en_str
				date_match = regex_date.findall(displayed_name)
				if len(date_match) > 0:
					category_name = category_name_base + date_match[0]
				else:
					category_name = category_name_base
# add the converted name into the list
				break
		# category item number
		items = category.find_elements_by_css_selector(".gwBoardCollect__board")
		item_number = len(items)
		# store the data into the dict
		category_dict[category_name] = item_number
	# return the dict
	return category_dict

def download_files(driver, category_dict, facility_en_name):
	category_tuple_list = list(category_dict.items())
	for category_tuple in category_tuple_list:
		file_index = 1
		# if the category is not empty
		if category_tuple[1] > 0:
			# loop through each item to download it
			for i in range(1, itemNum + 1):
				# CAUTION: the parent category element should be obtained every time before clicking the item
				category_container = driver.find_element_by_css_selector(".gwBoardCollect__folder:nth-child(%s)" %str(category_tuple_list.index(category_tuple) + 1))
				# get the item
				link = category_container.find_element_by_css_selector(".gwBoardCollect__board:nth-child(%s) a:nth-child(2)" %str(i))
				# get the item title text that will be used to extract date string if it has
				title_text = link.find_element_by_css_selector("span").text
				date_list = regex_date.findall(title_text)
				# if there is date string in the title text 
				if len(date_list) > 0:
					target_str = date_list[0]
					if "/" in target_str:
						date_str_list = target_str.split("/")
						date_str = "".join(date_str_list)
					else:
						date_str = target_str
					filename = "%s-%s-%s.html" %(facility_en_name, category_tuple[0], date_str)
				# otherwise create the filename in a different way
				else:
					filename = "%s-%s-%s.html" %(facility_en_name, category_tuple[0], str(file_index))

				# click the link 
				link.click()
				time.sleep(1)
				# press ctrl + s to save it 
				pyautogui.hotkey('ctrl', 's')
				time.sleep(1)
				# press delete to delete text in filename input area
				pyautogui.press("delete")
				time.sleep(0.5)
				# typewrite the filename 
				pyautogui.typewrite(filename)
				time.sleep(1)
				# press return to start downloading
				pyautogui.press('return')
				# wait until download is completed
				filepath = "c:\\Users\\user\\Downloads\\%s" %filename
				i = 0
				while not os.path.exists(filepath):
					time.sleep(1)
					logging.debug("saving...")
					i += 1
					if i == 10:
						logging.debug("download is disrupted.\n")
						break
				# prepare for the next download
				file_index += 1
				driver.back()
				time.sleep(1)
