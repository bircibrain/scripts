# add the following lines at the start of your script
import PyDAQmx
from PyDAQmx import Task
from PyDAQmx.DAQmxTypes import *
import numpy as np
data_trigger = np.array([1,0], dtype=np.uint8) #rising trigger
data_clear = np.array([0], dtype=np.uint8)
timeout = 1.0 # in seconds
daqTask = Task()

# The remaining lines require the DAQ to be connected. Comment out for testing without the device
daqTask.CreateDOChan(b'/Dev1/port1/line3', '', PyDAQmx.DAQmx_Val_ChanForAllLines)
daqTask.StartTask()
daqTask.WriteDigitalLines(1, 1, timeout, PyDAQmx.DAQmx_Val_GroupByChannel, data_clear, None, None)

# end section for the start of the script

# add the following line whenever you want to trigger the TMS system
daqTask.WriteDigitalLines(2, 1, timeout, PyDAQmx.DAQmx_Val_GroupByChannel, data_trigger, None, None)

# add this line at the end of the experiment
daqTask.StopTask()
