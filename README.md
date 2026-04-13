# 🛩️ 飞机大战 Airplane Battle v2.1 Enhanced

<div align="center">

**经典街机射击游戏 | Classic Arcade Shooter**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1_Enhanced-red.svg)]()

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
| 🏆 Top 10 排行榜持久化存储（JSON） | Persistent Top 10 leaderboard (JSON) |
| 📏 飞行距离实时计算 | Real-time flight distance tracking |
| 🔥 连击系统与等级提升（最高15级） | Combo system & level progression (max Lv.15) |
| 🪐 星空背景 + 行星装饰 + 流星效果 | Starfield background + planets + shooting stars |
| 🎯 碰撞检测修复 / 菜单鼠标点击支持 | Fixed collision detection / mouse menu support |

---

## 🚀 快速开始 / Quick Start

### 前置要求 / Prerequisites

- **Python 3.8+**
- **Pygame 2.0+**

### 安装 / Installation

```bash
# Install Pygame
pip install pygame

# Clone repository
git clone https://github.com/AZhua-dev/airplane-battle.git
cd airplane-battle
```

### 运行 / Run

```bash
python airplane_battle.py
```

> ⚠️ **注意 / Note**: 首次运行会在脚本同目录自动生成 `leaderboard.json` 排行榜文件。
> The `leaderboard.json` file will be auto-generated on first run.

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

## 📁 项目结构 / Structure

```
airplane-battle/
├── airplane_battle.py      # 主游戏源码 (~2600行) — Main game source (~2600 lines)
├── README.md               # 说明文档（本文件）
├── LICENSE                 # MIT 开源协议
└── .gitignore              # Git 忽略规则
```

**全部图形均为代码绘制，零外部依赖资源！**
All graphics are drawn in code — zero external asset dependencies!

---

## 🎯 游戏元素 / Game Elements

### 敌机类型 / Enemy Types

| 类型 Type | 生命 HP | 分数 Score | 特征 Description |
|-----------|---------|------------|------------------|
| 🔴 小型侦察机 Small Scout | 1 | 100 | 移动敏捷，红色造型，倒三角机身 |
| 🟣 中型战斗机 Medium Fighter | 4 | 350 | 会射击，紫色造型，双驾驶舱 |
| 🟤 大型轰炸机 Large Bomber | 12 | 900 | 高血量，棕色重型，多武器挂点 |

### 道具列表 / Power-ups

| 图标 Icon | 名称 Name | 效果 Effect |
|-----------|-----------|-------------|
| `P` | 火力 Power Up | 提升火力等级 (最高5级) |
| `+` | 回复 Heal | 恢复1点生命值 |
| `B` | 炸弹 Bomb | 全屏清场消灭所有敌人 |
| `S` | 护盾 Shield | 8秒无敌护盾 |
| `>` | 加速 Speed Boost | 6秒移动加速 |
| `M` | 磁铁 Magnet | 8秒吸引附近道具 |
| `F` | 冰冻 Freeze | 7秒减速所有敌机至25%速度 |
| `$` | 加分 Score Bonus | 直接获得500分 |
| `L` | 激光炮 Laser | 火力直接拉满至最高级(5级) |

### 障碍物 / Obstacles

| 类型 Type | 特征 Behavior |
|-----------|---------------|
| ☄️ 陨石 Asteroid | 缓慢飘落+旋转，可被子弹摧毁，碰撞伤害2HP |
| 💣 地雷 Mine | 带闪烁红灯警告，碰撞高伤害3HP |
| 🧱 障碍墙 Barrier | 横向移动的警告带，反弹运动模式，伤害1HP |

---

## 🔧 技术细节 / Technical Details

| 项目 | 规格 |
|------|------|
| 渲染引擎 Rendering Engine | Pygame SDL2 硬件加速 |
| 帧率 Frame Rate | 60 FPS |
| 分辨率 Resolution | 540×780 (竖屏 Portrait) |
| 音效 Audio | 程序化合成短音效 (无BGM，避免卡顿) |
| 字体 Font | 系统 SimHei (黑体) / 降级为默认字体 |
| 持久化 Storage | JSON 文件排行榜 (leaderboard.json) |

### 性能优化亮点 / Performance Highlights

- ✅ **Surface 缓存机制**: HUD背景、护盾效果、发光脉冲、粒子表面等全部预创建缓存，运行时复用，避免每帧重建 Surface 导致内存泄漏
- ✅ **粒子数量上限**: 粒子上限300个，尾迹上限150个，防止长时间游戏后内存爆炸
- ✅ **预分配绘制缓冲区**: 使用 `_draw_buffer` 静态属性预分配 game surface，避免每帧 `screen.copy()`
- ✅ **屏幕震动优化**: 震动幅度从 ±25 降至 ±5（除以4），大幅减少视觉抖动感
- ✅ **移除 BGM**: 程序化合成的 BGM 是卡顿主因，v2.1 移除后仅保留极短的射击/爆炸音效，流畅度显著提升
- ✅ **爆炸帧预缩放**: 不同尺寸的爆炸在创建时一次性缩存所有帧，避免每帧 `transform.scale`

### 难度曲线 / Difficulty Curve

