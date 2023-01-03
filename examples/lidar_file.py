# Пример для библиотеки LidarDelta2A
# сохранение массива точек в файл
#
# зависимости: numpy
# автор: Олег Евсегнеев
# e-mail: oleg.evsegneev@gmail.com
import LidarDelta2A
import numpy as np

port = 'COM10'
lidar = LidarDelta2A.LidarDelta2A(port, baudrate = 230400) 

while not ready:
    data = lidar.handleData()

np.savetxt('output.csv', data, delimiter=',', fmt='%f')
