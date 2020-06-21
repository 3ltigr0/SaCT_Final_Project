import time
import random as rnd
import math
import pygame
from player import Player
from bullet import Bullet

def collision(obj1, obj2):
    if math.sqrt((obj1.pos[0] - obj2.pos[0]) ** 2 + 
                 (obj1.pos[1] - obj2.pos[1]) ** 2) < 20:
        return True
    return False

def draw_text(txt, size, pos, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)

# Initialize the pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
WIDTH, HEIGHT = 1000, 800

# Background image
bg_image = pygame.image.load('bg.jpg')

# Background music
pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.75)

# SFX
hitsound = pygame.mixer.Sound('Crash_Steel_Pipe.ogg')

pygame.display.set_caption("총알 피하기")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS=60

player = Player(WIDTH/2, HEIGHT/2)

bullets = []
for i in range(10):
    bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))

time_for_adding_bullets = 0

start_time = time.time()

bg_pos = 0
bg_dt = -0.01

#Game Loop
running = True
gameover = False
score = 0
while running:

    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #게임 창의 X버튼을 눌렀을 때
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.goto(-1,0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1,0)
            elif event.key == pygame.K_UP:
                player.goto(0,-1)
            elif event.key == pygame.K_DOWN:
                player.goto(0,1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1,0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1,0)
            elif event.key == pygame.K_UP:
                player.goto(0,1)
            elif event.key == pygame.K_DOWN:
                player.goto(0,-1)
        
    # 화면에 검은색 채우기 (RGB - Red, Green, Blue)
    # screen.fill((0, 0, 0))
    
    bg_pos += bg_dt * dt
    if bg_image.get_width() + bg_pos - WIDTH <= 0 or bg_pos >= 0: bg_dt *= -1
    screen.blit(bg_image, (bg_pos, 0))

    player.update(dt, screen)
    player.draw(screen)
    for b in bullets:
        b.update_and_draw(dt, screen)

    

    if gameover:
        draw_text("GAME OVER", 100, (WIDTH/2 - 300, HEIGHT/2 - 50), (255,255,255))
        txt = "Time: {:.1f}  Bullets: {}".format(score, len(bullets))
        draw_text(txt, 32, (WIDTH/2 - 150, HEIGHT/2 + 50), (255,255,255))
    else:
        score = time.time() - start_time
        txt = "Time: {:.1f}  Bullets: {}".format(score, len(bullets))
        draw_text(txt, 32, (10, 10), (255,255,255))

    pygame.display.update() #화면에 새로운 그림을 그린다 (화면을 갱신한다)

    if not gameover:
        for b in bullets:
            if collision(player, b):
                gameover = True
                hitsound.play() #충돌 효과음 재생
                #time.sleep(2)
                #running = False
        
        time_for_adding_bullets += dt
        if time_for_adding_bullets > 1000:
            bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5))
            time_for_adding_bullets -= 1000