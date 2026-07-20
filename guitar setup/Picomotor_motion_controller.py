class picomotor:
    def __init__(self, connection=0, auto_detect=False):

        from pylablib.devices import Newport 

        self.stage = Newport.Picomotor8742(connection)

        if auto_detect:
            print("autodetection motors...")
            self.stage.autodetect_motors()
            self.stage.save_parameters()

    def info(self):
        return self.stage.get_id()
    
    def axes(self):
        return self.stage.get_all_axes()
    
    def position(self, axis):
        return self.stage.get_position(axis)

    def MoveTo(self, axis: int, position: int, wait=True):
        self.stage.move_to(axis, position)

        if wait:
            self.stage.wait_move(axis)

    def MoveBy(self, axis: int, steps: int, wait=True):
        self.stage.move_by(axis, steps)

        if wait: 
            self.stage.wait_move(axis)

    def Stop(self, axis="all"):
        self.stage.stop(axis)

    def zero(self, axis="all"):
        self.stage.set_position_reference(axis, 0)

    def wait(self, axis="all"):
        self.stage.wait_move(axis)

    def close_connection(self):
        self.stage.close()
    

    ## Class documentation: https://pylablib.readthedocs.io/en/latest/.apidoc/pylablib.devices.Newport.html#pylablib.devices.Newport.picomotor.Picomotor8742.move_by