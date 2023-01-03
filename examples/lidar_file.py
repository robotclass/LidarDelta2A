# Пример для библиотеки LidarDelta2A
# сохранение массива точек в файл
#
# зависимости: numpy
# автор: Олег Евсегнеев
# e-mail: oleg.evsegneev@gmail.com
import LidarDelta2A
import signal, sys
import time
import numpy as np

port = 'COM10'
lidar = LidarDelta2A.LidarDelta2A(port, baudrate = 230400) 

def signal_handler(sig, frame):
    print('Pressed Ctrl+C!')
    lidar.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while not ready:
    data = lidar.handleData()

np.savetxt('output.csv', data, delimiter=',', fmt='%f')
