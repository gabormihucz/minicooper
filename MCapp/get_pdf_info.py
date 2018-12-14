import urllib.request
import json

file_name = "file1"
url_destination = 'http://127.0.0.1:8000/get_pdf_info/?file_name='+file_name

req = urllib.request.Request(url_destination)
response = urllib.request.urlopen(req)
print(response.read().decode())
# returned = response.read().decode('utf-8')
# returned = json.loads(returned)
# print(returned)
