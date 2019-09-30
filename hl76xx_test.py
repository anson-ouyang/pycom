import serial
import time
from xml.dom.minidom import parse
import threading

class hl76xx_test:
    def serial_config(self):
        doc = parse("configuration.xml")  # 先把xml文件加载进来
        root = doc.documentElement  # 获取元素的根节点
        serial_config = root.getElementsByTagName('serial')  # 找到子节点，得到的是一个数组
        baud = serial_config[0].getElementsByTagName("baud")[0].childNodes[0].data.strip()
        com = serial_config[0].getElementsByTagName("portx")[0].childNodes[0].data.strip()
        timex = serial_config[0].getElementsByTagName("timex")[0].childNodes[0].data.strip()
        ser = serial.Serial(com, int(baud))
        return ser

    def send_command(self, ser, content):
        content = content + "\r\n"
        count = ser.write(content.encode("utf-8"))
        return count

    def recv_info(self, ser):
        return ser.read()

    def recv_lines(self, ser):
        return ser.readlines()

    def close(self, ser):
        ser.close()

test = hl76xx_test()
ser = test.serial_config()
test.send_command(ser, "8")
time.sleep(1)
test.send_command(ser, "4")
lines = test.recv_lines(ser)
commands = list()
for line in lines:
    if line.decode().strip().startswith("test"):
        commands.append(line.decode().strip())

for command in commands:
    print("start test ------ " + command)
    test.send_command(ser, command)
    test_log = test.recv_lines(ser)
    for log in test_log:
        print(log.decode())
    print("end test ----- " + command)


test.close(ser)

