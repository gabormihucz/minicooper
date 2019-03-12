#urllib is builtin lib that handles urls (we need it in order to work smoothly on json)
#base64 is to refctor binary of pdf in such a way that it fits smoothly in a json we post
import urllib.request
import json
import base64

def post(path, pdf, ip = '127.0.0.1:8000'):

        #opening the pdf file
        with open(path + '/' + pdf, 'rb') as f:
            data = base64.b64encode(f.read()) #encoding to fit into later json


        body = {"filename":pdf[:-4],"content":data.decode('utf-8')} #temporary directory that will be parsed into json
        url_destination = 'http://' + ip + '/upload_pdf/' #destination is an url that is linked to a view which handles post requests (uploads to a server)

	#creating a request
        req = urllib.request.Request(url_destination)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))

        #response from a server
        response = urllib.request.urlopen(req, jsondataasbytes)
        
        # if a template was not found by the server, return -1
        response_text = response.read().decode('utf-8')
        if 'template was not found' in response_text:
            return -1
