"""
飞机大战 v2.1 - Airplane Battle Enhanced
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
全新升级：
  ✅ 修复射击碰撞检测Bug
  ✅ 全新精美UI界面与飞机造型
  ✅ 多种障碍物系统（陨石/地雷/障碍墙）
  ✅ 飞行距离实时计算
  ✅ 排行榜持久化存储（Top 10）
  🆕 v2.1: 移除BGM消除卡顿 + 菜单鼠标点击支持

操作说明：
  ← → / A D : 左右移动
  ↑ ↓ / W S : 上下移动
  空格键     : 发射子弹（可长按连发）
  B 键      : 使用全屏炸弹
  P 键      : 暂停游戏
  R 键      : 重新开始（结束时）
  M 键      : 返回菜单（结束时）
  鼠标左键   : 菜单按钮点击
  ESC       : 退出/暂停

作者: 阿爪 🦞 | 2026-04
"""

import pygame
import random
import math
import sys
import json
import os
from datetime import datetime

# ======================== 初始化 Pygame ========================
pygame.init()
# 音效系统（仅音效，不含BGM，避免卡顿）
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

# ======================== 屏幕设置 ========================
SCREEN_WIDTH = 540
SCREEN_HEIGHT = 780
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🛩️ 飞机大战 v2.0 - Airplane Battle")
clock = pygame.time.Clock()

# ======================== 排行榜文件路径 ========================
# 自动定位到脚本同目录下的 leaderboard.json
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(_SCRIPT_DIR, "leaderboard.json")

# ======================== 颜色定义（扩展色板）========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
DARK_RED = (180, 30, 30)
GREEN = (50, 255, 100)
DARK_GREEN = (20, 120, 40)
BLUE = (60, 140, 255)
DARK_BLUE = (8, 15, 35)
NAVY = (12, 24, 52)
YELLOW = (255, 230, 0)
ORANGE = (255, 160, 0)
CYAN = (0, 220, 255)
LIGHT_CYAN = (120, 240, 255)
PURPLE = (180, 70, 255)
MAGENTA = (255, 80, 180)
PINK = (255, 150, 200)
GOLD = (255, 215, 0)
SILVER = (200, 210, 220)
GRAY = (100, 100, 110)
LIGHT_GRAY = (150, 155, 165)
BROWN = (160, 90, 45)
IVORY = (255, 250, 240)

# 渐变色工具
def gradient_color(c1, c2, ratio):
    """在两个颜色之间插值"""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * ratio) for i in range(3))

# ======================== 字体设置 ========================
try:
    font_tiny = pygame.font.SysFont("simhei", 16)
    font_small = pygame.font.SysFont("simhei", 22)
    font_medium = pygame.font.SysFont("simhei", 30)
    font_large = pygame.font.SysFont("simhei", 48)
    font_title = pygame.font.SysFont("simhei", 62)
    font_huge = pygame.font.SysFont("simhei", 76)
except:
    font_tiny = pygame.font.Font(None, 18)
    font_small = pygame.font.Font(None, 24)
    font_medium = pygame.font.Font(None, 34)
    font_large = pygame.font.Font(None, 52)
    font_title = pygame.font.Font(None, 68)
    font_huge = pygame.font.Font(None, 82)


# ================================================================
#                    ★★★ 资源生成（全面重绘）★
# ================================================================

def create_player_surface_v2():
    """绘制精美的玩家战斗机 V2 - 更具科技感的造型"""
    surf = pygame.Surface((56, 68), pygame.SRCALPHA)

    # ===== 机翼（后层，深色）=====
    wing_points = [
        (4, 42),   # 左翼尖后
        (18, 38),  # 左翼根后
        (18, 44),  # 左尾翼外
        (25, 50),  # 尾部左下
        (31, 50),  # 尾部右下
        (38, 44),  # 右尾翼外
        (38, 38),  # 右翼根后
        (52, 42),  # 右翼尖后
        (46, 32),  # 右翼尖前
        (36, 34),  # 右机身翼连接
        (28, 55),  # 引擎底部
        (28, 55),
    ]
    # 后掠翼
    back_wing = [(4, 40), (16, 36), (16, 44), (24, 52), (32, 52), (40, 44), (40, 36), (52, 40), (44, 30), (34, 33)]
    pygame.draw.polygon(surf, (20, 60, 120), back_wing)

    # ===== 主机身（流线型渐变效果）=====
    body_points = [
        (28, 0),     # 机头尖端
        (34, 14),    # 右上机身
        (40, 26),    # 右翼根前
        (36, 38),    # 右机身下部
        (32, 54),    # 右引擎上部
        (28, 58),    # 引擎中心底
        (24, 54),    # 左引擎上部
        (20, 38),    # 左机身下部
        (16, 26),    # 左翼根前
        (22, 14),    # 左上机身
    ]
    # 机身主体渐变填充
    pygame.draw.polygon(surf, CYAN, body_points)
    pygame.draw.polygon(surf, WHITE, body_points, 2)

    # 机身高光条纹
    highlight = [(27, 2), (32, 13), (37, 24), (33, 36), (29, 50)]
    if len(highlight) >= 2:
        pygame.draw.lines(surf, LIGHT_CYAN, False, highlight, 2)

    # ===== 前掠主翼（带细节）=====
    main_wing_l = [(16, 26), (2, 38), (6, 40), (18, 36)]
    main_wing_r = [(40, 26), (54, 38), (50, 40), (38, 36)]
    pygame.draw.polygon(surf, (40, 160, 220), main_wing_l)
    pygame.draw.polygon(surf, (40, 160, 220), main_wing_r)
    pygame.draw.polygon(surf, LIGHT_CYAN, main_wing_l, 1)
    pygame.draw.polygon(surf, LIGHT_CYAN, main_wing_r, 1)

    # 翼尖红色标记
    pygame.draw.circle(surf, RED, (5, 39), 3)
    pygame.draw.circle(surf, RED, (51, 39), 3)

    # ===== 驾驶舱（玻璃质感）=====
    cockpit_outer = [(25, 10), (31, 10), (33, 20), (29, 28), (23, 20)]
    pygame.draw.polygon(surf, (30, 80, 150), cockpit_outer)
    cockpit_inner = [(26, 12), (30, 12), (31, 19), (28, 25), (24, 19)]
    pygame.draw.polygon(surf, (100, 180, 230), cockpit_inner)
    # 驾驶舱反光
    pygame.draw.line(surf, (180, 220, 255), (26, 13), (28, 21), 1)

    # ===== 引擎（双发）=====
    # 左引擎喷口
    pygame.draw.ellipse(surf, (60, 60, 80), (20, 52, 8, 8))
    pygame.draw.ellipse(surf, ORANGE, (21, 54, 6, 4))
    # 右引擎喷口
    pygame.draw.ellipse(surf, (60, 60, 80), (30, 52, 8, 8))
    pygame.draw.ellipse(surf, ORANGE, (31, 54, 6, 4))

    # ===== 引擎火焰动画（静态绘制，运行时动态）=====
    # 左火焰
    flame_l = [(22, 57), (24, 70), (26, 57)]
    pygame.draw.polygon(surf, ORANGE, flame_l)
    flame_l_inner = [(23, 57), (24, 65), (25, 57)]
    pygame.draw.polygon(surf, YELLOW, flame_l_inner)
    # 右火焰
    flame_r = [(30, 57), (32, 70), (34, 57)]
    pygame.draw.polygon(surf, ORANGE, flame_r)
    flame_r_inner = [(31, 57), (32, 65), (33, 57)]
    pygame.draw.polygon(surf, YELLOW, flame_r_inner)

    # ===== 机头装饰线 =====
    pygame.draw.line(surf, GOLD, (28, 3), (28, 9), 2)

    # ===== 机体编号 ======
    return surf


def create_enemy_surface_v2(enemy_type='small'):
    """绘制精美敌机 V2 - 三种类型各具特色"""
    if enemy_type == 'small':
        # 小型侦察机 - 红色敏捷型
        surf = pygame.Surface((42, 46), pygame.SRCALPHA)
        cx, cy = 21, 22

        # 倒三角机身
        body = [
            (cx, 44),       # 机头(下)
            (cx + 10, 18),  # 右上
            (cx + 18, 6),   # 右翼尖
            (cx + 6, 16),   # 右内
            (cx + 4, 8),    # 右尾翼
            (cx, 3),        # 尾部顶
            (cx - 4, 8),    # 左尾翼
            (cx - 6, 16),   # 左内
            (cx - 18, 6),   # 左翼尖
            (cx - 10, 18),  # 左上
        ]
        pygame.draw.polygon(surf, RED, body)
        pygame.draw.polygon(surf, (255, 120, 120), body, 2)

        # 驾驶舱暗色
        pygame.draw.ellipse(surf, (60, 20, 20), (cx - 5, cy - 2, 10, 14))

        # 敌方标志
        pygame.draw.circle(surf, (255, 200, 0), (cx, int(cy + 4)), 5)
        pygame.draw.circle(surf, RED, (cx, int(cy + 4)), 3)

    elif enemy_type == 'medium':
        # 中型战斗机 - 紫色攻击型
        surf = pygame.Surface((52, 58), pygame.SRCALPHA)
        cx, cy = 26, 28

        body = [
            (cx, 56),
            (cx + 12, 24),
            (cx + 22, 6),
            (cx + 8, 20),
            (cx + 5, 10),
            (cx, 4),
            (cx - 5, 10),
            (cx - 8, 20),
            (cx - 22, 6),
            (cx - 12, 24),
        ]
        pygame.draw.polygon(surf, PURPLE, body)
        pygame.draw.polygon(surf, (220, 130, 255), body, 2)

        # 机身装甲线条
        pygame.draw.line(surf, MAGENTA, (cx, 10), (cx, 50), 2)

        # 双驾驶舱
        pygame.draw.ellipse(surf, (60, 20, 80), (cx - 7, cy, 14, 18))

        # 武器挂架
        pygame.draw.rect(surf, GRAY, (cx - 20, 14, 6, 4))
        pygame.draw.rect(surf, GRAY, (cx + 14, 14, 6, 4))

        # 标志
        pygame.draw.circle(surf, (255, 200, 0), (cx, int(cy + 6)), 6)
        pygame.draw.circle(surf, PURPLE, (cx, int(cy + 6)), 4)

    else:  # large
        # 大型轰炸机 - 棕色重型型
        surf = pygame.Surface((72, 78), pygame.SRCALPHA)
        cx, cy = 36, 38

        # 宽大机身
        body = [
            (cx, 76),
            (cx + 16, 32),
            (cx + 32, 8),
            (cx + 12, 26),
            (cx + 8, 12),
            (cx, 4),
            (cx - 8, 12),
            (cx - 12, 26),
            (cx - 32, 8),
            (cx - 16, 32),
        ]
        pygame.draw.polygon(surf, BROWN, body)
        pygame.draw.polygon(surf, (200, 140, 80), body, 2)

        # 装甲板纹理
        pygame.draw.line(surf, (120, 70, 30), (cx - 10, 16), (cx - 10, 64), 2)
        pygame.draw.line(surf, (120, 70, 30), (cx + 10, 16), (cx + 10, 64), 2)

        # 大型双驾驶舱
        pygame.draw.ellipse(surf, (50, 30, 20), (cx - 10, cy - 4, 20, 26))
        pygame.draw.ellipse(surf, (90, 60, 40), (cx - 7, cy, 14, 18))

        # 多武器挂点
        for ox in [-24, -8, 8, 24]:
            pygame.draw.rect(surf, DARK_RED, (cx + ox - 3, 20, 6, 8))
            pygame.draw.rect(surf, GRAY, (cx + ox - 2, 28, 4, 6))

        # 引擎
        pygame.draw.ellipse(surf, (50, 50, 60), (cx - 14, 64, 10, 10))
        pygame.draw.ellipse(surf, (50, 50, 60), (cx + 4, 64, 10, 10))

        # 标志
        pygame.draw.circle(surf, (255, 200, 0), (cx, int(cy + 8)), 8)
        pygame.draw.circle(surf, DARK_RED, (cx, int(cy + 8)), 5)

    return surf


