from pygame import *
from random import *
from time import time as timer

window = display.set_mode((700,500))
display.set_caption('Космос')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_music = mixer.Sound('fire.ogg')
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)


class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, p_speed, a, b):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (a, b))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, -10, 10, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -65
            self.rect.x = randint(65, 635)
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

player = Player('rocket.png', 300, 400, 10, 65, 65)
asteroids = sprite.Group()
for f in range(1):
    asteroid = Enemy("asteroid.png", randint(65, 635), -65, randint(1, 5), 65, 65)
    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(10):
    monster1 = Enemy('ufo.png', randint(65, 635), -65, randint(1,5), 65, 65)
    monsters.add(monster1)

num_fire = 0
rel_time = True
lifes = 3
bullets = sprite.Group()
lost = 0
kills = 0
clock = time.Clock()
finish = False
game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
            
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == True:
                    num_fire += 1
                    player.fire()
                    fire_music.play()
                if num_fire >= 5 and rel_time == True:
                    rel_time = False
                    reload_t_1 = timer()
    if finish != True:
        text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_kills = font1.render("Счёт:" + str(kills), 1, (255, 255, 255))
        window.blit(background, (0, 0))
        bullets.draw(window)
        bullets.update()
        player.reset()
        player.move()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        group_spr_cld = sprite.groupcollide(monsters, bullets, True, True)
        for e in group_spr_cld:
            kills += 1
            monster1 = Enemy('ufo.png', randint(65, 635), -65, randint(1,10), 65, 65)
            monsters.add(monster1)
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            lifes -= 1
        if lost >= 100:
            finish = True
            window.blit(font2.render("Проигрыш", 1, (255, 0, 0)), (250, 150))
        if kills >= 10:
            finish = True
            window.blit(font2.render("Выигрыш", 1, (0, 255, 0)), (250, 150))
        if lifes <= 0:
            finish = True
            window.blit(font2.render("Проигрыш", 1, (255, 0, 0)), (250, 150))
        if rel_time == False:
            reload_t_2 = timer()
            if reload_t_2 - reload_t_1 >= 3:
                rel_time = True
                num_fire = 0
            else:
                window.blit(font1.render("Перезарядка...", 1, (255, 255, 255)), (250, 400))
        window.blit(text_lose, (0, 10))
        window.blit(text_kills, (0, 40))
        window.blit(font1.render("Жизни: " + str(lifes), 1, (255, 255, 255)), (570, 10))
    else:
        finish = False
        lost = 0
        kills = 0
        lifes = 3
        num_fire = 0
        rel_time = True
        for monster1 in monsters:
            monster1.kill()
        for asteroid in asteroids:
            asteroid.kill()
        for bullet in bullets:
            bullet.kill()
        for f in range(1):
            asteroid = Enemy("asteroid.png", randint(65, 635), -65, randint(1, 5), 65, 65)
            asteroids.add(asteroid)
        for i in range(10):
            monster1 = Enemy('ufo.png', randint(65, 635), -65, randint(1,5), 65, 65)
            monsters.add(monster1)
            
#jhgfghjkloiuytfcvbnmkuytreszxcvbnjk,mnbvfdfrtyukl

    clock.tick(30)
    display.update()
