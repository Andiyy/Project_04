#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Showing the 0kg, 2.5kg and 5kg power and torque in a diagram."""

import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from database.database import open_sqlite3


matplotlib.rcParams.update({'font.size': 25})


y_rpm = np.zeros(18)
x_time = np.arange(0, 9, 0.5)

with open_sqlite3() as cursor:
    cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                   (1, 3))
    data = cursor.fetchall()

for line, row in enumerate(data):
    y_rpm[line] = row[0]


fig, ax = plt.subplots()
fig.dpi = 100

sns.set_style('whitegrid')

ax.plot(x_time, y_rpm)
ax.set_xlabel("Time in s")
ax.set_ylabel("RPM in 1/min")

ax.grid()
plt.show()

name = str(time.time())
fig.savefig(f'{name.replace(".", "_")}.png', transparent=True)
