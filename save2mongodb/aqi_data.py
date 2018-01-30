import urllib.request
import json
import xml.etree.ElementTree

#UV data: retrieve UV data in Taipei
uv_url = "http://opendata.cwb.gov.tw/opendataapi?dataid=O-A0005-001&authorizationkey=CWB-B74D517D-9F7C-44B9-90E9-4DF76361C725"
uv_res = urllib.request.urlretrieve(uv_url, "uv_data.xml")

uv_e = xml.etree.ElementTree.parse('uv_data.xml')
uv_root = uv_e.getroot()
print(" ==== parsing UV data ====")
foundTP = False
for child in uv_root:
    #print(child.tag,':',child.text)
    if child.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}sent':
        print('Sent Time : ',child.text)
    if child.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}dataset':
        #print('data set found!!!!!!')
        for grand_child in child:
            #print(grand_child.tag,':',grand_child.text)
            if grand_child.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}weatherElement':
                #print('weather element found!!!!!!')
                for gg_child in grand_child:
                    #print(gg_child.tag,':',gg_child.text)
                    if gg_child.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}location':
                        for ggg_child in gg_child:
                            if foundTP == True:
                                print('Taipei UV : ',ggg_child.text)
                                foundTP = False
                            if ggg_child.text == '466920':
                                foundTP = True





print(" ==== parsing AQI data ====")
#retrieve AQI data in Taipei
aqi_url = "http://opendata2.epa.gov.tw/AQI.json"
urllib.request.urlretrieve(aqi_url, "aqi.json")
aqi_f = open("aqi.json")
aqi_jdata = aqi_f.read()
aqi_f.close()

aqi_data = json.loads(aqi_jdata)

for data in aqi_data:   #aqi_data: list, data: dict
    if data['County'] == '臺北市':
        pm = data.pop('PM2.5')
        data['PM25'] = pm
        pm = data.pop('PM2.5_AVG')
        data['PM25_AVG'] = pm
        print(data)
        #print('PublishTime: ',data['PublishTime'])
        #print('SiteName: ',data['SiteName'])
        #print('AQI: ',data['AQI'])
        #print('PM2.5: ',data['PM2.5'])
