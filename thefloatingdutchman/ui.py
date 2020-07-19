
import pygame
import time
import os
from thefloatingdutchman.character.character_data import CharacterData
from thefloatingdutchman.game_settings import (WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, BLUE, YELLOW, WHITE, RED, GREEN, WIDTH_LEFT_BOUND, WIDTH_RIGHT_BOUND, PLAY_AGAIN_HEIGHT_LOWER_BOUND, PLAY_AGAIN_HEIGHT_UPPER_BOUND,
                                               QUIT_HEIGHT_LOWER_BOUND, QUIT_HEIGHT_UPPER_BOUND, RESUME__HEIGHT_LOWER_BOUND, RESUME_HEIGHT_UPPER_BOUND, RESTART_HEIGHT_LOWER_BOUND, RESTART_HEIGHT_UPPER_BOUND,
                                               VIEW_MAP_HEIGHT_LOWER_BOUND, VIEW_MAP_HEIGHT_UPPER_BOUND, VIEW_CONTROLS_HEIGHT_LOWER_BOUND, VIEW_CONTROLS_HEIGHT_UPPER_BOUND, QUIT_PAUSE_HEIGHT_LOWER_BOUND,
                                               QUIT_PAUSE_HEIGHT_UPPER_BOUND, OPTIONS_HEIGHT_LOWER_BOUND, OPTIONS_HEIGHT_UPPER_BOUND, BEGIN__HEIGHT_LOWER_BOUND, BEGIN_HEIGHT_UPPER_BOUND,
                                               OPTIONS_MENU_HEIGHT_LOWER_BOUND, OPTIONS_MENU_HEIGHT_UPPER_BOUND, VIEW_CONTROLS_MENU_HEIGHT_LOWER_BOUND, VIEW_CONTROLS_MENU_HEIGHT_UPPER_BOUND,
                                               EXIT_HEIGHT_LOWER_BOUND, EXIT_HEIGHT_UPPER_BOUND)


class Screen:
    # create surface
    def _draw_surface(self, width, height, font_size, text,
                           text_color, fill):

        # inserts surface onto screen
        surface = pygame.Surface(
            (width, height), pygame.SRCALPHA)  # create surface
        if fill:  # fill surface with color
            surface.fill(fill)

        font = pygame.font.SysFont('Comic Sans MS', font_size)  # font
        text = font.render(text, True, text_color)  # create text

        # center text onto surface
        surface.blit(text, ((surface.get_rect().width - text.get_width()) / 2,
                            (surface.get_rect().height - text.get_height()) / 2))

        return surface

    # draw pre-defined surfaces onto screen

    # screen, surfaces being attached to screen, y_value of surfaces being attached, index highlights surface to be highlighted
    def draw(self, screen, index):
        y_locations = None  # surface height on screen
        sleep_times = None
        tutorial = False
        if len(self._surfaces) == 5: # game over screen
            screen.fill(BLACK)
            y_locations = [WINDOW_HEIGHT*.2,
                           WINDOW_HEIGHT*.45, WINDOW_HEIGHT*.6]
            sleep_times = [0] * 5
        elif len(self._surfaces) == 7: # story screen
            y_locations = [-WINDOW_HEIGHT/3,-WINDOW_HEIGHT/5,-WINDOW_HEIGHT/(35/2),3,WINDOW_HEIGHT/7,WINDOW_HEIGHT/5,WINDOW_HEIGHT/3]
            sleep_times = [2.5,3,0,3,0,1.5,0]
            tutorial = True
        elif len(self._surfaces) == 2: # game controls screen
            y_locations = [-WINDOW_HEIGHT/3,WINDOW_HEIGHT/3]
            sleep_times = [0] * 2
            tutorial = True
        elif len(self._surfaces) == 9:
            screen.fill(BLACK)
            screen.blit(self._banner, (0,0))
            pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5, WINDOW_WIDTH / 2,
                                             WINDOW_HEIGHT / (10 / 7)), border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))
            y_locations = [WINDOW_HEIGHT*.2, WINDOW_HEIGHT*.35,
                           WINDOW_HEIGHT*.53, WINDOW_HEIGHT*.62, WINDOW_HEIGHT*.8]
            sleep_times = [0] * 9
        else: #pause screen
            pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5, WINDOW_WIDTH / 2,
                                             WINDOW_HEIGHT / (10 / 7)), border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))
            y_locations = [WINDOW_HEIGHT*.2, WINDOW_HEIGHT*.35, WINDOW_HEIGHT*.44,
                           WINDOW_HEIGHT*.53, WINDOW_HEIGHT*.62, WINDOW_HEIGHT*.71, WINDOW_HEIGHT*.8]
            sleep_times = [0] * 13

        # attach surfaces onto screen
        for surface, height, sleep_time in zip(self._surfaces, y_locations, sleep_times):
            # swap surface with highlighted one
            if not tutorial and surface == self._surfaces[index+1]:
                screen.blit(self._surfaces[1 + int(len(self._surfaces) / 2) + index], ((WINDOW_WIDTH - surface.get_width()) / 2,
                                                                                       height))
            else:  # draw non-selected surface
                screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                                      height))
            if sleep_time > 0:
                pygame.display.update()
                wait_for_user(sleep_time)

        pygame.display.update()  # update screen
        if tutorial:
            wait_for_user(float('inf'))
        return screen


