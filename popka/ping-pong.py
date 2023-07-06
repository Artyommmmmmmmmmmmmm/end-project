from pygame import *
from random import randint
win = display.set_mode((700, 500)) 
display.set_caption('Пинг-Понг') 
background = transform.scale(image.load('back.png'), (700, 500))
win.blit(background, (0, 0))
clock = time.Clock()
font.init()
text = font.Font(None, 40)
class Gamesprite(sprite.Sprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Pong(Gamesprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)

    def move(self, win):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= 5
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += 5
        win.blit(self.image, (self.rect.x, self.rect.y))

class Ball(Gamesprite):
    def __init__(self, pic, x, y, w, h):
        super().__init__(pic, x, y, w, h)
        self.ym = -3
        self.xm = -3


    def floating(self, win):
        if self.rect.y < 1:
            self.ym = 3
        if self.rect.y >= 670:
            self.ym = -3
        self.rect.y += self.ym
        self.rect.x += self.xm
        win.blit(self.image, (self.rect.x, self.rect.y))   

    def left_col(self):
        self.mx = 3
    def right_col(self):
        self.mx = -3


ball = Ball('square.png', 350, 250, 30, 30)
p1 = Pong('square.png', 10, 10, 15, 80)
p2 = Pong('square.png', 690, 10, 15, 80)

loop = True
while loop:
    clock.tick(60)
    win.blit(background, (0, 0))
    ball.floating(win)
    p1.move(win)
    p2.move(win)
    if sprite.spritecollide(ball, p1, False):
        ball.left_col()
    for e in event.get():
        if e.type == QUIT:
            loop = False
    display.update()











