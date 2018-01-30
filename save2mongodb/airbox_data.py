import urllib.request
import gzip
import json


airbox_url = "https://tpairbox.blob.core.windows.net/blobfs/AirBoxData_V3.gz"
urllib.request.urlretrieve(airbox_url, "airbox_data.gz")
airbox_f = gzip.open("airbox_data.gz", 'r')
airbox_jdata = airbox_f.read()
airbox_f.close()

airbox_data = json.loads(airbox_jdata)
print(airbox_data)

if airbox_data['status'] == 'ok':
    devices_list = airbox_data['devices']
    for device in devices_list: #device is a dict
        print('Device ID:',device['id'],'. Name: ',device['name'],'PM2.5: ',device['pm25'])
