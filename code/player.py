import math
import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.life = 10 # 생명력
        self.pos = [x, y]
        self.to = [0, 0]
        self.acc = [0, 0]
        self.angle = 0

        # Explosion
        self.expl_effect = pygame.image.load('flame.png')
        self.expl_effect = pygame.transform.scale(self.expl_effect, (64, 64))
        self.exploded = False

        #무적
        self.invinciblity = False

    def draw(self, screen):        
        if self.to == [-1, -1]: self.angle = 45
        elif self.to == [-1, 0]: self.angle = 90
        elif self.to == [-1, 1]: self.angle = 135
        elif self.to == [0, 1]: self.angle = 180
        elif self.to == [1, 1]: self.angle = -135
        elif self.to == [1, 0]: self.angle = -90
        elif self.to == [1, -1]: self.angle = -45
        elif self.to == [0, -1]: self.angle = 0

        rotated = pygame.transform.rotate(self.image, self.angle)
        calib_pos = (self.pos[0] - rotated.get_width()/2,
                     self.pos[1] - rotated.get_height()/2)
        
        screen.blit(rotated, calib_pos)
        
        if self.exploded == True:
            screen.blit(self.expl_effect, (self.pos[0] - 32, self.pos[1] - 32)) # 터지는 그림 효과
    
    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y

    def update(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = self.pos[0] + dt*self.to[0]*0.6
        self.pos[1] = self.pos[1] + dt*self.to[1]*0.6
        self.pos[0] = min(max(self.pos[0], 32), width-32)
        self.pos[1] = min(max(self.pos[1], 32), height-32)

    # 폭발
    def explode(self, value):
        self.exploded = value

    # 무적
    def invincible(self, value):
        self.invinciblity = value

    # 생명력 감소
    def minuslife(self, value):
        self.life -= value
    
    # 비행기 반짝
    def twinkile(self, value):
        if value:
            self.image = pygame.image.load('player_twinkle.png')
            self.image = pygame.transform.scale(self.image, (64, 64))

        else:
            self.image = pygame.image.load('player.png')
            self.image = pygame.transform.scale(self.image, (64, 64))