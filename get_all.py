#!usr/bin/python

import serial
import sys
import urllib2
import MySQLdb
import time
import datetime
from datetime import timedelta
power=[6800,2950 ,600 ,450 ,550 ,450, 550 ,1350, 600 ,1350, 550 ,450 ,550 ,500 ,550 ,450,550 ,500, 550 ,500 ,550 ,450, 550 ,450, 550 ,1400 ,550 ,1350, 550 ,500 ,550 ,450 ,550 ,500 ,550 ,500,550 ,450 ,550 ,1350, 550 ,1400, 550,450, 550 ,1400 ,550 ,500 ,550 ,450 ,600];
humi=0
act=0

result = [[], [], [], [], [], [], []]
dates = [[], [], [], [], [], [], []]
x = [[], [], [], [], [], [], []]
row_h, datetime_ = [], []
after30 = before30 = aver10 = 0
co2min = 2000
stand_gradient = 0.5
stand_co2 = 100
confirm_co2=0

def sensing() :
    global humi
    ser.write("sensor")
    data=ser.readline()
    print data
    temp = 0
    humi = 0
    co2 = 0

    for i in range(len(data)) :
        if data[i] is 'T' :
            if data[i+2] is '.' or data[i+4] is '.':
                continue
            else :
                temp += (int(data[i+1])) * 10
                temp += (int(data[i+2])) * 1
                temp += (int(data[i+4])) * 0.1
        elif data[i] is 'H' :
            if data[i+2] is '.' or data[i+4] is '.':
                continue
            else :
                humi += (int(data[i+1])) * 10
                humi += (int(data[i+2])) * 1
                humi += (int(data[i+4])) * 0.1
        elif data[i] is 'C' :
            if data[i+2] is '.' or data[i+3] is '.':
                continue
            elif data[i+5] is '.' :
                co2 += (int(data[i+1])) * 1000
                co2 += (int(data[i+2])) * 100
                co2 += (int(data[i+3])) * 10
                co2 += (int(data[i+4])) * 1
                co2 += (int(data[i+6])) * 0.1
            else :
                co2 += (int(data[i+1])) * 100
                co2 += (int(data[i+2])) * 10
                co2 += (int(data[i+3])) * 1
                co2 += (int(data[i+5])) * 0.1

#	print 1
    print 'temp = ' + str(temp)
    print 'humi = ' + str(humi)
    print 'co2 = ' + str(co2)
    print datetime.datetime.today().ctime()
    if co2>=1500 :
        print 'on!!!'
    now = time.localtime()
    if count>4 :
        sql = "insert into Pure_data (nodeid, Temperature, Humidity, Co2, regdate) values (1, %.1f, %.1f, %d, now()+ interval 9 hour )" % (temp, humi, co2)
        cursor.execute(sql)
        db.commit()

    time.sleep(3)

def api() :
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

    weather = getweather(getDataPage())
    temperature = gettemperature(getDataPage())
    humidity = gethumidity(getDataPage())
    #finedust = getdust(getDataPage2())
    finedust = 0
    pnt3 = ""

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

    sql ="insert into API_data (nodeid, dust, temperature, humidity, weather, regdate) values (1, %d, %d, %d, %s, now()+ interval 9 hour)" % (int(finedust), int(temperature), int(humidity), weather)
    cursor.execute(sql)
    db.commit()
    print datetime.datetime.today().ctime()

