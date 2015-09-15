#-*- coding: utf-8 -*-
__author__ = 'ji'

import MySQLdb
import time
import datetime
from datetime import timedelta

def typevalue_():
    global row_h
    sql = "select co2, regdate from Pure_data where now()+ interval 3 hour <= regdate and  regdate <= now()+ interval 9 hour order by regdate"
    cursor.execute(sql)
    row_h.append(cursor.fetchall())
    db.commit()
    return row_h


def afbe_():
    global after30, before30, aver10
    td1 = timedelta(minutes=20)
    td2 = row_h[0][0][1] + td1
    for j in range(0, len(row_h[0])):
            if td2 > row_h[0][j][1]:
                after30 = after30 + 1
    td3 = row_h[0][after30][1] - td1
    for k in range(0, len(row_h[0])):
        if td3 > row_h[0][k][1]:
            before30 = before30 + 1


def co2_():
    global co2min
    for i in range(0, len(row_h[0])):
        dates[1].append(row_h[0][i][1])
    for i in range(0, len(row_h[0])):
        result[1].append(row_h[0][i][0])
        if co2min > row_h[0][i][0]:
                co2min = row_h[0][i][0]


def gradient_():
    global after30, before30
    for i in range(after30, len(dates[1])):
        dates[2].append(dates[1][i])
    for i in range(after30, len(dates[1])):
        if len(dates[1])<before30 :
            break
        if (dates[1][i].minute - dates[1][before30].minute) > 0:
                result[2].append(float((result[1][i] - result[1][before30])) / 30)
        elif (dates[1][i].minute - dates[1][before30].minute) < 0:
                result[2].append(float((result[1][i] - result[1][before30])) / 30)
        elif (i != after30) and (dates[1][i].minute - dates[1][before30].minute == 0):
                result[2].append(float(result[2][i - after30 - 1]))  # result[4][i-n-1]
        else:
            result[2].append(0)
        before30 = before30 + 1


def co2init_():
    for i in range(0, len(dates[1])):
        dates[3].append(dates[1][i])
    for i in range(0, len(result[1])):
        result[3].append(result[1][i] - co2min)


def absence_(stand_gradient, stand_co2):
    global after30, before30
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

result = [[], [], [], [], [], [], []]
dates = [[], [], [], [], [], [], []]
x = [[], [], [], [], [], [], []]
row_h, datetime_ = [], []
after30 = before30 = aver10 = 0
co2min = 700
stand_gradient = 0.5
stand_co2 = 100

db = MySQLdb.connect(host="awshomework.csrmmxirvejo.ap-northeast-1.rds.amazonaws.com", port=3306, user="user", passwd="q1w2e3r4", db="indoor")
cursor = db.cursor()

sql ="select nodeid, temperature, humidity, regdate  from Pure_data order by regdate desc limit 1;"

cursor.execute(sql)
row=cursor.fetchone()
regdate_temp=row[3]

#print sql
while 1 :
    sql ="select nodeid, temperature, humidity, regdate  from Pure_data order by regdate desc limit 1;"
    cursor.execute(sql)
    row=cursor.fetchone()
    print row[3]
    if regdate_temp!=row[3]:
        result = [[], [], [], [], [], [], []]
        dates = [[], [], [], [], [], [], []]
        x = [[], [], [], [], [], [], []]
        row_h, datetime_ = [], []
        after30 = before30 = aver10 = 0
        co2min = 2000
        stand_gradient = 0.5
        stand_co2 = 100

        row_h = typevalue_()
        co2_()
        afbe_()
        gradient_()
        co2init_()
        absence_(stand_gradient, stand_co2)
        print "human : "+str(result[4][-1])

        regdate_temp=row[3]
        comfort=9/5*row[1]-(0.55)*(1-row[2]/100)*(9/5*row[1]-26)+32
        if(row[1]-26<0) :
            energy=(row[1]-26)*(-7)
        else :
            energy=0
        print "comfort : " + str(comfort)
        print "energy : " + str(energy)
        sql ="insert into Change_data (nodeid, energy, comfort, occupant, regdate) values (1, %d, %d, %d, '%s')" % (energy, comfort, result[4][-1], str(regdate_temp))
        cursor.execute(sql)
    db.commit()
    print datetime.datetime.today().ctime()
    time.sleep(10)

