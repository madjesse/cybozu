import os, re, logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
# get category names
categoryNames = ["morning2019", "morning2018", "confirm2019", "confirm2018", "meeting2019", "meeting2018", "info2019", "info2018", "infosharing", "report2019", "report2018", "training", "others"]
# create an empty dict to store data
data = {}
# get all the files in the targeted directory
files = os.listdir("cybozu_downloaded")
# loop through categoryNames to send all relevant html filenames to the category
for categoryName in categoryNames:
	# set up regex for each categoryName
	regex_string = "%s.+\.html" %categoryName
	# set up default key-value pairs
	data.setdefault(categoryName, [])
	# loop through all files 
	for file in files:
		# compare each filename with regex_string
		# if matched, add the filename into relevant list 
		if re.search(regex_string, file):
			data[categoryName].append(file)

# save the data to txt file 
data_file = open("data.txt", "w")
# write data 
for k, v in data.items():
	data_file.write("{'%s': %s}\n" %(k, v))

data_file.close()