import shutil
import requests
import os

def fetchImageAndSave(url, path, filename):
  r = requests.get(url, allow_redirects=True, stream=True)
  if r.status_code == 200:
    filepath = os.path.join(path, filename)
    with open(filepath, 'wb') as f:
      r.raw.decode_content = True
      shutil.copyfileobj(r.raw, f) 

def findChampionsInList(query, param_list):
  return list(filter(lambda a: query.lower() in a['champion'].lower(), param_list))