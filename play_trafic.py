# cannplayer candump log file
import os

def setup_vcan_interface():
    os.system('sudo modprobe vcan')
    os.system('sudo ip link add dev vcan0 type vcan')
    os.system('sudo ip link set up vcan0')

def replay_can_traffic(log_file):
    os.system(f'canplayer -I {log_file} vcan0=can0 -l 500')

if __name__ == "__main__":
    setup_vcan_interface()
    log_file = 'dumps/inject_ms.log'
    replay_can_traffic(log_file)