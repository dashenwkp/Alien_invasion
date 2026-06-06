import sys
from time import sleep
from pathlib import Path

import pygame

from settings import Settings
from game_stats import Gamestats
from scoreboard import ScoreBoard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.path = Path('high_score.txt')
        self.contents = self.path.read_text().strip()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # 创建一个用于存储游戏统计信息的实例, 并创建计分牌
        self.stats = Gamestats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bulltes = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 让游戏一开始处于非活动状态
        self.game_active = False

        # 创建play按钮
        self.play_button = Button(self, 'Play')
        self._make_difficulty_buttons()

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
            self.clock.tick(60)

    def _make_difficulty_buttons(self):
        '''制造不同难度的按钮'''
        self.easy_button = Button(self, 'Easy')
        self.medium_button = Button(self, 'Medium')
        self.hard_button = Button(self, 'Hard')
        self.easy_button.rect.top = (
            self.play_button.rect.top + 1.5 * self.play_button.rect.height)
        self.easy_button.update_msg_pos()
        self.medium_button.rect.top = (
            self.easy_button.rect.top + 1.5 * self.play_button.rect.height)
        self.medium_button.update_msg_pos()
        self.hard_button.rect.top = (
            self.medium_button.rect.top + 1.5 * self.play_button.rect.height)
        self.hard_button.update_msg_pos()
    
    def _check_events(self):
        '''相应按键和鼠标事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._write_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''在玩家单机Play按钮时开始新游戏'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 还原游戏设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏的统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bulltes.empty()

            # 创建一个新的外星舰队, 并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)

    def _check_difficulty_buttons(self, mouse_pos):
        '''在单击不同难度按钮时调整游戏的难度'''
        easy_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if easy_clicked and not self.game_active:
            self.settings.difficulty_level = 'easy'
        elif medium_clicked and not self.game_active:
            self.settings.difficulty_level = 'medium'
        elif hard_clicked and not self.game_active:
            self.settings.difficulty_level = 'hard'
        
    def _check_keydown_events(self, event):
        '''响应按下'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._write_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _write_high_score(self):
        '''将最高分写入文件'''
        self.path.write_text(str(self.stats.high_score))

    def _check_keyup_events(self, event):
        '''响应释放'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        
    def _fire_bullet(self):
        '''创建一颗子弹, 并将其加入编组bullets'''
        if len(self.bulltes) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bulltes.add(new_bullet)

    def _create_fleet(self):
        '''创建一个外星舰队'''
        # 创建一个外星人，再不断添加，只到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 9 * alien_height):    # 作者在这里使用的是3倍外星人高度，但我的外星人图像太扁使得9倍高度更合适
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        '''创建一个外星人并将其放到当前行中'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        '''在有外星人到达边缘时采取相应的措施'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''将整个外星舰队向下移动, 并改变它们的方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        '''更新屏幕上的图像，并切换到新屏幕'''
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bulltes.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态, 就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip()

    def _update_bullets(self):
        '''更新子弹的位置并删除已消失的子弹'''
        # 更新子弹的位置
        self.bulltes.update()

        # 删除已消失的子弹
        for bullet in self.bulltes.copy():
            if bullet.rect.bottom <= 0:
                self.bulltes.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''相应子弹和外星人的碰撞'''
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bulltes, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # 删除现有的子弹并创建一个新的外星舰队
            self.bulltes.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        '''检查是否有外星人位于屏幕边缘, 并更新整个外星舰队的位置'''
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _ship_hit(self):
        '''响应飞船和外星人的碰撞'''
        # 将ships_left减1并更新计分牌
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bulltes.empty()

            # 创建一个新的外星舰队, 并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        '''检查是否有外星人到达了屏幕的下边缘'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

if __name__ == '__main__':
    '''创建游戏实例并运行游戏'''
    ai = AlienInvasion()
    ai.run_game()