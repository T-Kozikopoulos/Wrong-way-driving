import pygame
import time
import random

# Need to call '.init()' to start using the pygame library.
pygame.init()

display_width = 400
display_height = 800
white = (255, 255, 255)

# Create a window.
game_display = pygame.display.set_mode((display_width, display_height))
# Gives the window a title.
pygame.display.set_caption("WRONG WAY DRIVER")
clock = pygame.time.Clock()

background = pygame.image.load_extended('background.jpg')
player = pygame.image.load_extended('player.png')
cars = pygame.image.load_extended('enemy.png')

player_height = 84
player_width = 84
car_height = 64
car_width = 100


def cars_dodged(count):
    font = pygame.font.SysFont(None, 36)
    text = font.render('Score: ' + str(count), True, white)
    game_display.blit(text, (0, 0))


def enemies(xx, yy):
    game_display.blit(cars, (xx, yy))


def create_player(x, y):
    game_display.blit(player, (x, y))


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def message_display(text, text_y=display_height / 3.3):
    text_specifications = pygame.font.Font('freesansbold.ttf', 20)
    text_surface, text_rectangle = text_objects(text, text_specifications)
    text_rectangle.center = (display_width / 2, text_y)
    game_display.blit(text_surface, text_rectangle)

    # Apply all the changes to the next frame.
    pygame.display.update()
    # How long to display the message.
    time.sleep(3)
    # Calling it here to restart the game when the player loses, instead of simply closing it.
    game_loop()


def game_over():
    message_display('BETTER LUCK NEXT TIME.')


def game_loop():
    x = display_width * 0.445
    y = display_height * 0.890
    x_change = 0
    
    # Randomize the spwn position of the each new enemy.
    cars_x = random.randrange(0, display_width - 85)
    cars_y = -30

    # How fast cars fall in pixels per frame.
    cars_speed = 8
    dodged = 0
    # Create a quit, reset or restart condition.
    game_exit = False

    while not game_exit:
        # event.get() = all actions(moving/clicking mouse, pressing a key, etc) in each frame.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # Upon pressing a key.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = - 7
                elif event.key == pygame.K_RIGHT:
                    x_change = 7

            # Upon releasing a key.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        # Apply changes in player's position and background.
        x += x_change

        game_display.blit(background, (0, 0))

        enemies(cars_x, cars_y)
        cars_y += cars_speed

        create_player(x, y)
        cars_dodged(dodged)

        # Creates window boundaries.
        if x > display_width - 67:
            x = -7
        if x < -8:
            x = display_width - 68

        # When a car reaches the bottom of the screen, create a new car.
        if cars_y > display_height:
            cars_y = -85
            cars_x = random.randrange(0, display_width - 85)
            # Update score.
            dodged += 1
            # Rate of increase in difficulty every time the score goes up.
            cars_speed += 0.2

        # Setting collision requirements.
        if y < cars_y + car_height - 30:
            if cars_x + car_width - 30 > x > cars_x + 30\
                    or cars_x + car_width + 30 > x + player_width > cars_x + 30:
                    game_over()

        # Using '.update()' instead of 'flip()', because it only applies to the changes between frames, so it's lighter.
        pygame.display.update()
        # sets FPS
        clock.tick(100)

game_loop()

pygame.quit()
quit()
