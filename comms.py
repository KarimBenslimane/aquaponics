import serial


def createConnection():
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        return ser
    except Exception as e:
        return False

def retrieveData(ser):
    try:
        line = 0
        while line == 0:
            if ser.in_waiting > 0:
                line = ser.readline()
                return line
    except Exception as e:
        f = open("/var/www/html/aquaponics/file.txt", "w+")
        f.write(str(e))
        f.close()
        return ''

