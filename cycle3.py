import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# ==========================================
# 1. 更加拟真的历史动态参数设定 (Dynamic Epochs Definition)
# ==========================================
BASE_PARAMS = {
    "V_th": 3.5, "gamma": 5.0,        
    "eta": 0.012, "C_max": 30.0, "lam": 0.8, "kappa_slow": 0.003, "kappa_fast": 0.3,
    "T0": 0.5, "mu": 0.25,            
    "k": 0.15, "beta": 0.6,           
    "alpha": 0.15, "delta": 0.05      
}

def merge_params(custom_params):
    p = BASE_PARAMS.copy()
    p.update(custom_params)
    return p

COUNTRY_PROFILES = {
    "USA": {
        "name": "USA (Gilded Age -> Great Compression -> Neoliberalism)",
        "keyframes": [
            # 镀金时代: 原始资本主义，高增长、高剥削
            (0.0, merge_params({"k": 0.30, "mu": 0.15, "eta": 0.018, "V_th": 4.0})),
            # 战后黄金时代: 极高的增长掩盖矛盾，中产崛起压制内卷
            (0.4, merge_params({"k": 0.08, "mu": 0.50, "eta": 0.022, "V_th": 4.5, "alpha": 0.10})),
            # 新自由主义时代: 资本重归内卷，极化导致社会容忍阈值下降
            (1.0, merge_params({"k": 0.28, "mu": 0.20, "eta": 0.015, "V_th": 3.0, "alpha": 0.20}))
        ]
    },
    "Nordic": {
        "name": "Nordic (Agrarian -> Social Democracy -> Modern Welfare)",
        "keyframes": [
            (0.0, merge_params({"k": 0.15, "alpha": 0.15, "delta": 0.05, "V_th": 3.5})),
            # 确立社会民主主义: 累进税极大限制资本无限增殖(k极低)，社会修复极强
            (0.5, merge_params({"k": 0.02, "alpha": 0.05, "delta": 0.18, "T0": 1.0, "V_th": 5.0})),
            # 现代高福利稳态: 创新稳定，无崩溃可能
            (1.0, merge_params({"k": 0.03, "alpha": 0.05, "delta": 0.15, "T0": 1.2, "V_th": 5.0, "eta": 0.012}))
        ]
    },
    "France": {
        "name": "France (Ancien Regime -> Age of Revolutions -> 5th Republic)",
        "keyframes": [
            # 旧制度: 容忍底线极低，财富高度集中
            (0.0, merge_params({"T0": 0.2, "k": 0.25, "V_th": 2.5})),
            # 大革命世纪: 相变阈值V_th极低，爆发极为暴烈(beta=0.95几乎清空旧贵族财富)
            (0.3, merge_params({"V_th": 1.2, "gamma": 15.0, "kappa_fast": 0.6, "beta": 0.95})),
            # 第五共和国: 回稳，但仍保留易罢工的“老区”体质
            (1.0, merge_params({"V_th": 2.8, "gamma": 8.0, "T0": 0.6, "k": 0.12}))
        ]
    },
    "Brazil": {
        "name": "Brazil (Export Economy -> Miracle -> Middle-Income Trap)",
        "keyframes": [
            # 初级产品出口: 创新极低，寡头内卷
            (0.0, merge_params({"eta": 0.005, "k": 0.30, "kappa_slow": 0.01})),
            # 经济奇迹: 进口替代引发短暂创新飙升，红利掩盖矛盾
            (0.4, merge_params({"eta": 0.035, "mu": 0.40, "k": 0.25})),
            # 中等收入陷阱: 腐败导致渐进腐蚀率爆表，高社会熵彻底锁死技术创新
            (1.0, merge_params({"eta": 0.002, "kappa_slow": 0.04, "lam": 2.0, "mu": 0.10, "alpha": 0.25}))
        ]
    }
}

def generate_dynamic_params(keyframes, steps):
    params_over_time = {key: np.zeros(steps) for key in BASE_PARAMS.keys()}
    for t in range(steps):
        t_ratio = t / (steps - 1)
        for i in range(len(keyframes) - 1):
            t1, p1 = keyframes[i]
            t2, p2 = keyframes[i+1]
            if t1 <= t_ratio <= t2:
                weight = (t_ratio - t1) / (t2 - t1) if t2 > t1 else 0
                for key in p1.keys():
                    params_over_time[key][t] = p1[key] * (1 - weight) + p2[key] * weight
                break
        if t_ratio >= keyframes[-1][0]:
            for key in p1.keys():
                params_over_time[key][t] = keyframes[-1][1][key]
    return params_over_time

