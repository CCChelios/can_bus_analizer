import can
import os
import time
import plotext as plt

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

TARGET_ID = 0x18DAF111
PREFIX = 0x21

def get_can_message():
    while True:
        message = bus.recv(timeout=1)
        if message and message.arbitration_id == TARGET_ID:
            if message.data and message.data[0] == PREFIX:
                #os.system("clear")
                message.data
            return message.data

# if __name__ == "__main__":
#     while True:
#         data = get_can_message()
#         if data:
#             value = int.from_bytes(data[3:4], byteorder='big')
#             print(f"Received valid data: {value}")

if __name__ == "__main__":
    try:
        while True:
            can_data = []
            data = get_can_message()
            value = int.from_bytes(can_data[3:4], byteorder='big')
            if value is not None:
                data.append(value)


                plt.clear_figure()
                plt.plot(data)
                plt.title("Real-time CAN Data")
                plt.show()
    except KeyboardInterrupt:
        print("\nExit.")
