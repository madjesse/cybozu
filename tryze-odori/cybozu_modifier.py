import time, bs4, os, re

# text to be added
add_text = '<script type="text/javascript" src="jquery-3.3.1.min.js"></script><script type="text/javascript" src="cybozu_tryze_odori.js"></script>\n'

# get all the files in the targeted directory
files = os.listdir("E:\\company\\cybozu\\tryze-odori")
# get all needed html fils 
file_list = []
for file in files:
	if re.search(".html", file):
		file_list.append(file)

for base_file in file_list:
	original_path = "E:\\company\\cybozu\\tryze-odori\\%s" %base_file
	original_file = open(original_path, encoding='utf-8', errors='replace')
	new_path = "E:\\company\\cybozu\\tryze-odori-edited\\%s" %base_file 
	new_file = open(new_path, "w", encoding='utf-8', errors='replace')
	for line in original_file:
		if "</head>\n" in line:
			new_file.write(add_text)
		new_file.write(line)
	new_file.close()
	original_file.close()

	