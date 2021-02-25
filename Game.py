import pygame
from pygame import *
import random
import mixer

pygame.mixer.init()

pygame.init()

screen_width = 1540
screen_height = 870
gameWindow = pygame.display.set_mode((screen_width, screen_height))
img = pygame.image.load("back.jpg")
img = pygame.transform.scale(img, [screen_width, screen_height]).convert_alpha()

gameWindow = pygame.display.set_mode((screen_width, screen_height))
gimg = pygame.image.load("backimg.jpg")
gimg = pygame.transform.scale(gimg, [screen_width, screen_height]).convert_alpha()

gameWindow = pygame.display.set_mode((screen_width, screen_height))
oimg = pygame.image.load("snake.jpg")
oimg = pygame.transform.scale(oimg, [screen_width, screen_height]).convert_alpha()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55, bold=True, italic=True)


def screen(text, red, x, y):
    screen_text = font.render(text, True, red)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, black, list, rad):
    for x, y in list:
        pygame.draw.rect(gameWindow, black, [x, y, rad, rad])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(oimg, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('snake_song.wav')
                    pygame.mixer.music.play(-1)
                    gameloop()

        pygame.display.update()
        clock.tick(120)


def gameloop():
    exit_game = False
    game_over = False
    pos_x = 45
    pos_y = 55
    rad = 15
    vel_x = 0
    vel_y = 0
    score = 0
    list = []
    length = 1
    food_x = random.randint(0, screen_width)
    food_y = random.randint(0, screen_height)
    fps = 120

    with open("highscore.txt", "r") as f:
        highscore = f.read()
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            # screen("Game Over! Press Enter to Continue", red, 150, 250)
            gameWindow.blit(gimg, [0, 0])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:
                        vel_x = 5
                        vel_y = 0
                    if event.key == pygame.K_LEFT:
                        vel_x = -5
                        vel_y = 0
                    if event.key == pygame.K_UP:
                        vel_y = -5
                        vel_x = 0
                    if event.key == pygame.K_DOWN:
                        vel_y = 5
                        vel_x = 0

            pos_x += vel_x
            pos_y += vel_y

            if abs(pos_x - food_x) < 6 and abs(pos_y - food_y) < 6:
                score += 1
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(img, [0, 0])
            screen("Score: " + str(score) + "  HighScore: " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, rad, rad])

            head = [pos_x, pos_y]
            list.append(head)

            if len(list) > length:
                del list[0]

            if head in list[:-1]:
                game_over = True
                pygame.mixer.music.load('game_over.wav')
                pygame.mixer.music.play()

            if pos_x < 0 or pos_x > screen_width or pos_y < 0 or pos_y > screen_height:
                game_over = True
                pygame.mixer.music.load('game_over.wav')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, list, rad)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
gameloop()
