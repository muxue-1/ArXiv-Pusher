
论文标题: DexterityGen: Foundation Controller for Unprecedented Dexterity
作者: Zhao-Heng Yin, Changhao Wang, Luis Pineda, Francois Hogan, Krishna Bodduluri, Akash Sharma, Patrick Lancaster, Ishita Prasad, Mrinal Kalakrishnan, Jitendra Malik, Mike Lambeta, Tingfan Wu, Pieter Abbeel, Mustafa Mukadam
发表日期: 2025-02-06 18:49:35
链接: http://arxiv.org/abs/2502.04307v1

### 1. 论文摘要概括

DexterityGen（DexGen）是一种基础控制器，通过生成模型将外部策略产生的不安全、粗略的运动指令转化为安全且精细的动作，实现了前所未有的灵巧操作行为。DexGen 通过在模拟环境中使用强化学习预训练大规模的灵巧运动原语，结合人类遥操作作为高层策略，能够在多样化任务中展示出卓越的操作能力。实验证明，DexGen 在仿真和现实世界中显著提升了稳定性，并首次展示了使用钢笔、注射器和螺丝刀等工具的复杂操作技能。

### 2. 三个主要创新点

1. **结合强化学习与人类遥操作**：DexGen 利用强化学习预训练低层次的灵巧运动原语，并通过人类遥操作提供高层次的粗略运动指令，实现了高效的复杂任务操控。
   
2. **基于生成模型的动作转换**：采用扩散模型（Diffusion Model）作为生成模型，能够将不安全和粗糙的运动指令转换为安全且精细的机器人动作，确保操作的稳定性和可靠性。
   
3. **大规模多任务模拟数据预训练**：在模拟环境中收集了超过10亿次的操作数据，通过多任务训练覆盖广泛的握持和操作场景，使得DexGen具备高度的泛化能力，能够应对多样化的现实世界任务。

### 3. 保持简洁专业

DexterityGen 提出了一种创新的控制框架，通过结合强化学习和人类遥操作，利用生成模型实现了从粗略指令到精细动作的转化，显著提升了机器人在复杂操作任务中的稳定性和灵巧性。其在模拟和现实世界中的成功应用，展示了该方法在多样化和高难度任务中的广泛适用性和优越性能。
============================================================
