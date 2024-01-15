import pygame
import os
import sys
import random
from board import Board


def main():
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    zombi_hp_dict = {}
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

    class Plant(pygame.sprite.Sprite):
        image = load_image("plant.png")
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = Plant.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = x
            self.rect.y = y
            self.count = 0
            self.frequency = 1

        def update(self):
            if self.count == 150:
                self.bullet = Bullet(self.rect.x + 50, self.rect.y + 5)
                bullet_group.add(self.bullet)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('data\shot.mp3'))
                self.count = 0
            self.count += self.frequency
            if pygame.sprite.groupcollide(zombi_group, plant_group, False, True):
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('data\plant_die.mp3'))


    class Zombi(pygame.sprite.Sprite):
        image = load_image("zombi.png")
        def __init__(self, HP):
            super().__init__(zombi_group)
            self.image = Zombi.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = random.choice([1050, 1100, 1150, 1200, 1250, 1300, 1350]) 
            self.rect.y = random.choice([130, 250, 370, 490, 610])
            self.HP = HP
            self.damage = 1

        def update(self):
            collision_dict = pygame.sprite.groupcollide(bullet_group, zombi_group, False, False)
            for current_key, val in collision_dict.items():
                key = id(val[0])
                if key in zombi_hp_dict:
                    zombi_hp_dict[key] -= self.damage
                    if zombi_hp_dict[key] <= 0:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data\zombi_die.mp3'))
                        val[0].kill()
                else:
                    zombi_hp_dict[key] = self.HP - self.damage
                current_key.kill()
            
    class Bullet(Plant):
        image = load_image("bullet.png")
        def __init__(self, x, y):
            super().__init__(x, y)
            self.image = Bullet.image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = 5

        def update(self):
            self.bullet_list = bullet_group.sprites()
            for bullet in self.bullet_list:
                bullet.rect.x += self.speed
                if bullet.rect.x > 1200:
                    bullet.kill()
            
    def add_plant(x, y):
        x = (int(x / 120) * 120) + 20
        y = (int((y - 190)/ 120) * 120 + 190) + 20
        plant = Plant(x, y)
        if pygame.sprite.spritecollide(plant, plant_group, False):
            plant.kill()
            return False
        else:
            bullet = Bullet(x + 50, y + 5)
            bullet_group.add(bullet)
            plant_group.add(plant)
            return True

    list_of_levels = [4, 7, 11, 15, 20, 26, 34, 37, 37]
    zombi_group = pygame.sprite.Group()
    plant_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    for i in range(list_of_levels[0]):
        zombi = Zombi(4)
        zombi_group.add(zombi)
    board = Board(10, 5)
    step = 1
    level = 1
    energy = 0
    total_energy = pygame.font.Font(None, 50)
    total_energy_out = total_energy.render(f"энергия: {energy}", False,
                    (0, 180, 0))
    energy_count = 0
    zombi_count = 0
    total_zombi = pygame.font.Font(None, 50)
    current_zombi_out = total_energy.render(f"зомби прошло: {zombi_count}/6", False,
                    (0, 180, 0))
    total_wave = pygame.font.Font(None, 50)
    total_wave_out = total_energy.render(f"волна: {level}/9", False,
                    (0, 180, 0))
    energy_out = 0
    limit_of_zombi = 6
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (level == (len(list_of_levels)) and len(zombi_group) == 0):
                running = False      
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and energy >= 150 and (200 <= y <= 800):
                success_plant = add_plant(x, y)
                if success_plant:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('data\shot.mp3'))
                    energy -= 150     
                    energy_out -= 150
                    total_energy_out = total_energy.render(f"энергия: {energy_out}", False,(0, 180, 0))
        screen.fill((0, 0, 0))
        board.render(screen)
        screen.blit(total_energy_out, (10, 10))
        current_zombi_out = total_energy.render(f"зомби прошло {zombi_count}/6", False, (0, 180, 0))
        screen.blit(current_zombi_out, (10, 50))
        total_wave_out = total_energy.render(f"волна: {level}/9", False, (0, 180, 0))
        screen.blit(total_wave_out, (10, 90))
        plant_group.draw(screen)
        zombi_group.draw(screen)
        bullet_group.draw(screen)
        plant_group.update()
        bullet_group.update()
        zombi_group.update()
        list_group = zombi_group.sprites()
        for sprite in list_group:
            if sprite.rect.x < 0:
                zombi_group.remove(sprite)
                zombi_count += 1
                if zombi_count >= limit_of_zombi:
                    running = False
                    break
            else:
                sprite.rect.x -= step    
        if len(zombi_group) == 0 and level < len(list_of_levels):
                for i in range(list_of_levels[level]):
                    zombi = Zombi(4)
                    zombi_group.add(zombi)
                level += 1        
        if level == (len(list_of_levels)) and len(zombi_group) == 0:               
            running = False
        if energy_count == 150:
            energy_out += 150
            total_energy_out = total_energy.render(f"энергия: {energy}", False,(0, 180, 0))
            energy_count = 0
        energy_count += 1
        energy += 1
        pygame.display.flip()
        clock.tick(50)    