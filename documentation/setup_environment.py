#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Installation of all required modules."""

import subprocess
import sys


def install_module(module: str):
    """Installing the python module."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])


if __name__ == '__main__':
    install_module('PyQt5')
    install_module('numpy')
    install_module('matplotlib')
    install_module('seaborn')
    install_module('gpiozero')
    install_module('paramiko')
    install_module('pigpio')
    install_module('pyserial')
