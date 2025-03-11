import matplotlib
matplotlib.use('TkAgg')  # Интерактивный backend
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading
import can
import os

os.system('sudo modprobe vcan')
os.system('sudo ip link add dev vcan0 type vcan')
os.system('sudo ip link set up vcan0')

# Настройка CAN-шины
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0'
can_bus = can.interface.Bus()

# Данные для графиков
x_data_344, y_data_344 = [], []  # ID 344
x_data_164, y_data_164 = [], []  # ID 164
x_data_200, y_data_200 = [], []  # ID 200

start_time = time.time()
update_event = threading.Event()

latest_value_344 = 10  # Начальные значения
latest_value_164 = 10
latest_value_200 = 10

# Создаем фигуру и оси
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

# Первоначальные графики
line_344, = ax1.plot([], [], 'bo-', label="CAN Data 344")
ax1.set_title("График для ID 344")
ax1.legend()

line_164, = ax2.plot([], [], 'ro-', label="CAN Data 164")
ax2.set_title("График для ID 164")
ax2.legend()

line_200, = ax3.plot([], [], 'go-', label="CAN Data 200")
ax3.set_title("График для ID 200")
ax3.legend()

# Функция обновления графиков
def update(frame):
    global latest_value_344, latest_value_164, latest_value_200
    if update_event.is_set():
        current_time = time.time() - start_time

        # Обновление данных
        x_data_344.append(current_time)
        y_data_344.append(latest_value_344)
        x_data_164.append(current_time)
        y_data_164.append(latest_value_164)
        x_data_200.append(current_time)
        y_data_200.append(latest_value_200)

        # Обновляем линии
        line_344.set_data(x_data_344, y_data_344)
        line_164.set_data(x_data_164, y_data_164)
        line_200.set_data(x_data_200, y_data_200)

        # Ограничиваем ось X 10 секундами
        for ax in [ax1, ax2, ax3]:
            ax.set_xlim(max(0, current_time - 10), current_time)

        # Динамический диапазон Y
        ax1.set_ylim(min(y_data_344, default=0) - 10, max(y_data_344, default=10) + 10)
        ax2.set_ylim(min(y_data_164, default=0) - 10, max(y_data_164, default=10) + 10)
        ax3.set_ylim(min(y_data_200, default=0) - 10, max(y_data_200, default=10) + 10)

        # Удаление старых данных
        for x_data, y_data in [(x_data_344, y_data_344), (x_data_164, y_data_164), (x_data_200, y_data_200)]:
            if x_data and x_data[0] < current_time - 10:
                x_data.pop(0)
                y_data.pop(0)

        update_event.clear()
    return line_344, line_164, line_200

ani = animation.FuncAnimation(fig, update, interval=100, blit=False)

# Функция получения данных из CAN
def can_listener():
    global latest_value_344, latest_value_164, latest_value_200
    while True:
        message = can_bus.recv()
        if message:
            if message.arbitration_id == 344 and len(message.data) >= 4:
                latest_value_344 = int.from_bytes(message.data, byteorder='big')
            elif message.arbitration_id == 0x18DAF111 and message.data[0] == 0x24:
                latest_value_164 = int.from_bytes(message.data[1:3], byteorder='big')
            elif message.arbitration_id == 0x18DAF111 and message.data[0] == 0x26:
                latest_value_200 = int.from_bytes(message.data[3:4], byteorder='big')
            update_event.set()

# Запуск потока для прослушивания CAN
threading.Thread(target=can_listener, daemon=True).start()

plt.show()
