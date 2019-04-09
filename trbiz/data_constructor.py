import os, re, logging

# get category names
categoryNames = ["others", "morning2019", "meeting2019", "info", "confirm2019", "training", "infosharing", "extra", "office", "happening2019"]
# create an empty dict to store data
data = {}
# get all the files in the targeted directory
files = os.listdir("E:\\company\\cybozu\\tryze-odori")
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
firs_file_data = open("first_files.txt", "w")
# write data 
data_file.write("[")
firs_file_data.write("[")
for k, v in data.items():
	data_file.write("{'%s': %s},\n" %(k, v))
	if len(v) == 0:
		firs_file_data.write("'',\n")
	else:
		firs_file_data.write("'%s',\n" %(v[0]))
data_file.write("]")
firs_file_data.write("]")

data_file.close()
firs_file_data.close()