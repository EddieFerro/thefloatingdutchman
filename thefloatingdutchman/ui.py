
import pygame
import time
import os
from thefloatingdutchman.character.character_data import CharacterData
from thefloatingdutchman.game_settings import (WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, BLUE, YELLOW, WHITE, RED, GREEN, WIDTH_LEFT_BOUND, WIDTH_RIGHT_BOUND, PLAY_AGAIN_HEIGHT_LOWER_BOUND, PLAY_AGAIN_HEIGHT_UPPER_BOUND,
                                               QUIT_HEIGHT_LOWER_BOUND, QUIT_HEIGHT_UPPER_BOUND, RESUME__HEIGHT_LOWER_BOUND, RESUME_HEIGHT_UPPER_BOUND, RESTART_HEIGHT_LOWER_BOUND, RESTART_HEIGHT_UPPER_BOUND,
                                               VIEW_MAP_HEIGHT_LOWER_BOUND, VIEW_MAP_HEIGHT_UPPER_BOUND, VIEW_CONTROLS_HEIGHT_LOWER_BOUND, VIEW_CONTROLS_HEIGHT_UPPER_BOUND, QUIT_PAUSE_HEIGHT_LOWER_BOUND,
                                               QUIT_PAUSE_HEIGHT_UPPER_BOUND, OPTIONS_HEIGHT_LOWER_BOUND, OPTIONS_HEIGHT_UPPER_BOUND)


class Screen:
    # create surface
    def _new_screen_helper(self, width, height, font_size, text,
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
    def draw_screens(self, screen, index):
        y_locations = None  # surface height on screen
        if len(self._surfaces) == 5:
            screen.fill(BLACK)
            y_locations = [WINDOW_HEIGHT*.2,
                           WINDOW_HEIGHT*.45, WINDOW_HEIGHT*.6]
        else:
            pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5, WINDOW_WIDTH / 2,
                                             WINDOW_HEIGHT / (10 / 7)), border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))
            y_locations = [WINDOW_HEIGHT*.2, WINDOW_HEIGHT*.35, WINDOW_HEIGHT*.44,
                           WINDOW_HEIGHT*.53, WINDOW_HEIGHT*.62, WINDOW_HEIGHT*.71, WINDOW_HEIGHT*.8]

        # attach surfaces onto screen
        for surface, height in zip(self._surfaces, y_locations):
            # swap surface with highlighted one
            if surface == self._surfaces[index+1]:
                screen.blit(self._surfaces[1 + int(len(self._surfaces) / 2) + index], ((WINDOW_WIDTH - surface.get_width()) / 2,
                                                                                       height))
            else:  # draw non-selected surface
                screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                                      height))
        pygame.display.update()  # update screen
        return screen


class GameOverScreen(Screen):
    def __init__(self):
        self._surfaces = self._initialize_game_over_screen()

    # initialize surfaces that compose the game over screen

    def _initialize_game_over_screen(self):
        # game over text
        surfaces = []
        surfaces.append(self._new_screen_helper(WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 5, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "GAME OVER!", WHITE, None))

        features = [["PLAY AGAIN", BLACK], ["QUIT", BLACK],
                    ["PLAY AGAIN", GREEN], ["QUIT", RED]]

        for feat in features:  # alternate between play again and quit
            surfaces.append(self._new_screen_helper(WINDOW_WIDTH / 4,
                                                    WINDOW_HEIGHT / 10, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), feat[0], WHITE, feat[1]))

        return surfaces

    def game_over_screen_options(self, screen):
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
                                screen = self.draw_screens(screen, 0)
                            most_recent_is_continue = True
                            # player clicked on Continue button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return False

                        # user hovers over Quit Button
                        elif QUIT_HEIGHT_UPPER_BOUND >= mouse[1] >= QUIT_HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                            if most_recent_is_continue:  # user selects Quit after selecting Play Again/Resume
                                screen = self.draw_screens(screen, 1)
                            most_recent_is_continue = False
                            # player clicked on Quit button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return True


