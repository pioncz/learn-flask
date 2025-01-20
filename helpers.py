import shutil
import requests

def fetchImageAndSave(url, filename):
  r = requests.get(url, allow_redirects=True, stream=True)
  if r.status_code == 200:
    with open('Avatars/Androc.png', 'wb') as f:
      r.raw.decode_content = True
      shutil.copyfileobj(r.raw, f) 

def findChampionsInList(query, list):
  return list(filter(lambda a: query.lower() in a['champion'].lower(), list))