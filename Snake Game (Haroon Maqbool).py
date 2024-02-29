import pygame
import random

pygame.init()

# Color constants
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Display dimensions
dis_width = 800
dis_height = 600

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Haroon Maqbool')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Snake properties
snake_block = 10
snake_speed = 15

# Font styles
font_style = pygame.font.SysFont("arial", 30)
score_font = pygame.font.SysFont("comicsansms", 35)

# Dictionary to store player names and their high scores
player_scores = {}


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [10, 10])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color, y_displacement=0, size=30):
    font = pygame.font.SysFont(None, size)
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displacement))
    dis.blit(mesg, text_rect)


def display_timer(remaining_time):
    timer_text = font_style.render("Time Left: " + str(round(remaining_time, 2)) + "s", True, yellow)
    text_rect = timer_text.get_rect(topright=(dis_width - 10, 10))  # Adjusting position to top right corner
    dis.blit(timer_text, text_rect)


def display_menu():
    menu = True
    while menu:
        dis.fill(blue)
        message("Snake Game", green, -150)
        message("Select Mode:", white, -50)
        message("1. Free Mode (No Time Limit)", white, 0)
        message("2. Target Mode (Time Limit)", white, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu = False
                    gameLoop(False)  # Start free mode
                elif event.key == pygame.K_2:
                    menu = False
                    gameLoop(True)  # Start target mode


def gameLoop(target_mode):
    game_over = False

    # Initialize food coordinates
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    if target_mode:
        game_time = 10  # 60 seconds
        start_time = pygame.time.get_ticks()

    # Game variables
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    while not game_over:

        if target_mode:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            remaining_time = game_time - elapsed_time
            if remaining_time <= 0:
                game_over = True

        while game_close:
            dis.fill(blue)
            message("You Lost!", red, -50, 50)
            Your_score(Length_of_snake - 1)
            if target_mode:
                display_timer(remaining_time)
            message("Press Q-Quit or M-Menu", white, 50, 40)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_m:
                        display_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        if target_mode:
            display_timer(remaining_time)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    # If the game ends in target mode, display score and options
    if target_mode:
        dis.fill(blue)
        message("Game Over!", red, -50, 50)
        Your_score(Length_of_snake - 1)
        message("Press Q-Quit or M-Menu", white, 50, 40)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_m:
                        display_menu()


display_menu()
