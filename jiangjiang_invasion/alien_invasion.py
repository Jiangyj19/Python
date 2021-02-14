import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("XiaoJiang Invasion")
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一艘飞船,一个子弹编组和一个江江编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    jiangjiangs = Group()
    # 创建江江群
    gf.create_fleet(ai_settings, screen, ship, jiangjiangs)
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 创建一个记分牌
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        # 监听输入
        gf.check_events(ai_settings, screen, stats, sb,
                        play_button, ship, jiangjiangs, bullets)
        if stats.game_active:
            # 更新飞船位置
            ship.update()
            # 更新子弹
            gf.update_bullets(ai_settings, screen, stats,
                              sb, ship, jiangjiangs, bullets)
            # 更新江江
            gf.update_jiangjiangs(ai_settings, screen, stats, sb,
                                  ship, jiangjiangs, bullets)
        # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship,
                         jiangjiangs, bullets, play_button)


run_game()
