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
#can_bus = can.Bus(channel='vcan0', bustype='socketcan')
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0'
can_bus = can.interface.Bus()



# Данные для графиков
x_data_344 = []  # Для первого графика (ID 344)
y_data_344 = []
x_data_164 = []  # Для второго графика (ID 164)
y_data_164 = []
start_time = time.time()
update_event = threading.Event()
latest_value_344 = 10  # Начальное значение для первого графика
latest_value_164 = 10  # Начальное значение для второго графика

# Создаем фигуру и оси
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Первоначальные графики
line_344, = ax1.plot([], [], 'bo-', label="CAN Data 344")
ax1.set_title("График для ID 344")
ax1.legend()

line_164, = ax2.plot([], [], 'ro-', label="CAN Data 164")
ax2.set_title("График для ID 164")
ax2.legend()

# Функция обновления графиков
def update(frame):
    global latest_value_344, latest_value_164
    if update_event.is_set():
        # Обновление для графика ID 344
        x_data_344.append(time.time() - start_time)  # Текущее время в секундах
        y_data_344.append(latest_value_344)
        
        # Обновление для графика ID 164
        x_data_164.append(time.time() - start_time)
        y_data_164.append(latest_value_164)
        
        # Обновляем линии на графиках
        line_344.set_data(x_data_344, y_data_344)
        line_164.set_data(x_data_164, y_data_164)
        
        # Ограничиваем ось X значением 10 секунд
        ax1.set_xlim(max(0, time.time() - start_time - 10), time.time() - start_time)
        ax2.set_xlim(max(0, time.time() - start_time - 10), time.time() - start_time)
        
        # Динамический диапазон Y
        ax1.set_ylim(min(y_data_344, default=0) - 10, max(y_data_344, default=10) + 10)
        ax2.set_ylim(min(y_data_164, default=0) - 10, max(y_data_164, default=10) + 10)
        
        # Удаляем старые данные, если время превысило 10 секунд
        if x_data_344[0] < time.time() - start_time - 10:
            x_data_344.pop(0)
            y_data_344.pop(0)
        if x_data_164[0] < time.time() - start_time - 10:
            x_data_164.pop(0)
            y_data_164.pop(0)

        update_event.clear()
    return line_344, line_164

ani = animation.FuncAnimation(fig, update, interval=100, blit=False)

# Функция для получения данных из CAN и обновления события
def can_listener():
    global latest_value_344, latest_value_164
    while True:
        message = can_bus.recv()
        if message:
            if message.arbitration_id == 344 and len(message.data) >= 4:
                latest_value_344 = int.from_bytes(message.data, byteorder='big')
                update_event.set()
            elif message.arbitration_id == int('18e', 16):
                latest_value_164 = int.from_bytes(message.data, byteorder='big')
                update_event.set()

# Запускаем поток прослушивания CAN
threading.Thread(target=can_listener, daemon=True).start()

plt.show()
