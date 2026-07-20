"""
KIM101
==================

An example showing the usage of the Thorlabs Kinesis .NET API in controlling the KCube Intertial Motor Controller.
Uses the clr module from pythonnet package
Written and tested in python 3.10.5
"""

#import os
#import time
#import sys
#import clr

#clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
#clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
#clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.InertialMotorCLI.dll")
#from Thorlabs.MotionControl.DeviceManagerCLI import *
#from Thorlabs.MotionControl.GenericMotorCLI import *
#from Thorlabs.MotionControl.KCube.InertialMotorCLI import *
#from System import Decimal  # necessary for real world units

class kim101:
    def __init__(self, serial: str, channel: int, sim: bool):

        import time
        import clr

        clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
        clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
        clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.InertialMotorCLI.dll")
        import Thorlabs.MotionControl.DeviceManagerCLI as DM
        import Thorlabs.MotionControl.KCube.InertialMotorCLI as IM
        import Thorlabs.MotionControl.GenericMotorCLI as GM
        #from Thorlabs.MotionControl.DeviceManagerCLI import (DeviceManagerCLI, SimulationManager)
        #from Thorlabs.MotionControl.KCube.InertialMotorCLI import (KCubeInertialMotor, ThorlabsInertialMotorSettings, IntertialMotorStatus)
        
        # this line initiates the Kinses simulator (commment out if a real device is connected)
        if sim:
            DM.SimulationManager.Instance.InitializeSimulations()
        else:
            pass

        # create/ connect to new device by serial
        DM.DeviceManagerCLI.BuildDeviceList()

        self.device = IM.KCubeInertialMotor.CreateKCubeInertialMotor(serial)

        self.device.Connect(serial)
        time.sleep(0.25)
    

        # Ensure that the device settings have been initialized
        if not self.device.IsSettingsInitialized():
            self.device.WaitForSettingsInitialized(10000)  # 10 second timeout
            assert self.device.IsSettingsInitialized() is True

        # Get Device Information and display description
        device_info = self.device.GetDeviceInfo()
        print(device_info.Description)
        # Start polling and enable channel
        self.device.StartPolling(250)  #250ms polling rate
        time.sleep(0.25)
        self.device.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        # Load any configuration settings needed by the controller/stage
        self.inertial_motor_config = self.device.GetInertialMotorConfiguration(serial)

        # Get parameters related to homing/zeroing/moving
        device_settings = IM.ThorlabsInertialMotorSettings.GetSettings(self.inertial_motor_config)

        # Step parameters for an intertial motor channel
        if channel == 1: 
            self.chan = IM.InertialMotorStatus.MotorChannels.Channel1  # enum chan ident
            device_settings.Drive.Channel(self.chan).StepRate = 500
            device_settings.Drive.Channel(self.chan).StepAcceleration = 100000
        
        if channel == 2: 
            self.chan = IM.InertialMotorStatus.MotorChannels.Channel2  # enum chan ident
            device_settings.Drive.Channel(self.chan).StepRate = 500
            device_settings.Drive.Channel(self.chan).StepAcceleration = 100000

        if channel == 3: 
            self.chan = IM.InertialMotorStatus.MotorChannels.Channel3  # enum chan ident
            device_settings.Drive.Channel(self.chan).StepRate = 500
            device_settings.Drive.Channel(self.chan).StepAcceleration = 100000
        
        if channel == 4: 
            self.chan = IM.InertialMotorStatus.MotorChannels.Channel4  # enum chan ident
            device_settings.Drive.Channel(self.chan).StepRate = 500
            device_settings.Drive.Channel(self.chan).StepAcceleration = 100000

        # Send settings to the device
        self.device.SetSettings(device_settings, True, True)

    def Zero(self):
        # Home or Zero the device (if a motor/piezo)
        print("Zeroing device")
        self.device.SetPositionAs(self.chan, 0)

    def MoveTo(self, new_pos, timeout = 60000): # Note 1 step ~ 1 micron
        self.device.MoveTo(self.chan, new_pos, timeout)

    def disconnect(self):
        self.device.StopPolling()
        self.device.Disconnect()

        # Uncomment this line if you are using Simulations
    
    #SimulationManager.Instance.UninitializeSimulations()


## PD1V/M documentation: https://www.thorlabs.com/item/PD1V_M
## KIM101 documentaion: https://www.thorlabs.com/item/KIM101
## Thorlabs GitHub page: https://github.com/Thorlabs


