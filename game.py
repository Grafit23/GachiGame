import pygame
import random
import math
from os import path 

WIDTH = 480
HEIGHT = 600
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

img_folder = path.join(path.dirname(__file__), 'img')
sound_folder = path.join(path.dirname(__file__), 'sounds')
music_folder = path.join(path.dirname(__file__), 'music')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_imgaes[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        # броня
        self.shield = 100
        # св-ва для зажатой стрельбы
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        # 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 80
        self.frame = 0
        self.size = len(player_imgaes)

        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == self.size:
                self.frame = 0
            self.image = player_imgaes[self.frame]
            self.image.set_colorkey(BLACK)
        
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
	        self.hidden = False
	        self.rect.centerx = WIDTH / 2
	        self.rect.bottom = HEIGHT - 10
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            random.choice(shoot_sounds).play()
    
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemy_images)
        self.image_orig.set_colorkey(BLACK)
        n = random.randint(30, 150)
        self.image_orig = pygame.transform.scale(
            self.image_orig, 
            (n, n*random.randint(1, 2))
            )
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width + self.rect.height)/4)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)


        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_ups_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation\
                    [self.size][self.frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center



font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (252, 15, 192))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, WHITE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gachi Club Production')
clock = pygame.time.Clock()


# Загрузка игровой графики
bg = pygame.image.load(path.join(img_folder, r"Backgrounds\billy.jpg")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg_rect = bg.get_rect()
# Спрайт игрока
player_imgaes = []
absolute_player_images = []
for i in range(20):
    if len(str(i)) < 2:
        i = '0'+str(i)
    player_img = pygame.image.load(path.join(img_folder, f"billy_h/IMG000{i}.bmp")).convert()
    player_img = pygame.transform.scale(player_img, (50, 50))
    player_imgaes.append(player_img)
    player_img = pygame.image.load(path.join(img_folder, f"absolute_billy_h/IMG000{i}.bmp")).convert()
    player_img = pygame.transform.scale(player_img, (50, 50))
    absolute_player_images.append(player_img)
# Спрайт врагов
enemy_images = []
for i in range(4):
    enemy_img = pygame.image.load(path.join(img_folder, f"enemy_{i}.jpg")).convert()  
    enemy_images.append(enemy_img)
# Спрайт снарядов
bullet_img = pygame.image.load(path.join(img_folder, r"heart.jpg")).convert()
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
# Спрайты взрыва
explosion_animation = dict()
explosion_animation['ss'] = list()
explosion_animation['ls'] = list()
explosion_animation['player'] = list()
for i in range(9):
    p = f"explosion_animation/regularExplosion0{i}.png"
    exp_img = pygame.image.load(path.join(img_folder, p)).convert()
    # small
    exp_img_transform_ms = pygame.transform.scale(exp_img, (32, 32))
    explosion_animation['ss'].append(exp_img_transform_ms)
    # large
    exp_img_transform_ls = pygame.transform.scale(exp_img, (100, 100))
    explosion_animation['ls'].append(exp_img_transform_ls)
    # player
    p = f'player_expl/sonicExplosion0{i}.png'
    exp_img = pygame.image.load(path.join(img_folder, p)).convert()
    exp_img.set_colorkey(BLACK)
    explosion_animation['player'].append(exp_img)
# Power-up
power_ups_images = dict()
for power_up, j in zip(['dick', 'semen'], ['gun', 'shield']):
    img = pygame.image.load(path.join(img_folder, f'power_up_{power_up}.png')).convert()
    img = pygame.transform.scale(img, (60, 60))
    img.set_colorkey(BLACK)
    power_ups_images[j] = img
# UI
# Иконка жизней.
player_icon = pygame.image.load(path.join(img_folder, 'billy_h/IMG00013.bmp')).convert()
player_mini_icon = pygame.transform.scale(player_icon, (25, 19))
player_mini_icon.set_colorkey(BLACK)

# Звуки
shoot_sounds = []
for i in range(1, 5):
    shoot_sounds.append(pygame.mixer.Sound(path.join(sound_folder, f"Orgasm_{i}.mp3")))
shoot_sounds.append(pygame.mixer.Sound(path.join(sound_folder, "Orgasm_6.mp3")))
exp_sound = pygame.mixer.Sound(path.join(sound_folder, "fuck you....mp3"))
death_sound = pygame.mixer.Sound(path.join(sound_folder, 'Iam cumming.mp3'))
hit_sound = pygame.mixer.Sound(path.join(sound_folder, 'Fucking slaves get your ass back here.mp3'))

# Музыка
pygame.mixer.music.  load(path.join(music_folder, "cadilac.mp3"))
pygame.mixer.music.set_volume(0.4)


# Группы спрайтов
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()


player = Player()
all_sprites.add(player)
for i in range(8):
    new_mob()


score = 0
pygame.mixer.music.play(loops=-1)
# Цикл игры
running = True
while running:
    # цикл на правильной скорости
    clock.tick(FPS)
    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Обновления
    all_sprites.update()

    # Проверка, не ударил ли моб игрока
    hits_player = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits_player:
        player.shield -= sum(hit.rect.size)*.1
        expl = Explosion(hit.rect.center, 'ss')
        all_sprites.add(expl)
        new_mob()
        if player.shield <= 0:
            death_explosion = Explosion(hit.rect.center, 'player')
            all_sprites.add(death_explosion)
            death_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100
    
    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
	    running = False

    # Проверка, не ударил ли моб игрока
    hits_mobs = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits_mobs:
        score += 450 - sum(hit.rect.size)
        expl = Explosion(hit.rect.center, 'ls')
        all_sprites.add(expl)
        if random.random() > 0.98:
            pu = Pow(hit.rect.center)
            all_sprites.add(pu)
            powerups.add(pu)
        new_mob()

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            pass

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(bg, bg_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, 
               player.lives, player_mini_icon)
    # После отрисовки переворачиваем экран
    pygame.display.flip()

pygame.quit()  