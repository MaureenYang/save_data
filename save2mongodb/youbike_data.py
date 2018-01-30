import urllib.request
import gzip
import json
import pymongo
import time

if False:
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.YoubikeDB
    col = db.YoubikeCol

if True:

    ubike_url = "http://data.taipei/youbike"
    urllib.request.urlretrieve(ubike_url, "ubike_data.gz")
    ubike_f = gzip.open("ubike_data.gz", 'r')
    ubike_jdata = ubike_f.read()
    ubike_f.close()
    ubike_data = json.loads(ubike_jdata)
    print(ubike_data)

    #print(type(ubike_jdata))
    #print(type(ubike_data))
    #data_id = col.insert_one(ubike_data['retVal']).inserted_id
    #print(data_id)
    #mon_data = col.find_one({'_id':data_id})
    #print(mon_data)
    if True:
        #for key,value in ubike_data.items():
        for key,value in ubike_data['retVal'].items():
            if False:
                sno = value['sno']
                sna = value['sna']
                tot = value['tot']
                sbi = value['sbi']
                sarea = value['sarea']
                mday = value['mday']
                lat = value['lat']
                lng = value['lng']
                ar = value['ar']
                sareaen = value['sareaen']
                snaen = value['snaen']
                aren = value['aren']
                bemp = value['bemp']
                act = value['act']
                print('-----------------------------')
                print("NO." + sno + " " + sna + "(" +sarea+")")
                print('Date : ' + mday)
            else:
                print(value)

    #time.sleep(60)
