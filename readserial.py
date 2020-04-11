import time
import re
import json
import serial
import serial.tools.list_ports as port_list
from Hologram.HologramCloud import HologramCloud

ports = list(port_list.comports())

#Python changes made it unable to grab dynamically
#Dynamically grabs port
for p in ports:
    print (p)

#Sets port information
comport = '/dev/ttyACM7'
print ("Using: " + comport)
serialPort = serial.Serial(comport, baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

# Used to hold data coming over UART
serialString = ""

def waterlevel(data):
    if data.startswith('<info> app: WL data:'):
            waterout = int(data[20:])
            percentfull = ((waterout)/177)
            gallons = (5.5*percentfull)
            return gallons

while(1):
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):
        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()
        message=(serialString.decode('Ascii'))

        # Print the contents of the serial data
        print(message)

        #Water logic if connected
        gallons = waterlevel(message)
        print('Gallons in Bucket:' + str(gallons))

	#Send information to the cloud
        hologram = HologramCloud(dict(), network='cellular')
        print('Cloud type: ' + str(hologram))
        payload = {"WaterLevel":gallons}
        recv = hologram.sendMessage(json.dumps(payload))

        time.sleep(30)
