import data, logging, re, pyautogui, unicodedata
import functions as f
from selenium import webdriver

# ============do NOT modify===========================
# configure logging
pyautogui.FAILSAFE = False

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.CRITICAL)
print("Press ctrl + c to quit.\n")

# driver: windows
# driver = webdriver.Chrome("./chromedriver.exe")
# driver: mac
driver = webdriver.Chrome("./chromedriver")
# login
f.login(driver)
# the regex to check date string
regex_date = re.compile('\d+')

# loop through each facility: the 3rd level loop==================================================================================================================================================
for facility_jp_name, facility_en_name in data.FACILITY.items():
	# pass the 2 facilities whose downloading has completed
	if facility_jp_name == "継続支援トラビズ" or facility_jp_name == "継続支援コネクトワークス大通東" or facility_jp_name == "就労支援ブリッジ":
		continue
	# click the facility link to proceed to the next page
	f.get_facility(driver, facility_jp_name)

	# get into the post board, scroll down to the bottom and click the collecting link
	f.get_post_board(driver)

	# build the dict for the facility
	category_dict = f.construct_dict(driver, regex_date)
	print(category_dict)
	# create a list based on the dict above
	category_tuple_list = list(category_dict.items())

	# loop through each category: the 2nd level loop================================================================================================================
	for category_tuple in category_tuple_list:
		file_index = 1 
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
				# only check whether there is a date string when the title text is less than 20 characters
				if len(unicodedata.normalize('NFKC', title_text)) <= 20:
					date_list = f.check_date(title_text, regex_date)
				else:
					date_list = []
				# create a proper filename 
				filename = f.construct_filename(date_list, facility_en_name, category_tuple[0], file_index)
				# set the path based on the filename 
				filepath = "c:\\Users\\user\\Downloads\\%s" %filename
				# for mac
				# filepath = "/Users/apple/Downloads/%s" %filename

				# if the file exists, log the message, back to the previous page and continue the loop
				if f.check_existing(filepath):
					# logging.debug("%s already exists.\n" %filename)
					file_index += 1
					print("%s: already exists.\n" %filename)
					continue
				# otherwise, download the file
				else:
					# download
					f.click_link(link)
					f.download_file(driver, link, filename, filepath, file_index)
					# prepare for the next download
					f.prepare_next(driver, file_index)

			# end of the 1st level loop==================================================================================================================

	# end of the 2nd level loop==========================================================================================================================================

	# back to the facility list page
	f.back_to_facility(driver)
	# give the user some time to manage the downloaded files before the download of the next category begins and the program terminates if "n" is pressed
	waiting = input("Start the next download? (y/n)")
	if waiting == "n":
		break
# end of the 3rd level loop=========================================================================================================================================================