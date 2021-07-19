import gspread
import json
import time
from oauth2client.service_account import ServiceAccountCredentials

'''SCRIPT TO TAKE DATA FROM GOOGLESHEET AND PUT ON GITHUB WIKI'''

# use creds to create a client to interact with the Google Drive API
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"] # multiple paths specified to solve error
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope) #need to generate json keys for API associated with account and reference here
client = gspread.authorize(creds)

#grab sheet 1 of workbook and pull 'data'
sheet = client.open("SHEET NAME HERE").sheet1 #this only pulls first sheet of data from workbook
sheetdata = sheet.get_all_records()

#function for writing pulled data to json file as backup. Called in clear_sheetdata. default filename of backup.json
def backup_to_jsonfile(new_data, filename='backup.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["backup"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def clear_sheetdata(list_of_data):
    #backup data first to backup.json
    backup_to_jsonfile(list_of_data) #default backup to backup.json, if other file wanted through in second param of func call.
    numrows = len(list_of_data)
    i = 1
    while i <= numrows:
        sheet.delete_rows(i)
        i += 1
        time.sleep(1) #delay can probably be shortened but needed to stop API from throwing error of too many requests

'''INSERT CODE HERE TO PUSH PULLED SHEET DATA TO GITHUB PAGES '''

#call to backup sheet data to json file and clear out sheet 1 of workbook selected
clear_sheetdata(sheetdata)
