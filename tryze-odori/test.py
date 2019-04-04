import selenium, pyautogui, time, os.path, logging, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import data
import functions as f
import unicodedata

# driver = webdriver.Chrome("./chromedriver.exe")
# functions.login(driver)
# functions.get_facility(driver, "継続支援プラスタ")
# functions.get_post_board(driver)

# categories = driver.find_elements_by_css_selector(".gwBoardCollect__folder")
# for category in categories:
# 	items = category.find_elements_by_css_selector(".gwBoardCollect__board")
# 	print(len(items))
# driver
driver = webdriver.Chrome("./chromedriver.exe")
# login
f.login(driver)
# the regex to check date string
regex_date = re.compile('\d+')

for facility_jp_name, facility_en_name in data.FACILITY.items():
	# pass the 2 facilities whose downloading has completed
	if facility_jp_name == "継続支援トラビズ" or facility_jp_name == "継続支援コネクトワークス大通東" or facility_jp_name == "就労支援ブリッジ":
		continue
	# click the facility link to proceed to the next page
	print(facility_jp_name)
	f.get_facility(driver, facility_jp_name)

	# get into the post board, scroll down to the bottom and click the collecting link
	f.get_post_board(driver)

	# build the dict for the facility
	category_dict = f.construct_dict(driver, regex_date)
	print(category_dict)

	# create a list based on the dict above
	category_tuple_list = list(category_dict.items())

	for category_tuple in category_tuple_list:
		file_index = 1 
		print(category_tuple[0])
		# if the category is not empty
		if category_tuple[1] > 0:

			# loop through each item: the 1st level loop=================================================================================================
			for i in range(1, category_tuple[1] + 1):
				container_index = category_tuple_list.index(category_tuple) + 1
				link_index = i 
				# get the link element 
				link = f.get_link_element(driver, container_index, link_index)
				# get the item title text that will be used to extract date string if it has
				title_text = f.get_title_text(link)
				date_list = []
				for date_item in data.DATE_RELEVANT:
					if date_item in category_tuple[0]:
						date_list = f.check_date(title_text, regex_date)
						break
				# create a proper filename 
				filename = f.construct_filename(date_list, facility_en_name, category_tuple[0], file_index)
				print(filename)
				file_index += 1
				time.sleep(0.5)
	break
				
				# date_list = f.check_date(title_text, regex_date)
				# # create a proper filename 
				# filename = f.construct_filename(date_list, facility_en_name, category_tuple[0], file_index)
				# # set the path based on the filename 
				# filepath = "c:\\Users\\user\\Downloads\\%s" %filename
				# # if the file exists, log the message, back to the previous page and continue the loop
				# if f.check_existing(filepath):
				# 	# logging.debug("%s already exists.\n" %filename)
				# 	print("exist.\n")
				# else:
				# 	# download
				# 	f.click_link(link)
				# 	f.download_file(driver, link, filename, filepath, file_index)
				# # prepare for the next download
				# f.prepare_next(driver, file_index)