class GameOverScreen(Screen):
    def __init__(self):
        self._initialize()

    # initialize surfaces that compose the game over screen

    def _initialize(self):
        # game over text
        self._surfaces = []
        self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 5, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "GAME OVER!", WHITE, None))

        features = [["PLAY AGAIN", BLACK], ["MAIN MENU", BLACK],
                    ["PLAY AGAIN", GREEN], ["MAIN MENU", RED]]

        for txt, color in features:  # alternate between play again and quit
            self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 4,
                                                    WINDOW_HEIGHT / 10, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), txt, WHITE, color))

    def open(self, screen):
        most_recent_is_continue = True

        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()  # mouse position
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:  # event has occurred

                    # player has chosen an option
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if most_recent_is_continue:  # either end program or continue it
                            return False
                        else:
                            return True

                    # button may be highlighted/selected, user hovers over proper width
                    if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP)) or (WIDTH_RIGHT_BOUND >= mouse[0] >= WIDTH_LEFT_BOUND):

                        # user hovers over Play Again button
                        if PLAY_AGAIN_HEIGHT_UPPER_BOUND >= mouse[1] >= PLAY_AGAIN_HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                            if not most_recent_is_continue:  # user selects Play Again/Resume after selecting Quit
                                screen = self.draw(screen, 0)
                            most_recent_is_continue = True
                            # player clicked on Play Again button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return False

                        # user hovers over Quit Button
                        elif QUIT_HEIGHT_UPPER_BOUND >= mouse[1] >= QUIT_HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                            if most_recent_is_continue:  # user selects Quit after selecting Play Again/Resume
                                screen = self.draw(screen, 1)
                            most_recent_is_continue = False
                            # player clicked on Quit button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return True


