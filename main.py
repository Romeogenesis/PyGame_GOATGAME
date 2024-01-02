import pygame
import os


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
                pygame.draw.rect(screen, colors[self.board[y][x]], (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size))
                pygame.draw.rect(screen, pygame.Color("white"), (
                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                self.cell_size), 1)

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
board = Board(10, 5)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False               
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
pygame.quit()