import pygame
import sys
from inputBox import InputBox
from label import Label

P = 60
L = 4


def game_intro(board, background_color):
    global P, L
    clock = pygame.time.Clock()
    label_4 = Label(20, 200, "L:")
    label_5 = Label(20, 250, "P = Population density (in percent):")
    label_6 = Label(20, 450, "To pause the animation press space.")
    label_7 = Label(20, 500, "To start the animation press Enter.")
    label_boxes = [label_4, label_5, label_6, label_7]
    input_box4 = InputBox(400, 190, 50, 32, str(L))
    input_box5 = InputBox(400, 240, 50, 32, str(P))
    input_boxes = [input_box4, input_box5]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    L = float(input_box4.text)
                    P = float(input_box5.text)
                    done = True

        for box in input_boxes:
            box.update()

        board.fill(background_color)
        for box in input_boxes:
            box.draw(board)

        for box in label_boxes:
            box.draw(board)

        pygame.display.flip()
        clock.tick(30)

    return P, L
