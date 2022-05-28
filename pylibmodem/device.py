#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from time import sleep
import serial

from pylibmodem.helpers import (
    convert_message,
    get_interval,
    is_baudrate,
    is_timeout,
    log_message
)


class Modem:
    """
    A class for interacting with gsm modem device
    """
    # Default values
    DFL_PORT = "/dev/ttyUSB0"
    DFL_BAUDRATE = 115200
    DFL_TIMEOUT = 1
    # Time interval between sending AT commands
    AT_TIMEOUT = 1
    # USSD commands of different operators to find out the balance
    BALANCE = {
        "megafon": "*102#"
    }

    def __init__(self,
                 port: str = DFL_PORT,
                 baudrate: int = DFL_BAUDRATE,
                 timeout: int = DFL_TIMEOUT):
        # Use passed arguments for setting device options
        # or default values if passed ones are in incorrect format
        self._port = port
        if is_baudrate(baudrate):
            self._baudrate = baudrate
        else:
            self._baudrate = Modem.DFL_BAUDRATE
        if is_timeout(timeout):
            self._timeout = timeout
        else:
            self._timeout = Modem.DFL_TIMEOUT
        self._device = serial.Serial()

    # ------------------------------------------
    # Properties and setters declaration section
    # ------------------------------------------
    @property
    def baudrate(self) -> int:
        return self._baudrate

    @baudrate.setter
    def baudrate(self, new_value: int):
        if is_baudrate(new_value):
            self._baudrate = new_value

    @property
    def connected(self) -> bool:
        return self._device.is_open

    @property
    def port(self) -> str:
        return self._port

    @port.setter
    def port(self, new_value: str):
        self._port = new_value

    @property
    def timeout(self) -> int:
        return self._timeout

    @timeout.setter
    def timeout(self, new_value: int):
        if is_timeout(new_value):
            self._timeout = new_value

    # ----------------------------------
    # Public methods declaration section
    # ----------------------------------
    def connect(self) -> None:
        """
        A method for raising connection with device
        """
        self._device.port = self._port
        self._device.baudrate = self._baudrate
        self._device.timeout = self._timeout
        try:
            self._device.open()
        except serial.ValueError as err:
            log_message(
                "Parameters are out of range\n" + err
            )
        except serial.SerialException as err:
            log_message(
                "The device can not be found or can not be configured\n" + err
            )

    def disconnect(self) -> None:
        """
        A method for droping connection with the device
        """
        try:
            self._device.close()
        except serial.ValueError as err:
            log_message("Parameters are out of range\n" + err)
        except serial.SerialException as err:
            log_message(
                "The device can not be found or can not be configured\n" + err
            )

    def get_balance(self) -> str:
        """
        A method for getting current balance
        """
        if self._device.is_open:
            self._device.write("ATZ\r\n".encode())
            sleep(Modem.AT_TIMEOUT)
            self._device.write("AT+CMGF=1\r\n".encode())
            sleep(Modem.AT_TIMEOUT)
            self._device.write("AT+CUSD=1,'{}',15\r\n".format(
                Modem.BALANCE["megafon"]).encode()
            )

    def send_message(self, number: str, message: str) -> None:
        """
        A method for sending passed message to a given number
        """
        if self._device.is_open:
            sleep(get_interval())
            msg = convert_message(message)
            try:
                self._device.write("ATZ\r\n".encode())
                sleep(Modem.AT_TIMEOUT)
                self._device.write("AT+CMGF=1\r\n".encode())
                sleep(Modem.AT_TIMEOUT)
                self._device.write("AT+CSMP=17,167,0,8\r\n".encode())
                sleep(Modem.AT_TIMEOUT)
                self._device.write("AT+CMGS='{}'\r\n".format(number).encode())
                sleep(Modem.AT_TIMEOUT)
                self._device.write(msg.encode())
                sleep(Modem.AT_TIMEOUT)
                self._device.write(chr(26).encode())
            except Exception as err:
                log_message(
                    "Attempt to SEND message was unsuccessful\n" + err
                )
        else:
            log_message("Cannon send message if device is not connected")
