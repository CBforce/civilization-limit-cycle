# civilization-limit-cycle
A 3D stochastic dynamical model of historical cycles and technological growth.
# Civilization: The Limit Cycle (文明：极限环)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)

[English](#english-introduction) | [中文简介](#中文简介)

---

## English Introduction

### Abstract
**Civilization: The Limit Cycle** is a 3D stochastic dynamical system designed to unify historical cycle theory (dynastic rise and fall) with endogenous growth theory. 

By mapping societal variables into a physical-mathematical framework, this model explains why civilizations oscillate in a "Limit Cycle" of inequality and collapse, and how technological capacity ($C$) dictates whether this cycle spirals upward (progress), stagnates (the Middle-Income Trap), or collapses brittlely (Techno-Feudalism / Singularity Collapse).

### The Three State Variables
1. **$x_1$ (Economic Layer):** Inequality / Elite Wealth Accumulation.
2. **$x_2$ (Social Layer):** Social Entropy / Relative Deprivation.
3. **$C$ (Technological Layer):** Carrying Capacity / Maximum potential of the civilization.

### Core Axioms
The simulation is strictly derived from 5 socio-physical axioms:
1. **Marxist Phase Transition:** Quantitative entropy accumulation triggers qualitative systemic collapse (modeled via a Boltzmann-Sigmoid function).
2. **Tainter’s Diminishing Returns:** Technological complexity yields diminishing marginal returns and is suppressed by high-entropy environments.
3. **Dynamic Tolerance:** Societal tolerance for inequality is a function of technological growth, leading to fragile stability (Brittle Collapse) when growth stagnates.
4. **Malthusian-Verhulst Competition:** Elite wealth grows logistically until it hits the ceiling of societal carrying capacity.
5. **Relative Deprivation & Resilience:** Unfairness generates social entropy, while societal forgetting provides system resilience.

### Quick Start
Run the 3D Python simulation to visualize the historical spiral:
```bash
git clone [https://github.com/CBforce/civilization-limit-cycle.git](https://github.com/CBforce/civilization-limit-cycle.git)
cd civilization-limit-cycle
pip install numpy matplotlib
python simulation_axiomatic.py
中文简介摘要《文明：极限环》是一个三维随机动力学模型，旨在统一“历史周期律”与“长期经济增长理论”。本模型将社会学变量映射为严密的物理与数学方程，解释了为何人类文明会在“不平等与崩溃”的极限环中反复震荡。同时揭示了技术承载力（$C$）如何决定这个循环是走向螺旋上升（文明进步）、停滞震荡（中等收入陷阱），还是最终走向灾难性的相变（高科技封建主义/脆性崩溃）。三个核心状态变量$x_1$（经济层）： 财富不平等程度 / 精英财富累积总量。$x_2$（社会层）： 社会熵 / 相对剥夺感与社会矛盾总量。$C$（技术层）： 文明承载力 / 生产力与技术上限。五大底层公理该系统的微分方程严格推导自以下五大社会物理学公理：量变到质变（马克思主义相变）： 社会矛盾的累积触发系统性的崩溃（基于最大熵原理推导的 Sigmoid 开关）。复杂性收益递减（泰恩特法则）： 技术突破具有边际收益递减特性，且高熵环境会物理性地破坏创新积累。动态容忍度： 经济增量会掩盖社会矛盾（提高容忍阈值），但一旦增长停滞，将引发剧烈的“脆性崩溃”。马尔萨斯-费尔哈斯竞争： 精英阶层的财富掠夺服从逻辑斯蒂（Logistic）内卷增长，受限于物理总盘子。相对剥夺感与社会遗忘： 超过容忍阈值的不公产生社会熵，而系统具备一定的时间遗忘与自愈能力。运行模拟本项目包含完整的 Python 3D 动力学仿真代码，运行以下命令即可观测“文明螺旋上升”与“治乱循环”的相空间轨迹：
git clone [https://github.com/CBforce/civilization-limit-cycle.git](https://github.com/CBforce/civilization-limit-cycle.git)
cd civilization-limit-cycle
pip install numpy matplotlib
python simulation_axiomatic.py
贡献与共建 (Contributing)We welcome researchers from physics, economics, sociology, and computer science to contribute.我们欢迎全球物理学、经济学、社会学以及计算机领域的同仁参与共建：参数拟合 (Parameter Fitting): 使用各国的历史基尼系数、通胀率、专利数据来拟合系统参数。政策干预反馈 (Policy Feedback Loops): 在方程中引入 $\theta$（税收/再分配减压阀），测试其在相平面中的镇定效果。AGI 终局模拟 (AGI Endgame Simulation): 修改 $C_{max}$ 极限参数，模拟通用人工智能降临后的终极稳态。
