import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Data
data = [[(0.05003237724304199, 0.036986589431762695), (0.08791947364807129, 0.08490180969238281),
         (0.11612272262573242, 0.10128974914550781), (0.2785630226135254, 0.25769925117492676)],
        [(0.09292268753051758, 0.08910655975341797), (0.1825425624847412, 0.17571282386779785),
         (1.1268956661224365, 1.0684473514556885), (0.8872373104095459, 0.8447301387786865)],
        [(0.18148517608642578, 0.1827833652496338), (1.1517338752746582, 1.1049458980560303),
         (0.8077394962310791, 0.7677545547485352), (11.389463901519775, 11.078904151916504)],
        [(0.23665237426757812, 0.20604228973388672), (6.42653751373291, 6.041924715042114),
         (23.923896074295044, 24.243812799453735), (145.04230666160583, 121.52642631530762)]]



# Prepare data for 3D plot
x_vals, y_vals, z1_vals, z2_vals = [], [], [], []

for i, row in enumerate(data):
    for j, val in enumerate(row):
        if val != 0:  # Ignore 0 entries as they don't have timing data
            x_vals.append(i + 4)
            y_vals.append(j + 4)
            z1_vals.append(val[0])
            z2_vals.append(val[1])

x_vals = np.array(x_vals)
y_vals = np.array(y_vals)
z1_vals = np.array(z1_vals)
z2_vals = np.array(z2_vals)

grid_x, grid_y = np.meshgrid(np.linspace(x_vals.min(), x_vals.max(), 50),
                             np.linspace(y_vals.min(), y_vals.max(), 50))

grid_z1 = griddata((x_vals, y_vals), z1_vals, (grid_x, grid_y), method='cubic')
grid_z2 = griddata((x_vals, y_vals), z2_vals, (grid_x, grid_y), method='cubic')

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_vals, y_vals, z1_vals, color='b', label='Algorithm 1 Time')
ax.scatter(x_vals, y_vals, z2_vals, color='r', label='Algorithm 2 Time')

ax.plot_surface(grid_x, grid_y, grid_z1, color='blue', alpha=0.2, label='Algorithm 1 Surface')
ax.plot_surface(grid_x, grid_y, grid_z2, color='red', alpha=0.2, label='Algorithm 2 Surface')

ax.set_xlabel('n')
ax.set_ylabel('m')
ax.set_zlabel('Time (seconds)')
ax.set_title('NxMxTime')

plt.show()
