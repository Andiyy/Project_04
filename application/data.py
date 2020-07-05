# -*- coding: utf-8 -*-

"""Data object."""


class Data:
    """Data object."""
    def __init__(self):
        self.user = None

        self.new_measurement = None
        self.measured_values = {'Current': None,
                                'Voltage': None,
                                'RPM': None
                                }

        self.old_measurement = []
        self.plot_measurement = {'m_header': None,
                                 'Voltage': None,
                                 'Current': None,
                                 'RPM': None,
                                 'rpm_time': None,
                                 'Time': None,
                                 'Power': None,
                                 'error_power': None
                                 }

        self.raspberry_pi = None
        self.nukleo = None
