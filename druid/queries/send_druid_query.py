import requests
from datetime import datetime
import sys

try:
  filename = sys.argv[1]
except IndexError:
  print("Please provide filename. Exiting")
  sys.exit(1)

f = open(filename, 'r')

now_dt = datetime.now().isoformat()
q = f.read()
q = q.replace('<<now>>', now_dt)

headers = {'Content-Type': 'application/json'}
r = requests.post('http://localhost:8082/druid/v2/?pretty', headers=headers, data=q)
print(r.content)

