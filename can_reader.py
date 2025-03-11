import can
import os
import time
import plotext as plt

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

DATA_ID = 0x18DAF111
RPM_ID = 0x158
PREFIX = 0x21

rpm = 0
ms = 0

def print_data():
    os.system('clear')
    print('rpm: ', rpm)
    print('ms: ', ms)
    #time.sleep(0.01)
    
if __name__ == "__main__":
    while True:
        message = bus.recv(timeout=1)
        if message is None:
            continue 
        if message.arbitration_id == RPM_ID:
            rpm = int.from_bytes(message.data[2:4], byteorder='big')
        elif message.arbitration_id == DATA_ID and message.data[0] == 0x22:
            ms = int.from_bytes(message.data, byteorder='big')
        print_data()

# if __name__ == "__main__":
#     try:
#         while True:
#             can_data = []
#             data = get_can_message()
#             value = int.from_bytes(can_data[3:4], byteorder='big')
#             if value is not None:
#                 data.append(value)


#                 plt.clear_figure()
#                 plt.plot(data)
#                 plt.title("Real-time CAN Data")
#                 plt.show()
#     except KeyboardInterrupt:
#         print("\nExit.")
