import urllib.request
import gzip
import json
import xml.etree.ElementTree
import pymongo
import time
import threading
from queue import Queue
import weather_parsing
import enum


ONE_MIN = 1
ONE_HOUR = ONE_MIN * 2
ONE_DAY = ONE_HOUR * 2

class MsgType(enum.IntEnum):
    YOUBIKE = 1
    WEATHER = 2
    AQI = 3
    AIRBOX = 4
    UV = 5


def UpdateUVData(queue):
    uv_url = "http://opendata.cwb.gov.tw/opendataapi?dataid=O-A0005-001&authorizationkey=CWB-B74D517D-9F7C-44B9-90E9-4DF76361C725"
    while True:
        uv_res = urllib.request.urlretrieve(uv_url, "uv_data.xml")

        uv_e = xml.etree.ElementTree.parse('uv_data.xml')
        uv_root = uv_e.getroot()
        a = weather_parsing.parsing_uv(uv_root)
        msg = {}
        msg['type'] = MsgType.UV
        msg['data'] = a
        queue.put(msg)
        time.sleep(ONE_DAY)            #everyday

def GetUbikeDataThread(queue):

    ubike_url = "http://data.taipei/youbike"
    while True:
        urllib.request.urlretrieve(ubike_url, "ubike_data.gz")
        ubike_f = gzip.open("ubike_data.gz", 'r')
        ubike_jdata = ubike_f.read()
        ubike_f.close()
        print(type(ubike_jdata))
        ubike_data = json.loads(ubike_jdata)
        print(type(ubike_data))
        for key,value in ubike_data['retVal'].items():
            msg = {}
            msg['type'] = MsgType.YOUBIKE
            msg['data'] = value
            queue.put(msg)
            #data_id = col.insert_one(value).inserted_id
        time.sleep(ONE_MIN)    #every minites


def GetWeatherThread(queue):
    uvdata = -1
    weather_url = "http://opendata.cwb.gov.tw/opendataapi?dataid=O-A0001-001&authorizationkey=CWB-B74D517D-9F7C-44B9-90E9-4DF76361C725"
    while True:
        res = urllib.request.urlretrieve(weather_url, "weather_data.xml")
        weather_e = xml.etree.ElementTree.parse('weather_data.xml')
        weather_root = weather_e.getroot()

        root_tmp = weather_root
        foundTP = False
        for child in root_tmp:
            for g_child in child:
                for gg_child in g_child:
                    if(gg_child.text == '臺北市'):
                        foundTP = True
            wdata = {}
            if foundTP == True: #print all data for this g_child
                weather_parsing.parsing_weather(child,wdata)
                #if not queue.empty():
                #    uvdata = queue.get()
                #    wdata['UV'] = uvdata
                #else:
                #    wdata['UV'] = uvdata
                foundTP = False
                #data_id = col.insert_one(wdata).inserted_id
                msg = {}
                msg['type'] = MsgType.WEATHER
                msg['data'] = wdata
                queue.put(msg)

        time.sleep(ONE_HOUR) #every hour

def GetAQIThread(queue):

    aqi_url = "http://opendata2.epa.gov.tw/AQI.json"
    while True:
        urllib.request.urlretrieve(aqi_url, "aqi.json")
        aqi_f = open("aqi.json")
        aqi_jdata = aqi_f.read()
        aqi_f.close()
        print(type(aqi_jdata))
        aqi_data = json.loads(aqi_jdata)
        print(type(aqi_data))
        for data in aqi_data:   #aqi_data: list, data: dict
            if data['County'] == '臺北市':
                pm = data.pop('PM2.5')
                data['PM25'] = pm
                pm = data.pop('PM2.5_AVG')
                data['PM25_AVG'] = pm
                #data_id = col.insert_one(data).inserted_id
                msg = {}
                msg['type'] = MsgType.AQI
                msg['data'] = data
                queue.put(msg)

        time.sleep(ONE_HOUR) #every hour

def GetAirboxThread(queue):

    airbox_url = "https://tpairbox.blob.core.windows.net/blobfs/AirBoxData_V3.gz"
    while True:
        urllib.request.urlretrieve(airbox_url, "airbox_data.gz")
        airbox_f = gzip.open("airbox_data.gz", 'r')
        airbox_jdata = airbox_f.read()
        airbox_f.close()

        airbox_data = json.loads(airbox_jdata)

        if airbox_data['status'] == 'ok':
            devices_list = airbox_data['devices']
            for device in devices_list: #device is a dict
                #device_id = col.insert_one(device).inserted_id
                msg = {}
                msg['type'] = MsgType.AIRBOX
                msg['data'] = device
                queue.put(msg)

        time.sleep(ONE_HOUR) #every hour




def MainThread(queue):
    uv_data = -1
    while True:
        item = queue.get()
        if item is None:
            time.sleep(10)
        if item['type'] == MsgType.UV:
            uv_data = item['data']
        else:
            if item['type'] == MsgType.YOUBIKE:
                

        queue.task_done()


#### main.py
if __name__ == "__main__":

    queue = Queue()
    #connect To MongoDB
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    #create 4 MongoDB collections in youbikedb
    youbikedb = client.YoubikeDB
    youbikecol = youbikedb.YoubikeCol
    weathercol = youbikedb.WeatherCol
    aqicol = youbikedb.AqiCol
    airboxcol = youbikedb.AirboxCol

    #create thread
    uv_thread = threading.Thread(target = UpdateUVData,args=(queue,))
    ubike_thread = threading.Thread(target = GetUbikeDataThread, args = (youbikecol,))
    aqi_thread = threading.Thread(target = GetAQIThread,args=(aqicol,))
    airbox_thread = threading.Thread(target = GetAirboxThread, args = (airboxcol,))
    weather_thread = threading.Thread(target = GetWeatherThread, args = (weathercol,queue))

    uv_thread.start()
    ubike_thread.start()
    aqi_thread.start()
    airbox_thread.start()
    weather_thread.start()

    uv_thread.join()
    ubike_thread.join()
    aqi_thread.join()
    airbox_thread.join()
    weather_thread.join()

    print ("Finished")

    client.close()
