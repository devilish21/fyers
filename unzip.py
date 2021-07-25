import os, zipfile
from posixpath import dirname

dir_name = 'C:\\Users\\Raghu Veera Reddy\\Desktop\\Data\\Stock Data'
extension = ".zip"
lst = []
os.chdir(dir_name) # change directory from working dir to dir with files

for i in os.walk(dir_name): # loop through items in dir
    for item in i:
        if "Users\Raghu Veera Reddy\Desktop\Data\Stock Data" in item:
            lst.append(item)

for i in lst:
    dir_name = i
    print(dir_name)
    for item in os.listdir(dir_name): # loop through items in dir
        os.chdir(dir_name)
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            print(file_name)
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file
        