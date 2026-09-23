from abc import ABC, abstractmethod
import pygame
import random

class GameObject(ABC):
    def __init__(self, x, y, window, health, image_png):
        self._health = health
        self.window = window
        self.image = pygame.image.load(image_png)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_width = self.window.get_width() - self.rect.width
        self.max_height = self.window.get_height() - self.rect.height
        
    @abstractmethod
    def move(self):
        raise NotImplementedError
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = value
    
    def draw(self):
        self.window.blit(self.image, self.rect)

class Player(GameObject):
    def __init__(self, window, x, y):
        super().__init__(x, y, window, 100, 'images/rocket (1).png')
        self.bullets = []
    
    def move(self, keys):
        """If left arrow is pressed and player is not on
        the left edge of the screen, move left, and do 
        the same thing with right arrow"""
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.x < self.max_width:
            self.rect.x += 5

        
    def shoot(self):
        if len(self.bullets) < 5:
            bullet = PlayerBullet(self.window, self.rect.x + self.rect.width // 2, self.rect.y)
            self.bullets.append(bullet)
    
    def update_bullets(self):
        "make the bullets move"
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)
    
    def draw(self):
        """Draw the player and its bullets"""
        self.window.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw()

class Enemy(GameObject):
    images = ['images/alien-ship (1).png', 
              'images/alien.png', 'images/space-ship (1).png',
              'images/ufo (2).png']
    
    def __init__(self, window, x, y):
        super().__init__(x, y, window, 1, random.choice(Enemy.images))
        self.bullets = []
        self._speed = 5
    
    def move(self):
        """Move from left to right. Once it reaches either side
        make it go the other direction"""
        self.rect.x += self._speed
        if self.rect.x < 0:
            self._speed = abs(self._speed)
        elif self.rect.x > self.max_width:
            self._speed = -1 * abs(self._speed)
        
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = value

    def shoot(self):
        """One bullet is shoot every 5 seconds"""
        if len(self.bullets) < 1:
            bullet = EnemyBullet(self.window, self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height)
            self.bullets.append(bullet)
    
    def update_bullets(self):
        """update the bullets if bullet collide with player remove bullet"""
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.rect.y > self.window.get_height():
                self.bullets.remove(bullet)
            
        

    def draw(self):
        """Draw the enemy"""
        self.window.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw()



class PlayerBullet(GameObject):

    def __init__(self, window, x, y):
        super().__init__(x, y, window, 1, 'images/bullet (1).png')
    
    def move(self):
        self.rect.y -= 5

    def draw(self):
        """draw the bullet"""
        self.window.blit(self.image, self.rect)


class EnemyBullet(GameObject):
    def __init__(self, window, x, y):
        super().__init__(x, y, window, 1, 'images/bullet (1).png')

    def move(self):
        """Allow the bullet to move up the screen"""
        self.rect.y += 5
   
    def draw(self):
        """Draw the bullet"""
        self.window.blit(self.image, self.rect)

        
