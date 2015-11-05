#-*- coding: utf-8 -*-
__author__ = 'ji'

import httplib
import MySQLdb
import time
import datetime
conn = httplib.HTTPConnection("192.168.0.56")
db = MySQLdb.connect(host="awshomework.csrmmxirvejo.ap-northeast-1.rds.amazonaws.com", port=3306, user="user", passwd="q1w2e3r4", db="indoor")
cursor = db.cursor()

occ_confirm=0

while 1:
    sql ="select * from Pure_data order by regdate desc limit 1;"
    cursor.execute(sql)
    row=cursor.fetchone()
    sql ="select * from Alarm_data order by regdate desc limit 1;"
    cursor.execute(sql)
    row_a=cursor.fetchone()
    sql ="select * from Change_data order by regdate desc limit 1;"
    cursor.execute(sql)
    row_c=cursor.fetchone()
    #print row_c
    #print row_a
    #print row

    if row_c[3]!=0 and occ_confirm==0:
        value='{"on":true, "sat":255, "bri": 255, "hue": 40000}'
        conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
        responses = conn.getresponse()
        data = responses.read()
        value='{"on":true}'
        conn.request("PUT", "/api/newdeveloper/lights/2/state", value)
        responses = conn.getresponse()
        data = responses.read()
        occ_confirm=1
        print "occupant on"
    	time.sleep(5)
        value='{"on":true, "sat":130, "bri":255, "hue":14000}'
        conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
        responses = conn.getresponse()
        data = responses.read()
        print "init"
        time.sleep(3)

    elif row_c[3]==0 and occ_confirm==1:
        value='{"on" : false}'
        conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
        responses = conn.getresponse()
        data = responses.read()
        conn.request("PUT", "/api/newdeveloper/lights/2/state", value)
        responses = conn.getresponse()
        data = responses.read()
        occ_confirm=0
        print "occupant off"
        time.sleep(3)

    if row[6].time().hour == row_a[5] and row[6].time().minute == row_a[6]:# and row_a[7]=='1' :
        sql ="select * from API_data order by regdate desc limit 1;"
        cursor.execute(sql)
        row_w=cursor.fetchone()
        print "wake up"
        for count in range(0,255) :
            value='{"on":true, "sat":255, "bri": %d, "hue": 20000}' % (count)
            conn.request("PUT", "2", value)
            responses = conn.getresponse()
            data = responses.read()
            time.sleep(0.2)
        #print row_w[3]
        for count in range(5) :
            print "weather"
            for value_bri in range(10,250,10) :
                if row_w[3]==1 :
                    value='{"on":true, "sat":255, "bri": %d, "hue": 65280}' % (value_bri)
                    conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
                    responses = conn.getresponse()
                    data = responses.read()
                    time.sleep(0.1)
                elif row_w[3]==2 :
                    value='{"on":true, "sat":255, "bri": %d, "hue": 10000}' % (value_bri)
                    conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
                    responses = conn.getresponse()
                    data = responses.read()
                    time.sleep(0.1)
                elif row_w[3]==3 :
                    value='{"on":true, "sat":255, "bri": %d, "hue": 30000}' % (value_bri)
                    conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
                    responses = conn.getresponse()
                    data = responses.read()
                    time.sleep(0.1)
                elif row_w[3]==4 :
                    value='{"on":true, "sat":255, "bri": %d, "hue": 60000}' % (value_bri)
                    conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
                    responses = conn.getresponse()
                    data = responses.read()
                    time.sleep(0.1)
                elif row_w[3]==5 :
                    value='{"on":true, "sat":255, "bri": %d, "hue": 40000}' % (value_bri)
                    conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
                    responses = conn.getresponse()
                    data = responses.read()
                    time.sleep(0.1)
        value='{"on" : false}'
        conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
        responses = conn.getresponse()
        data = responses.read()
        print "alarm off"
        value='{"on":true, "sat":130, "bri":255, "hue":14000}'
        conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
        responses = conn.getresponse()
        data = responses.read()
        print "init"
        time.sleep(3)

    if row[6].time().minute%5==0 :
        if row[2]> 1000 :
            value='{"on":true, "sat":255, "bri": 255, "hue": 25500}'
            conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
            responses = conn.getresponse()
            data = responses.read()
            print "co2"
            time.sleep(3)
        if row[3] >= 25:
            value='{"on":true, "sat":255, "bri": 255, "hue": 65280}'
            conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
            responses = conn.getresponse()
            data = responses.read()
            print "temperature"
            time.sleep(3)
        if row[4] > 60:
            value='{"on":true, "sat":255, "bri": 255, "hue": 46920}'
            conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
            responses = conn.getresponse()
            data = responses.read()
            print "humidity"
            time.sleep(3)
        value='{"on":true, "sat":130, "bri":255, "hue":14000}'
        conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
        responses = conn.getresponse()
        data = responses.read()
        print "init"
        time.sleep(3)
    
    """
    for test in range(42,255) :
        value='{"on":true, "sat":255, "bri": %d, "hue": 45555}' % (test)
        conn.request("PUT", "/api/newdeveloper/lights/1/state", value)
        responses = conn.getresponse()
        data = responses.read()
        time.sleep(0.1)
        print test
    #elif
    """

    db.commit()
    print datetime.datetime.today().ctime()
    time.sleep(5)