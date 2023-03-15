import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
class SENSOR:
    def __init__(self, linkName):
        self.values = np.zeros(10000)
        self.linkName = linkName
    
    def Get_Value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        np.save('sensor_values.npy', self.values)