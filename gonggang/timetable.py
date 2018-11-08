import requests,re
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ElementTree
from datetime import date

def my_timetable(userid, password, year, semester):
    result_xml = ""
    payload = {'userid': userid, 'password': password}
    url = 'https://everytime.kr/user/login'

    with requests.Session() as session:
        index_page_res = session.post(url, data=payload)

        soup = BeautifulSoup(index_page_res.text, 'html.parser')

        timetable_result = session.post("http://timetable.everytime.kr/ajax/timetable/wizard/getTableList", data={
            "semester": semester,
            "year": year,
        })

        tree = ElementTree.fromstring(timetable_result.text)
        for target in tree.findall('table[@is_primary="1"]'):
            id = target.get('id')
            table_xml = session.post("http://timetable.everytime.kr/ajax/timetable/wizard/getOneTable", data={
                "id": id,
            })
            result_xml = table_xml

    return result_xml.text

def friends_list(userid, password):
    result_xml = ""
    payload = {'userid': userid, 'password': password}
    url = 'https://everytime.kr/user/login'

    rtn = []
    with requests.Session() as session:
        index_page_res = session.post(url, data=payload)

        soup = BeautifulSoup(index_page_res.text, 'html.parser')

        friends = session.post("https://everytime.kr/find/friend/list")
        import re
        s = friends.text
        pat = re.compile(r'userid="\w*"')
        pat1 = re.compile(r'(name="\w{1,}")|(name="\w{1,} \w{1,}")')
        fs = pat.findall(s)
        names = pat1.findall(s)
        pt1 = []
        for i in range(len(fs)):
            first = names[i][0]
            second = names[i][1]
            if(first ==''):
                pt1.append(second)
            else:
                pt1.append(first)
        for i in range(len(fs)):
            tmp0 = []
            tmp0.append(fs[i][8:-1])
            tmp0.append(pt1[i][6:-1])
            rtn.append(tmp0)
    print(rtn)
    return rtn

def get_timetable(userid, password,id_):
    result_xml = ""
    payload = {'userid': userid, 'password': password}
    #url = 'https://everytime.kr/'+'@'+id_
    url = 'https://everytime.kr/find/timetable/table/friend'
    login_url = 'https://everytime.kr/user/login'

    with requests.Session() as session:
        index_page_res = session.post(login_url, data=payload)

        soup = BeautifulSoup(index_page_res.text, 'html.parser')
        tt = session.post(url,data={
            "identifier":  id_,
            "friendInfo": True
        })
        print(id_)
        return tt.text

def table2array(raw):
    #9시 108, 5분당 +1
    import re
    time = re.compile(r'starttime="\d{3}"|endtime="\d{3}"')
    day = re.compile(r'day="\d{1}"')
    times = time.findall(raw)
    days = day.findall(raw)
    rtn = []
    for i in range(len(days)):
        start = times[i*2][11:-1]
        end= times[i*2+1][9:-1]
        days[i] = days[i][5]
        rtn.append([(int(start),int(end)),int(days[i])])
    return rtn

def isavailable(tt, time):
    #time = [(hour,minute), day]
    hour = 108+(time[0][0]-9)*12
    minute = time[0][1]/5
    t = hour+minute
    #print(t)
    #print(tt)
    for i in tt:
        if((i[1] == time[1]) and (i[0][0]<=t and t<=i[0][1])):
            return False
    return True
