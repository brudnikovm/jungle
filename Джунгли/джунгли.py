from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire1(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    def fire2(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            global lost_score
            lost_score += 1
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.Font(None, 80) # для победы и проигрыша
font2 = font.Font(None, 36)  # для счетчиков убито пропущено
font3 = font.Font(None, 50) # для жизней

img_back = "фон.jpg" #фон игры
win_width = 700
win_height = 500
display.set_caption("Опасные джунгли")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player('player.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('monkey.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    monsters.add(enemy)

bullets = sprite.Group()

finish = False
run = True #флаг сбрасывается кнопкой закрытия окна
lost_score = 0
max_lost = 10
destroy_score = 0
life = 3
# ! перезарядка
rel_time = False
num_fire = 0

while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 10 and rel_time == False:
                        player.fire1()
                        num_fire += 1
                    if num_fire >= 10 and rel_time == False:
                        last_time = timer()
                        rel_time = True

    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        player.reset()
        player.update()
        # player.fire2()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)

        if sprite.spritecollide(player, monsters, False):
            life -= 1
            sprite.spritecollide(player, monsters, True)


        colides = sprite.groupcollide(monsters, bullets, True, True)
        for c in colides:
            destroy_score += 1
            enemy = Enemy('monkey.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            monsters.add(enemy)

        if life == 0 or lost_score >= max_lost:
            gameOver = font1.render(f'GAME OVER', True, (255,0,0))
            window.blit(gameOver, (200, 300))
            finish = True

        if destroy_score >= 30:
            game_win = font1.render(f'YOU WIN', True, (0,250,0))
            window.blit(game_win, (200, 300))
            finish = True

        destroy = font2.render(f'Убито: {destroy_score}', True, (255,255,255))
        lose = font2.render(f'Пропущено: {lost_score}', True, (255,255,255))
        if life == 3:
            life_color = (0,255,0)
        if life == 2:
            life_color = (255,255,0)
        if life == 1:
            life_color = (255,0,0)
        lifeScore = font3.render(str(life), True, life_color)
        window.blit(destroy, (10, 10))
        window.blit(lose, (10, 50))
        window.blit(lifeScore, (win_width - 40, 20))

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font3.render('Подождите, идет перезарадка',True, (255,0,0))
                window.blit(reload, (70, 440))
            else:
                num_fire = 0
                rel_time = False
        display.update()
    #цикл срабатывает каждые 0.05 секунд
    time.delay(50)