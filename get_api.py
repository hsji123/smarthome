#-*- coding: utf-8 -*-
import sys
import urllib2
import MySQLdb
import time
import datetime

def getWebpage(url, referer=''):
    debug = 0
    if debug:
        return file(url.split('/')[-1], 'rt').read()
    else:
        opener = urllib2.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'),
            ('Referer', referer),
        ]
        return opener.open(url).read()

def getDataPage():
    return getWebpage('http://www.kma.go.kr/weather/forecast/timeseries.jsp')

def getDataPage2():
    return getWebpage('http://www.airkorea.or.kr/index')

def printUsing():
    print sys.argv[0], '<output file name>'

#def getDatetime(buffers):
#    return buffers.split('<p class="now_time">')[1].split('<strong>')[1].split('</strong>')[0]

def getweather(buffers):
   weather=buffers.split('<dt class="bold Wimg">')[1].split('" class="png24"')[0].split('DY/')[1].split('.png')[0]
   return weather

def gettemperature(buffers):
   temp=buffers.split('<dd class="hum plus">')[1]
   temperature=temp.split('</dd>')[0]
   return temperature[0:-3]

def gethumidity(buffers):
   temp=buffers.split('<dd class="reh"><strong>')[1]
   humidity=temp.split('</dd>')[0].replace('</strong>','').replace('%','')
   #temperature=temp.split('/>')[2]
   return humidity

def getdust(buffers):
    temp = buffers.split('<tbody id="mt_mmc2_10007">')[1]
    dust = temp.split('</tbody>')[0].replace('<tr>','').replace('</tr>','').replace('</td>','').split('<td>')[2]
    return dust


#global data
if len(sys.argv) <> 1:
    printUsing()
    sys.exit(1)

db = MySQLdb.connect(host="awshomework.csrmmxirvejo.ap-northeast-1.rds.amazonaws.com", port=3306, user="user", passwd="q1w2e3r4", db="indoor")
cursor = db.cursor()

while 1:
    #datetime = "%s \n" % getDatetime(getDataPage2())
    weather = getweather(getDataPage())
    temperature = gettemperature(getDataPage())
    humidity = gethumidity(getDataPage())
    finedust = getdust(getDataPage2())
    pnt3 = ""
    """
    for i in pnt2:
        pnt3+=i
        pnt3+="\n"
    """
    #print pnt
    #print weather
    print weather
    if weather=="DB01" :
        weather=1
    elif weather=="DB01_N" :
        weather=1
    elif weather=="DB02" :
        weather=2
    elif weather=="DB02_N" :
	weather=2
    elif weather=="DB03" :
        weather=3
    elif weather=="DB03_N" :
        weather=3
    elif weather=="DB04" :
        weather=4
    elif weather=="DB04_N" :
        weather=4
    elif weather=="DB05" :
        weather=5
    elif weather=="DB08" :
        weather=6
    elif weather=="DB20" :
        weather=7
    elif weather=="DB11" :
        weather=8
    elif weather=="DB21" :
        weather=9
    elif weather=="DB12" :
        weather=10
    elif weather=="DB22" :
        weather=11
    elif weather=="DB13" :
        weather=12
    elif weather=="DB23" :
        weather=13
    elif weather=="DB14" :
        weather=14
    elif weather=="DB18" :
        weather=15
    elif weather=="DB15" :
        weather=16
    elif weather=="DB17" :
        weather=17
    elif weather=="DB16" :
        weather=18
    else :
        weather=20
    print 'weather '+str(weather)
    print 'temperature '+str(temperature)
    print 'humidity '+str(humidity)
    print 'finedust '+str(finedust)
    #print weather[:1]

    sql ="insert into API_data (nodeid, dust, temperature, humidity, weather, regdate) values (1, %d, %d, %d, %s, now()+ interval 9 hour)" % (int(finedust), int(temperature), int(humidity), weather)
    #sql ="insert into API_data (nodeid, dust, temperature, humidity, regdate) values (1, %d, %d, %d, now())" % (int(finedust), int(temperature), int(humidity))
    #print sql
    cursor.execute(sql)
    db.commit()
    print datetime.datetime.today().ctime()
    time.sleep(60)


