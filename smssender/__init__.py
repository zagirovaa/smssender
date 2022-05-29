#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
import logging
import os
import sys


# Used in logging module
APP_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
# Logging configuration section
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(os.getcwd(), APP_NAME)),
        logging.StreamHandler(sys.stdout)
    ]
)
