import re
import requests

def stations():
    url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9033'
    response=requests.get(url,verify=False)
    stations=re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response.text)
    return dict(stations)