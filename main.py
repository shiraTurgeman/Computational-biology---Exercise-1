import sys
import first_screen
from spreading_rumours import *
import numpy
import pygame

pygame.init()
size = (width, height) = 500, 550
bottom_footer_size = (width, height) = 500, 50
block_size = 5
board = pygame.display.set_mode(size)
pause = False
FONT = pygame.font.Font('freesansbold.ttf', 15)
cols, rows = 100, 100
background_color = (30, 30, 30)


def paused(current_iteration, generation_v_rate):
    global pause
    while (pause):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255), background_color)
    return textSurface, textSurface.get_rect()


def update_data(text, data, width, height):
    TextSurf, TextRect = text_objects(text + str(data), FONT)
    TextRect.center = (width, height)
    board.blit(TextSurf, TextRect)


def generation(board, grid, L):
    rate_of_spread = 0
    # Draw each cell and count neighbours
    for cellrow in grid:
        for cell in cellrow:
            if cell.hold_rumor and cell.is_man:
                rate_of_spread += 1
            cell.draw(board, block_size)
        pygame.display.update()
    for cellrow in grid:
        for cell in cellrow:
            cell.spread_rumor(grid=grid, cols=cols, rows=rows)
            cell.who_get_rumor(grid)

            cell.decide_if_spreading_rumor()
    return rate_of_spread


def update_info(current_iteration):
    # update the bottom footer
    pygame.draw.rect(board, background_color, (0, 500, 500, 50))
    update_data("Iteration: ", current_iteration, 70
                , board.get_height() - bottom_footer_size[1] / 2)
    pygame.display.update()


def main(P, L, skepticism_per, max_iterations):
    delay = 0
    current_iteration = 0
    generation_v_rate = []
    # print("generation_v_rate start", generation_v_rate)
    grid = initialize_grid(cols, rows, P, L, skepticism_per)
    global pause
    while not pause:
        if current_iteration == max_iterations - 1:
            pause = True
        # Check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True
                    paused(current_iteration, generation_v_rate=generation_v_rate)

        rate_of_spread = generation(board=board, grid=grid, L=L)
        # print(f"current_iteration: {current_iteration}, {rate_of_spread}, {generation_v_rate}")
        # generation_v_rate[current_iteration] = rate_of_spread
        generation_v_rate.append(rate_of_spread)
        # print(current_iteration, rate_of_spread)
        current_iteration += 1
        update_info(current_iteration)

        pygame.time.delay(delay)

    return generation_v_rate, current_iteration


if __name__ == '__main__':
    max_iterations = 1000
    num_rounds = 1
    skepticism_per = (0.4, 0.3, 0.2, 0.1)

    generation_v_rate_10_g = [0] * max_iterations
    for i in range(num_rounds):
        print(f"round number: {i}")
        P, L = first_screen.game_intro(board=board, background_color=(30, 30, 30))

        generation_v_rate, _ = main(P=P, L=L, skepticism_per=skepticism_per, max_iterations=max_iterations)
        print(generation_v_rate)
        generation_v_rate_10_g = [x + y for x, y in zip(generation_v_rate_10_g, generation_v_rate)]
        pause = False

    generation_v_rate_10_g = [x / num_rounds for x in generation_v_rate_10_g]
    print(generation_v_rate_10_g, '\n')
    print("p", P)
