import requests
import json
import datetime
import time
import sys
import os

def log(msg):
  utc_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
  print(utc_time + ': ' + msg)

def downloadFile(year):
  city = os.environ.get('ENV_CITY')
  street = os.environ.get('ENV_STREET')
  houseno = os.environ.get('ENV_HOUSENO')
  
  if city is None or street is None or houseno is None:
    log('Not all information is given. Define ENV variables. Exiting...')
    sys.exit(1)
  
  add_req_headers = {}
  url='https://www.zakb.de/online-service/abfallkalender/'
  s=requests.Session()
  log('Starting initial request for year ' + year)
  r1=s.get(url)
  log('Finished initial request')

  log('Starting selecting City')
  r2_data = {'aos[Ort]': '' + city + '', 'aos[Strasse]': 'Am Hofböhl', 'aos[Hausnummer]': '', 'aos[Hausnummerzusatz]': '', 'aos[CheckBoxRestabfallbehaelter]': 'on', 'aos[CheckBoxRestabfallcontainer]': 'on', 'aos[CheckBoxBioabfallbehaelter]': 'on', 'aos[CheckBoxPapierbehaelter]': 'on', 'aos[CheckBoxPapiercontainer]': 'on', 'aos[CheckBoxGruensperrmuell]': 'on', 'aos[CheckBoxGelber Sack]': 'on', 'aos[CheckBoxDSD-Container]': 'on', 'aos[Zeitraum]': 'Jahresübersicht 2021', 'submitAction': 'CITYCHANGED', 'pageName': 'Lageadresse'}
  r2=s.post(url, data=r2_data, headers=add_req_headers)
  log('Finished selecting City')

  log('Starting selecting street')
  r3_data = {'aos[Ort]': '' + city + '', 'aos[Strasse]': '' + street + '', 'aos[Hausnummer]': '', 'aos[Hausnummerzusatz]': '', 'aos[CheckBoxRestabfallbehaelter]': 'on', 'aos[CheckBoxRestabfallcontainer]': 'on', 'aos[CheckBoxBioabfallbehaelter]': 'on', 'aos[CheckBoxPapierbehaelter]': 'on', 'aos[CheckBoxPapiercontainer]': 'on', 'aos[CheckBoxGruensperrmuell]': 'on', 'aos[CheckBoxGelber Sack]': 'on', 'aos[CheckBoxDSD-Container]': 'on', 'aos[Zeitraum]': 'Jahresübersicht 2021', 'submitAction': 'changedEvent', 'pageName': 'Lageadresse'}
  r3=s.post(url, data=r3_data, headers=add_req_headers)
  log('Finished selecting street')

  log('Starting selecting house no')
  r4_data = {'aos[Ort]': '' + city + '', 'aos[Strasse]': '' + street + '', 'aos[Hausnummer]': '' + houseno + '', 'aos[Hausnummerzusatz]': '', 'aos[CheckBoxRestabfallbehaelter]': 'on', 'aos[CheckBoxRestabfallcontainer]': 'on', 'aos[CheckBoxBioabfallbehaelter]': 'on', 'aos[CheckBoxPapierbehaelter]': 'on', 'aos[CheckBoxPapiercontainer]': 'on', 'aos[CheckBoxGruensperrmuell]': 'on', 'aos[CheckBoxGelber Sack]': 'on', 'aos[CheckBoxDSD-Container]': 'on', 'aos[Zeitraum]': 'Jahresübersicht 2021', 'submitAction': 'nextPage', 'pageName': 'Lageadresse'}
  r4=s.post(url, data=r4_data, headers=add_req_headers)
  log('Finished selecting house no')

  log('Starting downloading ical file')
  r5_data = {'submitAction': 'filedownload_ICAL', 'pageName': 'Terminliste'}
  r5=s.post(url, data=r5_data, headers=add_req_headers)
  log('Finished downloading ical file')
  responseCT = r5.headers['Content-Type']
  if not responseCT.startswith('text/calendar'):
    log('DOWNLOAD ERROR! Did not receive calendar file. Will not overwrite old file.')
    return False

  log('Writing content to file')
  with open('./calendar.ics', 'wb') as f:
    for chunk in r5.iter_content(chunk_size=128):
      f.write(chunk)
  return True


while True:
  year = datetime.datetime.utcnow().strftime('%Y')
  sleepTime = 1 * 60 * 60 * 24 # 1 day
  try:
    downloadResult = downloadFile(year)
  except Exception as e:
    print(e)
    downloadResult = False
    log('Will try again soon!')
  if not downloadResult:
    sleepTime = 1 * 60 * 60    # 1 hour
  log('Waiting for ' + str(sleepTime) + ' seconds...')
  try:
    time.sleep(sleepTime)
  except:
    sys.exit(99)