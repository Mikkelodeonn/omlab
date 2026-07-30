class picomotor:
    def __init__(self, connection=0, auto_detect=False):

        import usb.backend.libusb1
        import libusb_package

        _original_get_backend = usb.backend.libusb1.get_backend

        def patched_get_backend(*args, **kwargs):
            kwargs.setdefault("find_library", libusb_package.find_library)
            return _original_get_backend(*args, **kwargs)

        usb.backend.libusb1.get_backend = patched_get_backend

        from pylablib.devices import Newport 

        self.stage = Newport.Picomotor8742(connection)

        if auto_detect:
            print("autodetection motors...")
            self.stage.autodetect_motors()
            self.stage.save_parameters()
        
        print(self.stage.get_id())
        print(self.stage.get_all_axes())

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


stage = picomotor(auto_detect=True)

stage.MoveBy(axis=1, steps=-350000)

