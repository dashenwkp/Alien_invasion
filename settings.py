class Settings:
    '''存储游戏《外星人入侵》中所有设置的类'''

    def __init__(self):
        '''初始化游戏的设置'''
        # 屏幕设置
        self.screen_width = 1200 # 默认值1200
        self.screen_height = 800 # 默认值800
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed = 10
        self.ship_limit = 3

        # 子弹的设置
        self.bullet_speed = 10.0 # 书中推荐值是2.5
        self.bullet_width = 3000 # 默认值是3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3 # 默认值是3

        # 外星人的设置
        self.alien_speed = 5.0 # 默认值1.0
        self.fleet_drop_speed = 20 # 默认值10
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1