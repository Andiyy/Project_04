import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.5)
rpm = np.arange(0, 5, 0.5)

power = np.arange(5, 10, 0.01)
average_power = []  # np.zeros(int(len(power)/50))
reset_counter = np.arange(0, len(power), 50)

print(len(power))
print(len(x))

counter = 0

for index, item in enumerate(power):
    counter += item
    if index in reset_counter:
        counter /= 50
        average_power.append(counter)
        counter = 0

fig, ax = plt.subplots()
ax.plot(x, rpm)
ax.plot(x, average_power)

ax.grid()
plt.show()



