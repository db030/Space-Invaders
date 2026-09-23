import pygame
from object import Player, PlayerBullet, Enemy, EnemyBullet
import random

pygame.init()
window = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

player = Player(window, 470, 400)
enemies_num = 20
#Create 20 enemies scattered above the enemy
enemies = []
for _ in range(enemies_num):
    x = random.randint(0, window.get_width() - 50)
    y = random.randint(0, 200)
    enemy = Enemy(window, x, y)
    enemies.append(enemy)

last_enemy_shoot = 0
SHOOT_DELAY = 1000
level = 1
score = 0
game_over = False
win = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        #player shoots using mouse 
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot()
    if not game_over and not win:
        keyPressedTuple = pygame.key.get_pressed
        #allow the player to move
        player.move(keyPressedTuple())
        player.update_bullets()

        for bullet in player.bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    score += 5
                    break
            
        
        for enemy in enemies[:]:
            for bullet in enemy.bullets[:]:
                if bullet.rect.colliderect(player.rect):
                    player.health = player.health - 5
                    enemy.bullets.remove(bullet)
                    if player.health <= 0:
                        game_over = True
                    break
                
        #One enemy to can shoot a every second and allow every enemy to move
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_shoot > SHOOT_DELAY:
            enemy = random.choice(enemies)
            enemy.shoot()
            last_enemy_shoot = current_time
        for enemy in enemies:
            enemy.move()
            enemy.update_bullets()

        if len(enemies) == 0:
            level += 1
            enemies_num += 10
            SHOOT_DELAY -= 100
            for _ in range(enemies_num):
                x = random.randint(0, window.get_width() - 50)
                y = random.randint(0, 200)
                enemy = Enemy(window, x, y)
                enemies.append(enemy)
                #enemy speed increase by 5 and move
            for enemy in enemies:
                enemy.speed += 5

                
        if level > 5:
            win = True
            level = 5

        window.fill("black")
        player.draw()
        #draw level and score in top right
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Level: {level} Score: {score}", True, "white")
        window.blit(text, (window.get_width() - text.get_width() - 10, 10))
        text2 = font.render(f"Health: {player.health}", True, "white")
        #draw top left
        window.blit(text2, (10, 10))
        text3 = font.render(f'Make it past level 5 to win', True, "white")
        #draw it in the top middle
        window.blit(text3, (window.get_width() // 2 - text3.get_width() // 2, 10))
        #draw bullet
        for bullet in player.bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
    
    elif game_over == True:
        #Game over in the middle of the screen
        font = pygame.font.SysFont(None, 75)
        text = font.render("Game Over", True, "red")
        window.blit(text, (window.get_width() // 2 - text.get_width() // 2, window.get_height() // 2 - text.get_height() // 2))
    
    elif win == True:
        #You win in the middle of the screen
        font = pygame.font.SysFont(None, 75)
        text = font.render("You Win!", True, "green")
        window.blit(text, (window.get_width() // 2 - text.get_width() // 2, window.get_height() // 2 - text.get_height() // 2))
    

    pygame.display.update()
    clock.tick(30)
