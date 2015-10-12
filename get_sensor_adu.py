#!usr/bin/python

import serial, os,time
import sys
import MySQLdb
import datetime

print "test uart"

ser =serial.Serial(port=12, baudrate=19200)
print ser
#ser.open()
print "successfully open"
db = MySQLdb.connect(host="awshomework.csrmmxirvejo.ap-northeast-1.rds.amazonaws.com", port=3306, user="user", passwd="q1w2e3r4", db="indoor")
cursor = db.cursor()
print "successfully connect"

while 1:
    data = ser.readline()
    print data
    temp = 0
    humi = 0
    co2 = 0
    #	print data[2], data[3], data[4], data[6]
    #	print data[10], data[11], data[12], data[14]
    #	print data[23]
    '''
    if not (data[2].isdigit() & data[3].isdigit() & data[4].isdigit() & data[6].isdigit()) :
        print 3
        continue
    if not (data[10].isdigit() & data[11].isdigit() & data[12].isdigit() & data[14].isdigit()) :
        print 4
        continue
    if not (data[23].isdigit()) :
        print 5
        continue
    '''
    print len(data)
    for i in range(len(data)) :
        if data[i] is 'T' :
            temp += (int(data[i+1])) * 10
            temp += (int(data[i+2])) * 1
            temp += (int(data[i+4])) * 0.1
        elif data[i] is 'H' :
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

    now = time.localtime()
    sql = "insert into Pure_data (nodeid, Temperature, Humidity, Co2, regdate) values (1, %.1f, %.1f, %d, now()+ interval 9 hour )" % (temp, humi, co2)
    cursor.execute(sql)
    db.commit()
    time.sleep(10)

ser.close()
