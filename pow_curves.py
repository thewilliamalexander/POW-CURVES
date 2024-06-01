import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

# Importing Data
kt_series = "kt-pow-curves.xlsx"
kq_series = "kq-pow-curves.xlsx"
df_kt = pd.read_excel(kt_series)
df_kq = pd.read_excel(kq_series)

# To handle NaN Values
df_kq['Cs,t,u,v'] = pd.to_numeric(df_kq['Cs,t,u,v'], errors='coerce')
df_kq['Cs,t,u,v'] = df_kq['Cs,t,u,v'].fillna(0)

def thrust(j, P_D, Ae_Ao, z):
    results = []
    cn = df_kt['Cs,t,u,v']
    sn = df_kt['s(J)']
    tn = df_kt['t(P/D)']
    un = df_kt['u(AE/AO)']
    vn = df_kt['v(Z)']
    for i in j:
        sum_results = (cn * i**sn * P_D**tn * Ae_Ao**un * z**vn).sum()
        results.append(sum_results)
    return results

def torque(j, P_D, Ae_Ao, z):
    results = []
    cn = df_kq['Cs,t,u,v']
    sn = df_kq['s(J)']
    tn = df_kq['t(P/D)']
    un = df_kq['u(AE/AO)']
    vn = df_kq['v(Z)']

    for i in j:
        sum_results = (cn * i**sn * P_D**tn * Ae_Ao**un * z**vn).sum()
        results.append(sum_results*10)
    return results

def efficiency(j, Kt, Kq):
    results = []
    for i, (kt, kq) in enumerate(zip(Kt, Kq)):
        efficiency_value = (kt / kq) * (j[i] / (2 * np.pi))
        results.append(efficiency_value)
    return results

P_D = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
r_R = np.arange(0, 1.1, 0.1)
z = 4
j = np.arange(0.1, 1.1, 0.1)

Ae_Ao = 0.53

# Data output result calculation
thrust_data = []
torque_data = []
efficiency_data = []

# Iteration of P_D value
for pd_value in P_D:
    x_axis = j
    ty_axis = thrust(j, pd_value, Ae_Ao, z)
    qy_axis = torque(j, pd_value, Ae_Ao, z)
    efficiency_axis = efficiency(j, ty_axis, qy_axis)

    if x_axis.size > 0 and len(ty_axis) == len(x_axis) and len(qy_axis) == len(x_axis) and len(efficiency_axis) == len(x_axis):
        # Append the data to lists
        thrust_data.append(ty_axis)
        torque_data.append(qy_axis)
        efficiency_data.append(efficiency_axis)

        # Plot
        plt.plot(x_axis, ty_axis, marker='o', label=f'Thrust (P/D={pd_value})')
        plt.plot(x_axis, qy_axis, marker='x', label=f'Torque (P/D={pd_value})')
        
        # Interpolation for smooth efficiency curve
        f = interp1d(x_axis, efficiency_axis, kind='cubic')
        x_new = np.linspace(min(x_axis), max(x_axis), 500)
        y_smooth = f(x_new)
        plt.plot(x_new, y_smooth, label=f'Efficiency (P/D={pd_value})')

# Plotting & Formatting data
plt.title('Thrust, Torque, and Efficiency Results vs. Advance Ratio (j)')
plt.xlabel('Advance Ratio (j)')
plt.ylabel('Results')
plt.grid(True)
plt.legend()
plt.show()

# CONVERT TO EXCEL
# Create DataFrame for thrust, torque, and efficiency data
thrust_df = pd.DataFrame(thrust_data, columns=[f'Thrust (P/D={pd_value})' for pd_value in P_D])
torque_df = pd.DataFrame(torque_data, columns=[f'Torque (P/D={pd_value})' for pd_value in P_D])
efficiency_df = pd.DataFrame(efficiency_data, columns=[f'Efficiency (P/D={pd_value})' for pd_value in P_D])

# Write DataFrames to Excel file
with pd.ExcelWriter('William Alexander Garcia Leonarto-233143-BPOW.xlsx') as writer:
    thrust_df.to_excel(writer, sheet_name='Thrust')
    torque_df.to_excel(writer, sheet_name='Torque')
    efficiency_df.to_excel(writer, sheet_name='Efficiency')
