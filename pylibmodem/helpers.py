#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from datetime import datetime
import logging
import os
import random
import serial
from serial.tools.list_ports import comports


TEMPLATE = """<DATETIME: {}>
<MODULE: {}>
<MESSAGE: {}>
"""


def convert_message(message: str) -> str:
    """
    Function converts text message to an
    appropriate form before sending to the device
    """
    if message.strip():
        return "".join("%04X" % ord(c) for c in message)
    else:
        log_message("Empty message is not allowed")


def get_datetime() -> str:
    """
    Funtion returns current date and time in text format
    Example: 27.05.2022 17:02:47
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def get_devices() -> dict:
    """
    Function returns device name, hardware id
    and port name of the attached devices

    Returns a dictionary in the form of:
    devices = {
        "/dev/ttyUSB0": [
            "HUAWEI Mobile",
            "USB VID:PID=12D1:1003 LOCATION=2-2:1.0"
        ],
        "/dev/ttyUSB1": [
            "HUAWEI Mobile",
            "USB VID:PID=12D1:1003 LOCATION=2-2:1.1"
        ]
    }
    """
    ports = comports()
    if ports:
        devices = {}
        for port, model, hwid in sorted(ports):
            devices[port] = [model, hwid]
        return devices
    else:
        log_message("No serial port found")


def get_interval() -> int:
    """
    Function generates random interval number
    """
    return round(random.uniform(1, 5), 2)


def get_module_name() -> str:
    """
    Function returns name of the
    module you are currently in
    """
    return __file__.split(os.path.sep)[-1]


def is_baudrate(baudrate: int) -> bool:
    """
    Function checks whether baudrate
    argument has an appropriate value
    """
    if type(baudrate) is int:
        if baudrate in serial.Serial.BAUDRATES:
            return True
        else:
            log_message("An inappropriate baudrate value")
    else:
        log_message("Baudrate value has to be of an integer type")


def is_timeout(timeout: int) -> bool:
    """
    Function checks whether timeout
    argument has an appropriate value
    """
    if type(timeout) is int:
        if timeout > 0 and timeout <= 60:
            return True
        else:
            log_message("An inappropriate timeout value")
    else:
        log_message("Timeout value has to be of an integer type")


def log_message(message: str) -> None:
    """
    Function logs given message
    to log file and std_out
    """
    curr_datetime = get_datetime()
    curr_module = get_module_name()
    logging.info(
        TEMPLATE.format(
            curr_datetime,
            curr_module,
            message
        )
    )
