import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# GLOBAL VARIABLES
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]         # If modifying these scopes, delete the file token.json.
spreadsheetID = "1OS_VwzPcNFk0I2TFZi40iKJ14Blk-_pxobjmw41FpSA"    # Spreadsheet ID can be found in the URL
range = "Residency Tracker!A:B"                                             # Range should contain correct SHEET NAME and COLUMNS
localLogPath = "registration.txt"                                          # Path to local file log 
    
# Upload log item to Google Sheets
def newLogSheets(creds, logData):
  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    
    #!!!! SHEETS OPERATIONS HERE!!!!
    values = []
    values.append(logData)
    body = {'values': values}
    
    result = (
        service.spreadsheets()
        .values()
        .append(
                spreadsheetId=spreadsheetID,
                range=range,
                valueInputOption="USER_ENTERED",
                body=body)
        .execute()
    )

    print("Rows Updated: ", result['updates']['updatedRows'])
  except HttpError as err:
    print(err)
    
# Save log item in backup local log file (.txt)
def newLogText(logData):
  try:
    textFile = open(localLogPath, "a")
  except:
    print("Error, log.txt not found. Creating one now.")
    textFile = open(localLogPath, "x")
    textFile = open(localLogPath, "a")
    
  textFile.write(logData[0] + "\t" + logData[1] + "\n")
    
  textFile.close()
  print("Added to local log file.")
    
def main():
  # Authenticate credentials with Google
    
  creds = None
  
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  # ***for testing purposes only, update once hardware is integrated
  
  choice = "Y"
  
  while choice == "Y":
    # Replace with RC522 read once hardware is setup and integrated
    log = input("Input ID: ")
    
    # Initialize log data list
    logData = [ ]
    
    # Append ID Code, Date, and Time to log data.
    logData.append(log)
    
    log = input("Input Name: ")
    
    logData.append(log)
    
    newLogSheets(creds, logData)
    newLogText(logData)

if __name__ == "__main__":
  main()