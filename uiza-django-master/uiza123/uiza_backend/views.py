from django.shortcuts import render
from django.http import HttpResponse
import json, requests



# Authorization_key and URl
Authorization_key = 'uap-ccd36da99ff54863a2c5a7f140a7d884-e0f44929'
url = 'https://development-api.uizadev.io/v1/live_entities'

#Global variables
stream_key = ''
stream_url = ''
stream_hls = ''
list_of_videos = []
NotPlayable = True

#This view renders the homepage 1. BroadcastPage and Viewers page
def homepage(request):
    
    return render(request,'homepage.html')
    

#This view renders the page which shows all the live broadcasting
def viewerspage(request):
    # if broadcast button is not clicked then this view is rendered
    if NotPlayable:
        print('got here')
        
        return render(request,'viewerspage.html')
    else:    
        # if broadcast button is clicked then this view is rendered and a context dictionary is passed with stream_key, stream_url, playback link
        print('in dict')
        stream_dict={'stream_key':stream_key,'stream_url':stream_url,'playback':stream_hls}
        global list_of_videos
        list_of_videos.append(stream_dict)
        print(stream_dict)

        return render(request,'viewerspage.html',{'list_of_videos':list_of_videos})






def create_event(request):
    #when broadcast button is click post method is triggered
    if request.method == "POST":
        region = request.POST['region']
        
        # necessary headers and data for the post request 
        headers = {'Authorization': Authorization_key ,
                'Content-Type': 'application/json',
                'cache-control': 'no-cache' }   
        data = {
                "name":"Demo",
                "region":region,
                "description":"AFF CUP"
                }
        #post request for the id of live stream    
        response = requests.post(url = url, headers = headers, params= data)
        print(response.text)
        #convert the response to json
        live_response = json.loads(response.text)
        #retrieved id from json
        created_id = live_response["id"]
       
        # Now make the get request using the headers and using the id retrieve the stream_key,stream_url and playback
        get_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Authorization': Authorization_key,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
        
        newUrl = url+'/' + created_id
        
        i=0
        #This while loop will make the get request from the uiza UPI till the status is not ready and retrieve the necessary info and then will render the homepage
        while True:
            retrieve_entity = requests.get(url = newUrl, headers=get_headers)
            retrieve_entity_json = json.loads(retrieve_entity.text)
            status = retrieve_entity_json["status"]
            print(status)
            print(i)
            if status == "ready":
                print(retrieve_entity_json)
                global stream_url
                stream_url = retrieve_entity_json["ingest"]["url"]
                global stream_key
                stream_key = retrieve_entity_json["ingest"]["key"]
                global stream_hls
                stream_hls = retrieve_entity_json['playback']['hls']
                global NotPlayable
                NotPlayable = False
               
                return render(request,'homepage.html')
            i+=1
       
    return render(request,'broadcastpage.html') #This render will be called if post request is not made   

