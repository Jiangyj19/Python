import sys
from bullet import Bullet
from jiangjiang import JiangJiang
from time import sleep
import pygame


def check_fleet_edges(ai_settings, jiangjiangs):
    '''有外星人到达边缘时采取相应的措施'''
    for jiangjiang in jiangjiangs.sprites():
        if jiangjiang.check_edges():
            change_fleet_direction(ai_settings, jiangjiangs)
            break


def change_fleet_direction(ai_settings, jiangjiangs):
    '''将整个外星人下移，并改变他们的方向'''
    for jiangjiang in jiangjiangs.sprites():
        jiangjiang.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_number_rows(ai_settings, ship_height, jiangjiang_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height-3 *
                         jiangjiang_height-ship_height)
    number_rows = int(available_space_y/(2*jiangjiang_height))
    return number_rows


def create_jiangjiang(ai_settings, screen, jiangjiangs, jiangjiang_num, row_num):
    '''创建一个外星人并将其放在当前行队列'''
    jiangjiang = JiangJiang(ai_settings, screen)
    jiangjiang_width = jiangjiang.rect.width
    jiangjiang.x = jiangjiang_width+2*jiangjiang_width*jiangjiang_num
    jiangjiang.rect.y = jiangjiang.rect.height+2*jiangjiang.rect.height*row_num
    jiangjiang.rect.x = jiangjiang.x
    jiangjiangs.add(jiangjiang)


def get_number_jiangjiangs_x(ai_settings, jiangjiang_width):
    '''计算每行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width-2*jiangjiang_width
    number_jiangjiangs_x = int(available_space_x/(2*jiangjiang_width))
    return number_jiangjiangs_x


def create_fleet(ai_settings, screen, ship, jiangjiangs):
    '''创建江江群'''
    # 创建一个江江，并计算一行可容纳多少个江江
    # 江江间距为江江的宽度
    jiangjiang = JiangJiang(ai_settings, screen)
    number_jiangjiangs_x = get_number_jiangjiangs_x(
        ai_settings, jiangjiang.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, jiangjiang.rect.height)
    # print(number_rows)
    # 创建江江群
    for row_number in range(number_rows):
        for jiangjiang_num in range(number_jiangjiangs_x):
            # print(str(jiangjiang.x)+' '+str(jiangjiang.rect.y))
            create_jiangjiang(ai_settings, screen,
                              jiangjiangs, jiangjiang_num, row_number)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''响应按下'''
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # ship.bullet_shotting = True
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    # 如果子弹数目还没到达上限，创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, jiangjiangs, bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, jiangjiangs, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, jiangjiangs, bullets, mouse_x, mouse_y):
    '''在玩家单击Play按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        pygame.mouse.set_visible(False)
        # 清空外星人列表和字典列表
        jiangjiangs.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, jiangjiangs)
        ship.center_ship()

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()


def update_screen(ai_settings, screen, stats, sb, ship, jiangjiangs, bullets, play_button):
    '''更新屏幕上的图像，并切换到新屏幕'''
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    jiangjiangs.draw(screen)
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让新绘制的屏幕重新可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, jiangjiangs, bullets):
    '''更新子弹的位置，并删除已消失的子弹'''
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_jiangjiang_collisions(
        ai_settings, screen, stats, sb, ship, jiangjiangs, bullets)


def check_high_score(stats, sb):
    '''检查是否诞生了最高得分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_jiangjiang_collisions(ai_settings, screen, stats, sb, ship, jiangjiangs, bullets):
    '''响应子弹和江江的碰撞'''
    # 删除现有的子弹并创建一群新的江江
    collisions = pygame.sprite.groupcollide(bullets, jiangjiangs, True, True)
    if collisions:
        for jiangjiangs in collisions.values():  # 此处jiangjiangs是一个列表，表示被同一颗子弹击中的所有jiangjiang
            stats.score += ai_settings.jiangjiang_points*len(jiangjiangs)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(jiangjiangs) == 0:
        ai_settings.increase_speed()
        bullets.empty()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, jiangjiangs)


def update_jiangjiangs(ai_settings, screen, stats, sb,  ship, jiangjiangs, bullets):
    '''检查是否有外星人位于屏幕边缘，并更新整群江江的位置'''
    check_fleet_edges(ai_settings, jiangjiangs)
    jiangjiangs.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, jiangjiangs):
        ship_hit(ai_settings, screen, stats, sb, ship, jiangjiangs, bullets)
    check_jiangjiang_bottom(ai_settings, screen, stats, sb,
                            ship, jiangjiangs, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, jiangjiangs, bullets):
    '''响应被江江撞到的飞船'''
    # 将ships_left减1
    if stats.ships_left > 0:
        stats.ships_left -= 1
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    # 更新记分牌
    sb.prep_ships()
    # 清空江江列表和子弹列表
    jiangjiangs.empty()
    bullets.empty()

    # 创建一群新的江江，并将飞船放到屏幕底端中间
    create_fleet(ai_settings, screen, ship, jiangjiangs)
    ship.center_ship()

    # 暂停
    sleep(2)


def check_jiangjiang_bottom(ai_settings, screen, stats, sb, ship, jiangjiangs, bullets):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for jiang in jiangjiangs.sprites():
        if jiang.rect.bottom > screen_rect.bottom:
            # 像飞船像被撞到一样进行处理
            ship_hit(ai_settings,  screen, stats,
                     sb, ship, jiangjiangs, bullets)
            break
