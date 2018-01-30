####################################################################
#   calculate_group.py
#       calculate group by position
#
# 0. get youbike station position
# 1. get weather data position
# 2. get airbox device position
# 3. calculate each weather station belong to which youbike station
# 4. calculate each airbox device belong to which youbike station
#
####################################################################
#
#   output :
#       data type: list of dict:
#       [index:sno, wno, dno]
#
####################################################################
import urllib.request
import gzip
import json
import xml.etree.ElementTree
import math

#ubike data parsing
ubike_f = gzip.open("ubike_data.gz", 'r')
ubike_jdata = ubike_f.read()
ubike_f.close()
ubike_data = json.loads(ubike_jdata)
ubike_pos = []
for key,value in ubike_data['retVal'].items():
    ubike_dict = [{'sno':value['sno'],'sname':value['sarea'],'slat':float(value['lat']),'slon':float(value['lng'])}]
    ubike_pos = ubike_pos + ubike_dict


# weather data parsing
weather_e = xml.etree.ElementTree.parse('weather_data.xml')
weather_root = weather_e.getroot()
weather_pos = []
root_tmp = weather_root
foundTP = False
for child in root_tmp:
    for g_child in child:
        for gg_child in g_child:
            if(gg_child.text == '臺北市'):
                foundTP = True

    if foundTP == True:              #print all data for this g_child
        for g_child in child:
            if g_child.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}stationId':
                wid = g_child.text
            if g_child.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}locationName':
                wname = g_child.text
            if g_child.tag ==  '{urn:cwb:gov:tw:cwbcommon:0.1}lat':
                wlat = float(g_child.text)
            if g_child.tag ==  '{urn:cwb:gov:tw:cwbcommon:0.1}lon':
                wlon = float(g_child.text)
        weather_dict = [{'wno':wid,'wname':wname,'wlat':wlat,'wlon':wlon}]
        weather_pos = weather_pos + weather_dict
        foundTP = False


# airbox data parsing
airbox_f = gzip.open("airbox_data.gz", 'r')
airbox_jdata = airbox_f.read()
airbox_f.close()

airbox_data = json.loads(airbox_jdata)

device_pos = []
if airbox_data['status'] == 'ok':
    devices_list = airbox_data['devices']
    for device in devices_list: #device is a dict
        device_dict = [{'did':device['id'],'dname':device['name'],'dlat':float(device['lat']),'dlon':float(device['lon'])}]
        device_pos = device_pos + device_dict

#
# grouping
#   for each ubike station, find the nearest weather stationId
#

def cal_dist(cords_1,cords_2):
    dist = math.sqrt(pow(abs(cords_1[0]-cords_2[0]),2)+pow(abs(cords_1[1]-cords_2[1]),2))
    return dist

position_list = []

for ubike_sta in ubike_pos:
    wmin_dist = -1
    wmin_no = None
    wmin_name = None
    coords_s = (ubike_sta['slat'], ubike_sta['slon'])
    #find nearest weather station
    for weather_sta in weather_pos:
        coords_w = (weather_sta['wlat'], weather_sta['wlon'])
        cur_dist = cal_dist(coords_s, coords_w)
        if wmin_dist == -1:
            wmin_dist = cur_dist
            wmin_no = weather_sta['wno']
            wmin_name = weather_sta['wname']
        else:
            if wmin_dist != -1 and cur_dist < wmin_dist:
                wmin_dist = cur_dist
                wmin_no = weather_sta['wno']
                wmin_name = weather_sta['wname']
    #find nearest AirBox
    amin_dist = -1
    amin_no = None
    amin_name = None
    for airbox_sta in device_pos:
        coords_a = (airbox_sta['dlat'], airbox_sta['dlon'])
        cur_dist = cal_dist(coords_s, coords_a)
        if amin_dist == -1:
            amin_dist = cur_dist
            amin_no = airbox_sta['did']
            amin_name = airbox_sta['dname']
        else:
            if amin_dist != -1 and cur_dist < amin_dist:
                amin_dist = cur_dist
                amin_no = airbox_sta['did']
                amin_name = airbox_sta['dname']

    dist = [{'sno': ubike_sta['sno'],'sname':ubike_sta['sname'],'wno': wmin_no,'wname':wmin_name,'did':amin_no,'dname':amin_name}]  #,'dis_sw':min_dist}]
    position_list = position_list + dist


# print result
for ubike_sta in position_list:
    print('Station No.',ubike_sta['sno'],':',ubike_sta['sname'], \
    ':\n\t weather station[',ubike_sta['wno'],']:',ubike_sta['wname'], \
    '\n\t airbox device[',ubike_sta['did'],']:',ubike_sta['dname'])
