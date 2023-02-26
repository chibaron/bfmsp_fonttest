
import serial, time, struct
import sys
from sys import stdout

def readfont(ser, addr):
    checksum = 0
    # send
    txdata = [0x24, 0x4d, 0x3c, 2, 86, addr&0xff, (addr>>8)&0xff ]
    for i in txdata[3:len(txdata)]:
        checksum = checksum ^ i
    txdata.append(checksum)
    print('send:', end='')
    for x in txdata:
        print('{:02x} '.format(x), end='')
    print('')
    ser.write(txdata)
    # recv = '$M>' + length + command + fontaddress(2byte) + data(64byte)
    rxhead = b'$M>'
    ser.read_until(rxhead)
    datalength = ser.read() 
    rxdata = rxhead + datalength + ser.read(datalength[0] +1)
    print('recv:', end='')
    for x in rxdata:
        print('{:02x} '.format(x), end='')
    print('')
    return rxdata[7:] # data


if __name__ == "__main__":

    args = sys.argv
    if len(args) != 2:
        print('need com port')
        exit()

    ser = serial.Serial()
    ser.port = args[1]          # com port
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    #ser.timeout = 0
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    ser.writeTimeout = 2
    ser.open()

    for addr in range(0x0, 0x200):
        print('=== addr:{:04x}==='.format(addr))
        data = readfont(ser, addr)
        count = 0
        for x in data:
            if count < 54:
                for index in [6,4,2,0]:
                    bit = (x >> index ) & 0x3
                    if (bit & 0x1) == 0x1 :
                        print('.', end='')
                    if bit == 0x0:
                        print('x', end='')  # black
                    if bit == 0x2:
                        print('o', end='')  # white
                if (count % 3) == 2:
                    print('')
            else:
                if count == 54:
                    print('metadata:', end='')
                print('{:02x} '.format(x), end='')
            count += 1
        print()