- 每击杀 **12** 架敌机升一级，最高 **15** 级
- 敌机生成间隔随等级缩短：`max(55 - level×3, 18)` 帧
- 高等级时三种敌机混合出现（小型35%/中型40%/大型25%）
- 障碍物出现概率随等级递增：`min(0.03 + level×0.005, 0.08)`
- 冰冻道具可暂时冻结所有敌机，创造反击窗口

---

## 📊 排行榜 / Leaderboard

游戏结束后可输入名字保存成绩。排行榜以 JSON 格式本地持久化存储，保留 Top 10 记录：

```json
{
  "entries": [
    {
      "name": "PILOT",
      "score": 25000,
      "distance": 12500,
      "kills": 45,
      "level": 8,
      "date": "2026-04-13 21:30"
    }
  ]
}
```

> ⚠️ `leaderboard.json` 已加入 `.gitignore`，不会上传到仓库。

---

## 📜 版本历史 & 升级对比 / Changelog & Version Comparison

### v2.1 Enhanced (当前版本 / Current)

这是目前最完整、最稳定的正式发布版。

#### 相比 v2.0 / v1.x 的核心升级：

| 改进领域 | v1.x (初版) | v2.0 | **v2.1 Enhanced (本版)** |
|---------|-------------|------|--------------------------|
| **射击碰撞** | ❌ 子弹经常穿透敌机不造成伤害 | ⚠️ 部分修复 | ✅ **完全重写碰撞检测逻辑**，精确判定子弹-敌机/障碍物的 colliderect 匹配 |
| **UI界面** | 基础矩形图形 | 精美升级 | ✅ **全面重绘 V2 造型系统**：流线型玩家战机(双发引擎+高光条纹)、三类敌机各具特色(装甲线/武器挂架/双驾驶舱)、六边形发光道具 |
| **障碍物** | 无 | 新增陨石/地雷/墙 | ✅ **完善物理行为**：陨石旋转飘落+弹坑纹理、地雷闪烁红灯+危险标志、障碍墙黄黑警示带+反弹运动 |
| **排行榜** | 无 | Top 10 JSON 存储 | ✅ **增强统计维度**：增加飞行距离、击杀数、最大连击等字段；前三名金银铜高亮 |
| **性能稳定性** | BGM导致严重卡顿 | 仍存在卡顿问题 | ✅ **彻底解决卡顿**：移除程序化合成BGM → 仅保留极短音效；Surface缓存机制全覆盖 → 内存泄漏归零 |
| **视觉效果** | 单色星空背景 | 星云+行星 | ✅ **新增流星彗星系统**：随机生成带拖尾粒子的流星；飞机引擎火焰尾迹动画 |
| **操作体验** | 仅键盘 | 键盘为主 | ✅ **完整鼠标菜单支持**：主菜单按钮悬停高亮+点击响应、排行榜/结算界面点击返回 |
| **道具系统** | 4种基础道具 | 扩展到7种 | ✅ **9种完整道具体系**：新增磁铁吸引(M)、冰冻减速(F)、加分($）、激光炮(L)，含加权随机掉落算法 |
| **状态反馈** | 基础HUD | 增强 | ✅ **通知队列系统**：获得道具/升级/炸弹清场均有中央弹出通知；连击数≥3时动态放大显示 |
| **代码质量** | 单文件基础结构 | 有注释但较散 | ✅ **模块化架构**：清晰分区的类体系(Player/Bullet/Enemy/Obstacle/PowerUp/Explosion/Particle/StarField/Planet/ShootingStar/Leaderboard/DistanceTracker/Game)；中英双语关键注释 |

#### 稳定性提升详情：

1. **内存泄漏修复**: 所有频繁调用的 `draw()` 方法中的动态 Surface 创建已替换为类级别缓存 (`_surf_cache`, `_shield_surf`, `_glow_cache`, `_draw_buffer`, `_hud_bg`, `_blink_surf`)
2. **集合遍历安全**: 所有 `for ... in list[:]+list.remove()` 循环改为先收集再批量清理，避免遍历中修改集合导致的异常
3. **异常容错**: 所有音效播放、字体渲染、Surface操作均包裹 `try/except`，确保在缺少音频设备或字体环境下仍能正常运行
4. **数值安全**: 磁铁吸引距离计算增加 `dist > 5` 保护，防止除零；Surface尺寸计算使用 `max()` 下界约束

---

## 🛠️ 开发信息 / Development Info

- **语言 / Language**: Python 3.8+
- **框架 / Framework**: Pygame 2.0+
- **代码行数 / Lines of Code**: ~2600 行 (单文件架构)
- **图形渲染 / Graphics**: 100% 程序化绘制 (Procedural Generation, Zero External Assets)
- **作者 / Author**: **阿爪 🦞** | AZhua
- **日期 / Date**: 2026.04
- **许可协议 / License**: [MIT](LICENSE)

---

## 📝 致谢 / Acknowledgments

- Pygame 社区提供的优秀 2D 游戏框架
- 所有测试玩家的反馈意见

---

<div align="center">

⭐ 如果喜欢这个项目，欢迎给一个 Star！ ⭐

If you enjoy this project, please consider giving it a Star!

**Made by 阿爪 🦞** | 2026.04

</div>