def change() :
    def typevalue_():
        global row_h
        sql = "select co2, regdate from Pure_data where now()+ interval 3 hour <= regdate and  regdate <= now()+ interval 9 hour order by regdate"
        cursor.execute(sql)
        row_h.append(cursor.fetchall())
        db.commit()
        return row_h

    def afbe_():
        global after30, before30, aver10
        td1 = timedelta(minutes=10)
        td2 = row_h[0][0][1] + td1
        for j in range(0, len(row_h[0])):
                if td2 > row_h[0][j][1]:
                    after30 = after30 + 1
        td3 = row_h[0][after30][1] - td1
        for k in range(0, len(row_h[0])):
            if td3 > row_h[0][k][1]:
                before30 = before30 + 1

    def co2_():
        global co2min, dates, result
        for i in range(0, len(row_h[0])):
            dates[1].append(row_h[0][i][1])
        for i in range(0, len(row_h[0])):
            result[1].append(row_h[0][i][0])
            if co2min > row_h[0][i][0]:
                co2min = row_h[0][i][0]
                if(co2min<=350):
                    co2min=350

    def gradient_():
        global after30, before30, dates, result
        for i in range(after30, len(dates[1])):
            dates[2].append(dates[1][i])
        for i in range(after30, len(dates[1])):
            if len(dates[1])<before30 :
                break
            if (dates[1][i].minute - dates[1][before30].minute) > 0:
                    result[2].append(float((result[1][i] - result[1][before30])) / 20)
            elif (dates[1][i].minute - dates[1][before30].minute) < 0:
                    result[2].append(float((result[1][i] - result[1][before30])) / 20)
            elif (i != after30) and (dates[1][i].minute - dates[1][before30].minute == 0):
                    result[2].append(float(result[2][i - after30 - 1]))  # result[4][i-n-1]
            else:
                result[2].append(0)
            before30 = before30 + 1

    def co2init_():
        global result, dates
        for i in range(0, len(dates[1])):
            dates[3].append(dates[1][i])
        for i in range(0, len(result[1])):
            result[3].append(result[1][i] - co2min)

    def absence_(stand_gradient, stand_co2):
        global after30, before30, result, dates

        for i in range(0, len(dates[2])):
            dates[4].append(dates[2][i])
        for i in range(0, len(dates[2])):
            if stand_gradient <= float(result[2][i]) and (result[3][i + after30] <=200):
                result[4].append(1)
            elif i != 0  and result[4][i - 1] == 1 and (result[3][i + after30] > 200) and (stand_gradient <= float(result[2][i])):
                result[4].append(2)
            elif i != 0  and result[4][i - 1] == 2 and (result[3][i + after30] > 400) and (stand_gradient <= float(result[2][i])):
                result[4].append(3)
            elif i != 0  and result[4][i - 1] == 3 and (result[3][i + after30] > 600) and (stand_gradient <= float(result[2][i])):
                result[4].append(4)
            elif i != 0  and result[4][i - 1] == 4 and (result[3][i + after30] > 800) and (stand_gradient <= float(result[2][i])):
                result[4].append(5)
            elif i != 0  and result[4][i - 1] == 5 and result[3][i + after30] >= 800:
                result[4].append(5)
            elif i != 0  and result[4][i - 1] == 5 and result[3][i + after30] < 800:
                result[4].append(4)
            elif i != 0  and result[4][i - 1] == 4 and (float((-2) * stand_gradient)) < float(result[2][i]):
                result[4].append(4)
            elif i != 0  and result[4][i - 1] == 4 and (stand_co2 <= result[3][i + after30] <800) and (float((-1) * stand_gradient)) >= float(result[2][i]):
                result[4].append(3)
            elif i != 0  and result[4][i - 1] == 3 and (float((-2) * stand_gradient)) < float(result[2][i]):
                result[4].append(3)
            elif i != 0  and result[4][i - 1] == 3 and (stand_co2 <= result[3][i + after30] <600) and (float((-1) * stand_gradient)) >= float(result[2][i]):
                result[4].append(2)
            elif i != 0  and result[4][i - 1] == 2 and (float((-2) * stand_gradient)) < float(result[2][i]):
                result[4].append(2)
            elif i != 0  and result[4][i - 1] == 2 and (stand_co2 <= result[3][i + after30] <400) and (float((-1) * stand_gradient)) >= float(result[2][i]):
                result[4].append(1)
            elif i != 0  and result[4][i - 1] == 1 and (float((-1) * stand_gradient)) < float(result[2][i]):
                result[4].append(1)
            elif i != 0  and result[4][i - 1] == 1 and (float((-1) * stand_gradient)) >= float(result[2][i]) and (stand_co2 < result[3][i + after30]) :
                result[4].append(1)
            elif i != 0  and result[4][i - 1] == 1 and (float((-1) * stand_gradient)) >= float(result[2][i]) and (stand_co2 >= result[3][i + after30]) :
                result[4].append(0)
            elif i != 0 :
                result[4].append(result[4][i-1])
            else :
                result[4].append(0)

    global result, dates, x, row_h, datetime, after30, before30, aver10, co2min, stand_co2, stand_gradient, confirm_co2, act
    sql ="select nodeid, temperature, humidity, regdate  from Pure_data order by regdate desc limit 1;"
    cursor.execute(sql)
    row=cursor.fetchone()
    print row[3]
    result = [[], [], [], [], [], [], []]
    dates = [[], [], [], [], [], [], []]
    x = [[], [], [], [], [], [], []]
    row_h, datetime_ = [], []
    after30 = before30 = aver10 = 0
    co2min = 2000
    stand_gradient = 0.5
    stand_co2 = 0

    row_h = typevalue_()
    co2_()
    print "co2 = "+str(result[1][-1])
    print "Co2min = "+str(co2min)
    afbe_()
    gradient_()
    print "gradient = "+str(result[2][-1])
    co2init_()
    print "init = "+str(result[3][-1])
    absence_(stand_gradient, stand_co2)
    print "human : "+str(result[4][-1])
    if result[4][-1]>=1:
        confirm_co2=1
    elif confirm_co2==1 and result[4][-1]==0 :
        remote()
        act=count;

    regdate_temp=row[3]
    comfort=9/5*row[1]-(0.55)*(1-row[2]/100)*(9/5*row[1]-26)+32
    if(row[1]-22>0) :
        energy=(row[1]-22)*(7)
    else :
        energy=0
    print "comfort : " + str(comfort)
    print "energy : " + str(energy)
    sql ="insert into Change_data (nodeid, energy, comfort, occupant, regdate) values (1, %d, %d, %d, '%s')" % (energy, comfort, result[4][-1], str(regdate_temp))
    cursor.execute(sql)
    db.commit()
    print datetime.datetime.today().ctime()
    time.sleep(3)


def remote() :
    ser.write("remote")
    data=ser.readline()
    print data

    if data[0] is '1' :
        print 3
        for i in range(0,len(power)) :
            ser.write(str(power[i]))
            print str(power[i])
        print "last"
        ser.write(str(-1).encode());




print "test uart"

ser =serial.Serial(port=12, baudrate=19200)
print ser
#ser.open()
print "successfully open"
db = MySQLdb.connect(host="awshomework.csrmmxirvejo.ap-northeast-1.rds.amazonaws.com", port=3306, user="user", passwd="q1w2e3r4", db="indoor")
cursor = db.cursor()
print "successfully connect"
count=0;

while 1:
    time.sleep(5);
    print count
    count=count+1
    sensing()
    if humi>=50 and act==0:
        remote()
        act=count
    if count%10==0 and count is not 0 :
        print 1
        api()
    if act<count+20 :
        act=0
    if count%2 is not 0 :
        change()
ser.close()

