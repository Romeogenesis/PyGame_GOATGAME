import pygame

class Plant(pygame.sprite.Sprite):
    image = load_image("plant.png")

    def __init__(self, *groupx, x, y):
        super().__init__(*group)
        self.image = Plant.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1, 
                                   random.randrange(3) - 1)