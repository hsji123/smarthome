__author__ = 'ji'
import serial

power={6800,2950 ,600 ,450 ,550 ,450, 550 ,1350, 600 ,1350, 550 ,450 ,550 ,500 ,550 ,450,550 ,500, 550 ,500 ,550 ,450, 550 ,450, 550 ,1400 ,550 ,1350, 550 ,500 ,550 ,450 ,550 ,500 ,550 ,500,550 ,450 ,550 ,1350, 550 ,1400, 550,450, 550 ,1400 ,550 ,500 ,550 ,450 ,600};

print "test uart"

ser =serial.Serial(port=12, baudrate=19200)
print ser

while 1:
    ser.write("remote")
    data=ser.readline()
    print data
    if data=="success" :
        print 3
        for i in range(0,51) :
            ser.write(power[i])
            print power[i]
        ser.write(-1);
ser.close()