class PauseScreen(Screen):
    def __init__(self):
        self._surfaces = self._initialize_pause_screen()

    # initialize surfaces that compose the pause screen

    def _initialize_pause_screen(self):
        surfaces = []
        surfaces.append(self._new_screen_helper(WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 6, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "PAUSED", BLACK, None))  # pause

        features = [["RESUME", BLACK], ["OPTIONS", BLACK], ["VIEW MAP", BLACK], ["VIEW GAME CONTROLS", BLACK], ["RESTART GAME", BLACK], ["QUIT", BLACK],
                    ["RESUME", GREEN], ["OPTIONS", GREEN], ["VIEW MAP", GREEN], ["VIEW GAME CONTROLS", GREEN], ["RESTART GAME", GREEN], ["QUIT", RED]]

        for feat in features:
            surfaces.append(self._new_screen_helper(WINDOW_WIDTH / 4, WINDOW_HEIGHT /
                                                    14, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 25), feat[0], WHITE, feat[1]))

        return surfaces

    def pause_screen_options(self, screen):
        curr_index = 0  # indicates option currently chosen
        prev_index = 0

        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()  # mouse position
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:  # event has occurred

                    # player has chosen an option
                    # (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if curr_index == 0:  # RESUME
                            return False, False, False, False
                        elif curr_index == 1:  # OPTIONS
                            return False, False, False, False
                        elif curr_index == 2:  # VIEW MAP
                            return False, False, True, False
                        elif curr_index == 3:  # VIEW GAME CONTROLS
                            return False, False, False, True
                        elif curr_index == 4:  # RESTART GAME
                            return False, True, False, False
                        elif curr_index == 5:  # QUIT
                            return True, False, False, False

                    # user presses up or down on keypad
                    if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP)):
                        if event.key == pygame.K_UP and curr_index > 0:
                            curr_index -= 1
                            self.draw_screens(screen, curr_index)

                        elif event.key == pygame.K_DOWN and curr_index < 5:
                            curr_index += 1
                            self.draw_screens(screen, curr_index)

                    # button may be highlighted/selected, user hovers over proper width
                    elif (WIDTH_RIGHT_BOUND >= mouse[0] >= WIDTH_LEFT_BOUND):

                        # user hovers over Resume button
                        if RESUME_HEIGHT_UPPER_BOUND >= mouse[1] >= RESUME__HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                            if prev_index != curr_index:
                                screen = self.draw_screens(screen, 0)
                            prev_index = curr_index
                            curr_index = 0
                            # player clicked on Resume button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return False, False, False, False

                        # user hovers over Options Button
                        elif OPTIONS_HEIGHT_UPPER_BOUND >= mouse[1] >= OPTIONS_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw_screens(screen, 1)
                            prev_index = curr_index
                            curr_index = 1
                            # player clicked on View Map button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return False, False, False, False

                        # user hovers over View Map Button
                        elif VIEW_MAP_HEIGHT_UPPER_BOUND >= mouse[1] >= VIEW_MAP_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw_screens(screen, 2)
                            prev_index = curr_index
                            curr_index = 2
                            # player clicked on View Map button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return False, False, True, False

                        # user hovers over View Game Controls Button
                        elif VIEW_CONTROLS_HEIGHT_UPPER_BOUND >= mouse[1] >= VIEW_CONTROLS_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw_screens(screen, 3)
                            prev_index = curr_index
                            curr_index = 3
                            # player clicked on View Game Controls button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return False, False, False, True

                        # user hovers over Restart Button
                        elif RESTART_HEIGHT_UPPER_BOUND >= mouse[1] >= RESTART_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw_screens(screen, 4)
                            prev_index = curr_index
                            curr_index = 4
                            # player clicked on Restart button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return False, True, False, False

                        # user hovers over Quit Button
                        elif QUIT_PAUSE_HEIGHT_UPPER_BOUND >= mouse[1] >= QUIT_PAUSE_HEIGHT_LOWER_BOUND:
                            if prev_index != curr_index:
                                screen = self.draw_screens(screen, 5)
                            prev_index = curr_index
                            curr_index = 5
                            # player clicked on Quit button
                            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                return True, False, False, False


