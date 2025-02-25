import pyshark
from collections import defaultdict
import matplotlib.pyplot as plt

# Открытие файла с дампом
cap = pyshark.FileCapture('ignitin_start_engine.pcapng')

ids = defaultdict(list)
for packet in cap:
    if packet.can.id == "344":
        ids[packet.can.id].append(int(packet.DATA.data[4:8], 16))
        continue
    if packet.can.id == "476":
        ids[packet.can.id].append(int(packet.DATA.data[2:8], 16))
        continue
    ids[packet.can.id].append(int(packet.DATA.data, 16))

plt.figure()
plt.plot(ids["344"])
plt.title(f'ID: обороты')

plt.figure()
plt.plot(ids["476"])
plt.title(f'ID: ')
plt.show()

# построй график по data
for key in ids:
    plt.plot(ids[key])
    plt.title(f'ID: {key}')
    plt.show()
# Показать график
