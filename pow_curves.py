import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Importing Data
kt_series = "kt-pow-curves.xlsx"
kq_series = "kq-pow-curves.xlsx"
df_kt = pd.read_excel(kt_series)
df_kq = pd.read_excel(kq_series)

# To handle NaN Values
df_kq['Cs,t,u,v'] = pd.to_numeric(df_kq['Cs,t,u,v'], errors='coerce')
df_kq['Cs,t,u,v'].fillna(0, inplace=True)

def thrust(j, P_D, Ae_Ao, z):
    results = []
    n = df_kt['n']
    cn = df_kt['Cs,t,u,v']
    sn = df_kt['s(J)']
    tn = df_kt['t(P/D)']
    un = df_kt['u(AE/AO)']
    vn = df_kt['v(Z)']
    for advance in j:
        sum_results = 0
        for i in range(len(n)):
            sum_results += (cn.iloc[i]) * (advance ** sn.iloc[i]) * (P_D ** tn.iloc[i]) * (Ae_Ao ** un.iloc[i]) * (z ** vn.iloc[i])
        results.append(sum_results)
    return results

def torque(j, P_D, Ae_Ao, z):
    results = []
    n = df_kq['n']
    cn = df_kq['Cs,t,u,v']
    sn = df_kq['s(J)']
    tn = df_kq['t(P/D)']
    un = df_kq['u(AE/AO)']
    vn = df_kq['v(Z)']

    for advance in j:
        sum_results = 0
        for i in range(len(n)):
            sum_results += (cn.iloc[i]) * (advance ** sn.iloc[i]) * (P_D ** tn.iloc[i]) * (Ae_Ao ** un.iloc[i]) * (z ** vn.iloc[i])
        results.append(sum_results)
    return results

P_D = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
r_R = np.arange(0, 1.1, 0.1)
z = 4
j = np.arange(0.1, 1.1, 0.1)

Ae_Ao = 0.53

# Advanced ratio J
x_axis = j

# THRUST
ty_axis = thrust(j, P_D[0], Ae_Ao, z)

# TORQUE
qy_axis = torque(j, P_D[0], Ae_Ao, z)

# Print the results for debugging
print(f"x_axis (j values): {x_axis}")
print(f"thrust (Thrust results): {ty_axis}")
print(f"torque (Torque results): {qy_axis}")

# Ensure the lists are not empty and have the same length
if x_axis.size > 0 and len(ty_axis) == len(x_axis) and len(qy_axis) == len(x_axis):
    # Plot
    plt.plot(x_axis, ty_axis, marker='o', label='Thrust')
    plt.plot(x_axis, qy_axis, marker='x', label='Torque')
    plt.title('Thrust and Torque Results vs. Advance Ratio (j)')
    plt.xlabel('Advance Ratio (j)')
    plt.ylabel('Results')
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("Error: x_axis and y_axis are empty or not the same length.")
