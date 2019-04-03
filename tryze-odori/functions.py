import selenium, pyautogui, time, os.path, logging, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import data, unicodedata

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

def login(driver):
	"""to login to the cybozu live system"""
	login_url = "https://cybozulive.com/login?dummy=1552289327620"
	driver.get(login_url)
	try:
		user_name = driver.find_element_by_name('loginMailAddress')
		user_name.send_keys('c.wei@yokazu.co.jp')
		password = driver.find_element_by_name('password')
		password.send_keys('wei880830')
	except:
		raise Exception("login failed.\n")
	else:
		password.send_keys(Keys.RETURN)
	time.sleep(1)

def get_facility(driver, facility_name):
	"""get the facility link and click it"""
	link_element = driver.find_element_by_xpath("//a[@class='groupwareList__groupwareName '][@title='" + facility_name + "']")
	# click it and wait 1s before the following actions
	link_element.click()
	time.sleep(1)

def get_post_board(driver):
	"""to get into the post board, scroll down to the bottom and click the collecting link"""
	# get into the post board
	info_element = driver.find_element_by_xpath("//a[@title='掲示板']")
	info_element.click()
	time.sleep(1)
	# scroll to the bottom
	pyautogui.moveTo(100, 500, duration=0.25)
	time.sleep(1)
	pyautogui.scroll(-4000)
	time.sleep(1)
	# click　collecting link
	list_element = driver.find_element_by_css_selector(".collectLink")
	list_element.click()
	time.sleep(1)

def construct_dict(driver, regex_date):
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

def check_date(title_text, regex_date):
	"""check wheter there is a date string in the title text"""
	date_list = regex_date.findall(unicodedata.normalize('NFKC', title_text))
	return date_list

def get_title_text(link):
	"""get title text of each link"""
	title_text = link.find_element_by_css_selector("span").text
	return title_text

def get_link_element(driver, container_index, link_index):
	"""get each link within the category"""
	# CAUTION: the parent category element should be obtained every time before clicking the item
	category_container = driver.find_element_by_css_selector(".gwBoardCollect__folder:nth-child(%s)" %str(container_index))
	# get the item
	link = category_container.find_element_by_css_selector(".gwBoardCollect__board:nth-child(%s) a:nth-child(2)" %str(link_index))
	# return the link 
	return link

def construct_filename(date_list, facility_en_name, category_en_name, file_index):
	"""create a proper filename for the file"""
	if len(date_list) > 0:
		target_str = "".join(date_list)
		filename = "%s-%s-%s.html" %(facility_en_name, category_en_name, target_str)
	# otherwise create the filename in a different way
	else:
		filename = "%s-%s-%s.html" %(facility_en_name, category_en_name, str(file_index))

	return filename

def click_link(link):
	"""click the link"""
	link.click()
	time.sleep(1)

def download_file(driver, link, filename, filepath, file_index):
	"""perform the download"""
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
	# wait for download to complete
	i = 0
	while not os.path.exists(filepath):
		time.sleep(0.5)
		# logging.debug("saving...")
		i += 1
		if i == 10:
			logging.debug("download is disrupted.\n")
			break

def check_existing(filepath):
	existing = os.path.exists(filepath)
	return existing

def prepare_next(driver, file_index):
	"""wait for the current download to complete and prepare for the next download"""
	# prepare for the next download
	file_index += 1
	driver.back()
	time.sleep(1)

def back_to_facility(driver):
	"""get the logo and click it"""
	logo = driver.find_element_by_css_selector(".globalNavi__logo a")
	logo.click()