def create_bullet_surface_v2(is_player=True):
    """绘制精美子弹 V2"""
    if is_player:
        # 玩家子弹 - 能量弹样式
        surf = pygame.Surface((8, 20), pygame.SRCALPHA)
        # 外发光
        pygame.draw.ellipse(surf, (0, 150, 255, 60), (-3, -3, 14, 26))
        # 弹头
        pygame.draw.ellipse(surf, CYAN, (0, 0, 8, 20))
        # 高光核心
        pygame.draw.ellipse(surf, WHITE, (2, 3, 4, 12))
        # 能量环
        pygame.draw.ellipse(surf, (100, 220, 255), (1, 1, 6, 18), 1)
    else:
        # 敌机子弹 - 红色激光
        surf = pygame.Surface((8, 16), pygame.SRCALPHA)
        # 发光
        pygame.draw.ellipse(surf, (255, 0, 0, 60), (-3, -2, 14, 20))
        # 弹体
        pygame.draw.ellipse(surf, RED, (0, 0, 8, 16))
        pygame.draw.ellipse(surf, ORANGE, (1, 2, 6, 10))
        # 核心
        pygame.draw.ellipse(surf, YELLOW, (3, 4, 2, 6))
    return surf


def create_asteroid_surface(size=1.0):
    """绘制陨石障碍物"""
    w, h = int(50 * size), int(50 * size)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx, cy = w // 2, h // 2

    # 不规则多边形模拟陨石
    points = []
    num_vertices = random.randint(7, 11)
    base_radius = min(w, h) // 2 - 2
    for i in range(num_vertices):
        angle = 2 * math.pi * i / num_vertices
        r = base_radius * random.uniform(0.7, 1.0)
        px = cx + int(r * math.cos(angle))
        py = cy + int(r * math.sin(angle))
        points.append((px, py))

    # 填充陨石颜色（灰褐色）
    pygame.draw.polygon(surf, (100, 85, 70), points)
    pygame.draw.polygon(surf, (140, 120, 100), points, 2)

    # 陨石坑纹理
    crater_color = (70, 58, 48)
    for _ in range(int(3 * size)):
        cr = random.randint(3, int(7 * size))
        cpos = (random.randint(cr + 2, w - cr - 2), random.randint(cr + 2, h - cr - 2))
        pygame.draw.circle(surf, crater_color, cpos, cr)

    return surf


def create_mine_surface():
    """绘制地雷障碍物"""
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    cx, cy = 16, 16

    # 地雷主体（球形）
    pygame.draw.circle(surf, (60, 60, 65), (cx, cy), 13)
    pygame.draw.circle(surf, (90, 90, 95), (cx, cy), 13, 2)

    # 高光
    pygame.draw.circle(surf, (130, 130, 140), (cx - 4, cy - 4), 4)

    # 危险标志（骷髅简化）
    pygame.draw.circle(surf, YELLOW, (cx, cy), 6)
    pygame.draw.circle(surf, (60, 60, 65), (cx, cy - 1), 2)
    pygame.draw.circle(surf, (60, 60, 65), (cx, cy + 3), 2)

    # 刺针
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = cx + int(12 * math.cos(rad))
        y1 = cy + int(12 * math.sin(rad))
        x2 = cx + int(16 * math.cos(rad))
        y2 = cy + int(16 * math.sin(rad))
        pygame.draw.line(surf, (80, 80, 85), (x1, y1), (x2, y2), 2)

    # 闪烁指示灯
    pygame.draw.circle(surf, RED, (cx, cy - 10), 3)

    return surf


