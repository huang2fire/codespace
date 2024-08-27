import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["SimSun"]
plt.rcParams["axes.unicode_minus"] = False
plt.figure(figsize=(8 * 2, 5 * 2))

n_min = 600  # 最低转速 (r/min)
n_max = 4000  # 最高转速 (r/min)
m = 3880  # 总质量 (kg)
r = 0.367  # 车轮半径 (m)
eta_T = 0.85  # 传动系机械效率
f = 0.013  # 滚动阻力系数
C_D_A = 2.77  # 空气阻力系数乘以迎风面积 (m^2)
i_0 = 5.83  # 主减速器传动比
I_f = 0.218  # 飞轮转动惯量 (kg·m^2)
I_w1 = 1.798  # 二前轮转动惯量 (kg·m^2)
I_w2 = 3.598  # 四后轮转动惯量 (kg·m^2)
i_g_4 = np.array([6.09, 3.09, 1.71, 1.00])  # 4 档变速器传动比
i_g_5 = np.array([5.56, 2.769, 1.644, 1.00, 0.793])  # 5 档变速器传动比

g = 10  # 重力加速度 (m/s^2)
G = m * g  # 重力 (N)

n = np.arange(n_min, n_max + 1).reshape(-1, 1)  # 转速范围

# 发动机转矩
T_q = (
    -19.313
    + 295.27 * (n / 1000)
    - 165.44 * (n / 1000) ** 2
    + 40.874 * (n / 1000) ** 3
    - 3.8445 * (n / 1000) ** 4
)

# 汽车行驶速度
u_a = 0.377 * r * n / (i_g_4 * i_0)

# 汽车旋转质量换算系数 * 汽车质量
delta_m = m + ((I_w1 + I_w2) + (I_f * (i_g_4**2) * (i_0**2) + eta_T)) / r**2

# 汽车的驱动力
F_t = T_q * i_g_4 * i_0 * eta_T / r

# 汽车的滚动阻力
F_f = G * f

# 汽车的空气阻力
F_w = (C_D_A / 21.15) * u_a**2

# 汽车的行驶加速度
a = (F_t - F_f - F_w) / delta_m
inv_a = np.reciprocal(a)  # 加速度倒数

# 汽车能爬上的道路坡度角
alpha = np.arcsin((F_t - F_f - F_w) / G)
i = np.tan(alpha)  # 坡度值

# 汽车的动力因数
D = (F_t - F_w) / G

# 发动机功率
P_e = T_q * i_g_4 * i_0 * u_a / (r * 3600)

# 阻力功率
P_fw = ((G * f * u_a / 3600) + (C_D_A * u_a**3 / 76140)) / eta_T

# 图例
labels = [f"{idx+1}档" for idx in range(i_g_4.size)]

# 图表1：汽车驱动力-行驶阻力平衡图
plt.subplot(2, 3, 1)
plt.plot(u_a, F_t, label=labels)
plt.plot(u_a, F_f + F_w, color="black")
plt.plot(u_a, np.full(a.shape, F_f), color="grey")
plt.xlabel("$u_{a} / (km/h)$")
plt.ylabel("$F_{t} / N , (F_{f}+F_{w}) / N$")
plt.title("汽车驱动力-行驶阻力平衡图")
plt.text(
    u_a[-1, -1],
    F_f + F_w[-1, -1],
    "$(F_f+F_w)$",
    ha="right",
    va="bottom",
)
plt.text(
    u_a[-1, -1],
    F_f,
    "$F_f$",
    ha="right",
    va="bottom",
)
plt.legend()

# 图表2：汽车的行驶加速度曲线
plt.subplot(2, 3, 2)
plt.plot(u_a, a, label=labels)
plt.xlabel("$u_{a} / (km/h)$")
plt.ylabel("$a / (m/s^{2})$")
plt.title("汽车的行驶加速度曲线")
plt.legend()

# 图表3：汽车的加速度倒数曲线
plt.subplot(2, 3, 3)
plt.plot(u_a, inv_a, label=labels)
plt.xlabel("$u_{a} / (km/h)$")
plt.ylabel("$\\frac{1}{a} / (s^{2}/m)$")
plt.title("汽车的加速度倒数曲线")
plt.legend()

# 图表4：汽车的爬坡度图
plt.subplot(2, 3, 4)
plt.plot(u_a, i * 100, label=labels)
plt.xlabel("$u_{a} / (km/h)$")
plt.ylabel("$i(\\%)$")
plt.title("汽车的爬坡度图")
plt.legend()

# 图表5：汽车的动力特性图
plt.subplot(2, 3, 5)
plt.plot(u_a, D, label=labels)
plt.plot(u_a, np.full(a.shape, f), color="grey")
plt.xlabel("$u_{a} / (km/h)$")
plt.ylabel("$D$")
plt.title("汽车的动力特性图")
plt.legend()

# 图表6：汽车的功率平衡图
plt.subplot(2, 3, 6)
plt.plot(u_a, P_e, label=labels)
plt.plot(u_a, P_fw, color="black")
plt.xlabel("$u_{a} / (km/h)$")
plt.ylabel("$P_{e} / kW$")
plt.title("汽车的功率平衡图")  #
plt.text(
    u_a[-1, -1],
    P_fw[-1, -1],
    "$\\frac{P_{f}+P_{w}}{\\eta_{T}}$",
    ha="right",
    va="bottom",
)
plt.legend()

plt.tight_layout()
# plt.savefig("car.png", dpi=200)
plt.show()
