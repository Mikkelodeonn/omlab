import usb.backend.libusb1
import libusb_package

backend = usb.backend.libusb1.get_backend(
    find_library=libusb_package.find_library
)

print(backend)