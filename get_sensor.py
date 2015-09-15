#!usr/bin/python

import serial, os,time
import sys
import MySQLdb
import datetime

print "test uart"

ser = serial.Serial('/dev/ttyAMA0',38400)
ser.open()
print "successfully open"
db = MySQLdb.connect(host="awshomework.csrmmxirvejo.ap-northeast-1.rds.amazonaws.com", port=3306, user="user", passwd="q1w2e3r4", db="indoor")
cursor = db.cursor()
print "successfully connect"

while 1:
    data = ser.read(28)
    print data
    temp = 0
    humi = 0
    co2 = 0
    #	print data[2], data[3], data[4], data[6]
    #	print data[10], data[11], data[12], data[14]
    #	print data[23]
    if not (data[2].isdigit() & data[3].isdigit() & data[4].isdigit() & data[6].isdigit()) :
        print 3
        continue
    if not (data[10].isdigit() & data[11].isdigit() & data[12].isdigit() & data[14].isdigit()) :
        print 4
        continue
    if not (data[23].isdigit()) :
        print 5
        continue
    #	print 2
    if (data[1] is '+') :
        temp += (int(data[2])) * 100
        temp += (int(data[3])) * 10
        temp += (int(data[4])) * 1
        temp += (int(data[6])) * 0.1
    else :
        temp += (int(data[2])) * 100
        temp += (int(data[3])) * 10
        temp += (int(data[4])) * 1
        temp += (int(data[6])) * 0.1
        temp * -1

    if (data[9] is '+') :
        humi += (int(data[10])) * 100
        humi += (int(data[11])) * 10
        humi += (int(data[12])) * 1
        humi += (int(data[14])) * 0.1
    else :
        humi += (int(data[10])) * 100
        humi += (int(data[11])) * 10
        humi += (int(data[12])) * 1
        humi += (int(data[14])) * 0.1
        humi * -1

    if (data[20] is ' ') :
        co2 += (int(data[21])) * 100
        co2 += (int(data[22])) * 10
        co2 += (int(data[23])) * 1
    else :
        co2 += (int(data[20])) * 1000
        co2 += (int(data[21])) * 100
        co2 += (int(data[22])) * 10
        co2 += (int(data[23])) * 1

    temp = temp-3.5
#	print 1
    print temp
    print humi
    print co2
    print datetime.datetime.today().ctime()

    now = time.localtime()
    sql = "insert into Pure_data (nodeid, Temperature, Humidity, Co2, regdate) values (1, %.1f, %.1f, %d, now()+ interval 9 hour )" % (temp, humi, co2)
    cursor.execute(sql)
    db.commit()
    time.sleep(10)

ser.close()
