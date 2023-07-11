from time import sleep
from pygame import *
from random import randint
win = display.set_mode((1000, 700)) #создание окна
display.set_caption('Dungeon labyrinth') #надпись на окне
background = transform.scale(image.load('back.png'), (1000, 700)) #загрузка изображения для заднего фона
win.blit(background, (0, 0)) #установка заднего фона
clock = time.Clock() #определение клока
font.init()
text = font.Font(None, 20)#шрифт для малых надписей
text_big = font.Font(None, 40)# шрифт для больших надписей


class Gamesprite(sprite.Sprite):#основной класс
    def __init__(self, pic, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# желательно сначала ознакомится со строением платформ на строке 207

class Player(Gamesprite):#игрок
    def __init__(self, pic, blink, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.blink_image = transform.scale(image.load(blink), (w, h))#введение картинки
        #которая появляется при мигании игрока от получения урона
        self.group = sprite.Group()
        self.group.add(self)# группа себя для удобства
        self.up = 4#скорость взлёта при прыжке jump
        self.down = 3#скорость падения gravity
        self.t = 0#таймер для jump
        self.endurable = 0#таймер неуязвимости для blinking
        self.j = False#инициализация для jump_init
        self.dmtaken = False#для не получения урона при неуязвимости blinking
        self.hp = 5#здоровье игрока blinking
        self.blink = False#если True то на экране выводится self.blink_image 
        # self.image вместо blinking gravity
        self.spring_init = False#инициализация пружинки touch_spring
        self.spring_timer = 0#таймер для пружинки touch_spring
        self.spring_speed = 15#скорость взлёта на пружине touch_spring
        self.dash_able = False#возможен ли рывок dash_left dash_right
        self.dash_bool_left = False#инициализация прыжка влево dash_left
        self.dash_bool_right = False#инициализация рывка вправо dash_right
        self.dash_active = False#рывок происходит dash_left dash_right
        self.dash_timer = 0# таймер рывка dash_left dash_right
        self.dash_speed = 10#скорость рывка dash_left dash_right


    def gravity(self, win):#отображает игрока и заставляет его падать
        if not sprite.groupcollide(self.group, platform_up, False, False) and self.t == 0 and not self.dash_active:
            self.rect.y += self.down
        if sprite.groupcollide(self.group, platform_up, False, False) and self.t == 0:
            self.dash_able = True

        
        win.blit(self.image, (self.rect.x, self.rect.y))
        
        if self.blink:
            win.blit(self.blink_image, (self.rect.x, self.rect.y))
    def blinking(self):#получение урона и таймер неуязвимости

        if sprite.groupcollide(self.group, enemies, False, False) and self.dmtaken == False:
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
        if self.endurable > 60:#неуязвимость длится секунду - 60 тиков
            self.dmtaken = False
            self.endurable = 0


    def move(self):#движение влево вправо
        if keys[K_LEFT]\
         and not sprite.groupcollide(self.group, platform_right, False, False):
            self.rect.x -= 3
        if keys[K_RIGHT]\
         and not sprite.groupcollide(self.group, platform_left, False, False):
            self.rect.x += 3

    def jump_init(self):#инициализация прыжка
        if keys[K_UP] and sprite.groupcollide(self.group, platform_up, False, False):
            self.j = True


    def jump(self):#прыжок
        if self.j:
            self.t += 1
            if self.t > 0:
                self.rect.y -= self.up
            if sprite.groupcollide(self.group, platform_down, False, False):
                #столкновение с потолком
                self.t = 0
                self.j = False
            if self.t == 30:#прыжок происходит пол секунды - 30 тиков
                self.t = 0
                self.j = False
            if self.dash_active:#после рывка прыжок тоже останавливается
                self.t = 0
                self.j = False

    def touch_spring(self):#касание пружины - зелёный прямоугольник
        if sprite.groupcollide(self.group, active_room_spring, False, False):
            self.spring_init = True
        if self.spring_init:
            self.spring_timer += 1
            self.rect.y -= self.spring_speed
            if self.spring_timer == 20:# прыжок на пружине длится треть секунды - 20 тиков
                self.spring_init = False
                self.spring_timer = 0 
            if sprite.groupcollide(self.group, platform_down, False, False):
                #столкновение с потолком останавливет взлёт
                self.spring_init = False
                self.spring_timer = 0 
            if self.dash_active:#рывок останавливает взлёт
                self.spring_init = False
                self.spring_timer = 0 

    def dash_left(self):#рывок влево
        if keys[K_n] and self.dash_able:
            self.dash_bool_left = True
        if self.dash_bool_left and not sprite.groupcollide(self.group, platform_right, False, False):          
            self.dash_active = True
            self.dash_able = False
            self.dash_timer += 1
            self.rect.x -= self.dash_speed
        if self.dash_timer == 5:#рывок происходи 5 тиков, секунда - 60 тиков
            self.dash_active = False
            self.dash_timer = 0
            self.dash_bool_left = False
        if sprite.groupcollide(self.group, platform_right, False, False) and self.dash_active:
            #в отличии от рывка вправо останавливается при столкновении
            #с правым краем твёрдых (белых) объектов
            self.rect.x += self.dash_speed
            self.dash_active = False
            self.dash_timer = 0
            self.dash_bool_left = False

    def dash_right(self):#рывок вправо
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
            #в отличии от рывка влево останавливается при столкновении
            #с левым краем твёрдых (белых) объектов
            self.rect.x -= self.dash_speed
            self.dash_active = False
            self.dash_timer = 0
            self.dash_bool_right = False
 



class Enemy(Gamesprite):#враг красный
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)

class Spring(Gamesprite):#пружина зелёная
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.group = sprite.Group()
        self.group.add(self)



class Platform(Gamesprite):#твёрдый объект белый
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)


    def exist(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Teleport(Gamesprite):#телепорт фиолетовый
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.group = sprite.Group()
        self.group.add(self)

    def exist(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Treasure(Gamesprite):#сокровище главная цель жёлтая
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)


def create_room1(pic, x, y, w, h):#создаёт твёрдый объект в первой комнате (второй комнаты нет)
    #работает чисто на математике при значении шир и выс меньше 5 работает неккоректно
    platform_left = Platform(pic, x, y+3, int(w/2), h-3)
    room1left.add(platform_left)#левый край объекта
    platform_up = Platform(pic, x+3, y, w-3, int(h/2))
    room1up.add(platform_up)#верхний край объекта
    w1 = int(w/2)
    x1 = w1-3
    y1 = y - w1
    platform_right = Platform(pic, x+x1, y+3, w1 + 6, h-3)
    room1right.add(platform_right)#правый край объекта
    h1 = h/2
    y1 = int(y+h1)
    platform_down = Platform(pic, x+3, y1, w-3, int(h/2))
    room1down.add(platform_down)#низ объекта




room1left = sprite.Group()
room1right = sprite.Group()
room1up = sprite.Group()
room1down = sprite.Group()
#группы для каёв объектов
room1spring = sprite.Group()
#группа для пружин
room1enemies = sprite.Group()
#группа для опасных объектов
room1treasure = sprite.Group()
#группа для сокровищ

#объекты создаются и сразу добавляются
treasure = Treasure('treasure.png', 10, 630, 20, 20)
room1treasure.add(treasure)

r1teleport1 = Teleport('teleport.png', 100, 695, 800, 100)


r1spring1 = Spring('spring.png', 153, 270, 227, 5)
room1spring.add(r1spring1)

r1enemy1 = Enemy('attack.png', 153, 250, 227, 20)
r1enemy2 = Enemy('attack.png', 690, 135, 30, 5)
r1enemy3 = Enemy('attack.png', 790, 135, 30, 5)
r1enemy4 = Enemy('attack.png', 890, 135, 30, 5)
r1enemy5 = Enemy('attack.png', 100, 670, 800, 100)
r1enemy6 = Enemy('attack.png', 405, 490, 50, 5)
r1enemy7 = Enemy('attack.png', 343, 540, 50, 5)
r1enemy8 = Enemy('attack.png', 405, 590, 50, 5)
r1enemy9 = Enemy('attack.png',335, 410, 120, 5)

room1enemies.add(r1enemy1)
room1enemies.add(r1enemy2)
room1enemies.add(r1enemy3)
room1enemies.add(r1enemy4)
room1enemies.add(r1enemy5)
room1enemies.add(r1enemy6)
room1enemies.add(r1enemy7)
room1enemies.add(r1enemy8)
room1enemies.add(r1enemy9)



#функция самостоятельно раскладывает всё по группам(создание оъестов)
create_room1('square.png', -24, 0, 20, 700)
create_room1('square.png', 1000, 0, 20, 700)
create_room1('square.png', 0, -20, 1000, 20)
create_room1('square.png', 0, 100, 150, 200)
create_room1('square.png', 380, -100, 300, 150)
create_room1('square.png', 380, 140, 300, 150)
create_room1('square.png', 680, 0, 500, 105)
create_room1('square.png', 670, 140, 250, 150)
create_room1('square.png', 900, 650, 400, 50)

create_room1('square.png', 750, 600, 15, 10)
create_room1('square.png', 600, 500, 30, 10)
create_room1('square.png', 610, 505, 10, 500)
create_room1('square.png', 500, 650, 15, 10)
create_room1('square.png', 550, 250, 10, 350)
create_room1('square.png', 400, 650, 15, 10)
create_room1('square.png', 0, 270, 920, 100)
create_room1('square.png', 455, 350, 15, 250)
create_room1('square.png', 330, 450, 10, 350)
create_room1('square.png', 230, 450, 10, 350)
create_room1('square.png', 130, 450, 10, 350)
create_room1('square.png', 280, 350, 10, 65)
create_room1('square.png', 180, 350, 10, 65)
create_room1('square.png', 0, 650, 98, 600)

create_room1('square.png', 330, 630, 50, 100)
create_room1('square.png', 405, 580, 50, 10)
create_room1('square.png', 340, 530, 50, 10)
create_room1('square.png', 405, 480, 50, 10)
create_room1('square.png', 335, 400, 120, 10)





#создание игрока
player = Player('blu.png', 'blink.png', 10, 10, 20, 20)


player_health = text.render("HP " + str(player.hp), True, (255, 255, 255))
#здоровье игрока
death = text_big.render('Вы погибли', True, (255, 50, 50))
#смерть игрока
winner = text_big.render('Вы добрались до сокровища', True, (150, 150, 250))
#победа игрока



room1active = True#игрок находится в комнате 1
loop = True
while loop:
    clock.tick(60)
    keys = key.get_pressed()
    win.blit(background, (0, 0))#отображение фона
    
    win.blit(player_health, (10, 10))#отображение здоровья

    for e in event.get():#реализация выхода на крестик
        if e.type == QUIT:
            loop = False

    if room1active:#комната 1
        platform_left = room1left
        platform_right = room1right
        platform_up = room1up
        platform_down = room1down
        active_room_spring = room1spring
        enemies = room1enemies
        treasure = room1treasure
        #назначение групп
        platform_left.draw(win)
        platform_right.draw(win)
        platform_up.draw(win)
        platform_down.draw(win)
        active_room_spring.draw(win)
        enemies.draw(win)
        r1teleport1.exist(win)
        treasure.draw(win)
        #отображение всех объектов
        player.gravity(win)
        player.move()
        player.jump_init()
        player.jump()
        player.touch_spring()
        player.blinking()
        player.dash_left()
        player.dash_right()
        #включение всех возможностей игрока
        if sprite.groupcollide(player.group, r1teleport1.group, False, False):
            player.rect.x = 950
            player.rect.y = 600
            #столкновение с  тп переносит игрока в указанную точку
        if sprite.groupcollide(player.group, treasure, False, False):
            win.blit(winner, (280, 300))
            display.update()
            sleep(2)
            loop = False
            #столкновение игрока с сокровищем заканчивает игру

    player_health = text.render("HP " + str(player.hp), True, (255, 255, 255))
    #изменение здоровья игрока на интерфейсе
    if player.hp == 0:
        win.blit(death, (360, 300))
        display.update()
        sleep(2)
        loop = False
        #реализация проигрыша от конца здоровья
    display.update()












