"""Discover USB devices."""

import serial.tools.list_ports

def list_usb_ports():
    """List all available USB ports."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Example usage
usb_ports = list_usb_ports()
print("Available USB ports:", usb_ports)
