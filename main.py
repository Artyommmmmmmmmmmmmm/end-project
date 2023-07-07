print("hello")
import sys
from time import sleep
from pygame import *
from random import randint
win = display.set_mode((1000, 700)) 
display.set_caption('Dungeon labyrinth') 
background = transform.scale(image.load('back.png'), (1000, 700)) #загрузка изображения для заднего фона
win.blit(background, (0, 0))
clock = time.Clock()
font.init()
text = font.Font(None, 20)
text_big = font.Font(None, 40)


class Gamesprite(sprite.Sprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(Gamesprite):
    def __init__(self, pic, blink, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.blink_image = transform.scale(image.load(blink), (w, h))
        self.group = sprite.Group()
        self.group.add(self)
        self.up = 4
        self.down = 3
        self.t = 0
        self.endurable = 0
        self.j = False
        self.dmtaken = False
        self.hp = 99
        self.blink = False
        self.spring_init = False
        self.spring_timer = 0
        self.spring_speed = 15
        self.dash_able = False
        self.dash_bool_left = False
        self.dash_bool_right = False
        self.dash_active = False
        self.dash_timer = 0
        self.dash_speed = 12


    def gravity(self, win):
        if not sprite.groupcollide(self.group, platform_up, False, False) and self.t == 0 and not self.dash_active:
            self.rect.y += self.down
        if sprite.groupcollide(self.group, platform_up, False, False) and self.t == 0:
            self.dash_able = True

        
        win.blit(self.image, (self.rect.x, self.rect.y))
        
        if self.blink:
            win.blit(self.blink_image, (self.rect.x, self.rect.y))
    def blinking(self):

        if sprite.groupcollide(self.group, enemies, False, False) and self.dmtaken == False:
            print(self.hp)
            self.hp -= 1
            self.dmtaken = True
            self.endurable += 1
        if self.endurable != 0:
            self.endurable += 1
        if self.endurable != 0 and self.endurable < 11:
            self.blink = True
        if self.endurable >10 and self.endurable < 21:
            self.blink = False
        if self.endurable >20 and self.endurable < 31:
            self.blink = True
        if self.endurable >30 and self.endurable < 41:
            self.blink = False
        if self.endurable >40 and self.endurable < 51:
            self.blink = True
        if self.endurable >50 and self.endurable < 61:
            self.blink = False
        if self.endurable > 60:
            self.dmtaken = False
            self.endurable = 0


    def move(self):
        if keys[K_LEFT]\
         and not sprite.groupcollide(self.group, platform_right, False, False):
            self.rect.x -= 3
        if keys[K_RIGHT]\
         and not sprite.groupcollide(self.group, platform_left, False, False):
            self.rect.x += 3

    def jump_init(self):
        if keys[K_UP] and sprite.groupcollide(self.group, platform_up, False, False):
            self.j = True


    def jump(self):
        if self.j:
            self.t += 1
            if self.t > 0:
                self.rect.y -= self.up
            if sprite.groupcollide(self.group, platform_down, False, False):
                self.t = 0
                self.j = False
            if self.t == 30:
                self.t = 0
                self.j = False
            if self.dash_active:
                self.t = 0
                self.j = False

    def touch_spring(self):
        if sprite.groupcollide(self.group, active_room_spring, False, False):
            self.spring_init = True
        if self.spring_init:
            self.spring_timer += 1
            self.rect.y -= self.spring_speed
            if self.spring_timer == 20:
                self.spring_init = False
                self.spring_timer = 0 
            if sprite.groupcollide(self.group, platform_down, False, False):
                self.spring_init = False
                self.spring_timer = 0 
            if self.dash_active:
                self.spring_init = False
                self.spring_timer = 0 

    def dash_left(self):
        if keys[K_n] and self.dash_able:
            self.dash_bool_left = True
        if self.dash_bool_left and not sprite.groupcollide(self.group, platform_right, False, False):          
            self.dash_active = True
            self.dash_able = False
            self.dash_timer += 1
            self.rect.x -= self.dash_speed
        if self.dash_timer == 5:
            self.dash_active = False
            self.dash_timer = 0
            self.dash_bool_left = False
        if sprite.groupcollide(self.group, platform_right, False, False) and self.dash_active:
            self.rect.x += 10
            self.dash_active = False
            self.dash_timer = 0
            self.dash_bool_left = False

    def dash_right(self):
        if keys[K_m] and self.dash_able:
            self.dash_bool_right = True
        if self.dash_bool_right and not sprite.groupcollide(self.group, platform_left, False, False):          
            self.dash_active = True
            self.dash_able = False
            self.dash_timer += 1
            self.rect.x += self.dash_speed
        if self.dash_timer == 5:
            self.dash_active = False
            self.dash_timer = 0
            self.dash_bool_right = False
        if sprite.groupcollide(self.group, platform_left, False, False) and self.dash_active:
            self.rect.x -= 10
            self.dash_active = False
            self.dash_timer = 0
            self.dash_bool_right = False
 




class Enemy(Gamesprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)

class Spring(Gamesprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.group = sprite.Group()
        self.group.add(self)

class Door(Gamesprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.group = sprite.Group()
        self.group.add(self)

    def exist(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Platform(Gamesprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)


    def exist(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Teleport(Gamesprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.group = sprite.Group()
        self.group.add(self)

    def exist(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


def create_room1(pic, x, y, w, h):
    platform_left = Platform(pic, x, y+3, int(w/2), h-3)
    room1left.add(platform_left)
    platform_up = Platform(pic, x+3, y, w-3, int(h/2))
    room1up.add(platform_up)
    w1 = int(w/2)
    x1 = w1-3
    y1 = y - w1
    platform_right = Platform(pic, x+x1, y+3, w1 + 6, h-3)
    room1right.add(platform_right)
    h1 = h/2
    y1 = int(y+h1)
    platform_down = Platform(pic, x+3, y1, w-3, int(h/2))
    room1down.add(platform_down)

def create_room2(pic, x, y, w, h):
    platform_left = Platform(pic, x, y+3, int(w/2), h-3)
    room2left.add(platform_left)
    platform_up = Platform(pic, x+3, y, w-3, int(h/2))
    room2up.add(platform_up)
    w1 = int(w/2)
    x1 = w1-3
    y1 = y - w1
    platform_right = Platform(pic, x+x1, y+3, w1 + 6, h-3)
    room2right.add(platform_right)
    h1 = h/2
    y1 = int(y+h1)
    platform_down = Platform(pic, x+3, y1, w-3, int(h/2))
    room2down.add(platform_down)


room1left = sprite.Group()
room1right = sprite.Group()
room1up = sprite.Group()
room1down = sprite.Group()
room1spring = sprite.Group()
room1enemies = sprite.Group()


r1teleport1 = Teleport('teleport.png', 100, 695, 800, 100)


r1spring1 = Spring('spring.png', 153, 270, 227, 5)
room1spring.add(r1spring1)

r1enemy1 = Enemy('attack.png', 153, 250, 227, 20)
r1enemy2 = Enemy('attack.png', 690, 135, 30, 5)
r1enemy3 = Enemy('attack.png', 790, 135, 30, 5)
r1enemy4 = Enemy('attack.png', 890, 135, 30, 5)
r1enemy5 = Enemy('attack.png', 100, 670, 800, 100)
room1enemies.add(r1enemy1)
room1enemies.add(r1enemy2)
room1enemies.add(r1enemy3)
room1enemies.add(r1enemy4)
room1enemies.add(r1enemy5)

r1door_to_room2 = Door('Door.png', 7000, 250, 50, 90)


create_room1('square.png', -24, 0, 20, 700)
create_room1('square.png', 1000, 0, 20, 700)
create_room1('square.png', 0, -20, 1000, 20)
create_room1('square.png', 0, 100, 150, 200)
create_room1('square.png', 380, -100, 300, 150)
create_room1('square.png', 380, 140, 300, 150)
create_room1('square.png', 680, 0, 500, 105)
create_room1('square.png', 670, 140, 250, 150)
create_room1('square.png', 900, 650, 400, 50)
#250 - 700, 100 - 900
create_room1('square.png', 750, 600, 15, 10)
create_room1('square.png', 600, 500, 30, 10)
create_room1('square.png', 610, 505, 10, 500)
create_room1('square.png', 500, 650, 15, 10)
create_room1('square.png', 550, 250, 10, 350)



room2left = sprite.Group()
room2right = sprite.Group()
room2up = sprite.Group()
room2down = sprite.Group()

create_room2('square.png', 0, 500, 1000, 10)
player = Player('blu.png', 'blink.png', 10, 10, 20, 20)


player_health = text.render("HP " + str(player.hp), True, (255, 255, 255))
death = text_big.render('Вы погибли', True, (255, 50, 50))
# room2 = sprite.Group()
# group.add(rocket)
# enemy_group = sprite.Group()
# enemy_group.add(Enemy('ufo.png'))
room2active = False
room1active = True
loop = True
while loop:
    clock.tick(60)
    keys = key.get_pressed()
    win.blit(background, (0, 0))
    
    win.blit(player_health, (10, 10))

    for e in event.get():
        if e.type == QUIT:
            loop = False

    if room1active:
        platform_left = room1left
        platform_right = room1right
        platform_up = room1up
        platform_down = room1down
        active_room_spring = room1spring
        enemies = room1enemies
        platform_left.draw(win)
        platform_right.draw(win)
        platform_up.draw(win)
        platform_down.draw(win)
        active_room_spring.draw(win)
        enemies.draw(win)
        r1door_to_room2.exist(win)
        r1teleport1.exist(win)
        player.gravity(win)
        player.move()
        player.jump_init()
        player.jump()
        player.touch_spring()
        player.blinking()
        player.dash_left()
        player.dash_right()
        if sprite.groupcollide(player.group, r1door_to_room2.group, False, False):
            room1active = False
            room2active = True
        if sprite.groupcollide(player.group, r1teleport1.group, False, False):
            player.rect.x = 950
            player.rect.y = 600
    if room2active:
        platform_left = room2left
        platform_right = room2right
        platform_up = room2up
        platform_down = room2down
        platform_left.draw(win)
        platform_right.draw(win)
        platform_up.draw(win)
        platform_down.draw(win)
        player.gravity(win)
        player.move()
        player.jump_init()
        player.jump()
        player.touch_spring()
        player.blinking()
        player.dash_left()
        player.dash_right()

    player_health = text.render("HP " + str(player.hp), True, (255, 255, 255))
    if player.hp == 0:
        win.blit(death, (280, 250))
        display.update()
        sleep(2)
        loop = False
    display.update()












