#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from typing import Dict

from pylibmodem.helpers import (
    get_devices,
    log_message
)
from pylibmodem.device import Modem


def main():
    devices: Dict[str, str] = get_devices()
    if devices:
        # Why not create a context manager for this?
        # with UseDevice(Modem()) as device:
        #     device.send_message("+79627746292", "Привет")
        device = Modem()
        if device.port in devices.keys():
            device.connect()
            device.send_message("+79627746292", "Привет")
            device.disconnect()
        else:
            log_message("Port used for connection does not exist")
    else:
        log_message("No attached usb gsm modem found")


if __name__ == "__main__":
    main()
