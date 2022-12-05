import pygame, sys
from random import choice
import string
pygame.init()

pygame.display.set_caption('Hangman')
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_x = screen.get_width()
screen_y = screen.get_height()
clock = pygame.time.Clock()
fps = 60
my_font = pygame.font.SysFont('freesanbold.ttf', screen_x//27)
my_big_font = pygame.font.SysFont('freesanbold.ttf', 76)
left, middle, right = pygame.mouse.get_pressed()
chosen_word = []
class Box_with_letter: # we need 26 boxes
    def __init__(self, x, y, letter, letter_colour, box_colour, mouse_pos):
        self.x = x
        self.y = y
        self.size = screen_x // 27
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y
        self.letter_colour = letter_colour
        self.box_colour = box_colour
        self.mouse_pos = mouse_pos
        self.letter = letter

    def draw_box(self):
        pygame.draw.rect(screen, self.box_colour, (self.rect.topleft[0], self.rect.topleft[1], self.size, self.size), 1)
        letter_sufrace = my_font.render(self.letter, False, self.letter_colour)
        letter_rect = letter_sufrace.get_rect()
        letter_rect.center = self.rect.center[0], self.rect.center[1]
        screen.blit(letter_sufrace, letter_rect)

boxes = []

def settings():
    boxes.clear()
    all_letters_set = set(string.ascii_uppercase)
    used_letters = set()

def get_random_word():
    filename = 'wordlist.txt'
    with open(filename) as file_object:
        words = file_object.readlines()
        word = choice(words).upper().strip('\n')
        return str(word)

def get_player_word():
    global chosen_word
    chosen_word=[]
    screen.fill('black')

    while True:
        chosen_word = ''.join(chosen_word).upper()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    return chosen_word

                # Check for backspace
                elif event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    chosen_word = chosen_word[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    chosen_word += event.unicode
        screen.fill('black')

        text_surface = my_font.render(f"Player one, choose your word: {chosen_word}", False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_x // 2, screen_y // 4)
        pygame.draw.rect(screen, 'white', (text_rect[0] - 10, text_rect[1] - 10, text_rect[2] + 20, text_rect[3] + 20), 1)
        screen.blit(text_surface, text_rect)
        if text_rect.collidepoint(pygame.mouse.get_pos()):
            if  pygame.mouse.get_pressed()[0]:
                continue
        pygame.display.update()
        clock.tick(fps)


def menu():
    global chosen_word
    settings()
    while True:  # game loop
        screen.fill('black')
        text_surface = my_font.render('Random word', False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_x//2 , screen_y//4)
        pygame.draw.rect(screen, 'white', (text_rect[0]-10, text_rect[1]-10, text_rect[2]+20, text_rect[3]+20), 1)
        screen.blit(text_surface, text_rect)
        if text_rect.collidepoint(pygame.mouse.get_pos()):
            if  pygame.mouse.get_pressed()[0]:
                chosen_word = get_random_word()
                game()
        text_surface = my_font.render("Player's choice", False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_x // 2, screen_y // 2)
        pygame.draw.rect(screen, 'white', (text_rect[0]-10, text_rect[1]-10, text_rect[2]+20, text_rect[3]+20), 1)
        screen.blit(text_surface, text_rect)
        if text_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                chosen_word = get_player_word()
                game()
        text_surface = my_font.render("Quit", False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_x // 2, screen_y // 1.25)
        pygame.draw.rect(screen, 'white', (text_rect[0] - 10, text_rect[1] - 10, text_rect[2] + 20, text_rect[3] + 20),
                         1)
        screen.blit(text_surface, text_rect)
        if text_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(fps)

def game():
    box_to_get_size = Box_with_letter(0, 0, None, None, 'white', 'white')
    x1, y1 = 0, screen_y -box_to_get_size.size*2
    x1 = screen_x // 2 - (13 * box_to_get_size.size) - 13
    all_letters = string.ascii_uppercase
    all_letters_set = set(string.ascii_uppercase)
    used_letters = set()
    lives = 7
    for a in range(26):
        if all_letters[a] in {'A', 'E', 'I', 'O', 'U', 'Y'}:
            box = Box_with_letter(x1, y1, all_letters[a], 'green', 'green', mouse_pos=None, )
        else:
            box = Box_with_letter(x1, y1, all_letters[a], 'white', 'white', mouse_pos=None, )
        boxes.append(box)
        x1 += box.size + 1

    hangman_letters = set(chosen_word)
    while len(hangman_letters) >0:  # game loop

        screen.fill('black')

        for letter in chosen_word:
            if letter not in all_letters:
                text_surface = my_font.render(f"Unexpected character: {letter}", False, 'white')
                text_rect = text_surface.get_rect()
                text_rect.center = (screen_x // 2, screen_y // 2)
                screen.blit(text_surface, text_rect)
                pygame.display.update()
                pygame.time.wait(2000)
                menu()
        if chosen_word == '' or chosen_word == ' ':

            menu()
        word_display = [letter if letter in used_letters else '--' for letter in chosen_word]
        word_display = '  '.join(word_display)
        text_surface = my_big_font.render(f"{word_display}", False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_x // 2, screen_y // 4)
        screen.blit(text_surface, text_rect)

        text_surface = my_font.render(f"Lives: {lives}", False, 'white')
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_x //10, screen_y // 10)
        pygame.draw.rect(screen, 'white', (text_rect[0] - 10, text_rect[1] - 10, text_rect[2] + 20, text_rect[3] + 20),
                         -1)
        screen.blit(text_surface, text_rect)

        for box in boxes:
            box.draw_box()
        for box in boxes:
            if box.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if box.letter in all_letters_set - used_letters:
                        used_letters.add(box.letter)
                        all_letters_set.remove(box.letter)
                        boxes.remove(box)
                        if box.letter in hangman_letters:
                            hangman_letters.remove(box.letter)
                        else:
                            lives -= 1
                            if lives < 1:
                                screen.fill('black')
                                text_surface = my_font.render(f"You lost, the word was: {chosen_word}", False, 'white')
                                text_rect = text_surface.get_rect()
                                text_rect.center = (screen_x // 2, screen_y // 4)
                                screen.blit(text_surface, text_rect)
                                pygame.display.update()
                                pygame.time.wait(3000)
                                used_letters.clear()
                                menu()


        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(fps)

    pygame.time.wait(100)
    screen.fill('black')
    text_surface = my_big_font.render(f"{'  '.join(chosen_word)}", False, 'white')
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_x // 2, screen_y // 4)
    screen.blit(text_surface, text_rect)
    text_surface = my_font.render(f"Congratulations, the word was indeed: {chosen_word}", False, 'white')
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_x // 2, screen_y // 2)
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    print("\nCongratulations, you have guessed the word:")
menu()