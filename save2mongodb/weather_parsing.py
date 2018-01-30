import urllib.request
import json
import xml.etree.ElementTree


def parsing_weather(node,wdata):

    for idx in node:
        idxt = idx.tag
        val = idx.text
        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}lat":
            wdata['lat'] = float(val)

        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}lon":
            wdata['lon'] = float(val)

        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}lat_wgs84":
            wdata['lat_wgs84'] = float(val)

        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}lon_wgs84":
            wdata['lon_wgs84'] = float(val)

        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}locationName":
            wdata['locationName'] = val

        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}stationId":
            wdata['stationId'] = val

        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}time":
            for child in idx:
                if(child.tag == "{urn:cwb:gov:tw:cwbcommon:0.1}obsTime"):
                    wdata['time'] = child.text
        #weather data:
        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}weatherElement":
            child = idx[0]
            if child.tag == "{urn:cwb:gov:tw:cwbcommon:0.1}elementName":
                name = child.text
                child = idx[1]
                if child.tag == "{urn:cwb:gov:tw:cwbcommon:0.1}elementValue":
                    child = child[0]
                    if name != "H_FXT":
                        wdata[name] = float(child.text)
                    else:
                        wdata[name] = child.text

        #parameter data:
        if idxt == "{urn:cwb:gov:tw:cwbcommon:0.1}parameter":
            child = idx[0]
            if child.tag == "{urn:cwb:gov:tw:cwbcommon:0.1}parameterName":
                name = child.text
                child = idx[1]
                if child.tag == "{urn:cwb:gov:tw:cwbcommon:0.1}parameterValue":
                    if name == "CITY" or name == "TOWN":
                        wdata[name] = child.text
                    else:
                        wdata[name] = int(child.text)




#weather_url = "http://opendata.cwb.gov.tw/opendataapi?dataid=O-A0001-001&authorizationkey=CWB-B74D517D-9F7C-44B9-90E9-4DF76361C725"
#res = urllib.request.urlretrieve(weather_url, "weather_data.xml")

weather_e = xml.etree.ElementTree.parse('weather_data.xml')
weather_root = weather_e.getroot()
print('weather root >>> ',weather_root.tag)

#print all structure
if False:
    for child in weather_root:
        print(child.tag,':',child.text)
        for grand_child in child:
            print('\t',grand_child.tag,':',grand_child.text)
            for gg_child in grand_child:
                print('\t\t',gg_child.tag,':',gg_child.text)
                for ggg_child in gg_child:
                    print('\t\t\t',ggg_child.tag,':',ggg_child.text)

weather_list = []
if True: #print all taipei data
    root_tmp = weather_root
    foundTP = False
    TPTownNum = 0
    for child in root_tmp:
        for g_child in child:
            for gg_child in g_child:
                if(gg_child.text == '臺北市'):
                    foundTP = True
                    TPTownNum = TPTownNum + 1
        wdata = {}
        if foundTP == True: #print all data for this g_child
            print('No.',TPTownNum,':')
            if False:
                for g_child in child:
                    #if g_child.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}locationName':
                    #    print(g_child.tag,':',g_child.text)
                    print(g_child.tag,":",g_child.text)
                    for gg_child in g_child:
                        print(gg_child.tag,":",gg_child.text)
                        for ggg_child in gg_child:
                            print(ggg_child.tag,":",ggg_child.text)
                            for gggg_child in ggg_child:
                                print(gggg_child.tag,":",gggg_child.text)
            else:
                parsing_weather(child,wdata)
                #print(wdata)
                weather_list = weather_list + [wdata]
            foundTP = False
    print(weather_list)
    print('There are ',TPTownNum,' Town in Taipei.')
