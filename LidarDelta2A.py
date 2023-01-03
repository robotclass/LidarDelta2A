# Python-класс для работы с лидаром Delta2A от компании 3iRobotics
# автор: Олег Евсегнеев
# e-mail: oleg.evsegneev@gmail.com
import numpy as np
import serial

DEBUG = 0

SECTORS = 16
DATALEN = 52

FRAME_HEAD = 0xAA
FRAME_TYPE = 0x61

FRAME_MEASURE_INFO = 0xAD
FRAME_DEVICE_HEALTH_INFO = 0xAE

class LidarDelta2A:
    _serial = None
    _data = None
    _sector = 0
    _size = 0

    def __init__( self, port, baudrate, timeout = 1 ):
        self._serial = serial.Serial( port, baudrate, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, timeout = timeout )
        self._data = np.zeros((DATALEN*SECTORS,2))

    def stop( self ):
        self._serial.close()

    def extractFrame( self, data ):
        for idx, bt in enumerate(data):
            if bt == FRAME_HEAD:
                frame = data[idx:]
                if len(frame) < 3:
                    if DEBUG: print("Frame length error 1")
                    return 0
                
                framelen = (frame[1]<<8) + frame[2]
                if len(frame) < (framelen+2):
                    if DEBUG: print("Frame length error 2")
                    return 0

                frametype = frame[4]
                if frametype != FRAME_TYPE:
                    if DEBUG: print("Frame type error");
                    return idx+1

                datalen = (frame[6]<<8) + frame[7]
                speed = frame[8]*0.05
                zeroshift = (frame[9]<<8) + frame[10]
                zerostart = ((frame[11]<<8) + frame[12]) * 0.01
                crc = (frame[framelen]<<8) + frame[framelen+1]

                if crc != sum(frame[:framelen]):
                    if DEBUG: print("Frame CRC error");
                    return idx+1

                n = int((datalen - 5) / 3)
                k = 22.5/n

                for i in range(n):
                    angle = i*k + zerostart
                    dist = ((frame[13 + i*3 + 1]<<8) + frame[13 + i*3 + 2]) * 0.25
                    self._data[self._sector*n + i] = [angle, dist]
                    
                self._sector += 1
                self._size += n

                return idx + framelen + 2

        return 0

    def handleData( self ): 
        self._sector = 0
        self._size = 0

        data = self._serial.read(1)
        while self._sector < SECTORS:
            data += self._serial.read(self._serial.in_waiting)
            cut = self.extractFrame( data )
            if cut:
                data = data[cut:]
        
        return self._data[:self._size]
