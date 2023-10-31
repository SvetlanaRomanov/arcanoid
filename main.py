import pygame
import time

pygame.init()
back = (200, 255, 255)
mw = pygame.display.set_mode((500, 500))
mw.fill(back)
clock = pygame.time.Clock()

platform_x = 200
platform_y = 350

dx = 4
dy = 4

count_of_monst = 0
time_of_game = 0

game_over = False


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = back

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)


class Pictures(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


ball = Pictures('ball.png', 160, 200, 50, 50)
platform = Pictures('platform.png', platform_x, platform_y, 100, 30)

start_x = 5
start_y = 5
count = 9
monsters = []
move_left = False
move_right = False
for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        d = Pictures('enemy.png', x, y, 50, 50)
        monsters.append(d)
        x = x + 55
    count -= 1

start_time = time.time()
cur_time = start_time
time_text = Label(0, 420, 50, 50, back)
time_text.set_text('Час:', 15, (0, 0, 0))
time_text.draw(20, 20)

timer = Label(64, 440, 50, 40, back)
timer.set_text('0', 15, (0, 0, 0))
timer.draw(0, 0)

score_text = Label(330, 414, 50, 50, back)
score_text.set_text('Pахунок: ', 15, (0, 0, 0))
score_text.draw(20, 20)

score = Label(430, 435, 50, 40, back)
score.set_text('0', 15, (0, 0, 0))
score.draw(0, 0)
while not game_over:
    ball.fill()
    platform.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False


    if ball.rect.y > 350:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text("YOU LOSE", 60, (255, 0, 0))
        time_text.draw(10, 10)
        game_over = True

    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text("YOU WIN", 60, (0, 200, 0))
        time_text.draw(10, 10)


        score_text = Label(150, 90, 50, 50, back)
        score_text.set_text(("Рахунок: " + str(count_of_monst)), 15, (255, 0, 0))
        score_text.draw(10, 10)

        game_over = True
    if ball.rect.colliderect(platform.rect):
        dy *= 1
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            count_of_monst += 1
            monsters.remove(m)
            m.fill()
            dy *= -1
        score.set_text(str(count_of_monst), 15, (0, 0, 0))
        score.draw(0, 0)

    new_time = time.time()
    if int(new_time) - int(cur_time) >= 1:
        timer.set_text(str(int(new_time - start_time)), 15, (0, 0, 0))
        timer.draw(0, 0)
        cur_time = new_time
    if platform.rect.x < 0:
        move_left = False
    elif platform.rect.x > 400:
        move_right = False
    if move_right:
        platform.rect.x += 5
    elif move_left:
        platform.rect.x -= 5

    for m in monsters:
        m.draw()

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    if ball.rect.colliderect(platform.rect):
        dy *= -1

    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(40)