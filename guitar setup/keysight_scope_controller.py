

class keysight_scope:
    def __init__(self, visa_address: str):
        
        import pyvisa
        import time

        rm = pyvisa.ResourceManager()
        self.scope = rm.open_resource(visa_address)
        self.scope.timeout = 5000
        print(self.scope.query("*IDN?"))

    def average_voltage(self, channel: int) -> float:
        self.scope.write(":MEASure:VAVerage CHANnel" + str(channel))
        avg = float(self.scope.query(":MEASure:VAVerage? CHANnel" + str(channel)))
        return avg



#scope = keysight_scope(visa_address="USB0::0x0957::0x1796::MY53100155::0::INSTR")
#print(scope.average_voltage(channel=1))