from pygame import *
from random import randint
font.init()

main_win = display.set_mode((700, 500))
background = transform.scale(image.load('6560073.jpg'), (700, 500))
display.set_caption('shooter')
mixer.init()
mixer.music.load('forshooter.mp3')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, p_speed, size1, size2):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (size1, size2))
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
        self.speed = p_speed
    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

score = 0
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x <= 695:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 25, self.rect.top, 3, 15, 20)
        bullets.add(bullet)      

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            lost += 1
            self.rect.x = randint(50, 650)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(50, 650), randint(0, 50), 2, 65, 65)
    monsters.add(enemy)
rocket = Player('rocket.png', 345, 395, 5, 65, 100)

bullets = sprite.Group()

game = True
clock = time.Clock()
text = font.Font(None, 30)
text1 = font.Font(None, 50)
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()   

    main_win.blit(background, (0, 0))
    
    if sprite.spritecollide(rocket, monsters, False) or lost == 3:
        finish = True
        loser = text1.render('YOU LOSE!', True, (255, 0, 0))
        main_win.blit(loser, (250, 230))
    
    sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    for s in sprites_list:
        score += 1
        enemy = Enemy('ufo.png', randint(50, 650), randint(0, 50), 2, 65, 65)
        monsters.add(enemy)
    
    if score == 1:
        finish = True
        win = text1.render('YOU WIN!', True, (0, 255, 0))
        main_win.blit(win, (250, 230))

    lose = text.render('Пропущено: ' + str(lost), True, (255, 255, 255))
    main_win.blit(lose, (10, 10))

    scored = text.render('Сбито: ' + str(score), True, (255, 255, 255))
    main_win.blit(scored, (10, 40))

    if not finish:
        rocket.reset()
        rocket.update()
        bullets.draw(main_win)
        bullets.update()
        monsters.draw(main_win)
        monsters.update()

    display.update()
    clock.tick(60)
    