def create_barrier_surface(width=80):
    """绘制移动障碍墙"""
    height = 24
    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    # 金属质感背景
    pygame.draw.rect(surf, (70, 75, 85), (0, 0, width, height), border_radius=4)
    pygame.draw.rect(surf, (100, 105, 115), (0, 0, width, height), 2, border_radius=4)

    # 警告条纹（黄黑相间）
    stripe_width = 16
    for i in range(0, width + stripe_width, stripe_width * 2):
        color = (200, 180, 0) if (i // stripe_width) % 2 == 0 else (40, 35, 30)
        end_x = min(i + stripe_width, width)
        if i < width:
            pygame.draw.rect(surf, color, (i, 2, end_x - i, height - 4))

    # 警告文字
    try:
        warn_text = font_tiny.render("!", True, RED)
        for j in range(0, width - 10, 25):
            surf.blit(warn_text, (j + 5, 4))
    except:
        pass

    return surf


def create_explosion_frames_v2():
    """创建增强爆炸动画帧"""
    frames = []
    for i in range(8):
        surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        radius = 6 + i * 5
        alpha = 255 - i * 30

        if i < 3:
            # 阶段1：橙红火球
            outer_c = (*ORANGE[:3], alpha)
            inner_c = (*YELLOW[:3], min(alpha + 40, 255))
            core_c = (*WHITE[:3], alpha)
        elif i < 6:
            # 阶段2：黄白扩散
            outer_c = (*YELLOW[:3], max(alpha - 20, 0))
            inner_c = (*WHITE[:3], min(alpha + 20, 255))
            core_c = (*CYAN[:3], max(alpha - 60, 0))
        else:
            # 阶段3：消散
            outer_c = (*GRAY[:3], max(alpha - 80, 0))
            inner_c = (*WHITE[:3], max(alpha - 40, 0))
            core_c = (0, 0, 0, 0)

        # 外圈
        if outer_c[3] > 0:
            pygame.draw.circle(surf, outer_c, (40, 40), radius)
        # 内圈
        r2 = radius - 4
        if r2 > 0 and inner_c[3] > 0:
            pygame.draw.circle(surf, inner_c, (40, 40), max(r2, 2))
        # 核心
        r3 = radius // 3
        if r3 > 0 and core_c[3] > 0:
            pygame.draw.circle(surf, core_c, (40, 40), max(r3, 1))

        # 火焰碎片
        for _ in range(3):
            frag_angle = random.uniform(0, 2 * math.pi)
            frag_dist = radius * random.uniform(0.8, 1.3)
            fx = int(40 + frag_dist * math.cos(frag_angle))
            fy = int(40 + frag_dist * math.sin(frag_angle))
            frag_r = random.randint(2, 5)
            fc = (*RED[:3], max(alpha - 50, 0)) if i < 4 else (*ORANGE[:3], max(alpha - 80, 0))
            if fc[3] > 0:
                pygame.draw.circle(surf, fc, (fx, fy), frag_r)

        frames.append(surf)
    return frames


def create_star_background_v2():
    """创建超丰富的星空背景 - 星球大战风格深空"""
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 深空渐变背景（更深的色调）
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(DARK_BLUE[0] * (1 - ratio * 0.2) + NAVY[0] * ratio * 0.2)
        g = int(DARK_BLUE[1] * (1 - ratio * 0.15) + NAVY[1] * ratio * 0.15)
        b = int(DARK_BLUE[2] * (1 - ratio * 0.1) + NAVY[2] * ratio * 0.1)
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    random.seed(42)
    # 更多星星
    for _ in range(300):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        r = random.choice([1, 1, 1, 1, 1, 2, 2, 3])
        brightness = random.randint(100, 255)
        tint = random.choice([(0, 0, 0), (20, 10, 0), (0, 10, 20),
                              (-10, 0, 10), (10, -5, -5), (0, 5, 15)])
        color = (
            max(0, min(255, brightness + tint[0])),
            max(0, min(255, brightness + tint[1])),
            max(0, min(255, brightness + tint[2])),
        )
        if r == 1:
            surf.set_at((x, y), color)
        else:
            pygame.draw.circle(surf, color, (x, y), r)

    # 更大更美的星云效果
    nebula_configs = [
        ((PURPLE[0]//2, PURPLE[1]//2, PURPLE[2]), 80),
        ((BLUE[0]//2, BLUE[1], BLUE[2]), 60),
        ((DARK_RED[0]//2+30, DARK_RED[1]//3, DARK_RED[2]//3), 55),
        ((CYAN[0]//3, CYAN[1]//3, CYAN[2]//2), 70),
    ]
    for nc, nr in nebula_configs:
        nx = random.randint(-20, SCREEN_WIDTH + 20)
        ny = random.randint(-20, SCREEN_HEIGHT + 20)
        nebula_surf = pygame.Surface((nr * 2, nr * 2), pygame.SRCALPHA)
        for rad in range(nr, 0, -2):
            alpha = int(6 * (nr - rad) / nr)
            pygame.draw.circle(nebula_surf, (*nc, alpha), (nr, nr), rad)
        surf.blit(nebula_surf, (nx - nr, ny - nr), special_flags=pygame.BLEND_RGBA_ADD)

    random.seed()
    return surf


# ================================================================
#                    ★★★ 行星绘制系统 ★
# ================================================================
class Planet:
    """背景中的装饰性行星"""

    PLANET_TYPES = [
        ((200, 150, 80), (180, 140, 60), True, (25, 45)),       # 土星型（带环）
        ((60, 120, 200), None, False, (18, 35)),                  # 地球型蓝色行星
        ((220, 80, 50), None, False, (14, 28)),                   # 火星型红色
        ((230, 210, 160), None, False, (12, 22)),                 # 金星型亮黄
        ((150, 130, 110), (130, 115, 95), True, (20, 38)),       # 木星型条纹
        ((100, 180, 140), None, False, (16, 30)),                  # 青绿色行星
        ((180, 140, 190), (160, 125, 170), True, (22, 36)),      # 紫色神秘行星
    ]

    def __init__(self):
        config = random.choice(self.PLANET_TYPES)
        self.base_color = config[0]
        self.ring_color = config[1]
        self.has_ring = config[2]
        size_min, size_max = config[3]
        self.radius = random.randint(size_min, size_max)

        self.x = random.randint(-self.radius * 2, SCREEN_WIDTH + self.radius * 2)
        self.y = random.randint(int(SCREEN_HEIGHT * 0.15), int(SCREEN_HEIGHT * 0.85))
        self.speed_y = random.uniform(0.12, 0.5)
        self.speed_x = random.uniform(-0.06, 0.06)
        self.tilt = random.uniform(15, 55)
        self._render()

    def _render(self):
        size = self.radius * 2 + 20 if self.has_ring else self.radius * 2 + 8
        self.surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx, cy = size // 2, size // 2

        # 大气层光晕
        for r_offset in range(6, 0, -1):
            atm_alpha = int(15 * (7 - r_offset) / 6)
            atm_r = self.radius + r_offset
            atm_c = tuple(min(255, c + 30) for c in self.base_color)
            pygame.draw.circle(self.surf, (*atm_c[:3], atm_alpha), (cx, cy), atm_r)

        # 行星主体
        pygame.draw.circle(self.surf, self.base_color, (cx, cy), self.radius)

        # 表面纹理/条纹
        stripe_count = random.randint(2, 5)
        for i in range(stripe_count):
            sy = cy - self.radius + int((i + 1) * self.radius * 2 / (stripe_count + 1))
            sw = int(math.sqrt(max(1, self.radius ** 2 - (sy - cy) ** 2)) * 2)
            if sw > 4:
                stripe_var = random.randint(-25, 25)
                stripe_color = tuple(max(0, min(255, c + stripe_var)) for c in self.base_color)
                stripe_surf = pygame.Surface((sw, 3), pygame.SRCALPHA)
                stripe_surf.fill((*stripe_color, 35))
                self.surf.blit(stripe_surf, (cx - sw // 2, sy))

        # 陨石坑
        n_craters = max(1, self.radius // 12)
        for _ in range(n_craters):
            cr = random.randint(2, max(3, self.radius // 5))
            cangle = random.uniform(0, 2 * math.pi)
            cdist = random.uniform(0.2, 0.75) * self.radius
            cx_off = int(cdist * math.cos(cangle))
            cy_off = int(cdist * math.sin(cangle))
            crater_dark = tuple(max(0, c - 35) for c in self.base_color)
            pygame.draw.circle(self.surf, crater_dark, (cx + cx_off, cy + cy_off), cr)

        # 高光
        hl_off = self.radius // 3
        hl_r = self.radius // 3
        hl_surf = pygame.Surface((hl_r * 2, hl_r * 2), pygame.SRCALPHA)
        for r in range(hl_r, 0, -1):
            alpha = int(25 * (hl_r - r + 1) / hl_r)
            pygame.draw.circle(hl_surf, (255, 255, 255, alpha), (hl_r, hl_r), r)
        self.surf.blit(hl_surf, (cx - hl_off - hl_r, cy - hl_off - hl_r),
                      special_flags=pygame.BLEND_RGBA_ADD)

        # 光环
        if self.has_ring and self.ring_color:
            tilt_rad = math.radians(self.tilt)
            ring_inner = int(self.radius * 1.3)
            ring_outer = int(self.radius * 1.9)
            ring_surf = pygame.Surface((ring_outer * 2 + 10, ring_outer + 20), pygame.SRCALPHA)
            rcx, rcy = ring_outer + 5, ring_outer // 2 + 5
            for rw in range(ring_outer, ring_inner, -1):
                ry = max(1, int(rw * abs(math.sin(tilt_rad))))
                ring_alpha = random.randint(80, 160)
                rc = self.ring_color if random.random() > 0.3 else \
                     tuple(min(255, c + 30) for c in self.ring_color)
                try:
                    pygame.draw.ellipse(ring_surf, (*rc[:3], ring_alpha),
                                       (rcx - rw, rcy - ry, rw * 2, ry * 2), 1)
                except:
                    pass
            self.surf.blit(ring_surf, (cx - rcx, cy - rcy))

        self.rect = self.surf.get_rect(center=(int(self.x), int(self.y)))

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        self.rect.center = (int(self.x), int(self.y))
        return self.rect.top < SCREEN_HEIGHT + self.radius * 2 and \
               self.rect.bottom > -self.radius * 2

    def draw(self, surface):
        surface.blit(self.surf, self.rect)


# ================================================================
#                    ★★★ 流星/彗星系统 ★
# ================================================================
class ShootingStar:
    """流星效果"""

    def __init__(self):
        side = random.choice(['top', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = -10
        elif side == 'left':
            self.x = -10
            self.y = random.randint(0, SCREEN_HEIGHT // 2)
        else:
            self.x = SCREEN_WIDTH + 10
            self.y = random.randint(0, SCREEN_HEIGHT // 2)

        angle = random.uniform(math.radians(50), math.radians(85))
        direction = random.choice([-1, 1])
        speed = random.uniform(8, 16)
        self.vx = speed * math.cos(angle) * direction
        self.vy = speed * math.sin(angle)
        self.length = random.randint(30, 70)
        self.thickness = random.randint(1, 3)
        self.color = random.choice([
            (255, 255, 255), (180, 220, 255), (255, 240, 200), (200, 200, 255),
        ])
        self.tail_particles = []
        self.alive = True
        self.life = 0
        self.max_life = random.randint(40, 90)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life += 1
        if self.life % 2 == 0:
            self.tail_particles.append({
                'x': self.x, 'y': self.y,
                'life': random.randint(15, 30),
                'size': max(1, self.thickness - 1),
            })
        for p in self.tail_particles[:]:
            p['life'] -= 1
            p['y'] += 0.3
            if p['life'] <= 0:
                self.tail_particles.remove(p)
        on_screen = (-50 < self.x < SCREEN_WIDTH + 50 and -50 < self.y < SCREEN_HEIGHT + 50)
        if not on_screen or self.life > self.max_life:
            self.alive = False
        return self.alive

    def draw(self, surface):
        # 预创建缓存surface（按尺寸缓存）
        max_t = max(self.thickness, 1)
        for p in self.tail_particles:
            alpha = int(200 * p['life'] / 30)
            ps = max(p['size'], 1)
            cache_key = ('tail', ps)
            if not hasattr(ShootingStar, '_cache'):
                ShootingStar._cache = {}
            if cache_key not in ShootingStar._cache:
                ShootingStar._cache[cache_key] = pygame.Surface((ps * 2 + 2, ps * 2 + 2), pygame.SRCALPHA)
            cs = ShootingStar._cache[cache_key]
            cs.fill((0, 0, 0, 0))
            pygame.draw.circle(cs, (*self.color[:3], min(alpha, 200)), (ps + 1, ps + 1), ps)
            surface.blit(cs, (int(p['x'] - ps - 1), int(p['y'] - ps - 1)))
        tail_x = self.x - self.vx * (self.length / max(abs(self.vy), 0.1) / 10)
        tail_y = self.y - self.vy * (self.length / max(abs(self.vy), 0.1) / 10)
        # 流星主体：直接用set_at绘制（避免每帧建Surface）
        for i in range(int(self.length)):
            t = i / self.length
            px = tail_x + (self.x - tail_x) * t
            py = tail_y + (self.y - tail_y) * t
            alpha = int(255 * t * t)
            thickness = max(1, int(max_t * t))
            pos_x, pos_y = int(px), int(py)
            if 0 <= pos_x < SCREEN_WIDTH and 0 <= pos_y < SCREEN_HEIGHT:
                color = (*self.color[:3], min(alpha, 255))
                # 用小圆代替Surface
                r = max(thickness // 2, 1)
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        if dx * dx + dy * dy <= r * r:
                            nx, ny = pos_x + dx, pos_y + dy
                            if 0 <= nx < SCREEN_WIDTH and 0 <= ny < SCREEN_HEIGHT:
                                try:
                                    surface.set_at((nx, ny), color)
                                except:
                                    pass


def create_powerup_surface_v2(ptype='power'):
    """绘制精美道具 V2 - 增强版含更多类型"""
    surf = pygame.Surface((36, 36), pygame.SRCALPHA)
    cx, cy = 18, 18

    colors = {
        'power': (PURPLE, MAGENTA, (220, 150, 255)),
        'heal': (GREEN, DARK_GREEN, (150, 255, 180)),
        'bomb': (ORANGE, RED, (255, 200, 100)),
        'shield': (CYAN, BLUE, (150, 230, 255)),
        'speed': (YELLOW, GOLD, (255, 255, 180)),
        'magnet': ((255, 80, 200), (200, 50, 150), (255, 150, 220)),   # 磁铁 - 粉红
        'freeze': ((100, 200, 255), (50, 150, 220), (180, 230, 255)),   # 冰冻 - 冰蓝
        'score': (GOLD, ORANGE, (255, 240, 160)),                         # 分数 - 金色
        'laser': ((255, 50, 50), (200, 30, 30), (255, 120, 100)),         # 激光炮 - 红色
    }
    main_color, edge_color, glow_color = colors.get(ptype, (WHITE, GRAY, LIGHT_GRAY))

    # 外发光
    for r in range(18, 10, -2):
        alpha = int(30 * (18 - r) / 8)
        glow_s = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_s, (*glow_color, alpha), (r + 2, r + 2), r)
        surf.blit(glow_s, (cx - r - 2, cy - r - 2))

    # 六边形主体
    hex_points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        hx = cx + int(14 * math.cos(angle))
        hy = cy + int(14 * math.sin(angle))
        hex_points.append((hx, hy))
    pygame.draw.polygon(surf, main_color, hex_points)
    pygame.draw.polygon(surf, WHITE, hex_points, 2)

    # 图标
    icons = {
        'power': 'P', 'heal': '+', 'bomb': 'B',
        'shield': 'S', 'speed': '>',
        'magnet': 'M', 'freeze': 'F', 'score': '$', 'laser': 'L',
    }
    icon_text = font_small.render(icons.get(ptype, '?'), True, WHITE)
    icon_rect = icon_text.get_rect(center=(cx, cy))
    surf.blit(icon_text, icon_rect)

    return surf


# ======================== 游戏资源实例化 ========================
player_img = create_player_surface_v2()
enemy_imgs = {
    'small': create_enemy_surface_v2('small'),
    'medium': create_enemy_surface_v2('medium'),
    'large': create_enemy_surface_v2('large'),
}
player_bullet_img = create_bullet_surface_v2(True)
enemy_bullet_img = create_bullet_surface_v2(False)
explosion_frames = create_explosion_frames_v2()
bg_image = create_star_background_v2()

# 预生成一些陨石变体
asteroid_cache = [create_asteroid_surface(random.uniform(0.7, 1.3)) for _ in range(8)]
mine_img = create_mine_surface()
barrier_img = create_barrier_surface(90)

powerup_imgs = {
    'power': create_powerup_surface_v2('power'),
    'heal': create_powerup_surface_v2('heal'),
    'bomb': create_powerup_surface_v2('bomb'),
    'shield': create_powerup_surface_v2('shield'),
    'speed': create_powerup_surface_v2('speed'),
    'magnet': create_powerup_surface_v2('magnet'),
    'freeze': create_powerup_surface_v2('freeze'),
    'score': create_powerup_surface_v2('score'),
    'laser': create_powerup_surface_v2('laser'),
}

# ======================== 音效合成 ========================
def create_sound(frequency=440, duration=0.1):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = bytes([int(128 + 50 * math.sin(2 * math.pi * frequency * t / sample_rate))
                 for t in range(n_samples)])
    sound = pygame.mixer.Sound(buffer=buf)
    sound.set_volume(0.12)
    return sound

try:
    shoot_sound = create_sound(800, 0.05)
    explosion_sound = create_sound(200, 0.15)
    powerup_sound = create_sound(1200, 0.1)
    hit_sound = create_sound(300, 0.08)
except Exception:
    shoot_sound = None
    explosion_sound = None
    powerup_sound = None
    hit_sound = None





# BGM已移除（程序化合成导致卡顿），仅保留射击/爆炸等短音效


# ================================================================
#                        ★★★ 粒子特效系统 ★
# ================================================================
class Particle:
    # 预创建粒子表面缓存（避免每帧新建Surface导致内存泄漏）
    _surf_cache = {}

    @classmethod
    def _get_cached_surf(cls, size):
        """获取或创建缓存的粒子表面"""
        if size not in cls._surf_cache:
            s = size * 2 + 4
            cls._surf_cache[size] = pygame.Surface((s, s), pygame.SRCALPHA)
        return cls._surf_cache[size], size + 2

    def __init__(self, x, y, color=None, speed_mult=1.0):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4) * speed_mult
        self.vy = random.uniform(-4, 4) * speed_mult
        self.life = random.randint(18, 35)
        self.max_life = self.life
        self.color = color or random.choice([YELLOW, ORANGE, RED, WHITE, CYAN])
        self.size = random.randint(2, 6)
        self.gravity = 0.12

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98  # 阻力
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * self.life / self.max_life)
        cached_surf, center = self._get_cached_surf(self.size)
        cached_surf.fill((0, 0, 0, 0))
        color_with_alpha = (*self.color[:3], alpha)
        pygame.draw.circle(cached_surf, color_with_alpha, (center, center), self.size)
        surface.blit(cached_surf, (int(self.x - center), int(self.y - center)))


class TrailParticle:
    """拖尾粒子 - 用于飞机尾迹"""
    # 预创建表面缓存
    _surf_cache = {}

    @classmethod
    def _get_cached_surf(cls, size):
        if size not in cls._surf_cache:
            cls._surf_cache[size] = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        return cls._surf_cache[size]

    def __init__(self, x, y, color=CYAN):
        self.x = x
        self.y = y
        self.life = random.randint(10, 20)
        self.max_life = self.life
        self.color = color
        self.size = random.randint(2, 4)

    def update(self):
        self.y += 1.5
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = int(120 * self.life / self.max_life)
        cached_surf = self._get_cached_surf(self.size)
        cached_surf.fill((0, 0, 0, 0))
        pygame.draw.circle(cached_surf, (*self.color[:3], alpha), (self.size, self.size), self.size)
        surface.blit(cached_surf, (int(self.x - self.size), int(self.y - self.size)))


# ================================================================
#                          ★★★ 星空背景 ★
# ================================================================
class StarField:
    """增强版星空背景 - 含行星和流星"""

    def __init__(self):
        self.stars = []
        for _ in range(120):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(1.5, 5),
                'size': random.choice([1, 1, 1, 2, 2]),
                'brightness': random.randint(140, 255),
                'color_offset': random.choice([(0, 0, 0), (20, 10, 0), (0, 10, 20), (-10, 0, 10)]),
                'twinkle_phase': random.uniform(0, 6.28),
                'twinkle_speed': random.uniform(0.03, 0.12),
            })

        # 背景行星（2-4颗缓慢移动）
        self.planets = [Planet() for _ in range(random.randint(2, 4))]

        # 流星
        self.shooting_stars = []
        self.shooting_star_timer = 0
        self.next_shooting_star = random.randint(120, 350)

    def update(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
            star['twinkle_phase'] += star['twinkle_speed']

        self.planets = [p for p in self.planets if p.update()]
        if len(self.planets) < 2 and random.random() < 0.002:
            self.planets.append(Planet())

        self.shooting_star_timer += 1
        if self.shooting_star_timer >= self.next_shooting_star:
            self.shooting_stars.append(ShootingStar())
            self.shooting_star_timer = 0
            self.next_shooting_star = random.randint(180, 450)
        self.shooting_stars = [ss for ss in self.shooting_stars if ss.update()]

    def draw(self, surface):
        surface.blit(bg_image, (0, 0))
        for star in self.stars:
            base_b = star['brightness']
            co = star['color_offset']
            twinkle = int(20 * math.sin(star['twinkle_phase']))
            brightness = max(80, min(255, base_b + twinkle))
            color = (
                max(0, min(255, brightness + co[0])),
                max(0, min(255, brightness + co[1])),
                max(0, min(255, brightness + co[2])),
            )
            pos = (int(star['x']), int(star['y']))
            if star['size'] == 1:
                surface.set_at(pos, color)
            else:
                pygame.draw.circle(surface, color, pos, star['size'])

        # 行星（按大小排序，小的在前营造深度感）
        for planet in sorted(self.planets, key=lambda p: p.radius):
            planet.draw(surface)

        # 流星（最上层）
        for ss in self.shooting_stars:
            ss.draw(surface)


# ================================================================
#                           ★★★ 玩家类 ★
# ================================================================
class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 40
        self.speed = 6
        self.hp = 5
        self.max_hp = 5
        self.fire_rate = 10
        self.fire_timer = 0
        self.power_level = 1
        self.invincible = 0
        self.alive = True
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.engine_flicker = 0  # 引擎火焰闪烁帧
        # 新增：磁铁和冰冻状态
        self.magnet_active = False
        self.magnet_range = 150
        self.freeze_timer = 0  # 冰冻剩余帧数

    def update(self, keys):
        if not self.alive:
            return

        current_speed = self.speed * (1.5 if self.speed_boost else 1.0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += current_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= current_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += current_speed

        self.rect.clamp_ip(screen.get_rect())

        if self.invincible > 0:
            self.invincible -= 1

        # 护盾计时
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

        # 加速计时
        if self.speed_boost:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost = False

        # 磁铁计时
        if self.magnet_active:
            if not hasattr(self, 'magnet_timer') or self.magnet_timer <= 0:
                self.magnet_active = False
            else:
                self.magnet_timer -= 1

        if self.fire_timer > 0:
            self.fire_timer -= 1

        self.engine_flicker = (self.engine_flicker + 1) % 4

    def shoot(self):
        if not self.alive or self.fire_timer > 0:
            return []
        self.fire_timer = max(self.fire_rate - self.power_level, 4)

        bullets = []
        center_x = self.rect.centerx

        if self.power_level == 1:
            bullets.append(Bullet(center_x - 4, self.rect.top, True))
        elif self.power_level == 2:
            bullets.append(Bullet(center_x - 14, self.rect.top + 5, True))
            bullets.append(Bullet(center_x + 6, self.rect.top + 5, True))
        elif self.power_level == 3:
            bullets.append(Bullet(center_x - 4, self.rect.top, True))
            bullets.append(Bullet(center_x - 24, self.rect.top + 10, True, -1))
            bullets.append(Bullet(center_x + 16, self.rect.top + 10, True, 1))
        elif self.power_level >= 4:
            bullets.append(Bullet(center_x - 4, self.rect.top, True))
            bullets.append(Bullet(center_x - 18, self.rect.top + 6, True, -1))
            bullets.append(Bullet(center_x + 10, self.rect.top + 6, True, 1))
            bullets.append(Bullet(center_x - 28, self.rect.top + 14, True, -2))
            bullets.append(Bullet(center_x + 20, self.rect.top + 14, True, 2))

        if shoot_sound:
            try: shoot_sound.play()
            except: pass
        return bullets

    def hit(self):
        if self.invincible > 0:
            return False
        if self.shield_active:
            self.shield_active = False
            self.invincible = 30
            return False
        self.hp -= 1
        self.invincible = 90
        self.power_level = max(1, self.power_level - 1)
        if self.hp <= 0:
            self.alive = False
        return True

    def draw(self, surface):
        if not self.alive:
            return
        if self.invincible > 0 and (self.invincible // 5) % 2 == 0:
            return

        surface.blit(self.image, self.rect)

        # 护盾效果（预缓存Surface）
        if self.shield_active:
            sw, sh = self.rect.width + 20, self.rect.height + 20
            if not hasattr(Player, '_shield_surf') or Player._shield_surf.get_size() != (sw, sh):
                Player._shield_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
            shield_surf = Player._shield_surf
            shield_surf.fill((0, 0, 0, 0))
            shield_alpha = 100 + int(50 * math.sin(pygame.time.get_ticks() * 0.01))
            pygame.draw.ellipse(shield_surf, (*CYAN[:3], shield_alpha),
                              shield_surf.get_rect(), 3)
            surface.blit(shield_surf,
                        (self.rect.centerx - self.rect.width // 2 - 10,
                         self.rect.centery - self.rect.height // 2 - 10))


# ================================================================
#                           ★★★ 子弹类 ★
# ================================================================
class Bullet:
    def __init__(self, x, y, is_player=True, direction=0):
        self.is_player = is_player
        self.image = player_bullet_img if is_player else enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.speed = -14 if is_player else 5.5
        self.direction = direction
        self.dx = direction * 2.5
        self.active = True

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.dx
        if not (-30 <= self.rect.top <= SCREEN_HEIGHT + 30 and
                -30 <= self.rect.right <= SCREEN_WIDTH + 30):
            self.active = False
        return self.active

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ================================================================
#                           ★★★ 敌机类 ★
# ================================================================
class Enemy:
    TYPES = {
        'small': {'hp': 1, 'score': 100, 'speed': [3, 5.5], 'shoot_chance': 0.004},
        'medium': {'hp': 4, 'score': 350, 'speed': [2, 4], 'shoot_chance': 0.01},
        'large': {'hp': 12, 'score': 900, 'speed': [1, 2.5], 'shoot_chance': 0.02},
    }

    def __init__(self, enemy_type='small'):
        self.type = enemy_type
        info = self.TYPES[enemy_type]
        self.image = enemy_imgs[enemy_type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, SCREEN_WIDTH - self.rect.width - 20)
        self.rect.y = -self.rect.height - random.randint(0, 60)
        self.hp = info['hp']
        self.max_hp = info['hp']
        self.score = info['score']
        self.speed_y = random.uniform(info['speed'][0], info['speed'][1])
        self.speed_x = random.uniform(-0.8, 0.8)
        self.shoot_chance = info['shoot_chance']
        self.move_pattern = random.choice(['straight', 'sine', 'zigzag', 'dive'])
        self.frame = 0
        self.alive = True
        self.hit_flash = 0  # 受击闪白

    def update(self, frozen=False):
        """frozen参数：是否被冰冻（冰冻时速度降为0.25倍）"""
        if not self.alive:
            return False
        self.frame += 1

        if self.hit_flash > 0:
            self.hit_flash -= 1

        speed_mult = 0.25 if frozen else 1.0

        if self.move_pattern == 'straight':
            self.rect.y += self.speed_y * speed_mult
        elif self.move_pattern == 'sine':
            self.rect.y += self.speed_y * speed_mult
            self.rect.x += math.sin(self.frame * 0.05) * 2.5 * speed_mult
        elif self.move_pattern == 'zigzag':
            self.rect.y += self.speed_y * speed_mult
            if self.frame % 50 < 25:
                self.rect.x += 1.8 * speed_mult
            else:
                self.rect.x -= 1.8 * speed_mult
        elif self.move_pattern == 'dive':
            # 俯冲攻击模式
            if self.frame < 60:
                self.rect.y += self.speed_y * 0.6 * speed_mult
            elif self.frame < 100:
                self.rect.y += self.speed_y * 2.5 * speed_mult
                self.rect.x += math.copysign(1.5 * speed_mult, screen.get_rect().centerx - self.rect.centerx)
            else:
                self.rect.y += self.speed_y * speed_mult

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
            self.rect.clamp_ip(screen.get_rect())

        return self.rect.top <= SCREEN_HEIGHT + 50

    def shoot(self):
        if random.random() < self.shoot_chance:
            return Bullet(self.rect.centerx - 4, self.rect.bottom, is_player=False)
        return None

    def hit(self, damage=1):
        self.hp -= damage
        self.hit_flash = 6
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw_hp_bar(self, surface):
        bar_width = self.rect.width - 6
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (40, 40, 40),
                        (self.rect.left + 3, self.rect.top - 10, bar_width, 6))
        color = GREEN if hp_ratio > 0.5 else YELLOW if hp_ratio > 0.25 else RED
        pygame.draw.rect(surface, color,
                        (self.rect.left + 3, self.rect.top - 10,
                         int(bar_width * hp_ratio), 6))
        pygame.draw.rect(surface, WHITE,
                        (self.rect.left + 3, self.rect.top - 10, bar_width, 6), 1)

    def draw(self, surface):
        if not self.alive:
            return
        # 受击闪白效果
        if self.hit_flash > 0:
            flash_surf = self.image.copy()
            flash_surf.fill(WHITE, special_flags=pygame.BLEND_RGB_ADD)
            surface.blit(flash_surf, self.rect)
        else:
            surface.blit(self.image, self.rect)
        self.draw_hp_bar(surface)


# ================================================================
#                       ★★★ 障碍物系统 ★
# ================================================================
class Obstacle:
    """障碍物基类"""
    OBSTACLE_TYPES = ['asteroid', 'mine', 'barrier']

    def __init__(self, obs_type=None):
        self.type = obs_type or random.choice(self.OBSTACLE_TYPES)
        self.alive = True
        self.frame = 0

        if self.type == 'asteroid':
            self._init_asteroid()
        elif self.type == 'mine':
            self._init_mine()
        elif self.type == 'barrier':
            self._init_barrier()

    def _init_asteroid(self):
        """陨石 - 缓慢飘落的大型障碍"""
        img = random.choice(asteroid_cache)
        self.image = img
        self.rect = img.get_rect()
        self.rect.x = random.randint(10, SCREEN_WIDTH - self.rect.width - 10)
        self.rect.y = -self.rect.height - random.randint(0, 100)
        self.speed_y = random.uniform(1.5, 3)
        self.speed_x = random.uniform(-1, 1)
        self.rotation_speed = random.uniform(-2, 2)
        self.rotation = 0
        self.damage = 2
        self.score = 50

    def _init_mine(self):
        """地雷 - 静止或缓慢移动的危险区域"""
        self.image = mine_img
        self.rect = mine_img.get_rect()
        self.rect.x = random.randint(30, SCREEN_WIDTH - self.rect.width - 30)
        self.rect.y = -self.rect.height - random.randint(0, 80)
        self.speed_y = random.uniform(1, 2)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.blink_phase = random.randint(0, 60)
        self.damage = 3
        self.score = 80

    def _init_barrier(self):
        """障碍墙 - 横向移动的墙壁"""
        self.image = barrier_img
        self.rect = barrier_img.get_rect()
        self.direction = random.choice([-1, 1])  # 从左边或右边进入
        if self.direction == 1:
            self.rect.right = 0
        else:
            self.rect.left = SCREEN_WIDTH
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 200)
        self.speed_x = 3 * self.direction
        self.speed_y = 0.3
        self.damage = 1
        self.score = 30

    def update(self):
        if not self.alive:
            return False
        self.frame += 1

        if self.type == 'asteroid':
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x
            self.rotation += self.rotation_speed
        elif self.type == 'mine':
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x
            self.blink_phase += 1
        elif self.type == 'barrier':
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            # 墙壁反弹
            if self.rect.top < 60 or self.rect.bottom > SCREEN_HEIGHT - 60:
                self.speed_y *= -1

        # 边界检查
        if self.type != 'barrier':
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.speed_x *= -1
                self.rect.clamp_ip(screen.get_rect())

        # 是否还在屏幕内
        if self.type == 'barrier':
            return -50 <= self.rect.left <= SCREEN_WIDTH + 50
        return self.rect.top <= SCREEN_HEIGHT + 50

    def draw(self, surface):
        if not self.alive:
            return

        if self.type == 'asteroid':
            # 旋转效果
            rotated = pygame.transform.rotate(self.image, self.rotation)
            rot_rect = rotated.get_rect(center=self.rect.center)
            surface.blit(rotated, rot_rect)
        elif self.type == 'mine':
            surface.blit(self.image, self.rect)
            # 闪烁红灯 - 使用预创建的缓存surface
            if (self.blink_phase // 15) % 2 == 0:
                if not hasattr(Obstacle, '_blink_surf'):
                    Obstacle._blink_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
                bs = Obstacle._blink_surf
                bs.fill((0, 0, 0, 0))
                pygame.draw.circle(bs, (255, 0, 0, 200), (4, 4), 4)
                surface.blit(bs, (self.rect.centerx - 4, self.rect.centery - 12))
        elif self.type == 'barrier':
            surface.blit(self.image, self.rect)


# ================================================================
#                           ★★★ 道具类 ★
# ================================================================
class PowerUp:
    TYPES = ['power', 'heal', 'bomb', 'shield', 'speed',
             'magnet', 'freeze', 'score', 'laser']

    # 权重：出现概率
    TYPE_WEIGHTS = [20, 18, 12, 14, 15, 10, 8, 8, 5]

    def __init__(self, x, y, ptype=None):
        if ptype is None:
            # 加权随机选择道具类型
            total = sum(self.TYPE_WEIGHTS)
            r = random.randint(1, total)
            cumulative = 0
            for i, w in enumerate(self.TYPE_WEIGHTS):
                cumulative += w
                if r <= cumulative:
                    ptype = self.TYPES[i]
                    break

        self.type = ptype
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame = 0
        self.alive = True
        self.float_offset = 0

    def update(self):
        self.frame += 1
        self.float_offset = math.sin(self.frame * 0.1) * 3
        self.rect.y += 1.8
        actual_rect = self.rect.copy()
        actual_rect.y += self.float_offset
        return actual_rect.bottom < SCREEN_HEIGHT + 20

    def apply(self, player):
        if self.type == 'power':
            player.power_level = min(player.power_level + 1, 5)
            player.fire_rate = max(player.fire_rate - 2, 4)
        elif self.type == 'heal':
            player.hp = min(player.hp + 1, player.max_hp)
        elif self.type == 'bomb':
            pass  # 由Game处理
        elif self.type == 'shield':
            player.shield_active = True
            player.shield_timer = 480
        elif self.type == 'speed':
            player.speed_boost = True
            player.speed_boost_timer = 360
        elif self.type == 'magnet':
            player.magnet_active = True
            player.magnet_range = 180
            player.magnet_timer = 480  # 8秒磁力
        elif self.type == 'freeze':
            game.freeze_timer = 420  # 7秒全屏冰冻
            game.show_notification('❄ 敌机冻结!')
        elif self.type == 'score':
            # 直接加500分
            game.score += 500
        elif self.type == 'laser':
            # 激光炮：火力提升到最高级
            player.power_level = 5
            player.fire_rate = 4

        if powerup_sound:
            try: powerup_sound.play()
            except: pass

    def draw(self, surface):
        # 浮动效果
        float_rect = self.rect.copy()
        float_rect.y += self.float_offset

        # 发光脉冲 - 使用预创建的缓存surface（修复内存泄漏）
        pulse = abs(math.sin(self.frame * 0.08))
        glow_size = int(20 + pulse * 8)
        if not hasattr(PowerUp, '_glow_cache'):
            PowerUp._glow_cache = {}
        glow_key = glow_size
        if glow_key not in PowerUp._glow_cache:
            PowerUp._glow_cache[glow_key] = pygame.Surface((glow_size * 2 + 10, glow_size * 2 + 10), pygame.SRCALPHA)
        glow_surf = PowerUp._glow_cache[glow_key]
        glow_surf.fill((0, 0, 0, 0))
        glow_colors = {
            'power': PURPLE, 'heal': GREEN, 'bomb': ORANGE,
            'shield': CYAN, 'speed': YELLOW,
            'magnet': (255, 80, 200), 'freeze': (100, 200, 255),
            'score': GOLD, 'laser': RED,
        }
        gc = glow_colors.get(self.type, WHITE)
        pygame.draw.circle(glow_surf, (*gc[:3], int(40 + pulse * 30)),
                          (glow_size + 5, glow_size + 5), glow_size)
        surface.blit(glow_surf,
                    (float_rect.centerx - glow_size - 5,
                     float_rect.centery - glow_size - 5))
        surface.blit(self.image, float_rect)


# ================================================================
#                         ★★★ 爆炸特效 ★
# ================================================================
class Explosion:
    def __init__(self, x, y, size=1.0, color_override=None):
        self.x = x
        self.y = y
        self.frame = 0
        self.max_frame = len(explosion_frames)
        self.size = size
        self.alive = True
        self.color_override = color_override
        # 粒子数量随尺寸增加
        n_particles = int(15 * size)
        self.particles = [Particle(x, y, color=color_override, speed_mult=size * 0.8)
                         for _ in range(n_particles)]

        # 预缩放爆炸帧（避免每帧transform.scale创建新Surface）
        if size != 1.0:
            self._scaled_frames = []
            for ef in explosion_frames:
                new_size = (int(ef.get_width() * size), int(ef.get_height() * size))
                self._scaled_frames.append(pygame.transform.scale(ef, new_size))
        else:
            self._scaled_frames = explosion_frames

    def update(self):
        self.frame += 1
        if self.frame >= self.max_frame:
            self.alive = False
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface):
        if self.frame < self.max_frame:
            frame = self._scaled_frames[min(self.frame, self.max_frame - 1)]
            rect = frame.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(frame, rect)

        for p in self.particles:
            p.draw(surface)


# ================================================================
#                      ★★★ 飞行距离计算器 ★
# ================================================================
class DistanceTracker:
    """飞行距离追踪器"""
    def __init__(self):
        self.distance = 0.0          # 总距离（米）
        self.base_speed = 100         # 基础速度 米/秒
        self.last_update = pygame.time.get_ticks()

    def reset(self):
        self.distance = 0.0
        self.last_update = pygame.time.get_ticks()

    def update(self, level, speed_boost=False):
        """根据等级和加速状态更新距离"""
        now = pygame.time.get_ticks()
        dt = (now - self.last_update) / 1000.0  # 秒
        self.last_update = now

        # 速度 = 基础速度 × (1 + 等级×0.15) × 加速倍率
        multiplier = 1.0 + level * 0.15
        if speed_boost:
            multiplier *= 1.5
        self.distance += self.base_speed * multiplier * dt

    @property
    def display_distance(self):
        """格式化显示距离"""
        if self.distance >= 10000:
            return f"{self.distance / 1000:.2f} km"
        elif self.distance >= 1000:
            return f"{self.distance / 1000:.2f} km"
        else:
            return f"{int(self.distance)} m"


# ================================================================
#                      ★★★ 排行榜系统 ★
# ================================================================
class Leaderboard:
    """排行榜管理 - JSON文件持久化"""

    def __init__(self, filepath=LEADERBOARD_FILE):
        self.filepath = filepath
        self.entries = []  # list of dict: {name, score, distance, kills, level, date}
        self.load()

    def load(self):
        """从文件加载排行榜"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.entries = data.get('entries', [])
            except (json.JSONDecodeError, IOError):
                self.entries = []

    def save(self):
        """保存排行榜到文件"""
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump({'entries': self.entries}, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"[排行榜] 保存失败: {e}")

    def add_entry(self, name, score, distance, kills, level):
        """添加新记录"""
        entry = {
            'name': name[:10],
            'score': int(score),
            'distance': round(distance, 1),
            'kills': kills,
            'level': level,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.entries.append(entry)
        # 按分数降序排列，保留Top 10
        self.entries.sort(key=lambda x: x['score'], reverse=True)
        self.entries = self.entries[:10]
        self.save()
        rank = next((i + 1 for i, e in enumerate(self.entries) if e['score'] == entry['score']), len(self.entries))
        return rank

    def get_top_n(self, n=10):
        """获取前N名"""
        return self.entries[:n]

    def is_high_score(self, score):
        """检查是否进入排行榜"""
        if len(self.entries) < 10:
            return True
        return score > self.entries[-1]['score']

    @property
    def top_score(self):
        return self.entries[0]['score'] if self.entries else 0


# ================================================================
#                          ★★★ 主游戏类 ★
# ================================================================
class Game:
    def __init__(self):
        self.state = 'menu'  # menu, playing, paused, gameover, leaderboard, enter_name
        self.player = Player()
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.particles_list = []
        self.trail_particles = []  # 飞机尾迹
        self.powerups = []
        self.obstacles = []
        self.star_field = StarField()
        self.leaderboard = Leaderboard()

        self.score = 0
        self.high_score = self.leaderboard.top_score
        self.level = 1
        self.enemy_spawn_timer = 0
        self.obstacle_spawn_timer = 0
        self.enemies_killed = 0
        self.combo = 0
        self.combo_timer = 0
        self.combo_max = 0
        self.screen_shake = 0
        self.bombs_available = 2
        self.freeze_timer = 0  # 全屏冰冻计时器

        # 飞行距离
        self.distance_tracker = DistanceTracker()

        # 游戏时间
        self.game_time = 0

        # 待输入的名字
        self.input_name = "PILOT"
        self.name_cursor_visible = True
        self.name_cursor_timer = 0
        self.current_rank = 0

        # UI 动画参数
        self.menu_bg_stars_offset = 0
        self.notification_queue = []  # 屏幕通知队列
        self.level_up_display_timer = 0  # 升级提示显示

        # 菜单按钮区域（用于鼠标点击检测）
        self.menu_btn_start = pygame.Rect(0, 0, 1, 1)
        self.menu_btn_leaderboard = pygame.Rect(0, 0, 1, 1)

    def reset(self):
        """重置游戏到初始状态"""
        old_high = self.high_score
        self.__init__()
        self.high_score = max(old_high, self.leaderboard.top_score)
        self.state = 'playing'
        self.distance_tracker.reset()

    def spawn_enemy(self):
        self.enemy_spawn_timer -= 1
        if self.enemy_spawn_timer <= 0:
            rand = random.random()
            if self.level < 2:
                etype = 'small'
            elif self.level < 4:
                etype = 'small' if rand < 0.7 else 'medium'
            elif self.level < 6:
                etype = 'small' if rand < 0.5 else ('medium' if rand < 0.85 else 'large')
            else:
                weights = [0.35, 0.40, 0.25]
                cumulative = sum(weights[:3])
                if rand < weights[0] / cumulative:
                    etype = 'small'
                elif rand < (weights[0] + weights[1]) / cumulative:
                    etype = 'medium'
                else:
                    etype = 'large'

            self.enemies.append(Enemy(etype))
            base_interval = max(55 - self.level * 3, 18)
            self.enemy_spawn_timer = base_interval + random.randint(0, 25)

    def spawn_obstacle(self):
        """生成障碍物"""
        self.obstacle_spawn_timer -= 1
        if self.obstacle_spawn_timer <= 0:
            # 障碍物出现概率随等级增加
            chance = min(0.03 + self.level * 0.005, 0.08)
            if random.random() < chance:
                self.obstacles.append(Obstacle())
            # 间隔也随等级缩短
            interval = max(150 - self.level * 8, 60)
            self.obstacle_spawn_timer = interval + random.randint(0, 50)

    def check_collisions(self):
        """碰撞检测 - 修复版"""
        # ========== 玩家子弹 vs 敌机 ==========
        for bullet in self.player_bullets[:]:
            if not bullet.active:
                continue
            for enemy in self.enemies[:]:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    bullet.active = False
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if enemy.hit():
                        combo_bonus = 1 + self.combo * 0.15
                        self.score += int(enemy.score * combo_bonus)
                        self.enemies_killed += 1
                        self.combo += 1
                        self.combo_timer = 90
                        if self.combo > self.combo_max:
                            self.combo_max = self.combo
                        self.explosions.append(
                            Explosion(enemy.rect.centerx, enemy.rect.centery,
                                     1.2 if enemy.type != 'large' else 1.8))
                        self.screen_shake = 4
                        # 掉落道具 - 提高掉率
                        if random.random() < 0.20:
                            self.powerups.append(
                                PowerUp(enemy.rect.centerx, enemy.rect.centery))
                        if explosion_sound:
                            try: explosion_sound.play()
                            except: pass
                    break

        # ========== 玩家子弹 vs 障碍物 ==========
        for bullet in self.player_bullets[:]:
            if not bullet.active:
                continue
            for obs in self.obstacles[:]:
                if obs.alive and bullet.rect.colliderect(obs.rect):
                    bullet.active = False
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    # 陨石可以被摧毁，地雷和墙不能
                    if obs.type == 'asteroid':
                        obs.alive = False
                        self.score += obs.score
                        self.explosions.append(
                            Explosion(obs.rect.centerx, obs.rect.centery, 1.3, BROWN))
                        self.screen_shake = 2
                        # 陨石爆炸产生碎片粒子
                        for _ in range(8):
                            self.particles_list.append(
                                Particle(obs.rect.centerx, obs.rect.centery,
                                       color=random.choice([BROWN, GRAY, ORANGE])))
                    break

        # ========== 敌机子弹 vs 玩家 ==========
        for bullet in self.enemy_bullets[:]:
            if bullet.rect.colliderect(self.player.rect) and self.player.alive:
                bullet.active = False
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                if self.player.hit():
                    self.explosions.append(
                        Explosion(self.player.rect.centerx, self.player.rect.centery, 0.8))
                    self.screen_shake = 5
                    self.combo = 0
                    if hit_sound:
                        try: hit_sound.play()
                        except: pass

        # ========== 敌机 vs 玩家（碰撞）==========
        for enemy in self.enemies[:]:
            if enemy.alive and enemy.rect.colliderect(self.player.rect) and self.player.alive:
                if self.player.hit():
                    enemy.alive = False
                    self.explosions.append(
                        Explosion(enemy.rect.centerx, enemy.rect.centery, 1.2))
                    self.explosions.append(
                        Explosion(self.player.rect.centerx, self.player.rect.centery, 0.8))
                    self.screen_shake = 6
                    self.combo = 0

        # ========== 障碍物 vs 玩家 ==========
        for obs in self.obstacles[:]:
            if obs.alive and obs.rect.colliderect(self.player.rect) and self.player.alive:
                damage = obs.damage
                for _ in range(damage):
                    if self.player.alive and self.player.hit():
                        pass
                if obs.type != 'barrier':
                    # 非墙壁障碍物碰撞后消失
                    obs.alive = False
                    self.explosions.append(
                        Explosion(obs.rect.centerx, obs.rect.centery, 1.0, ORANGE))
                self.screen_shake = 4
                self.combo = 0

        # ========== 道具 vs 玩家 ==========
        for pu in self.powerups[:]:
            if pu.rect.colliderect(self.player.rect):
                pu.apply(self.player)
                if pu.type == 'bomb':
                    self.use_bomb()

                # 显示获得通知
                type_names = {
                    'power': '火力提升!',
                    'heal': '生命回复!',
                    'bomb': '炸弹!',
                    'shield': '护盾激活!',
                    'speed': '加速启动!',
                    'magnet': '磁铁吸力!',
                    'freeze': '冰冻减速!',
                    'score': '+500分!',
                    'laser': '激光炮!',
                }
                self.show_notification(type_names.get(pu.type, ''))

                if pu in self.powerups:
                    self.powerups.remove(pu)

    def use_bomb(self):
        """全屏炸弹"""
        for e in self.enemies:
            if e.alive:
                self.score += e.score // 2
                self.explosions.append(
                    Explosion(e.rect.centerx, e.rect.centery, 1.3))
        # 也清除障碍物中的陨石
        for o in self.obstacles:
            if o.alive and o.type == 'asteroid':
                o.alive = False
                self.score += o.score // 2
                self.explosions.append(
                    Explosion(o.rect.centerx, o.rect.centery, 1.0, BROWN))

        self.enemies.clear()
        self.obstacles = [o for o in self.obstacles if o.type != 'asteroid']
        self.enemy_bullets.clear()
        self.screen_shake = 8
        self.show_notification('💥 全屏清场!')
        if explosion_sound:
            try: explosion_sound.play()
            except: pass

    def show_notification(self, text):
        """显示屏幕中央通知"""
        self.notification_queue.append({
            'text': text,
            'timer': 90,  # 1.5秒显示
            'y_offset': 0,
        })

    def update_notifications(self):
        """更新通知队列"""
        for notif in self.notification_queue[:]:
            notif['timer'] -= 1
            notif['y_offset'] = max(0, (90 - notif['timer']) * 0.5)
            if notif['timer'] <= 0:
                self.notification_queue.remove(notif)

    def update_level(self):
        """根据击杀数升级"""
        new_level = 1 + self.enemies_killed // 12
        if new_level > self.level:
            self.level = min(new_level, 15)
            self.bombs_available += 1
            self.level_up_display_timer = 90  # 显示1.5秒升级信息
            self.show_notification(f'⬆ LEVEL {self.level}!')

    def update(self):
        if self.state != 'playing':
            return

        keys = pygame.key.get_pressed()
        self.game_time += 1

        # 更新星空
        self.star_field.update()

        # 更新玩家
        self.player.update(keys)

        # 飞机尾迹效果
        if self.player.alive and self.game_time % 3 == 0:
            self.trail_particles.append(
                TrailParticle(
                    self.player.rect.centerx + random.randint(-6, 6),
                    self.player.rect.bottom - 5,
                    color=ORANGE if self.player.engine_flicker < 2 else YELLOW))

        # 射击（按住空格持续发射）
        if keys[pygame.K_SPACE]:
            new_bullets = self.player.shoot()
            self.player_bullets.extend(new_bullets)

        # 更新子弹
        self.player_bullets = [b for b in self.player_bullets if b.update()]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.update()]
        # 清理不活跃的子弹
        self.player_bullets = [b for b in self.player_bullets if b.active]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.active]

        # 生成
        self.spawn_enemy()
        self.spawn_obstacle()

        # 更新敌机（传入冰冻状态）
        is_frozen = self.freeze_timer > 0
        for enemy in self.enemies:
            enemy.update(frozen=is_frozen)
            bullet = enemy.shoot()
            # 冰冻时降低射击概率
            if bullet and not is_frozen:
                self.enemy_bullets.append(bullet)
        self.enemies = [e for e in self.enemies if e.alive and e.rect.top <= SCREEN_HEIGHT + 50]

        # 更新障碍物
        self.obstacles = [o for o in self.obstacles if o.update() and o.alive]

        # 更新道具
        self.powerups = [p for p in self.powerups if p.update()]
        self.powerups = [p for p in self.powerups if p.alive]

        # 更新爆炸
        for ex in self.explosions[:]:
            ex.update()
            if not ex.alive:
                self.explosions.remove(ex)

        # 更新粒子（限制最大数量，防止内存爆炸）
        self.particles_list = [p for p in self.particles_list if p.update()]
        if len(self.particles_list) > 300:
            self.particles_list = self.particles_list[-300:]
        self.trail_particles = [p for p in self.trail_particles if p.update()]
        if len(self.trail_particles) > 150:
            self.trail_particles = self.trail_particles[-150:]

        # 屏幕震动衰减
        if self.screen_shake > 0:
            self.screen_shake -= 1

        # 连击计时
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo = 0

        # 升级提示计时
        if self.level_up_display_timer > 0:
            self.level_up_display_timer -= 1

        # 通知更新
        self.update_notifications()

        # 更新飞行距离
        self.distance_tracker.update(self.level, self.player.speed_boost)

        # 冰冻计时衰减
        if self.freeze_timer > 0:
            self.freeze_timer -= 1

        # 磁铁效果：自动吸引附近道具
        if hasattr(self.player, 'magnet_active') and self.player.magnet_active:
            magnet_range = getattr(self.player, 'magnet_range', 150)
            for pu in self.powerups:
                dx = self.player.rect.centerx - pu.rect.centerx
                dy = self.player.rect.centery - pu.rect.centery
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < magnet_range and dist > 5:
                    # 向玩家方向加速移动
                    pull_speed = 4
                    pu.rect.x += int(dx / dist * pull_speed)
                    pu.rect.y += int(dy / dist * pull_speed)

        # 碰撞检测
        self.check_collisions()

        # 升级检查
        self.update_level()

        # 最高分
        if self.score > self.high_score:
            self.high_score = int(self.score)

        # 游戏结束判断
        if not self.player.alive:
            self.state = 'enter_name'
            self.input_name = "PILOT"

    # ==================== HUD 绘制 ====================
    def draw_hud(self, surface):
        """绘制增强HUD界面"""

        # ===== 顶部信息栏背景（预创建，避免每帧重建）=====
        if not hasattr(Game, '_hud_bg'):
            Game._hud_bg = pygame.Surface((SCREEN_WIDTH, 72), pygame.SRCALPHA)
            Game._hud_bg.fill((0, 0, 0, 140))
        surface.blit(Game._hud_bg, (0, 0))

        # 底部分隔线
        pygame.draw.line(surface, CYAN, (0, 72), (SCREEN_WIDTH, 72), 2)

        # ===== 分数（左侧）=====
        score_label = font_tiny.render("SCORE", True, SILVER)
        surface.blit(score_label, (12, 4))
        score_val = font_medium.render(f"{int(self.score):,}", True, YELLOW)
        surface.blit(score_val, (10, 24))

        # ===== 飞行距离 =====
        dist_label = font_tiny.render("DISTANCE", True, SILVER)
        surface.blit(dist_label, (12, 52))
        dist_val = font_small.render(self.distance_tracker.display_distance, True, CYAN)
        surface.blit(dist_val, (95, 51))

        # ===== 等级（中间偏左）=====
        level_bg = pygame.Surface((70, 56), pygame.SRCALPHA)
        level_bg.fill((0, 50, 100, 150))
        level_bg_rect = level_bg.get_rect(topleft=(SCREEN_WIDTH // 2 - 100, 8))
        surface.blit(level_bg, level_bg_rect)
        pygame.draw.rect(surface, CYAN, level_bg_rect, 1, border_radius=4)

        lv_label = font_tiny.render("LV", True, SILVER)
        surface.blit(lv_label, (SCREEN_WIDTH // 2 - 92, 10))
        lv_val = font_large.render(str(self.level), True, GREEN)
        lv_rect = lv_val.get_rect(centerx=level_bg_rect.centerx, top=24)
        surface.blit(lv_val, lv_rect)

        # ===== 击杀数 =====
        kill_text = font_small.render(f"KILL:{self.enemies_killed}", True, WHITE)
        surface.blit(kill_text, (SCREEN_WIDTH // 2 - 20, 8))

        # ===== 生命值（右上角 - 精美心形）=====
        hp_start_x = SCREEN_WIDTH - 35
        for i in range(self.player.max_hp):
            color = RED if i < self.player.hp else (60, 60, 70)
            px = hp_start_x - i * 30
            py = 10
            # 心形
            pygame.draw.circle(surface, color, (px - 7, py + 5), 8)
            pygame.draw.circle(surface, color, (px + 7, py + 5), 8)
            pts = [(px - 15, py + 8), (px, py + 22), (px + 15, py + 8)]
            pygame.draw.polygon(surface, color, pts)
            if i < self.player.hp:
                # 高光
                pygame.draw.arc(surface, (255, 150, 150),
                              (px - 12, py, 10, 10), 3.14, 0, 2)

        # ===== 火力等级条 =====
        power_bar_x = SCREEN_WIDTH - 115
        power_bar_y = 42
        pygame.draw.rect(surface, (40, 40, 50),
                        (power_bar_x, power_bar_y, 100, 14), border_radius=3)
        pw_fill = int(100 * self.player.power_level / 5)
        pw_color = CYAN if self.player.power_level < 3 else (PURPLE if self.player.power_level < 5 else GOLD)
        if pw_fill > 0:
            pygame.draw.rect(surface, pw_color,
                            (power_bar_x, power_bar_y, pw_fill, 14), border_radius=3)
        pw_label = font_tiny.render(f"PWR Lv.{self.player.power_level}", True, WHITE)
        surface.blit(pw_label, (power_bar_x, power_bar_y - 1))

        # ===== 炸弹数量 =====
        bomb_text = font_small.render(f"BOMB x{self.bombs_available}", True, ORANGE)
        surface.blit(bomb_text, (SCREEN_WIDTH - 118, 58))

        # ===== 护盾/加速/磁铁/冰冻状态指示 =====
        status_y = 74
        if self.player.shield_active:
            shield_txt = font_tiny.render(f"🛡 SHIELD {self.player.shield_timer // 60}s", True, CYAN)
            surface.blit(shield_txt, (10, status_y))
        if self.player.speed_boost:
            spd_txt = font_tiny.render(f"⚡ SPEED {self.player.speed_boost_timer // 60}s", True, YELLOW)
            surface.blit(spd_txt, (160, status_y))
        # 冰冻状态显示
        if self.freeze_timer > 0:
            freeze_txt = font_tiny.render(f"❄ FREEZE {self.freeze_timer // 60}s", True, (100, 200, 255))
            surface.blit(freeze_txt, (10, status_y + 16))

        # ===== 连击显示 =====
        if self.combo >= 3:
            combo_scale = min(1.0 + self.combo * 0.03, 1.5)
            combo_color = YELLOW if self.combo < 8 else ORANGE if self.combo < 15 else RED
            combo_str = f"{self.combo} COMBO!"
            combo_text = font_large.render(combo_str, True, combo_color)
            # 放大并居中
            cw = int(combo_text.get_width() * combo_scale)
            ch = int(combo_text.get_height() * combo_scale)
            combo_scaled = pygame.transform.scale(combo_text, (cw, ch))
            combo_rect = combo_scaled.get_rect(centerx=SCREEN_WIDTH // 2, top=78)
            surface.blit(combo_scaled, combo_rect)

        # ===== 升级提示 =====
        if self.level_up_display_timer > 0:
            alpha = min(255, self.level_up_display_timer * 4)
            lvl_surf = pygame.Surface((160, 40), pygame.SRCALPHA)
            lvl_bg_color = (*GREEN[:3], min(150, alpha // 2))
            pygame.draw.rect(lvl_surf, lvl_bg_color, (0, 0, 160, 40), border_radius=8)
            lvl_txt = font_medium.render(f"LEVEL UP! → {self.level}", True, (*GOLD[:3], alpha))
            lvl_txt_rect = lvl_txt.get_rect(center=(80, 20))
            lvl_surf.blit(lvl_txt, lvl_txt_rect)
            surface.blit(lvl_surf, (SCREEN_WIDTH // 2 - 80, 120))

        # ===== 通知显示 =====
        for i, notif in enumerate(self.notification_queue):
            alpha = min(255, notif['timer'] * 3)
            notif_surf = font_medium.render(notif['text'], True, (*WHITE[:3], alpha))
            notif_rect = notif_surf.get_rect(centerx=SCREEN_WIDTH // 2,
                                             centery=SCREEN_HEIGHT // 2 - 80 - i * 40 -
                                                     notif['y_offset'])
            surface.blit(notif_surf, notif_rect)

    # ==================== 主菜单 ====================
    def draw_menu(self, surface):
        self.star_field.update()
        self.star_field.draw(surface)
        self.menu_bg_stars_offset += 0.5

        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        surface.blit(overlay, (0, 0))

        # ===== 标题（带动画效果）=====
        title_y_base = 150
        title_y = title_y_base + math.sin(pygame.time.get_ticks() * 0.002) * 6

        # 标题光晕（单层，柔和扩散）
        for offset in range(3, 0, -1):
            alpha = 20 + 15 * offset
            shadow_surf = font_title.render("飞机大战", True, (*CYAN[:3], alpha))
            sr = shadow_surf.get_rect(centerx=SCREEN_WIDTH // 2, y=title_y + offset * 2)
            surface.blit(shadow_surf, sr)

        # 主标题（只画一次）
        title = font_title.render("飞机大战", True, WHITE)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH // 2, y=title_y)
        surface.blit(title, title_rect)

        # 版本标签
        ver = font_small.render("v2.1 ENHANCED", True, GOLD)
        vr = ver.get_rect(centerx=SCREEN_WIDTH // 2, y=title_y + 58)
        surface.blit(ver, vr)

        # 副标题
        sub = font_medium.render("- 经典街机射击 -", True, LIGHT_GRAY)
        sub_rect = sub.get_rect(centerx=SCREEN_WIDTH // 2, y=215)
        surface.blit(sub, sub_rect)

        # 菜单选项框
        menu_box = pygame.Surface((340, 280), pygame.SRCALPHA)
        menu_box.fill((10, 20, 40, 180))
        menu_box_rect = menu_box.get_rect(centerx=SCREEN_WIDTH // 2, y=270)
        pygame.draw.rect(surface, CYAN, menu_box_rect, 2, border_radius=10)
        surface.blit(menu_box, menu_box_rect)

        # 开始按钮（闪烁 + 鼠标支持）
        mouse_pos = pygame.mouse.get_pos()
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            start_color = YELLOW
        else:
            start_color = WHITE
        start_text = font_medium.render("▶ 点击或按 ENTER 开始", True, start_color)
        start_rect = start_text.get_rect(centerx=SCREEN_WIDTH // 2, y=290)
        # 扩大点击区域（比文字更大，方便点击）
        self.menu_btn_start = start_rect.inflate(80, 16)
        # 鼠标悬停高亮
        if self.menu_btn_start.collidepoint(mouse_pos):
            pygame.draw.rect(surface, (40, 80, 140), self.menu_btn_start, border_radius=8)
            start_text = font_medium.render("▶ 点击或按 ENTER 开始", True, GOLD)
        surface.blit(start_text, start_rect)

        # 排行榜入口（鼠标支持）
        lb_text = font_medium.render("🏆 按 L 或点击查看排行", True, ORANGE)
        lb_rect = lb_text.get_rect(centerx=SCREEN_WIDTH // 2, y=340)
        self.menu_btn_leaderboard = lb_rect.inflate(80, 16)
        if self.menu_btn_leaderboard.collidepoint(mouse_pos):
            pygame.draw.rect(surface, (40, 80, 140), self.menu_btn_leaderboard, border_radius=8)
            lb_text = font_medium.render("🏆 按 L 或点击查看排行", True, GOLD)
        surface.blit(lb_text, lb_rect)

        # 操作说明
        instructions = [
            ("━ 操作说明 ━", GOLD),
            ("方向键/WASD  移动", IVORY),
            ("空格键       射击", IVORY),
            ("B 键        炸弹", IVORY),
            ("P 键        暂停", IVORY),
        ]
        for i, (line, color) in enumerate(instructions):
            text = font_small.render(line, True, color)
            tr = text.get_rect(centerx=SCREEN_WIDTH // 2, y=390 + i * 28)
            surface.blit(text, tr)

        # 最高分
        if self.high_score > 0:
            hs_box = pygame.Surface((200, 40), pygame.SRCALPHA)
            hs_box.fill((100, 50, 0, 150))
            hs_br = hs_box.get_rect(centerx=SCREEN_WIDTH // 2, y=550)
            pygame.draw.rect(surface, GOLD, hs_br, 2, border_radius=6)
            surface.blit(hs_box, hs_br)
            hs = font_medium.render(f"最高分: {self.high_score:,}", True, GOLD)
            hs_rect = hs.get_rect(centerx=SCREEN_WIDTH // 2, centery=hs_br.centery)
            surface.blit(hs, hs_rect)

        # 底部装饰
        footer = font_tiny.render("Made by 阿爪 🦞", True, GRAY)
        fr = footer.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 25)
        surface.blit(footer, fr)

    # ==================== 暂停画面 ====================
    def draw_paused(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        # 暂停框
        pause_box = pygame.Surface((280, 180), pygame.SRCALPHA)
        pause_box.fill((10, 20, 40, 220))
        pb_rect = pause_box.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2)
        pygame.draw.rect(surface, CYAN, pb_rect, 2, border_radius=12)
        surface.blit(pause_box, pb_rect)

        pt = font_title.render("暂 停", True, WHITE)
        ptr = pt.get_rect(centerx=SCREEN_WIDTH // 2, centery=pb_rect.top + 50)
        surface.blit(pt, ptr)

        hint = font_medium.render("按 P 或 ESC 继续", True, YELLOW)
        hr = hint.get_rect(centerx=SCREEN_WIDTH // 2, centery=pb_rect.top + 115)
        surface.blit(hint, hr)

        # 当前分数预览
        cs = font_small.render(f"当前分数: {int(self.score):,}", True, SILVER)
        csr = cs.get_rect(centerx=SCREEN_WIDTH // 2, centery=pb_rect.top + 155)
        surface.blit(cs, csr)

    # ==================== 名字输入画面 ====================
    def draw_enter_name(self, surface):
        self.star_field.update()
        self.star_field.draw(surface)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        # 输入框
        input_box = pygame.Surface((400, 380), pygame.SRCALPHA)
        input_box.fill((8, 16, 36, 230))
        ib_rect = input_box.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2)
        pygame.draw.rect(surface, GOLD, ib_rect, 3, border_radius=12)
        surface.blit(input_box, ib_rect)

        # Game Over
        go = font_title.render("GAME OVER", True, RED)
        gor = go.get_rect(centerx=SCREEN_WIDTH // 2, y=ib_rect.top + 20)
        surface.blit(go, gor)

        # 统计数据
        stats = [
            (f"得分: {int(self.score):,}", YELLOW),
            (f"飞行距离: {self.distance_tracker.display_distance}", CYAN),
            (f"击杀敌机: {self.enemies_killed}", WHITE),
            (f"最高等级: Lv.{self.level}", GREEN),
            (f"最大连击: {self.combo_max}", ORANGE),
        ]
        for i, (text, color) in enumerate(stats):
            st = font_medium.render(text, True, color)
            sr = st.get_rect(centerx=SCREEN_WIDTH // 2, y=ib_rect.top + 85 + i * 38)
            surface.blit(st, sr)

        # 新纪录标识
        is_new_record = self.leaderboard.is_high_score(int(self.score))
        if is_new_record and int(self.score) > 0:
            nr = font_medium.render("🎉 新纪录! 请输入名字 🎉", True, GOLD)
            nrr = nr.get_rect(centerx=SCREEN_WIDTH // 2, y=ib_rect.top + 280)
            surface.blit(nr, nrr)

        # 名字输入
        self.name_cursor_timer += 1
        if self.name_cursor_timer >= 30:
            self.name_cursor_visible = not self.name_cursor_visible
            self.name_cursor_timer = 0

        cursor = "|" if self.name_cursor_visible else ""
        name_display = self.input_name + cursor

        # 输入框背景
        name_bg = pygame.Surface((260, 44), pygame.SRCALPHA)
        name_bg.fill((20, 30, 50))
        nbr = name_bg.get_rect(centerx=SCREEN_WIDTH // 2, y=ib_rect.top + 320)
        pygame.draw.rect(surface, CYAN, nbr, 2, border_radius=6)
        surface.blit(name_bg, nbr)

        nt = font_medium.render(name_display, True, WHITE)
        ntr = nt.get_rect(centerx=SCREEN_WIDTH // 2, centery=nbr.centery)
        surface.blit(nt, ntr)

        # 提示
        ht = font_small.render("输入名字按 ENTER 确认 | 跳过按 ESC", True, GRAY)
        htr = ht.get_rect(centerx=SCREEN_WIDTH // 2, y=ib_rect.top + 350)
        surface.blit(ht, htr)

    # ==================== 排行榜画面 ====================
    def draw_leaderboard(self, surface):
        self.star_field.update()
        self.star_field.draw(surface)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        # 排行榜面板
        lb_panel = pygame.Surface((460, 600), pygame.SRCALPHA)
        lb_panel.fill((8, 16, 36, 235))
        lbp_rect = lb_panel.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2 - 20)
        pygame.draw.rect(surface, GOLD, lbp_rect, 3, border_radius=12)
        surface.blit(lb_panel, lbp_rect)

        # 标题
        lt = font_title.render("🏆 排行榜 TOP 10", True, GOLD)
        ltr = lt.get_rect(centerx=SCREEN_WIDTH // 2, y=lbp_rect.top + 15)
        surface.blit(lt, ltr)

        # 表头
        headers = ["排名", "飞行员", "分数", "距离", "击杀", "日期"]
        header_x_positions = [lbp_rect.left + 20, lbp_rect.left + 80,
                             lbp_rect.left + 200, lbp_rect.left + 290,
                             lbp_rect.left + 370, lbp_rect.left + 420]
        header_y = lbp_rect.top + 70
        for hx, header in zip(header_x_positions, headers):
            ht = font_tiny.render(header, True, CYAN)
            surface.blit(ht, (hx, header_y))

        # 分隔线
        pygame.draw.line(surface, GRAY,
                        (lbp_rect.left + 15, header_y + 22),
                        (lbp_rect.right - 15, header_y + 22), 1)

        # 数据行
        entries = self.leaderboard.get_top_n(10)
        if entries:
            for i, entry in enumerate(entries):
                row_y = lbp_rect.top + 95 + i * 42

                # 行高亮（前三名）
                if i < 3:
                    row_highlight = (*[GOLD, SILVER, (205, 127, 50)][i][:3], 30)
                    row_surf = pygame.Surface((430, 38), pygame.SRCALPHA)
                    row_surf.fill(row_highlight)
                    surface.blit(row_surf, (lbp_rect.left + 15, row_y - 2))

                # 排名
                medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i + 1}."
                rank_text = font_small.render(medal, True, WHITE)
                surface.blit(rank_text, (lbp_rect.left + 20, row_y))

                # 名字
                name_text = font_small.render(entry.get('name', '---')[:8], True, IVORY)
                surface.blit(name_text, (lbp_rect.left + 80, row_y))

                # 分数
                score_text = font_small.render(f"{entry.get('score', 0):,}", True, YELLOW)
                surface.blit(score_text, (lbp_rect.left + 200, row_y))

                # 距离
                d = entry.get('distance', 0)
                if d >= 1000:
                    dist_str = f"{d/1000:.1f}km"
                else:
                    dist_str = f"{int(d)}m"
                dist_text = font_small.render(dist_str, True, CYAN)
                surface.blit(dist_text, (lbp_rect.left + 290, row_y))

                # 击杀
                kill_text = font_small.render(str(entry.get('kills', 0)), True, WHITE)
                surface.blit(kill_text, (lbp_rect.left + 370, row_y))

                # 日期（截短）
                date_str = entry.get('date', '')[:10]
                date_text = font_tiny.render(date_str, True, GRAY)
                surface.blit(date_text, (lbp_rect.left + 420, row_y + 4))
        else:
            empty = font_medium.render("暂无记录，快去创造历史吧！", True, GRAY)
            er = empty.get_rect(centerx=SCREEN_WIDTH // 2, centery=lbp_rect.centery)
            surface.blit(empty, er)

        # 返回提示
        back_hint = font_medium.render("按 ESC 或 M 返回菜单", True, WHITE)
        bhr = back_hint.get_rect(centerx=SCREEN_WIDTH // 2, y=lbp_rect.bottom - 45)
        surface.blit(back_hint, bhr)

    # ==================== 游戏结束（旧兼容）====================
    def draw_gameover(self, surface):
        # 直接使用名字输入界面
        self.draw_enter_name(surface)

    # ==================== 主绘制函数 ====================
    def draw(self):
        sx, sy = 0, 0
        if self.screen_shake > 0:
            # 震动幅度大幅降低：最大偏移从±25降到±5
            shake_intensity = max(1, self.screen_shake // 4)
            sx = random.randint(-shake_intensity, shake_intensity)
            sy = random.randint(-shake_intensity, shake_intensity)

        # 使用预分配的game_surface，避免每帧screen.copy()（性能优化）
        if not hasattr(Game, '_draw_buffer'):
            Game._draw_buffer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surface = Game._draw_buffer
        game_surface.fill(DARK_BLUE)

        if self.state == 'menu':
            self.draw_menu(game_surface)

        elif self.state == 'playing':
            # 背景
            self.star_field.draw(game_surface)

            # 尾迹
            for tp in self.trail_particles:
                tp.draw(game_surface)

            # 道具
            for pu in self.powerups:
                pu.draw(game_surface)

            # 障碍物
            for obs in self.obstacles:
                obs.draw(game_surface)

            # 玩家
            self.player.draw(game_surface)

            # 玩家子弹
            for b in self.player_bullets:
                b.draw(game_surface)

            # 敌机
            for e in self.enemies:
                e.draw(game_surface)

            # 敌机子弹
            for b in self.enemy_bullets:
                b.draw(game_surface)

            # 爆炸
            for ex in self.explosions:
                ex.draw(game_surface)

            # 粒子
            for p in self.particles_list:
                p.draw(game_surface)

            # HUD
            self.draw_hud(game_surface)

        elif self.state == 'paused':
            # 先画完整游戏场景
            self.star_field.draw(game_surface)
            for pu in self.powerups: pu.draw(game_surface)
            for obs in self.obstacles: obs.draw(game_surface)
            self.player.draw(game_surface)
            for b in self.player_bullets: b.draw(game_surface)
            for e in self.enemies: e.draw(game_surface)
            for b in self.enemy_bullets: b.draw(game_surface)
            for ex in self.explosions: ex.draw(game_surface)
            for p in self.particles_list: p.draw(game_surface)
            self.draw_hud(game_surface)
            self.draw_paused(game_surface)

        elif self.state == 'gameover' or self.state == 'enter_name':
            self.draw_enter_name(game_surface)

        elif self.state == 'leaderboard':
            self.draw_leaderboard(game_surface)

        # 输出
        screen.fill(DARK_BLUE)
        screen.blit(game_surface, (sx, sy))
        pygame.display.flip()


# ================================================================
#                         ★★★ 主循环 ★
# ================================================================
def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 鼠标点击支持
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if game.state == 'menu':
                    if game.menu_btn_start.collidepoint(mx, my):
                        game.reset()
                    elif game.menu_btn_leaderboard.collidepoint(mx, my):
                        game.state = 'leaderboard'
                elif game.state == 'leaderboard':
                    # 排行榜界面点击任意位置返回菜单
                    game.state = 'menu'
                elif game.state == 'gameover' or game.state == 'enter_name':
                    # 结束界面点击返回菜单
                    game.state = 'menu'

            elif event.type == pygame.KEYDOWN:
                key = event.key

                # ESC 处理
                if key == pygame.K_ESCAPE:
                    if game.state == 'playing':
                        game.state = 'paused'
                    elif game.state == 'paused':
                        game.state = 'playing'
                    elif game.state in ('leaderboard', 'gameover', 'enter_name'):
                        game.state = 'menu'

                # Enter 开始 / 确认名字
                elif key == pygame.K_RETURN:
                    if game.state == 'menu':
                        game.reset()
                    elif game.state == 'enter_name':
                        # 保存分数到排行榜
                        game.leaderboard.add_entry(
                            game.input_name,
                            game.score,
                            game.distance_tracker.distance,
                            game.enemies_killed,
                            game.level
                        )
                        game.high_score = game.leaderboard.top_score
                        game.state = 'leaderboard'

                # 暂停
                elif key == pygame.K_p:
                    if game.state == 'playing':
                        game.state = 'paused'
                    elif game.state == 'paused':
                        game.state = 'playing'

                # 重新开始
                elif key == pygame.K_r:
                    if game.state in ('gameover', 'enter_name'):
                        game.reset()

                # 返回菜单
                elif key == pygame.K_m:
                    if game.state in ('gameover', 'enter_name'):
                        game.state = 'menu'

                # 排行榜
                elif key == pygame.K_l:
                    if game.state == 'menu':
                        game.state = 'leaderboard'
                    elif game.state == 'leaderboard':
                        game.state = 'menu'

                # 炸弹
                elif key == pygame.K_b:
                    if game.state == 'playing' and game.bombs_available > 0:
                        game.bombs_available -= 1
                        game.use_bomb()

                # 名字输入处理
                elif game.state == 'enter_name':
                    if key == pygame.K_BACKSPACE:
                        game.input_name = game.input_name[:-1] if game.input_name else ""
                    elif key == pygame.K_SPACE:
                        game.input_name += "_"
                    elif event.unicode and len(game.input_name) < 10:
                        # 只接受可打印字符
                        if event.unicode.isprintable() and event.unicode.isascii():
                            game.input_name += event.unicode.upper()

        # 更新 & 绘制
        game.update()
        game.draw()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# ======================== 入口 ========================
if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 55)
    print("  *** 飞机大战 v2.1 Enhanced ***")
    print("=" * 55)
    print("\n  功能:")
    print("    • 修复射击碰撞检测")
    print("    • 全新UI界面与精美飞机")
    print("    • 多种障碍物（陨石/地雷/障碍墙）")
    print("    • 飞行距离实时计算 + Top 10 排行榜")
    print("    • 菜单鼠标点击支持 | BGM已移除(更流畅)\n")

    print("  操作: 方向键/WASD移动  空格射击  B炸弹  P暂停  鼠标点击菜单")
    print("  正在启动游戏...\n")

    main()
