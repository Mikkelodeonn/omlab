"""
KIM101
==================

An example showing the usage of the Thorlabs Kinesis .NET API in controlling the KCube Intertial Motor Controller.
Uses the clr module from pythonnet package
Written and tested in python 3.10.5
"""

import os
import time
import sys
import clr

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.InertialMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.InertialMotorCLI import *
from System import Decimal  # necessary for real world units

class kim101:
    def __init__(self, serial: str, sim: bool):      
        # this line initiates the Kinses simulator (commment out if a real device is connected)
        if sim:
            SimulationManager.Instance.InitializeSimulations()
        else:
            pass

        # create/ connect to new device by serial
        DeviceManagerCLI.BuildDeviceList()

        self.device = KCubeInertialMotor.CreateKCubeInertialMotor(serial)

        self.device.Connect(serial)
        time.sleep(0.25)
    

        # Ensure that the device settings have been initialized
        if not self.device.IsSettingsInitialized():
            self.device.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert self.device.IsSettingsInitialized() is True

        # Get Device Information and display description
        device_info = self.device.GetDeviceInfo()
        print(device_info.Description)
        print("Serial: ", str(serial))
        # Start polling and enable channel
        self.device.StartPolling(250)  #250ms polling rate
        time.sleep(0.25)
        self.device.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        # Load any configuration settings needed by the controller/stage
        self.inertial_motor_config = self.device.GetInertialMotorConfiguration(serial)

                # Get parameters related to homing/zeroing/moving
        device_settings = ThorlabsInertialMotorSettings.GetSettings(self.inertial_motor_config)
        
        # Step parameters for an intertial motor channel
        channel1 = InertialMotorStatus.MotorChannels.Channel1  
        channel2 = InertialMotorStatus.MotorChannels.Channel2

        device_settings.Drive.Channel(channel1).StepRate = 100
        device_settings.Drive.Channel(channel1).StepAcceleration = 10000
            
        device_settings.Drive.Channel(channel2).StepRate = 100
        device_settings.Drive.Channel(channel2).StepAcceleration = 10000

        # Send settings to the device
        self.device.SetSettings(device_settings, True, True)

    def Home(self, channel: int):
        # Home or Zero the device (if a motor/piezo)
        if channel == 1:
            chan = InertialMotorStatus.MotorChannels.Channel1  
        if channel == 2: 
            chan = InertialMotorStatus.MotorChannels.Channel2

        print("Homing device")
        self.device.SetPositionAs(chan, 0)

    def MoveTo(self, new_pos: int, channel: int, timeout = 600000): # Note 1 step ~ 1 micron according to documentation for PD1V/M
        if channel == 1:
            chan = InertialMotorStatus.MotorChannels.Channel1  
        if channel == 2: 
            chan = InertialMotorStatus.MotorChannels.Channel2

        self.device.MoveTo(chan, new_pos, timeout)

    def MoveBy(self, steps: int, channel: int, timeout = 600000):
        if channel == 1:
            chan = InertialMotorStatus.MotorChannels.Channel1  
        if channel == 2: 
            chan = InertialMotorStatus.MotorChannels.Channel2

        self.device.MoveBy(chan, steps, timeout)

    def GetPosition(self, channel: int):
        if channel == 1:
            chan = InertialMotorStatus.MotorChannels.Channel1  
        if channel == 2: 
            chan = InertialMotorStatus.MotorChannels.Channel2
            
        position = self.device.GetPosition(chan)
        #print(position)
        return position

    def disconnect(self):
        self.device.StopPolling()
        self.device.Disconnect()

        # Uncomment this line if you are using Simulations
    
    #SimulationManager.Instance.UninitializeSimulations()

#stage = kim101(serial="97251709", sim=False)

## PD1V/M documentation: https://www.thorlabs.com/item/PD1V_M
## KIM101 documentaion: https://www.thorlabs.com/item/KIM101
## Thorlabs GitHub page: https://github.com/Thorlabs


