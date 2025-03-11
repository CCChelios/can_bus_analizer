import time
import plotext as plt
from can_reader import get_can_message

data = []

try:
    while True:
        value = get_can_message()
        if value is not None:
            data.append(value)
            if len(data) > 30:
                data.pop(0)

            plt.clt()
            plt.plot(data, marker="dot")
            plt.title("Real-time CAN Data")
            plt.show()
            time.sleep(0.5)
except KeyboardInterrupt:
    print("\nExit.")
