# LidarDelta2A
Python-модуль для работы с лидаром Delta2A от компании 3iRobotics

За каждый оборот, лидар отправляет в COM-порт 16 пакетов данных (фрейм). Каждый пакет, кроме всего прочего, содержит данные о 51 точке (в среднем). Количество точек в пакете может варьироваться, в зависимости от скорости вращения мотора (бывает и 52 точки, например).

Метод handleData класса LidarDelta2A возвращает массив точек, сформированный путем склеивания 16 последовательных пакетов. Данные представлены в виде двумерного массива numpy, где каждый элемент массива - это пара: [угол,дистанция] 

# Зависимости
- matplotlib
- numpy

# Пример

```
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
```
