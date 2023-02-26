
import serial, time, struct
import sys
from sys import stdout
 
def writefont(ser, addr, data):
    checksum = 0
    # send
    txdata = bytearray([0x24, 0x4d, 0x3c, 2+64, 87, addr&0xff, (addr>>8)&0xff]) + data
    #print(txdata)
    for i in txdata[3:len(txdata)]:
        checksum = checksum ^ i
    txdata.append(checksum)
    print('send:', end='')
    for x in txdata:
        print('{:02x} '.format(x), end='')
    print('')
    ser.write(txdata)
    return


if __name__ == "__main__":

    args = sys.argv
    if len(args) != 2:
        print('need com port')
        exit()

    ser = serial.Serial()
    ser.port = args[1]
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    ser.writeTimeout = 2
    ser.open()

    f = open('betaflight.mcm')
    print(f.readline())

    for addr in range(0x200):
        print('=== addr:{:04x}==='.format(addr))
        data = bytearray()
        for x in range(64):
            bytedata = f.readline().encode('utf-8')
            if len(bytedata) == 0:
                f.close()
                ser.close()
                exit()
            d = 0
            for x in bytedata:
                if (x == 0x30 or x == 0x31):
                    d = (d<<1) + (x & 0x1)
            data.append(d)
        writefont(ser, addr, data)
        time.sleep(0.05)



