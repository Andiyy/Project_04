#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Showing the 0kg, 2.5kg and 5kg power and torque in a diagram."""

import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from database.database import open_sqlite3

rpm_1 = np.zeros(18)

with open_sqlite3() as cursor:
    cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                   (1, 3))
    data = cursor.fetchall()

for line, row in enumerate(data):
    rpm_1[line] = row[0]


time_2 = np.arange(0, 9, 0.5)

fig, ax = plt.subplots()

fig.dpi = 100

sns.set_style('whitegrid')

ax.plot(time_2, rpm_1)


ax.set_xlabel("Time in s")
ax.set_ylabel("RPM in 1/min")

# plt.legend(['0kg', '2.5kg', '5kg'], loc=1)

ax.grid()
plt.show()

name = str(time.time())

fig.savefig(f'{name.replace(".", "_")}.png', transparent=True)