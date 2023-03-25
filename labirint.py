from pygame import *
img_back = 'fon.png'
img_hero = 'red.png'
img_enemy = 'peg.png'
img_goal = 'chak.png'
img_bullet ='bomb.png'

mixer.init()
mixer.music.load('Angry-Birds-_4_.ogg')
mixer.music.play()
fire = mixer.Sound('bird-01-flying.ogg')

font.init()
font = font.SysFont('Comic Sans MS',50)
win = font.render('you win!',True,(255,255,0))
lose = font.render('you lose',True,(255,255,255))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x,player_y,width,height,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed = player_speed
        self.rect  = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_widht - 45:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 45:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery,25,25,10)
        bullets.add(bullet)
class Enemy(GameSprite):
    side = "left"
    def update(self):
        if self.rect.x <= 190:
            self.side = "right"
        if self.rect.x >= win_widht - 225:
            self.side = "left"
        if self.side == "left":
            self .rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Enemy2(GameSprite):
    side = "up"
    def update(self):
        if self.rect.y <= 30:
            self.side = "up"
        if self.rect.y >= win_widht - 500:
            self.side = "down"
        if self.side == "down":
            self .rect.y -= self.speed
        else:
            self.rect.y += self.speed
class Wall(sprite.Sprite):
    def __init__(self, red, green,blue, wall_x, wall_y, width,height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.w = width
        self.h = height
        self.image = Surface((self.w, self.h))
        self.image.fill((red,green,blue))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_widht+10:
            self.kill()

'''окно игры'''
win_widht = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_widht, win_height))
back = transform.scale(image.load(img_back),(win_widht,win_height))

hero = Player(img_hero,5,win_height - 80,40,40,5)
monster = Enemy(img_enemy, win_widht - 225,330,65,65,2)
final = GameSprite(img_goal, win_widht - 120,win_height - 80,65,65,0)
monster2 = Enemy2(img_enemy, win_widht - 507,30,65,65,2)
monster3 = Enemy2(img_enemy, win_widht - 507,30,65,65,2)

w1 = Wall(102,255,0,90,20,460,10)
w2 = Wall(102,255,0,90,20,10,380)
w3 = Wall(102,255,0,90,480,450,10)
w4 = Wall(102,255,0,180,100,10,380)
w5 = Wall(102,255,0,180,400,90,10)
w6 = Wall(102,255,0,340,400,200,10)
w7 = Wall(102,255,0,540,400,10,90)
w9 = Wall(102,255,0,260,100,10,220)
w10 = Wall(102,255,0,340,100,10,220)
w11 = Wall(102,255,0,540,100,10,300)
w12 = Wall(102,255,0,460,20,10,300)
w13 = Wall(102,255,0,340,100,120,10)

bullets = sprite.Group()
monsters = sprite.Group()
walls = sprite.Group()

monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)
walls.add(w6)
walls.add(w7)
walls.add(w9)
walls.add(w10)
walls.add(w11)
walls.add(w12)
walls.add(w13)

points = 0 

game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
                fire.play()
    if finish != True:
        window.blit(back,(0,0))
        walls.draw(window)
        monsters.update()
        monsters.draw(window)
        hero.reset()
        hero.update()
        final.reset()
        bullets.draw(window)
        bullets.update()
        sprite.groupcollide(bullets,walls, True,False)
        if sprite.groupcollide(bullets,monsters,True,True):
            points += 1
        x = font.render(str(points),True,(255,255,255))
        window.blit(x, (20, 20))

        if sprite.spritecollide(hero,walls,False):
            finish = True
            window.blit(lose,(200,200))
        
        if sprite.spritecollide(hero,monsters,False):
            finish = True
            window.blit(lose,(200,200))

        if sprite.collide_rect(hero,final):
            finish = True
            window.blit(win,(200,200))

    display.update()
    clock.tick(FPS)