class PauseScreen(Screen):
    def __init__(self):
        self._initialize()

    # initialize surfaces that compose the pause screen

    def _initialize(self):
        self._surfaces = []
        self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 6, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "PAUSED", BLACK, None))  # pause

        features = [["RESUME", BLACK], ["OPTIONS", BLACK], ["VIEW MAP", BLACK], ["VIEW GAME CONTROLS", BLACK], ["RESTART GAME", BLACK], ["RETURN TO MAIN MENU", BLACK],
                    ["RESUME", GREEN], ["OPTIONS", GREEN], ["VIEW MAP", GREEN], ["VIEW GAME CONTROLS", GREEN], ["RESTART GAME", GREEN], ["RETURN TO MAIN MENU", RED]]

        for txt, color in features:
            self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 4, WINDOW_HEIGHT /
                                                    14, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 25), txt, WHITE, color))

    def open(self, screen):
        curr_index = 0  # indicates option currently chosen
        prev_index = 0

        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()  # mouse position
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:  # event has occurred

                    # player has chosen an option
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if curr_index >= 0 and curr_index <= 5:  # return chosen option
                            return curr_index

                    # user presses up or down on keypad
                    if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP)):
                        if event.key == pygame.K_UP and curr_index > 0:
                            curr_index -= 1
                            self.draw(screen, curr_index)

                        elif event.key == pygame.K_DOWN and curr_index < 5:
                            curr_index += 1
                            self.draw(screen, curr_index)

                    # button may be highlighted/selected, user hovers over proper width
                    elif (WIDTH_RIGHT_BOUND >= mouse[0] >= WIDTH_LEFT_BOUND):

                        # user hovers over Resume button
                        if RESUME_HEIGHT_UPPER_BOUND >= mouse[1] >= RESUME__HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 0)
                            prev_index = curr_index
                            curr_index = 0
                            # player clicked on Resume button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over Options Button
                        elif OPTIONS_HEIGHT_UPPER_BOUND >= mouse[1] >= OPTIONS_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 1)
                            prev_index = curr_index
                            curr_index = 1
                            # player clicked on Options button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over View Map Button
                        elif VIEW_MAP_HEIGHT_UPPER_BOUND >= mouse[1] >= VIEW_MAP_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 2)
                            prev_index = curr_index
                            curr_index = 2
                            # player clicked on View Map button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over View Game Controls Button
                        elif VIEW_CONTROLS_HEIGHT_UPPER_BOUND >= mouse[1] >= VIEW_CONTROLS_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 3)
                            prev_index = curr_index
                            curr_index = 3
                            # player clicked on View Game Controls button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over Restart Button
                        elif RESTART_HEIGHT_UPPER_BOUND >= mouse[1] >= RESTART_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 4)
                            prev_index = curr_index
                            curr_index = 4
                            # player clicked on Restart button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over Quit Button
                        elif QUIT_PAUSE_HEIGHT_UPPER_BOUND >= mouse[1] >= QUIT_PAUSE_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 5)
                            prev_index = curr_index
                            curr_index = 5
                            # player clicked on Quit button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index


class MainMenu(Screen):
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self._banner = pygame.image.load(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "space_images/menu_banner.png"))
        self._banner = pygame.transform.scale(
            self._banner, (WINDOW_WIDTH, int(WINDOW_HEIGHT/5)))

        self._surfaces = []
        self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 6, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "THE FLOATING DUTCHMAN", BLACK, None))  # title
        
        features = [["BEGIN GAME", BLACK], ["OPTIONS", BLACK], ["VIEW GAME CONTROLS", BLACK], ["EXIT GAME", BLACK],
                    ["BEGIN GAME", GREEN], ["OPTIONS", GREEN], ["VIEW GAME CONTROLS", GREEN], ["EXIT GAME", RED]]

        for txt, color in features:
            self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 4, WINDOW_HEIGHT /
                                                    14, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 25), txt, WHITE, color))

    def open(self, screen):
        curr_index = 0  # indicates option currently chosen
        prev_index = 0

        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()  # mouse position
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:  # event has occurred

                    # player has chosen an option
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if curr_index >= 0 and curr_index <= 3:  # return chosen option
                            return curr_index

                    # user presses up or down on keypad
                    if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP)):
                        if event.key == pygame.K_UP and curr_index > 0:
                            curr_index -= 1
                            self.draw(screen, curr_index)

                        elif event.key == pygame.K_DOWN and curr_index < 3:
                            curr_index += 1
                            self.draw(screen, curr_index)

                    # button may be highlighted/selected, user hovers over proper width
                    elif (WIDTH_RIGHT_BOUND >= mouse[0] >= WIDTH_LEFT_BOUND):

                        # user hovers over Begin button
                        if BEGIN_HEIGHT_UPPER_BOUND >= mouse[1] >= BEGIN__HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 0)
                            prev_index = curr_index
                            curr_index = 0
                            # player clicked on Begin button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over Options Button
                        elif OPTIONS_MENU_HEIGHT_UPPER_BOUND >= mouse[1] >= OPTIONS_MENU_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 1)
                            prev_index = curr_index
                            curr_index = 1
                            # player clicked on Options button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over View Game Controls Button
                        elif VIEW_CONTROLS_MENU_HEIGHT_UPPER_BOUND >= mouse[1] >= VIEW_CONTROLS_MENU_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 2)
                            prev_index = curr_index
                            curr_index = 2
                            # player clicked on View Game Controls button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index

                        # user hovers over Quit Button
                        elif EXIT_HEIGHT_UPPER_BOUND >= mouse[1] >= EXIT_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw(screen, 3)
                            prev_index = curr_index
                            curr_index = 3
                            # player clicked on Quit button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return curr_index


