import time
import random as rnd
import math
import pygame
from player import Player
from bullet import Bullet
from rank import Rank

def collision(obj1, obj2):
    if math.sqrt((obj1.pos[0] - obj2.pos[0]) ** 2 + 
                 (obj1.pos[1] - obj2.pos[1]) ** 2) < 13 + obj2.radius[obj2.kind]: # 총알 크기에 따른 충돌 거리 수정
        return True
    return False

def draw_text(txt, size, pos, color):
    intpos = []
    intpos.append(round(pos[0]))
    intpos.append(round(pos[1]))
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, intpos)

# Initialize the pygame
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
WIDTH, HEIGHT = 1000, 800

# Background image
bg_image = pygame.image.load('bg.jpg')

# Background music
pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

# SFX
hitsound = pygame.mixer.Sound('Crash_Steel_Pipe.ogg')
explodesound = pygame.mixer.Sound('Big_Explosion_Cut_Off.ogg')

# Rank
ranking = Rank()
rank_tog = 0

pygame.display.set_caption("총알 피하기")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS=60

player = Player(WIDTH/2, HEIGHT/2)
maxlife = player.life # 최대 생명력

bullets = []
for i in range(10):
    bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5, rnd.randint(0,2)))

time_for_adding_bullets = 0
time_for_invincible = 0
time_for_rankblink = 0

twinkle_dt = 0 # dt 기준으로 반짝이는 시간 정하기
blink_dt = 0 # dt 기준으로 깜빡이는 시간 정하기

start_time = time.time()

#bg_pos = 0
#bg_dt = -0.01
bg_pos = [0 - (bg_image.get_width()-WIDTH)/2, 0 - (bg_image.get_height()-HEIGHT)/2]

#Game Loop
running = True
gameover = False
score = 0
ranktxt = []
rankcolor = []
ranked = 999
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
    
    #bg_pos += bg_dt * dt
    #if bg_image.get_width() + bg_pos - WIDTH <= 0 or bg_pos >= 0: bg_dt *= -1
    #screen.blit(bg_image, (bg_pos, 0))

    # 배경 그림이 비행기의 움직임에 반응하여 이동
    bg_pos[0] -= player.to[0] + dt*player.to[0]*0.5
    bg_pos[1] -= player.to[1] + dt*player.to[1]*0.3
    bg_pos[0] = round(min(max(bg_pos[0], 0-(bg_image.get_width()-WIDTH)), 0))
    bg_pos[1] = round(min(max(bg_pos[1], 0-(bg_image.get_height()-HEIGHT)), 0))
    screen.blit(bg_image, (bg_pos))

    player.update(dt, screen)
    player.draw(screen)
    for b in bullets:
        b.update_and_draw(dt, screen)

    

    if gameover:
        player.twinkile(False)
        draw_text("GAME OVER", 100, (WIDTH/2 - 300, HEIGHT/2 - 300), (255,255,255))
        txt = "Time: {:.1f}  Bullets: {}".format(score, len(bullets))
        draw_text(txt, 32, (WIDTH/2 - 150, HEIGHT/2 - 200), (255,255,255))
        if rank_tog == 0:
            ranking.setrec(score)
            ranking.save()
            rank_tog = 1

            # 랭킹을 텍스트에 넣어주기
            for i in range(10):
                if len(ranking.ranklist) > i:
                    if i == 9:
                        ranktxt.append("{}: {:.3f} ".format(i+1, ranking.ranklist[i]))
                    else:
                        ranktxt.append("  {}: {:.3f} ".format(i+1, ranking.ranklist[i]))
                else:
                    break

            # 랭크된 경우 강조를 위해 내 점수 찾기
            if score in ranking.ranklist:
                    ranked = ranking.ranklist.index(score) # 동점자 발생한 경우 두 점수 중 높은 순위의 점수를 강조 (틱레이트가 60이고 score가 float 이므로 동점자가 발생하기 쉽지 않다고 생각)
        # Top 10 출력
        draw_text("Top 10", 32 , (WIDTH/2 - 40, HEIGHT/2 - 150), (255, 255, 255))
        for i in range(10):
            if len(ranktxt) > i:
                if ranked == i:
                    if time_for_rankblink <= 3000:
                        blink_dt += dt
                        if blink_dt < 100:
                            draw_text(ranktxt[i], 32 , (WIDTH/2 - 80, HEIGHT/2 - 100 + i*50), (255,255,0))
                        elif blink_dt >= 200:
                            blink_dt -= 200
                        time_for_rankblink += dt
                    else:
                        draw_text(ranktxt[i], 32 , (WIDTH/2 - 80, HEIGHT/2 - 100 + i*50), (255,255,0))
                else:
                    draw_text(ranktxt[i], 32 , (WIDTH/2 - 80, HEIGHT/2 - 100 + i*50), (255, 255, 255))
            else:
                break
    else:
        score = time.time() - start_time
        txt = "Time: {:.1f}".format(score)
        draw_text(txt, 32, (10, 10), (255,255,255))
        txt = "Bullets: {}".format(len(bullets))
        draw_text(txt, 32, (200, 10), (255,255,255))
        txt = "Life: {}".format(player.life) # Life: 생명력 숫자
        draw_text(txt, 32, (400, 10), (255,255,255))
        # 생명력 막대기
        pygame.draw.rect(screen, (255, 0, 0), (550, 11, 100, 30)) # 전체 생명력
        pygame.draw.rect(screen, (0, 255, 0), (550, 11, int(100/maxlife*player.life), 30)) # 현재 생명력

    pygame.display.update() #화면에 새로운 그림을 그린다 (화면을 갱신한다)

    if not gameover:
        for b in bullets:
            if collision(player, b) and player.invinciblity == False:
                hitsound.play() #충돌 효과음 재생
                player.explode(True) #폭발
                player.minuslife(b.getdamage()) #생명력 감소
                player.invincible(True) # 무적

                if player.life <= 0:
                    explodesound.play() #폭발 효과음 재생
                    gameover = True
                #time.sleep(2)
                #running = False

        # 무적    
        if player.invinciblity == True:
            time_for_invincible += dt
            twinkle_dt += dt

            # 반짝반짝
            if twinkle_dt < 100:
                player.twinkile(True)
                
            elif twinkle_dt < 200:
                player.twinkile(False)
                
            else:
                player.twinkile(True)
                twinkle_dt -= 200

            if time_for_invincible > 500: # 0.5초 후 폭발 효과 지우기
                player.explode(False)

            if time_for_invincible > 2000:
                player.invincible(False)
                time_for_invincible = 0
                player.twinkile(False)
                twinkle_dt = 0
        
        time_for_adding_bullets += dt
        if time_for_adding_bullets > 1000:
            bullets.append(Bullet(0, rnd.random()*HEIGHT, rnd.random()-0.5, rnd.random()-0.5, rnd.randint(0,2)))
            time_for_adding_bullets -= 1000
