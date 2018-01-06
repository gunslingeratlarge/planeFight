import time
import pygame
from pygame.locals import *
import random

class BasePlane(object):
    def __init__(self,screen,x,y,image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.screen = screen
        self.bullet_list = []

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))
        
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullet_list.remove(bullet)
    #hostile_plane 指的是敌对机，玩家机对于电脑机来说也是敌对机
    def check_hit(self,hostile_plane):
        for bullet in self.bullet_list:
            if bullet.x < hostile_plane.x + 50 and bullet.x > hostile_plane.x and bullet.y<hostile_plane.y + 50 and bullet.y > hostile_plane.y:
                hostile_plane.destory_plane()
    
    def  destory_plane(self):
        self.image = pygame.image.load("./feiji/enemy0_down4.png")
    

        
class HeroPlane(BasePlane):
    def __init__(self,screen):
        BasePlane.__init__(self,screen,200,700,"./feiji/hero1.png")
        self.list = [i for i in range(0,20)]
        self.index = 0

    def move_left(self):
        self.x -= 5 
    def move_right(self):
        self.x += 5   

    def fire(self):
        if self.index > 19:
            self.index = 0
        num = self.list[self.index]
        self.index += 1
        if num == 10:
            self.bullet_list.append(Bullet(self.screen,self.x+40,self.y-15))

    

        
class EnemyPlane(BasePlane):
    def __init__(self,screen):
        BasePlane.__init__(self,screen,200,0,"./feiji/enemy0.png")
        self.direction = "right"

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5
        
        if self.x > 430 :
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"
   
    def fire(self):
        rnum = random.randint(1,100) 
        if(rnum == 2 or rnum==88 or rnum == 50): 
            self.bullet_list.append(EnemyBullet(self.screen,self.x+20,self.y+30))    

class BaseBullet(object):
    def __init__(self,screen,x,y,image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.screen = screen

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))


    
            
class Bullet(BaseBullet):
    def __init__(self,screen,x,y):
        BaseBullet.__init__(self,screen,x,y,"./feiji/bullet.png")

    def move(self):
        self.y -= 10

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False

class EnemyBullet(BaseBullet):
    def __init__(self,screen,x,y):
        BaseBullet.__init__(self,screen,x,y,"./feiji/bullet1.png")
    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 850:
            return True
        else:
            return False

def key_control(hero):
        #获取事件，比如按键等
        
        for event in pygame.event.get():
            print(event)
            #判断是否是点击了退出按钮
            if event.type == pygame.QUIT:
                print("exit")
                exit()
            #判断是否是按下了键
            elif event.type == pygame.KEYDOWN:
                #检测按键是否是a或者left
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    print('left')
                    hero.move_left()
                #检测按键是否是d或者right
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    print('right')
                    hero.move_right()
                #检测按键是否是空格键
                elif event.key == pygame.K_SPACE:
                   # hero.fire()
                    print('space')
                    


def main():
    #1. 创建窗口
    screen = pygame.display.set_mode((480,852),0,32)

    #2. 创建一个背景图片
    background = pygame.image.load("./feiji/background.png")
    

    hero = HeroPlane(screen)
    enemy =  EnemyPlane(screen)

    
    pygame.key.set_repeat(30, 30)
    print(pygame.key.get_repeat())

    while True:
        screen.blit(background, (0,0))

        hero.display()    
        enemy.display()
        enemy.move()
        enemy.fire()
        hero.fire()
        enemy.check_hit(hero)
        hero.check_hit(enemy)
        pygame.display.update()
        key_control(hero)
        time.sleep(0.01)
   

if __name__ == "__main__":
    main()
