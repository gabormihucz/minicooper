import urllib.request
import json

#this part is hardcode right now. When using GET request it, you need to structure the url like shown below( ?than name of parameter, then = and actual value) 'http://127.0.0.1:8000/get_pdf_info/?file_name='+file_name
file_name = "file1"
url_destination = 'http://127.0.0.1:8000/get_pdf_info/?file_name='+file_name

req = urllib.request.Request(url_destination)
response = urllib.request.urlopen(req)

#print response from a server
print(response.read().decode())

#what to do when we decide to return json instead of a string as a response
# returned = response.read().decode('utf-8')
# returned = json.loads(returned)
# print(returned)
