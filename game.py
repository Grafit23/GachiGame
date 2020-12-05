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
        self.image = player_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100

    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 8

        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        random.choice(shoot_sounds).play()

class Mob(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemy_images)
        self.image_orig.set_colorkey(BLACK)
        self.image_orig = pygame.transform.scale(
            self.image_orig, 
            (random.randint(25, 150), random.randint(25, 150))
            )
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
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
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


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
player_img = pygame.image.load(path.join(img_folder, r"billy_player.jpg")).convert()
player_img = pygame.transform.scale(player_img, (50, 40))
# Спрайт врагов
enemy_images = []
for i in range(4):
    enemy_img = pygame.image.load(path.join(img_folder, f"enemy_{i}.jpg")).convert()  
    enemy_images.append(enemy_img)
# Спрайт снарядов
bullet_img = pygame.image.load(path.join(img_folder, r"heart.jpg")).convert()
bullet_img = pygame.transform.scale(bullet_img, (10, 20))


# Звуки
shoot_sounds = []
for i in range(1, 5):
    shoot_sounds.append(pygame.mixer.Sound(path.join(sound_folder, f"Orgasm_{i}.mp3")))
shoot_sounds.append(pygame.mixer.Sound(path.join(sound_folder, "Orgasm_6.mp3")))
exp_sound = pygame.mixer.Sound(path.join(sound_folder, "fuck you....mp3"))

# Музыка
pygame.mixer.music.  load(path.join(music_folder, "cadilac.mp3"))
pygame.mixer.music.set_volume(0.4)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Обновления
    all_sprites.update()

    # Проверка, не ударил ли моб игрока
    hits_player = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits_player:
        player.shield -= sum(hit.rect.size)*.1
        new_mob()
        if player.shield <= 0:
            running = False
    
    # Проверка, не ударил ли моб игрока
    hits_mobs = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits_mobs:
        score += 300 - sum(hit.rect.size)
        new_mob()

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(bg, bg_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    # После отрисовки переворачиваем экран
    pygame.display.flip()

pygame.quit()  