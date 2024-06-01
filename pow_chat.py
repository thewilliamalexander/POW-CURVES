import matplotlib.pyplot as plt
import pandas as pd
import numpy


def load_data(filename):
    df = pd.read_excel(filename)
    df["Cs,t,u,v"] = pd.to_numeric(df["Cs,t,u,v"], errors="coerce").fillna(0)
    return df


def calculate(df, j, P_D, Ae_Ao, z):
    n = df["n"]
    cn = df["Cs,t,u,v"]
    sn = df["s(J)"]
    tn = df["t(P/D)"]
    un = df["u(AE/AO)"]
    vn = df["v(Z)"]
    results = []
    for advance in j:
        sum_results = (cn * advance**sn * P_D**tn * Ae_Ao**un * z**vn).sum()
        results.append(sum_results)
    return results


def main():
    kt_series = "kt-pow-curves.xlsx"
    kq_series = "kq-pow-curves.xlsx"
    df_kt = load_data(kt_series)
    df_kq = load_data(kq_series)

    P_D_values = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
    j = numpy.arange(0.1, 1.1, 0.1)
    z = 4
    Ae_Ao = 0.53

    fig, ax = plt.subplots()

    for pd in P_D_values:
        thrust_results = calculate(df_kt, j, pd, Ae_Ao, z)
        torque_results = calculate(df_kq, j, pd, Ae_Ao, z)
        label = f"P_D = {pd}"
        ax.plot(j, thrust_results, marker="o", label=f"{label} - Thrust")
        ax.plot(j, torque_results, marker="x", label=f"{label} - Torque")

    ax.set_title("Thrust and Torque Results vs. Advance Ratio (j)")
    ax.set_xlabel("Advance Ratio (j)")
    ax.set_ylabel("Results")
    ax.grid(True)
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
