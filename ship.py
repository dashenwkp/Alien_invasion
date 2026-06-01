import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''管理飞船的类'''

    def __init__(self, ai_game):
        '''初始化飞船并设置其初始位置'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() # 这里应该是屏幕的矩形

        # 加载图像并获取其外接矩形
        self.image = pygame.image.load(r'images\rocket_small.png')
        self.rect = self.image.get_rect() # 这里就是飞船的矩形了

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x中储存一个浮点数
        self.x = float(self.rect.x)

        # 移动标志（飞船一开始不动）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''根据移动标志调整飞船的位置'''
        # 更新飞船的属性x的值，而不是其外接矩形的属性x的值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据self.x更新rect对象
        self.rect.x = self.x
        
    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect) # 第二个参数是绘制的位置

    def center_ship(self):
        '''将飞船放到屏幕底部的中央'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)