import serial
ser = serial.Serial(
port='/dev/ttyS0',
baudrate=115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS
)
counter = 0
ser.write(b"hola\r\n")
while True:
    x = ser.readline()
    cn = len(x)
    if cn>0:  # lint:ok
        print (x)
        counter += 1
        if (counter==10):  # lint:ok
            break
ser.close()
