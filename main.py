# захват пакетов candump и вывод на экран
import os
import subprocess
import time

def setup_vcan_interface():
    os.system('sudo modprobe vcan')
    os.system('sudo ip link add dev vcan0 type vcan')
    os.system('sudo ip link set up vcan0')
    
def replay_can_traffic(log_file):
    os.system(f'canplayer -I {log_file} vcan0=can0 -l 50')
    
def capture_can_traffic(log_file):