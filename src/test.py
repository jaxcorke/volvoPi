import serial
import serial.tools.list_ports

com_ports = list(serial.tools.list_ports.comports())

for port in com_ports:
    print(port)