# ==========================================
# 2. 核心动态仿真逻辑 (修复物理边界约束)
# ==========================================
def run_simulation(profile, steps=8000, dt=0.05):
    np.random.seed(42)
    time = np.linspace(0, steps * dt, steps)
    
    x1, x2, C = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    x1[0], x2[0], C[0] = 0.5, 0.0, 2.0

    P = generate_dynamic_params(profile["keyframes"], steps)
    sigma_1, sigma_2, sigma_c = 0.02, 0.05, 0.01

    for t in range(steps - 1):
        x1_now, x2_now, C_now = x1[t], x2[t], C[t]
        
        V_th, gamma = P['V_th'][t], P['gamma'][t]
        eta, C_max, lam = P['eta'][t], P['C_max'][t], P['lam'][t]
        kappa_slow, kappa_fast = P['kappa_slow'][t], P['kappa_fast'][t]
        T0, mu = P['T0'][t], P['mu'][t]
        k, beta = P['k'][t], P['beta'][t]
        alpha, delta = P['alpha'][t], P['delta'][t]
        
        T_curr = T0 + mu * C_now
        S_Marx = 1.0 / (1.0 + np.exp(-gamma * (x2_now - V_th)))

        dW1, dW2, dW3 = np.random.normal(0, np.sqrt(dt), 3)

        drift_x1 = k * x1_now * (1 - x1_now / C_now) - beta * x1_now * S_Marx
        x1_next = x1_now + drift_x1 * dt + sigma_1 * x1_now * dW1
        
        excess = max(0, x1_now - T_curr)
        drift_x2 = alpha * excess - delta * x2_now
        x2_next = x2_now + drift_x2 * dt + sigma_2 * dW2

        growth = eta * C_now * (1 - C_now / C_max) * np.exp(-lam * x2_now)
        decay  = C_now * (kappa_slow * x2_now + kappa_fast * S_Marx)
        drift_C = growth - decay
        C_next = C_now + drift_C * dt + sigma_c * C_now * dW3

        # ========================================================
        # 修复逻辑: 严格执行公理四物理约束，x1(精英财富) 绝不可超越 C(总承载力)
        # ========================================================
        C[t+1]  = max(0.50, C_next)
        x2[t+1] = max(0.00, x2_next)
        
        # 将 x1 限制在最高不超过当前承载力 C 的 99%
        x1_clamped = min(x1_next, C[t+1] * 0.99)
        x1[t+1] = max(0.01, x1_clamped)

    return time, x1, x2, C, P

# ==========================================
# 3. 动图 (GIF) 渲染模块
# ==========================================
def generate_gif_for_country(country_key, profile, steps=8000):
    print(f"开始仿真并生成 GIF: {country_key}...")
    time, x1, x2, C, P = run_simulation(profile, steps)
    
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(f"Civilization Dynamics: {profile['name']}", fontsize=18)
    
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    ax4 = fig.add_subplot(2, 2, 4)
    
    # 图1 (已彻底移除 x2，保持量纲纯粹)
    line_C, = ax1.plot([], [], 'g-', lw=2, label='Capacity $C$')
    line_x1, = ax1.plot([], [], 'b-', lw=1.5, alpha=0.8, label='Inequality $x_1$')
    line_T, = ax1.plot([], [], 'c--', lw=1.5, alpha=0.6, label='Tolerance $T(C)$')
    
    ax1.set_xlim(0, max(time))
    ax1.set_ylim(0, max(C) * 1.1)  # C 现在是绝对的最大值
    ax1.set_title('Macro-History: Growth & Inequality (Consistent Dim)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # 图2 (保持原样)
    line_x2, = ax2.plot([], [], 'r-', lw=1.5, label='Entropy $x_2$')
    line_Vth, = ax2.plot([], [], 'k--', lw=1.5, label='Dynamic Phase Threshold $V_{th}$')
    ax2.set_xlim(0, max(time))
    ax2.set_ylim(0, max(max(x2), max(P['V_th'])) * 1.2)
    ax2.set_title('Social Stability Cycles')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # 图3
    ax3.set_xlim(0, max(x1) * 1.1)
    ax3.set_ylim(0, max(x2) * 1.1)
    ax3.set_zlim(0, max(C) * 1.1)
    ax3.set_xlabel('Inequality $x_1$')
    ax3.set_ylabel('Entropy $x_2$')
    ax3.set_zlabel('Capacity $C$')
    ax3.set_title('Evolutionary Spiral')
    line_3d, = ax3.plot([], [], [], 'b-', lw=1, alpha=0.6)

    # 图4
    ax4.axhline(y=np.mean(P['V_th']), color='r', ls='--', alpha=0.5, label='Avg Phase Threshold')
    ax4.set_xlim(0, max(x1) * 1.1)
    ax4.set_ylim(0, max(x2) * 1.1)
    ax4.set_xlabel('Inequality $x_1$')
    ax4.set_ylabel('Entropy $x_2$')
    ax4.set_title('Phase Portrait')
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)
    scat_4d = ax4.scatter([], [], c=[], cmap='Greens', s=10, alpha=0.6)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)

    frames_count = 150 
    step_size = steps // frames_count

    def update(frame_idx):
        idx = (frame_idx + 1) * step_size
        
        # 更新图1
        line_C.set_data(time[:idx], C[:idx])
        line_x1.set_data(time[:idx], x1[:idx])
        line_T.set_data(time[:idx], P['T0'][:idx] + P['mu'][:idx] * C[:idx])
        
        # 更新图2
        line_x2.set_data(time[:idx], x2[:idx])
        line_Vth.set_data(time[:idx], P['V_th'][:idx])
        
        # 更新图3 
        line_3d.set_data(x1[:idx], x2[:idx])
        line_3d.set_3d_properties(C[:idx])
        
        # 更新图4
        scat_4d.set_offsets(np.column_stack((x1[:idx], x2[:idx])))
        scat_4d.set_array(C[:idx])
        
        return line_C, line_x1, line_T, line_x2, line_Vth, line_3d, scat_4d

    ani = animation.FuncAnimation(fig, update, frames=frames_count, interval=80, blit=False)
    
    filename = f"sim_{country_key}.gif"
    ani.save(filename, writer='pillow', fps=15)
    plt.close(fig)
    print(f"✅ 生成完毕: {filename}")

if __name__ == "__main__":
    for country, profile in COUNTRY_PROFILES.items():
        generate_gif_for_country(country, profile)