import pygame
import os
import sys
import random

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 190
        self.cell_size = 120

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    
    def render(self, screen):
        colors = [pygame.Color("black"), pygame.Color("white")]
        
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 165, 0), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size))
                pygame.draw.rect(screen, colors[self.board[y][x]], (
                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                self.cell_size), 1)
        
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def zombi():
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("zombi.png")
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = random.choice([1050, 1080, 1110, 1140, 1170, 1200, 1230]) 
    sprite.rect.y = random.choice([130, 250, 370, 490, 610])
    return sprite

list_of_levels = [4, 8, 12]
zombi_group = pygame.sprite.Group()
for i in range(list_of_levels[0]):
    sprite = zombi()
    zombi_group.add(sprite)


class Zombi(pygame.sprite.Sprite):
    image = load_image("zombi.png")
    
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Zombi.image
        self.rect = self.image.get_rect()
        
    def update(self, x, y):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


board = Board(10, 5)
step = 5
level = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (level == (len(list_of_levels)) and len(zombi_group) == 0):
            running = False               
    screen.fill((0, 0, 0))
    board.render(screen)
    zombi_group.draw(screen)
    list_group = zombi_group.sprites()
    for sprite in list_group:
        if sprite.rect.x < 0:
            zombi_group.remove(sprite)
        else:
            sprite.rect.x -= step
        if len(zombi_group) == 0 and level < len(list_of_levels):
            for i in range(list_of_levels[level]):
                sprite = zombi()
                zombi_group.add(sprite)
            level += 1
    if level == (len(list_of_levels)) and len(zombi_group) == 0:
        print("1")
        running = False
    pygame.display.flip()
    clock.tick(90)    
pygame.quit()