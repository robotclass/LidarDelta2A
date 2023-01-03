# Пример для библиотеки LidarDelta2A
# отображение массива точек на графике типа scatter
# для уменьшения задержки отрисовки применён blit
#
# зависимости: matplotlib, numpy
# автор: Олег Евсегнеев
# e-mail: oleg.evsegneev@gmail.com
import LidarDelta2A
import signal
import time
import matplotlib.pyplot as plt
import math
import numpy as np

port = 'COM10'
lidar = LidarDelta2A.LidarDelta2A(port, baudrate = 230400) 

points = np.zeros((16*52,2))

def on_close(event):
    print('Closed window!')
    ready = 0

def signal_handler(sig, frame):
    print('Pressed Ctrl+C!')
    global ready
    ready = 0

signal.signal(signal.SIGINT, signal_handler)

fig, ax = plt.subplots()

fig.canvas.mpl_connect('close_event', on_close)

ln = ax.scatter(points[:,0], points[:,1], animated=True)
ax.set_xlim([-5000,5000])
ax.set_ylim([-5000,5000])

plt.show(block=False)
plt.pause(0.1)

bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(ln)
fig.canvas.blit(fig.bbox)

to = 0.01
t = time.time()
nxt = time.time() + to

ready = 1
while ready:
    data = lidar.handleData()
    for i,v in enumerate(data):
        points[i] = [v[1] * math.cos(math.radians(v[0])), v[1] * math.sin(math.radians(v[0]))]

    if time.time() > nxt:
        nxt = time.time() + to

        fig.canvas.restore_region(bg)
        ln.set_offsets(points)
        ax.draw_artist(ln)
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()

plt.close("all")
lidar.stop()
