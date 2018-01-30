import urllib.request
import time
import threading
from queue import Queue
import datetime
import os, sys
import shutil
import socket


ONE_MIN = 60
ONE_HOUR = ONE_MIN * 60
ONE_DAY = ONE_HOUR * 24


def UpdateUVData():
    uv_url = "http://opendata.cwb.gov.tw/opendataapi?dataid=O-A0005-001&authorizationkey=CWB-B74D517D-9F7C-44B9-90E9-4DF76361C725"
    while True:
        try:
            uv_res = urllib.request.urlretrieve(uv_url, "uv_data.xml")
            # move data to uv_data dir and rename
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            fname = "uv_data_" + st + ".xml"
            os.rename("uv_data.xml",fname)
            shutil.move(fname,"uv_data")
            print("get file : "+fname,flush=True)
            time.sleep(ONE_DAY)            #everyday
        except urllib.error.HTTPError as e:
            # Maybe set up for a retry, or continue in a retry loop
            print("[UV HTTPerror]", flush=True)
            time.sleep(10)
        except urllib.error.URLError as e:
            # catastrophic error. bail.
            print("[UV URLerror]", flush=True)
            time.sleep(10)
        except TimeoutError as e:
            print ("[UV Timeouterror]", flush=True)
            time.sleep(10)
        except:
            print ("[UV]Unexpected Error!", flush=True)
            time.sleep(10)


def GetUbikeDataThread():

    ubike_url = "http://data.taipei/youbike"
    while True:
        try:
            urllib.request.urlretrieve(ubike_url, "ubike_data.gz")
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            fname = "ubike_data_" + st + ".gz"
            os.rename("ubike_data.gz",fname)
            shutil.move(fname,"youbike_data")

            print("get file : "+fname,flush=True)
            time.sleep(ONE_MIN)    #every minites
        except urllib.error.HTTPError as e:
            # Maybe set up for a retry, or continue in a retry loop
            print("[Youbike HTTPerror]", flush=True)
            time.sleep(10)
        except urllib.error.URLError as e:
            # catastrophic error. bail.
            print("[Youbike URLerror]", flush=True)
            time.sleep(10)
        except TimeoutError as e:
            print("[Youbike Timeouterror]", flush=True)
            time.sleep(10)
        except:
            print("[Youbike]Unexpected Error!", flush=True)
            time.sleep(10)


def GetWeatherThread():
    uvdata = -1
    weather_url = "http://opendata.cwb.gov.tw/opendataapi?dataid=O-A0001-001&authorizationkey=CWB-B74D517D-9F7C-44B9-90E9-4DF76361C725"
    while True:
        try:
            res = urllib.request.urlretrieve(weather_url, "weather_data.xml")
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            fname = "weather_data_" + st + ".xml"
            os.rename("weather_data.xml",fname)
            shutil.move(fname,"weather_data")
            print("get file : "+fname,flush=True)
            time.sleep(ONE_HOUR) #every hour
        except socket.Timeouterror:
            # Maybe set up for a retry, or continue in a retry loop
            print("[Weather error]socket time out! try again",flush=True)
            time.sleep(30)
        except TimeoutError as e:
            # Maybe set up for a retry, or continue in a retry loop
            print("[Weather error]time out! try again",flush=True)
            time.sleep(30)
        except urllib.error.HTTPError as e:
            # Maybe set up for a retry, or continue in a retry loop
            print("[Weather HTTP error]",flush=True)
            time.sleep(10)
        except urllib.error.URLError as e:
            # catastrophic error. bail.
            print("[Weather URL error]",flush=True)
            time.sleep(10)


def GetAQIThread():

    aqi_url = "http://opendata2.epa.gov.tw/AQI.json"
    while True:
        try:
            urllib.request.urlretrieve(aqi_url, "aqi.json")
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            fname = "aqi_" + st + ".json"
            os.rename("aqi.json",fname)
            shutil.move(fname,"aqi_data")

            print("get file : "+fname,flush=True)
            time.sleep(ONE_HOUR)
        except urllib.error.HTTPError as e:
            # Maybe set up for a retry, or continue in a retry loop
            print("[AQI HTTPerror]", flush=True)
            time.sleep(10)
        except urllib.error.URLError as e:
            # catastrophic error. bail.
            print("[AQI URLerror]", flush=True)
            time.sleep(10)
        except TimeoutError as e:
            print("[AQI Timeouterror]", flush=True)
            time.sleep(10)
        except:
            print("[AQI]Unexpected Error!", flush=True)
            time.sleep(10)


def GetAirboxThread():

    airbox_url = "https://tpairbox.blob.core.windows.net/blobfs/AirBoxData_V3.gz"
    while True:
        try:
            urllib.request.urlretrieve(airbox_url, "airbox_data.gz")
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
            fname = "airbox_data_" + st + ".gz"
            os.rename("airbox_data.gz",fname)
            shutil.move(fname,"airbox_data")
            print("get file : "+fname,flush=True)
            time.sleep(ONE_HOUR) #every hour

        except urllib.error.HTTPError as e:
            # Maybe set up for a retry, or continue in a retry loop
            print("[Airbox HTTPerror]", flush=True)
            time.sleep(10)
        except urllib.error.URLError as e:
            # catastrophic error. bail.
            print("[Airbox URLerror]", flush=True)
            time.sleep(10)
        except TimeoutError as e:
            print("[Airbox Timeouterror]", flush=True)
            time.sleep(10)
        except:
            print("[Airbox]Unexpected Error!", flush=True)
            time.sleep(10)


#### main.py
if __name__ == "__main__":

    print ("Starting...",flush=True)
    #create thread
    uv_thread = threading.Thread(target = UpdateUVData)
    ubike_thread = threading.Thread(target = GetUbikeDataThread)
    aqi_thread = threading.Thread(target = GetAQIThread)
    airbox_thread = threading.Thread(target = GetAirboxThread)
    weather_thread = threading.Thread(target = GetWeatherThread)

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

    print ("Finished",flush=True)
