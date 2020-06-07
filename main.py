#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main file."""

from application.application import Application
from application.run import clear

from PyQt5 import QtWidgets
from contextlib import contextmanager
import sys
import datetime


@contextmanager
def error_handler():
    """Writes the errors into the error.txt file."""
    try:
        yield

    except KeyboardInterrupt:
        print('The Program was stopped!')

    finally:
        clear()

        error = sys.exc_info()

        if error[0] is not None and error[0] != SystemExit:
            with open('application/files/error.txt', 'a') as file:
                file.write(f'{datetime.datetime.now()}, {error}\n')


def main():
    """Start of the program."""
    with error_handler():
        app = QtWidgets.QApplication(sys.argv)
        window = Application()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