class LevelSurface(Screen):
    # initialize surface with level being equal to 0
    def __init__(self):
        self._level_surface = self.draw_new_level(0)

    # draw new surface containing new level when level is incremented
    def draw_new_level(self, level):
        surface = self._new_screen_helper(
            WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), "LEVEL " + str(level), WHITE, None)
        return surface

    # drawing surface to screen
    def update_screen_level(self, screen):
        screen.blit(self._level_surface, ((WINDOW_WIDTH - self._level_surface.get_width()) / 2,
                                          -WINDOW_HEIGHT/3))


class TutorialElements(Screen):
    # initialize surface elements and background image
    def __init__(self):
        self._story_elements = self._generate_story_elements()
        self._game_controls_elements = self._generate_game_controls_elements()
        self._background = image_fill_background(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "space_images/space6.jpg"))

    # initialize elements for story
    def _generate_story_elements(self):
        story_text = [("THE FLOATING DUTCHMAN", -WINDOW_HEIGHT/3, 2.5, YELLOW, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10)),
                      ("You Are the Captain of the Flying Dutchman", -
                       WINDOW_HEIGHT/5, 3, YELLOW, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15)),
                      ("You have ended up in space and your crew", -
                       WINDOW_HEIGHT/(35/2), 0, YELLOW, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15)),
                      ("has been captured by the Ghost Bustas", 3, 3,
                       YELLOW, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15)),
                      ("It is up to you to rescue your crew",
                       WINDOW_HEIGHT/7, 0, YELLOW, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15)),
                      ("and defeat the Ghost Bustas", WINDOW_HEIGHT/5, 1.5,
                       YELLOW, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15)),
                      ("Press the Spacebar to Continue", WINDOW_HEIGHT/3, 0, BLUE, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15))]
        return story_text

    # initialize elements for game controls
    def _generate_game_controls_elements(self):
        game_controls_text = [("GAME CONTROLS", -WINDOW_HEIGHT/3, 0, YELLOW, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 14)),
                              ("Press the Spacebar to Begin",
                               WINDOW_HEIGHT/3, 0, BLUE, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15))]
        self.game_controls_image = pygame.image.load(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "game_controls.png"))
        self.game_controls_image = pygame.transform.scale(
            self.game_controls_image, (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2)))
        return game_controls_text

    # begin tutorial
    def spawn_tutorial(self, screen):
        self.spawn_story(screen)
        self.spawn_game_controls(screen)

    # print story onto screen
    def spawn_story(self, screen):
        screen.blit(self._background, self._background.get_rect())
        self._spawn_onto_screen(screen, self._story_elements)

    # print game controls onto screen
    def spawn_game_controls(self, screen):
        screen.blit(self._background, self._background.get_rect())
        screen.blit(self.game_controls_image, ((WINDOW_WIDTH-self.game_controls_image.get_width()
                                                )/2, (WINDOW_HEIGHT-self.game_controls_image.get_height())/2))
        self._spawn_onto_screen(screen, self._game_controls_elements)

    # print either story or game controls onto screen
    def _spawn_onto_screen(self, screen, text):
        for txt, height, sleep_time, color, text_size in text:
            surface = self._new_screen_helper(
                WINDOW_WIDTH, WINDOW_HEIGHT, text_size, txt, color, None)
            screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                                  height))
            if sleep_time > 0:
                pygame.display.update()
                wait_for_user(sleep_time)
        pygame.display.update()
        wait_for_user(float('inf'))

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