class LevelSurface(Screen):
    # initialize surface with level being equal to 1
    def __init__(self):
        self.draw_new_level(1)

    # draw new surface containing new level when level is incremented
    def draw_new_level(self, level):
        self._level_surface = self._draw_surface(
            WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), "LEVEL " + str(level), WHITE, None)

    # drawing surface to screen
    def update_screen(self, screen):
        screen.blit(self._level_surface, ((WINDOW_WIDTH - self._level_surface.get_width()) / 2,
                                          -WINDOW_HEIGHT/3))


class Tutorial(Screen):
    # initialize surface elements and background image
    def __init__(self):
        self._generate_story_elements()
        self._generate_game_controls_elements()
        self._background = image_fill_background(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "space_images/space6.jpg"))

    # initialize elements for story
    def _generate_story_elements(self):
        self._story_surfaces = []
        features = [[(int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "THE FLOATING DUTCHMAN", YELLOW],
        [(int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "You Are the Captain of the Flying Dutchman", YELLOW],
        [(int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "You have ended up in space and your crew", YELLOW],
        [(int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "has been captured by the Ghost Bustas", YELLOW],
        [(int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "It is up to you to rescue your crew", YELLOW],
        [(int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "and defeat the Ghost Bustas", YELLOW],
        [(int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "Press the Spacebar to Continue", BLUE]]
        for size, txt, color in features:
            self._story_surfaces.append(self._draw_surface(WINDOW_WIDTH, WINDOW_HEIGHT, size, txt, color, None))

    # initialize elements for game controls
    def _generate_game_controls_elements(self):
        self._game_controls_surfaces = []
        self._game_controls_surfaces.append(self._draw_surface(WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 14), "GAME CONTROLS", YELLOW, None))
        self._game_controls_surfaces.append(self._draw_surface(WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "Press the Spacebar to Begin", BLUE, None))
        self.game_controls_image = pygame.image.load(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "game_controls.png"))
        self.game_controls_image = pygame.transform.scale(
            self.game_controls_image, (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2)))

    # begin tutorial
    def begin_tutorial(self, screen):
        self.show_story(screen)
        self.show_game_controls(screen)

    # print story onto screen
    def show_story(self, screen):
        screen.blit(self._background, self._background.get_rect())
        self._surfaces = self._story_surfaces
        self.draw(screen, 0)

    # print game controls onto screen
    def show_game_controls(self, screen):
        screen.blit(self._background, self._background.get_rect())
        screen.blit(self.game_controls_image, ((WINDOW_WIDTH-self.game_controls_image.get_width()
                                                )/2, (WINDOW_HEIGHT-self.game_controls_image.get_height())/2))
        self._surfaces = self._game_controls_surfaces
        self.draw(screen, 0)

# scales image to screen size


def image_fill_background(image_name):
    image = pygame.image.load(image_name)
    image = pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    return image

# health bar that shows player's health


def health_bar(screen, playermanager):
    current_hp = playermanager.player._data.health
    temp1 = pygame.draw.rect(
        screen, WHITE, (WINDOW_WIDTH/2 - 150, 97.5, 300, 50))
    temp2 = pygame.draw.rect(
        screen, GREEN, (WINDOW_WIDTH/2 - 140, 100, 280 * (current_hp/100), 45))

# pauses game until either spacebar is pressed or the time spent in function is greater than sleep_time


def wait_for_user(sleep_time):
    t0 = time.time()
    while True:
        if (time.time() - t0 > sleep_time):
            return
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE)):
                return
