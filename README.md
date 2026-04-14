# 🛩️ 飞机大战 Airplane Battle v3.0 - Chapter Boss Edition

<div align="center">

**经典竖版街机射击游戏 · 章节Boss版**
**Classic Vertical Arcade Shooter · Chapter Boss Edition**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Deeplearning67/airplane-battle?style=social)](https://github.com/Deeplearning67/airplane-battle/stargazers)

</div>

---

## 📖 简介 / Introduction

**飞机大战 v3.0** 是一款基于 Pygame 开发的经典竖版街机射击游戏终极版本，包含完整的 **5章章节系统** 和 **章节专属Boss战**。玩家需要在每章击败独特设计的Boss才能解锁下一章，挑战极限！

**Airplane Battle v3.0** is the ultimate edition of the classic vertical arcade shooter built with Pygame. Featuring a complete **5-chapter system** with **unique bosses per chapter**, players must defeat specially designed bosses to unlock the next chapter and reach the ultimate challenge!

---

## ✨ 核心特色 / Key Features

| 特色 Feature | 描述 Description |
|------------|----------------|
| 🎮 **5章完整章节** | 每章独立配色、敌机造型、Boss设计，循序渐进的难度曲线 |
| 👾 **5个章节Boss** | 每章独特Boss，多阶段攻击，密集弹幕设计 |
| 📈 **章节解锁系统** | 击败Boss解锁下一章，第5章通关即胜利 |
| 🎁 **9种道具系统** | 火力增强、生命恢复、护盾、冰冻、磁铁等道具 |
| 🏆 **Top 10排行榜** | 本地JSON持久化存储，含章节记录追踪 |
| 🎨 **100%程序化绘图** | 无需任何外部图片资源，纯代码绘制所有图形 |
| 📊 **性能优化** | Surface缓存、粒子数量限制、异常保护 |

---

## 🗺️ 章节设计 / Chapter Design

| 章节 | 名称 | Boss | 血量 | 难度 | 特色弹幕 |
|------|------|------|------|------|----------|
| Ch.1 | 红色尖兵 | HP:80 | ⭐⭐ | 十字交叉 + 扇形 |
| Ch.2 | 紫色利刃 | HP:150 | ⭐⭐⭐ | 旋转螺旋 + 环形 |
| Ch.3 | 棕色重甲 | HP:250 | ⭐⭐⭐⭐ | 3方向散射 + 宽幅扇形 |
| Ch.4 | 绿色精英 | HP:400 | ⭐⭐⭐⭐⭐ | 追踪弹 + 散布弹 |
| Ch.5 | 黄金终焉 | HP:600 | ⭐⭐⭐⭐⭐⭐ | 全屏乱射 + 激光预警 |

### 中文版本 / Chinese Version

```
第一章 · 红色尖兵 (Red Sentinel)
  └─ 十字交叉弹幕 + 宽幅扇形弹幕

第二章 · 紫色利刃 (Purple Blade)
  └─ 旋转双螺旋弹幕 + 12发环形弹幕

第三章 · 棕色重甲 (Brown Fortress)
  └─ 3方向散射弹幕 + 宽幅扇形叠加

第四章 · 绿色精英 (Green Elite)
  └─ 追踪弹 + 9发散布弹 + 横向弹幕

第五章 · 黄金终焉 (Golden Nemesis)
  └─ 3连随机弹幕 + 16发环形弹幕 + 激光预警
```

---

## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements

- Python 3.8 或更高版本
- Pygame 2.0 或更高版本

### 安装 / Installation

```bash
# 克隆仓库
git clone https://github.com/Deeplearning67/airplane-battle.git
cd airplane-battle

# 安装依赖
pip install pygame
```

### 运行 / Running the Game

```bash
# Linux / macOS
python airplane_battle3.py

# Windows (双击或命令行)
run.bat

# 或者直接
python airplane_battle3.py
```

---

## 🎮 操作说明 / Controls

| 按键 / Key | 功能 / Action |
|------------|--------------|
| `← → ↑ ↓` 或 `W A S D` | 移动飞机 / Move aircraft |
| `空格 Space` | 发射子弹（长按连发）/ Fire (hold for continuous) |
| `B` | 使用全屏炸弹 / Use screen-clearing bomb |
| `P` 或 `ESC` | 暂停/继续 / Pause/Resume |
| `R` | 重新开始（游戏结束时）/ Restart (when game over) |
| `M` | 返回菜单 / Return to menu |
| `L` | 查看排行榜 / View leaderboard |
| `鼠标左键` | 菜单按钮点击 / Menu button click |

---

## 🎯 Boss弹幕示例 / Boss Pattern Examples

```
Chapter 1 Boss - 红色尖兵:
  阶段0: 十字交叉 (0°/90°/180°/270°) 弹幕
  阶段1: 宽幅扇形弹幕 (7发)

Chapter 2 Boss - 紫色利刃:
  阶段0: 旋转双螺旋弹幕
  阶段1: 环形弹幕 + 螺旋弹幕叠加

Chapter 3 Boss - 棕色重甲:
  阶段0: 3方向散射弹幕
  阶段1: 宽幅扇形弹幕 + 3方向叠加

Chapter 4 Boss - 绿色精英:
  阶段0: 追踪弹 + 散布弹
  阶段1: 追踪弹 + 横向弹幕 + 散布弹

Chapter 5 Boss - 黄金终焉:
  阶段0: 3连随机弹幕 + 16发环形弹幕
  阶段1: 快速激光预警弹幕 + 环形弹幕
```

---

## 🛠️ 技术细节 / Technical Specifications

| 项目 / Item | 规格 / Spec |
|-------------|-------------|
| 渲染引擎 / Rendering Engine | Pygame SDL2 |
| 帧率 / Frame Rate | 60 FPS |
| 分辨率 / Resolution | 540×780 (竖屏 / Portrait) |
| 代码行数 / Lines of Code | ~2500 行单文件 / Single file |
| 图形 / Graphics | 100% 程序化绘制 / 100% Procedural |
| 外部依赖 / External Assets | **零** / None |

### 性能优化 / Performance Optimizations

- ✅ Surface 预缓存（陨石旋转/HUD背景/护盾效果）
- ✅ 粒子数量上限（150粒子+80尾迹）
- ✅ 全局异常保护主循环
- ✅ Bullet.update 方法注入（支持Boss自定义弹幕）

---

## 📜 版本历史 / Changelog

### v3.0 Chapter Boss Edition (2026.04) ⭐ 当前版本

- ✅ 5章完整章节系统
- ✅ 每章专属Boss（密集弹幕设计）
- ✅ 章节进度追踪
- ✅ 排行榜增加章节字段
- ✅ Boss血量逐章递增 (80→150→250→400→600)
- ✅ Boss入场警告动画
- ✅ 章节通关动画

### v2.3 Stability

- ✅ emoji字体崩溃修复
- ✅ 玩家死亡后HUD安全访问
- ✅ PowerUp.apply引用修复
- ✅ 陨石旋转缓存限制

---

## 📁 项目结构 / Project Structure

```
airplane-battle/
├── airplane_battle3.py   # 主游戏源码 (~2500行)
├── README.md             # 说明文档
├── requirements.txt      # Python依赖
├── run.bat               # Windows一键启动
├── LICENSE               # MIT开源协议
└── .gitignore            # Git忽略文件
```

---

## 🛡️ 安全与隐私

- 本游戏为纯本地运行程序，**无任何网络通信**
- 排行榜数据存储在本地 `leaderboard3.json` 文件
- 不收集任何用户数据

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

---

## 📜 许可 / License

本项目基于 MIT License 开源，详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**作者 / Author**: 阿爪 🦞 (AZhua)  
**日期 / Date**: 2026.04  
**许可 / License**: [MIT](LICENSE)

⭐ 如果喜欢，欢迎 Star！⭐

</div>
