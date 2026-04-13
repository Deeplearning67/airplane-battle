# 🛩️ 飞机大战 Airplane Battle v2.1 Enhanced

<div align="center">

**经典街机射击游戏 | Classic Arcade Shooter**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Game Preview](https://img.shields.io/badge/🎮-Play_Now-red)

</div>

---

## 📖 简介 / About

**飞机大战 (Airplane Battle)** 是一款使用 **Pygame** 开发的经典竖版街机射击游戏，采用纯代码绘制所有图形资源（无需外部图片文件）。

**Airplane Battle** is a classic vertical arcade shooter built entirely with **Pygame**. All graphics are procedurally generated in code — no external image files needed.

### ✨ 核心特色 / Features

| 功能 | Feature |
|------|---------|
| 🎮 三种敌机类型（小型侦察机/中型战斗机/大型轰炸机） | 3 enemy types (scout/fighter/bomber) |
| 💣 多种障碍物（陨石/地雷/障碍墙） | Multiple obstacles (asteroid/mine/barrier) |
| 🎁 9 种道具系统（火力/生命/护盾/磁铁/冰冻等） | 9 power-up types |
| 💥 全屏炸弹 + 粒子特效爆炸动画 | Screen bomb + particle explosion effects |
| 🏆 Top 10 排行榜持久化存储 | Persistent Top 10 leaderboard |
| 📏 飞行距离实时计算 | Real-time flight distance tracking |
| 🔥 连击系统与等级提升 | Combo system & level progression |
| 🪐 星空背景 + 行星装饰 + 流星效果 | Starfield background + planets + shooting stars |
| 🎯 碰撞检测修复 / 菜单鼠标点击支持 | Fixed collision detection / mouse menu support |

---

## 🎮 操作说明 / Controls

| 按键 Key | 功能 Action |
|----------|------------|
| `←` `→` `↑` `↓` 或 `A` `W` `S` `D` | 移动飞机 Move |
| `空格 Space` (可长按连发) | 发射子弹 Fire (hold for auto-fire) |
| `B` | 使用全屏炸弹 Use Bomb |
| `P` 或 `ESC` | 暂停/继续 Pause/Resume |
| `R` | 重新开始 Restart (game over) |
| `M` | 返回菜单 Return to Menu |
| `L` | 查看排行榜 View Leaderboard |
| `鼠标左键 Left Click` | 菜单按钮点击 Menu click |

---

## 🚀 快速开始 / Quick Start

### 前置要求 / Prerequisites

- **Python 3.8+**
- **Pygame 2.0+**

### 安装 / Installation

```bash
# 安装 Pygame
pip install pygame

# 克隆仓库
git clone https://github.com/[your-username]/airplane-battle.git
cd airplane-battle
```

### 运行 / Run

```bash
python airplane_battle.py
```

> **注意**: 首次运行会在脚本同目录自动生成 `leaderboard.json` 排行榜文件。

---

## 📁 项目结构 / Structure

```
airplane-battle/
├── airplane_battle.py      # 主游戏源码 (~2600行)
├── README.md               # 说明文档（本文件）
├── .gitignore              # Git 忽略规则
└── leaderboard.json        # 排行榜数据 (运行后自动生成)
```

**全部图形均为代码绘制，零外部依赖资源！**
All graphics are drawn in code — zero external asset dependencies!

---

## 🎯 游戏元素 / Game Elements

### 敌机类型 / Enemy Types

| 类型 Type | 生命 HP | 分数 Score | 特征 Description |
|-----------|---------|------------|------------------|
| 🔴 小型侦察机 Small Scout | 1 | 100 | 移动敏捷，红色造型 |
| 🟣 中型战斗机 Medium Fighter | 4 | 350 | 会射击，紫色造型 |
| 🟤 大型轰炸机 Large Bomber | 12 | 900 | 高血量，棕色重型 |

### 道具列表 / Power-ups

| 图标 Icon | 名称 Name | 效果 Effect |
|-----------|-----------|-------------|
| `P` | 火力 Power Up | 提升火力等级 (最高5级) |
| `+` | 回复 Heal | 恢复1点生命值 |
| `B` | 炸弹 Bomb | 全屏清场消灭所有敌人 |
| `S` | 护盾 Shield | 8秒无敌护盾 |
| `>` | 加速 Speed Boost | 6秒移动加速 |
| `M` | 磁铁 Magnet | 8秒吸引附近道具 |
| `F` | 冰冻 Freeze | 7秒减速所有敌机 |
| `$` | 加分 Score Bonus | 直接获得500分 |
| `L` | 激光炮 Laser | 火力直接拉满至最高级 |

### 障碍物 / Obstacles

| 类型 Type | 特征 Behavior |
|-----------|---------------|
| ☄️ 陨石 Asteroid | 缓慢飘落，可被子弹摧毁 |
| 💣 地雷 Mine | 带闪烁警告灯，碰撞高伤害 |
| 🧱 障碍墙 Barrier | 横向移动的墙壁警告带 |

---

## 🔧 技术细节 / Technical Details

- **渲染引擎**: Pygame SDL2 硬件加速
- **帧率**: 60 FPS
- **分辨率**: 540×780 (竖屏)
- **音效**: 程序化合成 (无需音频文件)
- **字体**: 系统 SimHei (黑体) / 降级为默认字体
- **性能优化**:
  - Surface 缓存机制避免每帧重建
  - 粒子数量上限防止内存泄漏
  - 预分配绘制缓冲区
- **难度曲线**: 每击杀12架敌机升一级，最高15级

---

## 📊 排行榜 / Leaderboard

游戏结束后可输入名字保存成绩，排行榜以 JSON 格式本地持久化存储，保留 Top 10 记录：

```json
{
  "entries": [
    {"name": "PILOT", "score": 25000, "distance": 12500, "kills": 45, "level": 8, "date": "2026-04-13 21:30"}
  ]
}
```

---

## 📜 更新日志 / Changelog

### v2.1 Enhanced (当前 / Current)
- ✅ 修复射击碰撞检测 Bug
- ✅ 全新精美 UI 界面与飞机造型
- ✅ 多种障碍物系统（陨石/地雷/障碍墙）
- ✅ 飞行距离实时计算
- ✅ Top 10 排行榜持久化存储
- ✅ 菜单鼠标点击支持
- ✅ 移除 BGM 消除卡顿（仅保留短音效）
- ✅ 新增：磁铁、冰冻、激光炮道具
- ✅ 屏幕震动效果 + 连击系统

---

## 📝 许可证 / License

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 👨‍💻 作者 / Author

**Made by 阿爪 🦞** | 2026.04

<div align="center">
⭐ 如果喜欢这个项目，欢迎给一个 Star！ ⭐
<br>
If you enjoy this project, please consider giving it a Star!
</div>
