import requests
import pandas as pd
import streamlit as st
from streamlit_google_oauth import st_google_oauth

menu_options = {
	'Get help': 'YOUR_HELP_URL',
	'Report a bug': 'YOUR_BUG_PAGE_URL',
	'About': '''
	 ## My Custom App

	 This app uses our ML Model to demonstrate churn prediction.   
	'''
}

st.set_page_config(menu_options=menu_options)

SCOPES = [
  "https://www.googleapis.com/auth/drive.metadata.readonly",
  "https://www.googleapis.com/auth/spreadsheets.readonly",
]

token = st_google_oauth(st.secrets["CLIENT_ID"], st.secrets["CLIENT_SECRET"], SCOPES)
if token is None:
  st.stop()

all_files = [{ 'id': None, 'name': "(None Selected)" }]
needs_request = True
nextPageToken = None

while needs_request:
  page_param = "" if nextPageToken is None else "&pageToken=" + nextPageToken
  r = requests.get('https://www.googleapis.com/drive/v3/files?q=mimeType%3D%22application%2Fvnd.google-apps.spreadsheet%22&fields=nextPageToken%2C%20files(id%2C%20name)&access_token=' + token + page_param)
  json = r.json()
  all_files.extend(json['files'])
  if 'nextPageToken' in json['nextPageToken']:
    nextPageToken = json['nextPageToken']
  else:
    needs_request = False

if st.checkbox("Peek at Files JSON"):
  st.json(all_files)

file = st.selectbox("Select File", all_files, format_func=lambda f: f['name'])

if file['id'] is None:
  st.stop()

spreadsheet_id = file['id']
r = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?access_token=' + token)
spreadsheet_metadata = r.json()
if st.checkbox("Peek at Spreadsheet Metadata"):
  st.json(spreadsheet_metadata)
sheet = st.selectbox("Select Sheet", spreadsheet_metadata['sheets'], format_func=lambda s: s['properties']['title'])
r = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet["properties"]["title"]}?access_token=' + token)
sheet_data = r.json()
if st.checkbox("Peek at Spreadsheet Values"):
  st.json(sheet_data)
columns = sheet_data['values'][0]
df = pd.DataFrame(sheet_data['values'][1:], columns=columns)
st.write(df)