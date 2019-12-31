from django.shortcuts import render
from django.http import HttpResponse
import uiza, json, requests

from uiza.api_resources.entity import Entity
from uiza.exceptions import ServerException
# Create your views here.
def homepage(request):
    return render(request,'homepage.html')






def index(request):   
    # uiza.authorization = "uap-49dc22c0f6b44687a718488d4c54a7c8-ba25a4ed"
    headers = {'Authorization': 'uap-49dc22c0f6b44687a718488d4c54a7c8-ba25a4ed' ,
                'Content-Type': 'application/json' }   
    data = {
        "inputType": "http",
        "appId":"49dc22c0f6b44687a718488d4c54a7c8",
        "type": "vod",
        "name":"Demo Video",
        "url": "http://static.uiza.io/media/big_buck_bunny_720p_10mb.mp4"
        }
    response = requests.post(url = 'https://ap-southeast-1-api.uiza.co/api/public/v4/media/entity'
                ,data = data, headers = headers)
    final_json = json.loads(response.text)  
    print(final_json['requestId'])        
    return HttpResponse(response.text)

def retrieve(request):
    uiza.authorization = "uap-49dc22c0f6b44687a718488d4c54a7c8-ba25a4ed"
    
    res, status_code = Entity().list(name="Title")
    print(res)
    return HttpResponse(res)

    