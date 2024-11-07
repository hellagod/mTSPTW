from plot import plot_2d, plot_3d_interpolation
from testing import compute_for_pair
import csv

tl = 1
r11, r12 = [], []
r21, r22 = [], []

clients = (7, 25)
salesmen = (4, 20)
r1 = [[(0, 0)] * (salesmen[1] - salesmen[0] + 1) for _ in range(clients[0], clients[1] + 1)]
r2 = [[(0, 0)] * (salesmen[1] - salesmen[0] + 1) for _ in range(clients[0], clients[1] + 1)]

for n in range(clients[0], clients[1] + 1):
    for m in range(salesmen[0], salesmen[1] + 1):
        print(f"\nn={n}\tm={m}")
        res = compute_for_pair(n, m, tl=tl)
        print(res)
        if 'error' not in res.keys():
            r1[n - clients[0]][m - salesmen[0]] = (res['variables_model'], res['variables_short_model'])
            r2[n - clients[0]][m - salesmen[0]] = (res['constraints_model'], res['constraints_short_model'])

print("\nr1 ", r1)
print("r2 ", r2)

csv_name_r1 = f'var_num_n_{clients[0]}-{clients[1]}_m_{salesmen[0]}-{salesmen[1]}.csv'
with open(csv_name_r1, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in r1:
        row_str = [str(cell) for cell in row]
        writer.writerow(row_str)

csv_name_r2 = f'constr_num_n_{clients[0]}-{clients[1]}_m_{salesmen[0]}-{salesmen[1]}.csv'
with open(csv_name_r2, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in r2:
        row_str = [str(cell) for cell in row]
        writer.writerow(row_str)

r = []
for row1, row2 in zip(r1, r2):
    total_dims = []
    for (x1, y1), (x2, y2) in zip(row1, row2):
        total_dims.append((x1 + x2, y1 + y2))
    r.append(total_dims)

plt_1 = plot_3d_interpolation(r)
plt_1.show()