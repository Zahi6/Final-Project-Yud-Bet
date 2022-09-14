# author: Zahi Akad Yud bet 3 Hertzog Kfar Saba

# import:
# outer modules:
import datetime
import math
import socket
import string
import threading
import time
import itertools
import pygame
import sys

# my files:
import dh_aes
import tcp_by_size

# constants
IP = "192.168.99.94"
PORT = 30017
WINDOW_HEIGHT = 700  # last one was 761, 1100
WINDOW_WIDTH = 900

# protocol:
MESSAGE_TYPE_LENGTH = 7
# game/screen state:
QUIT_STATE = 0
WELCOME_STATE = 1
CREATE_ACCOUNT_STATE = 2
LOGIN_STATE = 3
HOME_STATE = 4
# STAGES_MENU_STATE = 5
# CAMPAIGN_STAGE_STATE = 6
# COMPETITIVE_TIME_STATE = 7
# COMPETITIVE_STAGE_STATE = 8

# Account screen:
DEFAULT = 21
INSERTING_USER_NAME = 22
INSERTING_PASSWORD = 23
SUBMITTED = 24
SHOW_HIDE_PASSWORD = 25
ACCOUNT_BACK = 26

# Home screen:
STAGES_MENU_STATE = 31
COMPETITIVE_STATE = 32
RECORDS_OPTIONS_STATE = 33
HOW_TO_PLAY_STATE = 34



# Campaign stage:
CAMPAIGN_STAGE = 41
CAMPAIGN_FAILED_STAGE = 42
CAMPAIGN_SUCCEEDED_STAGE = 43
# Competitive options:
COMPETITIVE_STAGE_STATE = 51

# Records:
RECORDS_STATE = 61
AMOUNT_OF_RECORDS = 5


# mouse:
LEFT = 1
SCROLL = 2
RIGHT = 3


# text- pos and size:
BIG_TEXT_SIZE = 50
MEDIUM_TEXT_SIZE = 30
FONT = 'freesansbold.ttf'
SMALL_SPACE = 5
# Welcome screen:
TITLE_X = WINDOW_WIDTH // 2
TITLE_Y = BIG_TEXT_SIZE // 2
WELCOME_CREATE_ACCOUNT_X = 300
WELCOME_CREATE_ACCOUNT_Y = WINDOW_HEIGHT // 2  # - 150
WELCOME_CREATE_ACCOUNT_WIDTH = 490
WELCOME_LOGIN_X = 700
WELCOME_LOGIN_Y = WINDOW_HEIGHT // 2
WELCOME_LOGIN_WIDTH = 138
# Account(login/create account) screen:
USERNAME_X = 80
USERNAME_Y = 100
PASSWORD_X = 75
PASSWORD_Y = USERNAME_Y + MEDIUM_TEXT_SIZE * 2
SUBMIT_X = 55
SUBMIT_Y = PASSWORD_Y + MEDIUM_TEXT_SIZE * 2
SUBMIT_WIDTH = 106
SUBMIT_HEIGHT = MEDIUM_TEXT_SIZE
SHOW_HIDE_PASSWORD_X = PASSWORD_X + 700
SHOW_HIDE_PASSWORD_Y = PASSWORD_Y
SHOW_HIDE_PASSWORD_WIDTH = 234
SHOW_HIDE_PASSWORD_HEIGHT = MEDIUM_TEXT_SIZE
MAX_USERNAME_LEN = 16
USERNAME_FIELD_WIDTH = MAX_USERNAME_LEN * MEDIUM_TEXT_SIZE
USERNAME_FIELD_HEIGHT = MEDIUM_TEXT_SIZE
MAX_PASSWORD_LEN = 16
PASSWORD_FIELD_WIDTH = MAX_PASSWORD_LEN * MEDIUM_TEXT_SIZE
PASSWORD_FIELD_HEIGHT = MEDIUM_TEXT_SIZE
ACCOUNT_RESULT_X = 300
ACCOUNT_RESULT_Y = 300

# Campaign stage screen:
MAP_WIDTH = 700
MAP_HEIGHT = 700
STAGE_WORLD_X, STAGE_WORLD_Y = MAP_WIDTH + 100, BIG_TEXT_SIZE//2 + 5
STAGE_TITLE_X, STAGE_TITLE_Y = STAGE_WORLD_X, STAGE_WORLD_Y + BIG_TEXT_SIZE
UNDO_TEXT_X = MAP_WIDTH + 75
UNDO_TEXT_Y = BIG_TEXT_SIZE*4
UNDO_IMG_X = MAP_WIDTH + 125
UNDO_IMG_Y = UNDO_TEXT_Y - BIG_TEXT_SIZE // 2 + 5
RUN_X, RUN_Y = MAP_WIDTH + 100, BIG_TEXT_SIZE * 6
HOUSES_COUNT_X, HOUSE_COUNT_Y = WINDOW_WIDTH - 100, BIG_TEXT_SIZE * 5
COMP_STAGE_X = MAP_WIDTH + 100
COMP_STAGE_Y = BIG_TEXT_SIZE * 5//2

CAMPAIGN_STAGE_RESULT_X, CAMPAIGN_STAGE_RESULT_Y = MAP_WIDTH + 57, 350
CAMPAIGN_FAILED_X, CAMPAIGN_FAILED_Y = MAP_WIDTH + 50, 380
CAMPAIGN_SUCCESS, CAMPAIGN_SUCCESS_Y = MAP_WIDTH + 66, 380
CAMPAIGN_TRY_AGAIN_X, CAMPAIGN_TRY_AGAIN_Y = MAP_WIDTH + 100, 450
CAMPAIGN_TO_QUIT_X, CAMPAIGN_TO_QUIT_Y = CAMPAIGN_TRY_AGAIN_X, 570


# Home screen:
CAMPAIGN_WIDTH = 256
CAMPAIGN_HEIGHT = BIG_TEXT_SIZE
CAMPAIGN_X = WINDOW_WIDTH // 2
CAMPAIGN_Y = 200

COMPETITIVE_WIDTH = 300
COMPETITIVE_HEIGHT = BIG_TEXT_SIZE
COMPETITIVE_X = WINDOW_WIDTH // 2
COMPETITIVE_Y = 300

NOT_UPDATED_YET = 0
BROKEN = 1
NOT_BROKEN = 2

RECORDS_WIDTH = 206
RECORDS_HEIGHT = BIG_TEXT_SIZE
RECORDS_X = WINDOW_WIDTH // 2
RECORDS_Y = 400

HOW_TO_PLAY_WIDTH = 300
HOW_TO_PLAY_HEIGHT = 50
HOW_TO_PLAY_X = WINDOW_WIDTH//2
HOW_TO_PLAY_Y = 500

# stages menu screen:
FIRST_STAGE_X = 50
FIRST_STAGE_Y = 150
STAGE_WIDTH = 75
STAGE_SPACE_X = 25
STAGE_SPACE_Y = BIG_TEXT_SIZE * 3 // 2
STAGE_HEIGHT = 50
#game:
FINAL_WORLD = 4
FINAL_STAGE = 9

# colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (61,145,64)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
PINK = (255, 20, 147)
YELLOW = (255,255,0)
ORANGE = (255,97,3)
BANANA = (205,205,0)
GOLD = (255,185,15)
SILVER = (192, 192, 192)
BRONZE = 205, 127, 50

# globals:
#ip = ""
tid = 1
locker = threading.Lock()
background_color = BLACK
font_color = WHITE
font_size = BIG_TEXT_SIZE
did_quit = False
login = False
create_account = False
username = ""
password = ""
account_response = ""
stage_reached = 1
stage_selected = 0
stage_only_presentation = 0
bool_selected_stage = False
stage_map_list = []
passed_campaign_stage = False
# competitive:
time_limit = 3
comp_stage = 0
lives = 3
curr_time_left = 0.0
prev_time_left = 0.0
need_comp_level = False  # for communication thread
difficulty = 0  # for communication thread
finished_competitive = False # if that is true it means we need to check if the record was broken
record_broken = NOT_UPDATED_YET
need_records = False
records = ""
records_time = 0

# 'static' functions:
def find_best_route(points):
    points_len = len(points)
    nums_str = ""
    for i in range(points_len):
        nums_str += str(i)
    gen = itertools.permutations(nums_str, points_len)
    min_dist = 10000
    route = []
    n = next(gen)
    print(list(n))
    run = True
    while run:
        order = list(n)
        for i in range(len(order)):
            order[i] = int(order[i])
        distance = calc_total_dist(points, order)
        if distance < min_dist:
            min_dist = distance
            route = n
        n = next(gen, ())
        if n == ():
            run = False
    return min_dist, route


def find_best_route_ver2(points):
    points_len = len(points)
    nums_str = ""
    for i in range(points_len):
        nums_str += str(i)
    gen = itertools.permutations(nums_str, points_len)
    lst = []
    for g in gen:
        g = list(g)
        for i in range(len(g)):
            g[i] = int(g[i])
        lst.append(g)
    min_dist = 10000
    route = []
    for l in lst:
        distance = calc_total_dist(points, l)
        if distance < min_dist:
            min_dist = distance
            route = l
    return min_dist, route


def calc_total_dist(points, order):
    dist_sum = 0
    for i in range(len(order) - 1):
        #dist_sum += math.dist(points[order[i]], points[order[i + 1]])
        dist_sum += get_distance(points[order[i]], points[order[i + 1]])
    return dist_sum


def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# classes:-------------------------

class DoubleNode:
    def __init__(self, value, prev, n):
        self.value = value
        self.prev = prev
        self.next = n

    def __str__(self):
        s = ""
        p = self
        while p.prev != None:
            p = p.prev
        while p != None:
            s += str(p.value) + ", "
            p = p.next
        return s[:-2]

    def set_next(self, value):
        self.next = DoubleNode(value, self, None)

    def set_prev(self, value):
        self.prev = DoubleNode(value, None, self)


class Dequeue:
    def __init__(self):
        self.head = None
        self.tail = None

    def __str__(self):
        s = ""
        p = self.tail
        while p is not None:
            s += str(p.value) + ", "
            p = p.prev
        if s:
            return s[:-2]
        return ""

    def get_list_of_all(self):
        res = []
        p = self.tail
        while p is not None:
            res.append(p.value)
            p = p.prev
        return res

    def remove_head(self):
        if self.head is not None:
            if self.head is self.tail:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None
            return True
        return False

    def remove_tail(self):
        if self.tail is not None:
            if self.tail is self.head:
                self.tail = None
                self.head = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
            return True
        return False

    def add_head(self, val_to_add):
        if self.head is None:
            self.head = DoubleNode(val_to_add, None, None)
            self.tail = self.head
        else:
            self.head.set_prev(val_to_add)
            self.head = self.head.prev

    def add_tail(self, val_to_add):
        if self.tail is None:
            self.tail = DoubleNode(val_to_add, None, None)
            self.head = self.tail
        else:
            self.tail.set_next(val_to_add)
            self.tail = self.tail.next

class Thread(threading.Thread):
    def __init__(self):
        super(Thread, self).__init__()
        # another way to call to super __init__  (in case of multi inheritance)
        # threading.Thread.__init__(self)
        global tid
        self.tid = tid
        tid += 1
        global locker
        self.lock = locker

    def run(self):
        print("thread " + str(tid) + " started at " + str(datetime.datetime.now()))

    def thread_started(self):
        print("Thread (tid=" + str(self.tid) + ") started at " + str(datetime.datetime.now()))


class ScreenThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("finished ScreenThread init")
        self.screen = None

    def run(self):
        global stage_reached, did_quit
        self.thread_started()
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Find Best Route Game")
        self.screen.fill(BLACK)
        pygame.display.update()
        screen_state = WELCOME_STATE
        running = True
        while running:
            if screen_state == QUIT_STATE:
                pygame.quit()
                did_quit = True
                break
            if screen_state == WELCOME_STATE:
                screen_state = self.welcome_screen()
            elif screen_state == CREATE_ACCOUNT_STATE:
                screen_state = self.account_screen(log_in=False)
                if stage_reached < 1:
                    stage_reached =1
                print("created account, stage =", stage_reached)
            elif screen_state == LOGIN_STATE:
                screen_state = self.account_screen(log_in=True)
                if stage_reached < 1:
                    stage_reached = 1
                print("logged in, stage =", stage_reached)
            elif screen_state == HOME_STATE:
                screen_state = self.home_screen()
            elif screen_state == STAGES_MENU_STATE:
                screen_state = self.stages_menu_screen()
            elif screen_state == RECORDS_OPTIONS_STATE:
                screen_state = self.records_options_screen()
            elif screen_state == HOW_TO_PLAY_STATE:
                screen_state = self.how_to_play_screen()
            elif screen_state == RECORDS_STATE:
                screen_state = self.records_screen()
            elif screen_state == CAMPAIGN_STAGE:
                screen_state = self.stage_screen(False)
            elif screen_state == CAMPAIGN_FAILED_STAGE:
                screen_state = self.campaign_failed_stage()
            elif screen_state == CAMPAIGN_SUCCEEDED_STAGE:
                screen_state = self.campaign_succeeded_stage()
            elif screen_state == COMPETITIVE_STATE:
                screen_state = self.competitive_options_screen()
            elif screen_state == COMPETITIVE_STAGE_STATE:
                screen_state = self.stage_screen(True)


            '''elif event.type == pygame.KEYDOWN:# keyboard input
            if event.key == pygame.K_LEFT:'''

    def how_to_play_screen(self):
        global font_size, font_color, background_color
        font_size = MEDIUM_TEXT_SIZE
        font_color = WHITE
        background_color = BLACK
        state = HOW_TO_PLAY_STATE
        with open('how_to_play.txt', 'r') as file:
            file_data = file.read()
        file_lines = file_data.split('\n')
        self.screen.fill(BLACK)
        self.show_text_colorful('How to play', TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)
        self.show_lines(file_lines, WINDOW_WIDTH//2, 75)
        self.update_back_arrow()
        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                is_on_back_arrow = self.update_back_arrow()
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    print("mouse left click, pos:", mouse_pos)
                    if is_on_back_arrow:
                        return HOME_STATE


    def draw_run(self, amount_of_houses, is_mouse_on_run):
        global stage_map_list
        background_color = RED
        font_color = WHITE
        if amount_of_houses == len(stage_map_list):
            background_color = GREEN
            if is_mouse_on_run:
                font_color = BLUE
        self.show_text_colorful('Run', RUN_X, RUN_Y, MEDIUM_TEXT_SIZE, font_color, background_color)
    def draw_house(self, location, is_competitive):
        if not is_competitive:
            self.show_image('photos/house.png', location[0], location[1])
        else:
            if location[0] < MAP_WIDTH//2 and location[1] < MAP_HEIGHT//2:
                    self.show_image('photos/blue_bg_house.png', location[0], location[1])
            elif location[0] >= MAP_WIDTH//2 and location[1] < MAP_HEIGHT//2:
                self.show_image('photos/red_bg_house.png', location[0], location[1])
            elif  location[0] < MAP_WIDTH//2 and location[1] >= MAP_HEIGHT//2:
                self.show_image('photos/yellow_bg_house.png', location[0], location[1])
            elif location[0] >= MAP_WIDTH//2 and location[1] >= MAP_HEIGHT//2:
                self.show_image('photos/green_bg_house.png', location[0], location[1])
    def stage_screen(self, is_competitive):
        global stage_only_presentation, stage_selected, world_selected # for campaign only
        global time_limit, comp_stage, lives, prev_time_left,curr_time_left, difficulty, need_comp_level, finished_competitive # for competitive only
        global stage_map_list # both campaign and competitive
        start = datetime.datetime.now()
        prev_time_diff_in_seconds = (datetime.datetime.now()-start).seconds
        curr_time_diff_in_seconds = prev_time_diff_in_seconds
        state = CAMPAIGN_STAGE
        self.screen.fill(BLACK)
        if not is_competitive:
            self.screen.fill(WHITE, (0, 0, 700, 700))
        else:
            self.screen.fill(BLUE, (0, 0, MAP_WIDTH // 2, MAP_HEIGHT // 2))
            self.screen.fill(RED, (MAP_WIDTH // 2, 0, MAP_WIDTH // 2, MAP_HEIGHT // 2))
            self.screen.fill(YELLOW, (0, MAP_HEIGHT // 2, MAP_WIDTH // 2, MAP_HEIGHT // 2))
            self.screen.fill(GREEN, (MAP_WIDTH // 2, MAP_HEIGHT // 2, MAP_WIDTH // 2, MAP_HEIGHT // 2))
        if not is_competitive:
            self.show_text_colorful('World ' + str(world_selected), STAGE_WORLD_X, STAGE_WORLD_Y, MEDIUM_TEXT_SIZE, GREEN,
                                    BLACK)
            self.show_text_colorful('Stage ' + str(stage_selected), STAGE_TITLE_X, STAGE_TITLE_Y, MEDIUM_TEXT_SIZE, YELLOW,
                                    BLACK)
        else:
            self.update_time(0)
            #self.show_text_colorful(str(curr_time_diff_in_seconds), STAGE_WORLD_X, STAGE_WORLD_Y, MEDIUM_TEXT_SIZE, GREEN,
            #                        BLACK)
            self.show_text_colorful('lives: ' + str(lives), STAGE_TITLE_X, STAGE_TITLE_Y, MEDIUM_TEXT_SIZE, YELLOW,
                                    BLACK)

            self.show_text_colorful('Stage: ' + str(comp_stage), COMP_STAGE_X, COMP_STAGE_Y, MEDIUM_TEXT_SIZE, WHITE, BLACK)

        self.show_text_colorful('Undo', UNDO_TEXT_X, UNDO_TEXT_Y, MEDIUM_TEXT_SIZE, WHITE, BLACK)
        house_count = 0
        self.draw_run(house_count, False)
        self.show_image('photos/white_undo.png', UNDO_IMG_X, UNDO_IMG_Y)

        for location in stage_map_list:
            self.draw_house(location, is_competitive)

        houses_dq = Dequeue()

        self.show_text_colorful('Selected: ' + str(house_count) + '/' + str(len(stage_map_list)), HOUSES_COUNT_X, HOUSE_COUNT_Y, MEDIUM_TEXT_SIZE, WHITE,
                                BLACK)
        house_dict = {}
        last_houses = []
        on_undo = False
        on_run = False
        for i in range(len(stage_map_list)):
            house_dict[i] = False
        while True:
            if is_competitive:
                curr_time_diff_in_seconds = (datetime.datetime.now()-start).seconds
                if prev_time_diff_in_seconds != curr_time_diff_in_seconds:
                    prev_time_diff_in_seconds = curr_time_diff_in_seconds
                    there_is_time = self.update_time(curr_time_diff_in_seconds)
                    if not there_is_time:
                        print("no time left - game over")
                        lives = 3
                        finished_competitive = True
                        while finished_competitive:
                            time.sleep(0.01)
                        if record_broken == BROKEN:
                            self.show_text_colorful('Got to top 5 well played!', WINDOW_WIDTH//2, WINDOW_HEIGHT//2, BIG_TEXT_SIZE, GREEN, BLACK)
                            time.sleep(2)
                        comp_stage = 0
                        return HOME_STATE
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                is_on_back_arrow = self.update_back_arrow()
                mouse_pos = pygame.mouse.get_pos()
                if self.is_mouse_in_rect(MAP_WIDTH + 10, RUN_Y - MEDIUM_TEXT_SIZE // 2, WINDOW_WIDTH,
                                      RUN_Y + MEDIUM_TEXT_SIZE // 2):
                    if not on_run:
                        on_run = True
                        self.draw_run(house_count, on_run)
                else:
                    if on_run:
                        on_run = False
                        self.draw_run(house_count, on_run)
                if self.is_mouse_in_rect(MAP_WIDTH + 10, UNDO_TEXT_Y - MEDIUM_TEXT_SIZE // 2, WINDOW_WIDTH,
                                      UNDO_TEXT_Y + MEDIUM_TEXT_SIZE // 2):
                    if not on_undo:
                        on_undo = True
                        self.show_text_colorful('Undo', UNDO_TEXT_X, UNDO_TEXT_Y, MEDIUM_TEXT_SIZE, BLUE, BLACK)
                        self.show_image('photos/blue_undo.png', UNDO_IMG_X, UNDO_IMG_Y)
                else:
                    if on_undo:
                        on_undo = False
                        self.show_text_colorful('Undo', UNDO_TEXT_X, UNDO_TEXT_Y, MEDIUM_TEXT_SIZE, WHITE, BLACK)
                        self.show_image('photos/white_undo.png', UNDO_IMG_X, UNDO_IMG_Y)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    print("mouse left click, pos:", mouse_pos)
                    if is_on_back_arrow:
                        if not is_competitive:
                            return STAGES_MENU_STATE
                        return HOME_STATE
                    if on_run and house_count == len(stage_map_list):
                        stage_best_distance, stage_best_route = find_best_route(stage_map_list)
                        selected_houses_list = houses_dq.get_list_of_all()
                        distance_got = calc_total_dist(stage_map_list, selected_houses_list)
                        print("stage_best_route", stage_best_route)
                        print("stage_best_distance", stage_best_distance)
                        print("distance_got", distance_got)
                        print("selected_houses_list", selected_houses_list)
                        if distance_got - stage_best_distance < 0.01 or selected_houses_list == stage_best_route:
                            print("victory")
                            global stage_reached, passed_campaign_stage
                            print("stage_reached", stage_reached)
                            print("stage_selected", stage_selected)
                            if not is_competitive:
                                if stage_reached == stage_only_presentation:
                                    stage_reached += 1
                                    passed_campaign_stage = True
                                return CAMPAIGN_SUCCEEDED_STAGE
                            comp_stage += 1
                            if difficulty < 5:
                                difficulty += 1
                            print("new comp stage", comp_stage)
                            prev_time_left = curr_time_left
                            need_comp_level = True
                            while need_comp_level:
                                time.sleep(0.01)
                            return COMPETITIVE_STAGE_STATE

                        else:
                            print("defeat")
                            if not is_competitive:
                                return CAMPAIGN_FAILED_STAGE
                            lives -= 1
                            print("new lives", lives)
                            if lives == 0:
                                finished_competitive = True
                                while finished_competitive:
                                    time.sleep(0.01)
                                if record_broken == BROKEN:
                                    self.show_text_colorful('Record broken well played', WINDOW_WIDTH//2, WINDOW_HEIGHT//2, BIG_TEXT_SIZE, GREEN, BLACK)
                                    self.show_text_colorful('lives: ' + str(lives), STAGE_TITLE_X, STAGE_TITLE_Y, MEDIUM_TEXT_SIZE, YELLOW,
                                                            BLACK)
                                    lives = 3
                                    time.sleep(2)
                                print("0 lives left - game over")
                                comp_stage = 0
                                return HOME_STATE
                            else:
                                prev_time_left = curr_time_left
                                need_comp_level = True
                                while need_comp_level:
                                    time.sleep(0.01)
                                return COMPETITIVE_STAGE_STATE
                            #self.stage_screen()

                    if on_undo and house_count > 0:
                        houses_dq.remove_tail()
                        h = last_houses[len(last_houses) - 1]
                        loc = stage_map_list[h]
                        if house_dict[h]:
                            house_dict[h] = False
                            self.draw_house(loc, is_competitive)
                            #self.screen.fill(WHITE, (loc[0] + 10, loc[1] + 50, 30, 23))
                            last_houses.remove(h)
                        print("pressed undo. houses_dq str", houses_dq.__str__())
                        print("dict", house_dict)
                        self.draw_run(house_count, on_run)
                        house_count -= 1
                        self.show_text_colorful('Selected: ' + str(house_count) + '/' + str(len(stage_map_list)), HOUSES_COUNT_X, HOUSE_COUNT_Y,
                                                MEDIUM_TEXT_SIZE, WHITE, BLACK)
                    else:
                        for i, house in enumerate(stage_map_list):
                            #if math.dist((house[0] + 25, house[1] + 25), mouse_pos) < 30:
                            if get_distance((house[0] + 25, house[1] + 25), mouse_pos) < 30:
                                if not house_dict[i]:
                                    houses_dq.add_tail(i)
                                    house_count += 1
                                    self.draw_run(house_count, on_run)
                                    house_dict[i] = True
                                    last_houses.append(i)
                                    print("houses_dq str", houses_dq.__str__())
                                    self.show_text_colorful('Selected: ' + str(house_count) + '/' + str(len(stage_map_list)), HOUSES_COUNT_X,
                                                            HOUSE_COUNT_Y, MEDIUM_TEXT_SIZE, WHITE, BLACK)
                                    self.show_image('photos/small_green_vi1.png', house[0] + 15, house[1]+10)
                                break

    def update_time(self, time_diff_in_seconds):
        global prev_time_left, curr_time_left
        curr_time_left = (prev_time_left - time_diff_in_seconds)
        minutes_left = curr_time_left//60
        seconds_left = curr_time_left%60
        str_time_left = str(minutes_left) + ":" + str(seconds_left).zfill(2)
        self.screen.fill(BLACK,(MAP_WIDTH, 0, WINDOW_WIDTH, BIG_TEXT_SIZE+5))
        self.show_text_colorful(str_time_left, STAGE_WORLD_X, STAGE_WORLD_Y, BIG_TEXT_SIZE, GREEN,
                                BLACK)
        return curr_time_left > 0.0
    def campaign_succeeded_stage(self):
        text_size = MEDIUM_TEXT_SIZE
        state = CAMPAIGN_SUCCEEDED_STAGE
        self.show_text_colorful('Result:', CAMPAIGN_STAGE_RESULT_X, CAMPAIGN_STAGE_RESULT_Y , text_size, WHITE, BLACK)
        self.show_text_colorful('Success', CAMPAIGN_SUCCESS, CAMPAIGN_SUCCESS_Y, text_size, WHITE, BLACK)
        self.screen.fill(DARK_GRAY, (CAMPAIGN_TRY_AGAIN_X-92, CAMPAIGN_TRY_AGAIN_Y-text_size//2, 184, text_size*2+1))
        self.show_lines_colorful(['try different', 'solution'], CAMPAIGN_TRY_AGAIN_X, CAMPAIGN_TRY_AGAIN_Y, text_size, WHITE, DARK_GRAY)
        self.show_lines_colorful(['back to stage', 'selection:'], CAMPAIGN_TO_QUIT_X, CAMPAIGN_TO_QUIT_Y, text_size, WHITE, BLACK)
        is_on_try_again = False
        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                if self.is_mouse_in_rect(CAMPAIGN_TRY_AGAIN_X-92, CAMPAIGN_TRY_AGAIN_Y-text_size//2, CAMPAIGN_TRY_AGAIN_X +92, CAMPAIGN_TRY_AGAIN_Y + text_size*3//2):
                    if not is_on_try_again:
                        is_on_try_again = True
                        self.show_lines_colorful(['try different', 'solution'], CAMPAIGN_TRY_AGAIN_X, CAMPAIGN_TRY_AGAIN_Y, text_size, BLUE, DARK_GRAY)
                else:
                    if is_on_try_again:
                        self.show_lines_colorful(['try different', 'solution'], CAMPAIGN_TRY_AGAIN_X, CAMPAIGN_TRY_AGAIN_Y, text_size, WHITE, DARK_GRAY)
                        is_on_try_again = False
                is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if is_on_back_arrow:
                        return STAGES_MENU_STATE
                    if is_on_try_again:
                        return CAMPAIGN_STAGE

    def campaign_failed_stage(self):
        text_size = MEDIUM_TEXT_SIZE
        state = CAMPAIGN_FAILED_STAGE
        self.show_text_colorful('Result:', CAMPAIGN_STAGE_RESULT_X, CAMPAIGN_STAGE_RESULT_Y , text_size, WHITE, BLACK)
        self.show_text_colorful('Failed', CAMPAIGN_FAILED_X, CAMPAIGN_FAILED_Y, text_size, WHITE, BLACK)
        self.screen.fill(DARK_GRAY, (CAMPAIGN_TRY_AGAIN_X-92, CAMPAIGN_TRY_AGAIN_Y-text_size//2, 184, text_size*2+1))
        self.show_lines_colorful(['Click here to', 'try again'], CAMPAIGN_TRY_AGAIN_X, CAMPAIGN_TRY_AGAIN_Y, text_size, WHITE, DARK_GRAY)
        self.show_lines_colorful(['or click here', 'to quit:'], CAMPAIGN_TO_QUIT_X, CAMPAIGN_TO_QUIT_Y, text_size, WHITE, BLACK)
        is_on_try_again = False
        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                if self.is_mouse_in_rect(CAMPAIGN_TRY_AGAIN_X-92, CAMPAIGN_TRY_AGAIN_Y-text_size//2, CAMPAIGN_TRY_AGAIN_X +92, CAMPAIGN_TRY_AGAIN_Y + text_size*3//2):
                    if not is_on_try_again:
                        is_on_try_again = True
                        self.show_lines_colorful(['Click here to', 'try again'], CAMPAIGN_TRY_AGAIN_X, CAMPAIGN_TRY_AGAIN_Y, text_size, BLUE, DARK_GRAY)
                else:
                    if is_on_try_again:
                        self.show_lines_colorful(['Click here to', 'try again'], CAMPAIGN_TRY_AGAIN_X, CAMPAIGN_TRY_AGAIN_Y, text_size, WHITE, DARK_GRAY)
                        is_on_try_again = False
                is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if is_on_back_arrow:
                        return STAGES_MENU_STATE
                    if is_on_try_again:
                        return CAMPAIGN_STAGE



    def refresh_stages_menu_screen(self):
        # self.screen.fill(BLACK)
        # self.show_text_colorful('Stages menu', WINDOW_WIDTH // 2, BIG_TEXT_SIZE, BIG_TEXT_SIZE, GREEN, BLACK)
        global stage_reached
        world_got_to = (stage_reached - 1) // FINAL_STAGE + 1
        stage_got_to = stage_reached % 9
        if stage_got_to == 0:
            stage_got_to = 9
        for world_num in range(1, FINAL_WORLD+1):
            for stage_num in range(1, FINAL_STAGE+1):
                bg_color = RED
                if world_num == world_got_to and stage_num == stage_got_to:
                    bg_color = BANANA
                elif world_num < world_got_to or (world_num == world_got_to and stage_num < stage_got_to):
                    bg_color = DARK_GREEN
                self.show_text_colorful(str(world_num) + '-' + str(stage_num), FIRST_STAGE_X + (STAGE_WIDTH + STAGE_SPACE_X) * (stage_num - 1),
                                        FIRST_STAGE_Y + STAGE_SPACE_Y*(world_num-1), BIG_TEXT_SIZE, WHITE,
                                        bg_color)
        # pygame.display.flip()

    def stages_menu_screen(self):
        global stage_reached
        state = STAGES_MENU_STATE
        self.screen.fill(BLACK)
        self.show_text_colorful('Stages', WINDOW_WIDTH // 2, BIG_TEXT_SIZE, BIG_TEXT_SIZE, GREEN, BLACK)

        # self.show_text_colorful('1', 50, 50, BIG_TEXT_SIZE, WHITE, RED)
        # self.show_text_colorful('2', 100, 50, BIG_TEXT_SIZE, WHITE, RED)
        # self.show_text_colorful('3', 150, 50, BIG_TEXT_SIZE, WHITE, RED)
        self.refresh_stages_menu_screen()

        highlighted = []
        stage, world = -1, -1
        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE

                stage, world = self.check_is_on_stage()
                if stage != -1 and world != -1:
                    if highlighted == [] or stage != highlighted[0] or world != highlighted[1]:
                        if world <= FINAL_WORLD:
                            self.refresh_stages_menu_screen()
                            global stage_reached
                            world_got_to = (stage_reached - 1) // FINAL_STAGE + 1
                            stage_got_to = stage_reached % 9
                            if stage_got_to == 0:
                                stage_got_to = 9
                            bg_color = RED
                            if world == world_got_to and stage == stage_got_to:
                                bg_color = BANANA
                            elif world < world_got_to or (world == world_got_to and stage < stage_got_to):
                                bg_color = DARK_GREEN
                            self.show_text_colorful(str(world) + '-' + str(stage),
                                                    FIRST_STAGE_X + (STAGE_WIDTH + STAGE_SPACE_X) * (stage - 1),
                                                    FIRST_STAGE_Y + STAGE_SPACE_Y * (world-1), BIG_TEXT_SIZE, BLUE,
                                                    bg_color)
                        highlighted = [stage, world]
                else:
                    if highlighted != []:
                        highlighted = []
                        self.refresh_stages_menu_screen()
                is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if is_on_back_arrow:
                        return HOME_STATE
                    if highlighted:
                        self.screen.fill(BLACK, (100, 565, 700, 70))  # erase last message
                        print(pygame.mouse.get_pos())
                        print("selected", highlighted)
                        print("stage reached", stage_reached)
                        global stage_only_presentation, stage_selected, world_selected, stage_map_list, bool_selected_stage
                        stage_map_list = []
                        stage_only_presentation = highlighted[0] + (highlighted[1] - 1) * 9
                        stage_selected = highlighted[0]
                        world_selected = highlighted[1]
                        str_world_stage = str(highlighted[1]) + "-" + str(highlighted[0])
                        print('stage only presentation:', stage_only_presentation)
                        if stage_only_presentation > stage_reached:
                            print("user didn't reach this stage yet")
                            self.show_text_colorful("didn't reach stage " + str_world_stage + " yet", WINDOW_WIDTH // 2,
                                                    600, BIG_TEXT_SIZE, RED, BLACK)

                        else:
                            #self.show_text_colorful("selected stage " + str_world_stage, WINDOW_WIDTH // 2, 600,
                                                    #BIG_TEXT_SIZE, RED, BLACK)
                            bool_selected_stage = True
                            while not stage_map_list:
                                time.sleep(0.01)
                            print("stage map in screen thread", stage_map_list)
                            if stage_map_list == [[0]]:
                                print("stage is not available")
                                print("got here")
                                self.show_text_colorful("stage " + str_world_stage + " is not available yet", WINDOW_WIDTH // 2,
                                                    600, BIG_TEXT_SIZE, RED, BLACK)
                                stage_map_list = []

                            else:
                                return CAMPAIGN_STAGE

            # self.refresh_stages_screen()

            # stage = self.check_is_on_stage()
            # if stage != -1:
            #    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            #        STAGE_STATE = 1278
            #        return STAGE_STATE, stage

    def check_is_on_stage(self):
        world = -1
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # check x- stage:
        xmod100 = mouse_x % 100
        ymod75 = (mouse_y-125) % 75
        if (xmod100 >= 0 and xmod100 < 14) or (xmod100 > 87 and xmod100 < 100):
            # print("in the holes")
            return -1, -1
        if mouse_y >= 125 and ymod75 > 50 and ymod75 < 75:
            # print("in the holes")
            return -1, -1
        if mouse_x < 13:
            stage = -1
        else:
            stage = (mouse_x - 13) // (STAGE_WIDTH + STAGE_SPACE_X) + 1
        if stage > 9:
            # print("stage above 9")
            stage = -1

        # check y- world:
        if mouse_y < FIRST_STAGE_Y - BIG_TEXT_SIZE // 2:
            return -1, -1
        if mouse_y > FIRST_STAGE_Y - BIG_TEXT_SIZE // 2 and mouse_y < FIRST_STAGE_Y + BIG_TEXT_SIZE // 2:
            world = 1
        elif mouse_y > FIRST_STAGE_Y + BIG_TEXT_SIZE and mouse_y < FIRST_STAGE_Y + BIG_TEXT_SIZE * 2:
            world = 2
        world = (mouse_y - (FIRST_STAGE_Y - BIG_TEXT_SIZE // 2)) // STAGE_SPACE_Y + 1
        # print('stage', stage)
        # print('world', world)
        return stage, world

    def competitive_options_screen(self):
        global time_limit, prev_time_left, stage_map_list, need_comp_level, difficulty
        state = COMPETITIVE_STATE
        chose_option = False
        self.screen.fill(BLACK)
        self.show_text_colorful('Choose time limit', TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)
        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if is_on_back_arrow:
                        return HOME_STATE
                if self.check_state(event, '3 minutes', RECORDS_X, RECORDS_Y, RECORDS_WIDTH, RECORDS_HEIGHT):
                    time_limit = 3
                    chose_option = True
                if self.check_state(event, '5 minutes', COMPETITIVE_X, COMPETITIVE_Y, COMPETITIVE_WIDTH, COMPETITIVE_HEIGHT):
                    time_limit = 5
                    chose_option = True
                if self.check_state(event, '10 minutes', CAMPAIGN_X, CAMPAIGN_Y, CAMPAIGN_WIDTH, CAMPAIGN_HEIGHT):
                    time_limit = 10
                    chose_option = True
                if chose_option:
                    need_comp_level = True
                    stage_map_list = []
                    print("need_comp_level", need_comp_level)
                    difficulty = 0
                    stage_map_list = []
                    prev_time_left = time_limit * 60
                    while need_comp_level:
                        time.sleep(0.01)
                    if stage_map_list == [[0]]:
                        print("stage not available")
                        self.show_text_colorful("helper server disconnected", WINDOW_WIDTH // 2,
                                                600, BIG_TEXT_SIZE, RED, BLACK)
                        time.sleep(1)
                        return COMPETITIVE_STATE
                    return COMPETITIVE_STAGE_STATE

    def records_options_screen(self):
        print("in options records screen")
        global records_time, need_records
        global background_color, font_color, font_size
        self.screen.fill(background_color)
        self.show_text_colorful('Choose record time', TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)
        state = RECORDS_OPTIONS_STATE
        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if is_on_back_arrow:
                        return HOME_STATE
                if self.check_state(event, '3 minutes', RECORDS_X, RECORDS_Y, RECORDS_WIDTH, RECORDS_HEIGHT):
                    records_time = 3
                    need_records = True
                    while need_records:
                        time.sleep(0.01)
                    return RECORDS_STATE
                elif self.check_state(event, '5 minutes', COMPETITIVE_X, COMPETITIVE_Y, COMPETITIVE_WIDTH, COMPETITIVE_HEIGHT):
                    records_time = 5
                    need_records = True
                    while need_records:
                        time.sleep(0.01)
                    return RECORDS_STATE
                elif self.check_state(event, '10 minutes', CAMPAIGN_X, CAMPAIGN_Y, CAMPAIGN_WIDTH, CAMPAIGN_HEIGHT):
                    records_time = 10
                    need_records = True
                    while need_records:
                        time.sleep(0.01)
                    return RECORDS_STATE


    def records_screen(self):
        global records, records_time
        print("in records screen")
        state = RECORDS_OPTIONS_STATE
        global background_color, font_color, font_size
        font_color = WHITE
        self.screen.fill(background_color)
        print("records", records)
        self.show_text_colorful(str(records_time) + ' minutes records', TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)
        self.show_text_colorful('Rank', 50, TITLE_Y+BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE, WHITE, BLACK)
        self.show_text_colorful('Stage', 200, TITLE_Y + BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE,
                                font_color, BLACK)
        self.show_text_colorful('Username', 430, TITLE_Y + BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE,
                                font_color, BLACK)
        self.show_text_colorful('Date', 750, TITLE_Y + BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE,
                                font_color, BLACK)

        records_str_list = records.split('\n')
        records_list = []
        records_to_show = []
        #for i in range(len(records_list)):
        #    records_to_show.append("")
        #    records_list = records_list[1:len(records_list)-1] # removing parenthesis
        #    records_to_show.append(sql_orm.Record(r.stage, ))
        #    records_to_show[i] = str(i + 1) # rank

        for i in range(AMOUNT_OF_RECORDS):
            if len(records_str_list) > i:
                records_str_list[i] = records_str_list[i].replace("(", "")
                records_str_list[i] = records_str_list[i].replace(")", "")
                records_list.append(records_str_list[i].split(", "))
                lst = records_str_list[i].split(", ")
            else:
                lst = []
            print("lst", lst)
            if len(lst) < 5:
                rank, time, stage, name, date = "#" + str(i+1), 'N/A', 'N/A', 'N/A', 'N/A'
            else:
                rank, time, stage, name, date = "#" + lst[0], lst[1], lst[2], lst[3][1:len(lst[3])-1], lst[4][1:len(lst[4])-1]
            if rank == "#1":
                color = GOLD
            elif rank == "#2":
                color = SILVER
            elif rank == "#3":
                color = BRONZE
            else:
                color = font_color
            records_to_show.append(rank + "|" + stage + "|" + name + "|" + date)
            self.show_text_colorful(rank, 50, TITLE_Y + BIG_TEXT_SIZE*2 + i*BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE, color, BLACK)
            self.show_text_colorful(stage, 200, TITLE_Y + BIG_TEXT_SIZE * 2+ i*BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE, color, BLACK)
            if len(name) > 12:
                self.show_text_colorful(name, 430, TITLE_Y + BIG_TEXT_SIZE * 2 + i * BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE-10,
                                        color, BLACK)
            else:
                self.show_text_colorful(name, 430, TITLE_Y + BIG_TEXT_SIZE * 2+ i*BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE, color, BLACK)
            self.show_text_colorful(date, 750, TITLE_Y + BIG_TEXT_SIZE * 2+ i*BIG_TEXT_SIZE, MEDIUM_TEXT_SIZE, color, BLACK)
        #for r in records_list:

        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if is_on_back_arrow:
                        return RECORDS_OPTIONS_STATE

    def home_screen(self):
        global background_color, font_color, font_size, need_records
        state = HOME_STATE
        font_size = BIG_TEXT_SIZE
        font_color = WHITE
        background_color = BLACK
        self.screen.fill(background_color)
        self.show_text_colorful('Home', TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)

        self.show_text('Campaign', CAMPAIGN_X, CAMPAIGN_Y)
        self.show_text('Competitive', COMPETITIVE_X, COMPETITIVE_Y)
        self.show_text('Records', RECORDS_X, RECORDS_Y)
        self.show_text('How to play', HOW_TO_PLAY_X, HOW_TO_PLAY_Y)

        # self.update_back_arrow()

        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                # is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    pass
                    # if is_on_back_arrow:
                    # return WELCOME_STATE
                if self.check_state(event, 'Records', RECORDS_X, RECORDS_Y, RECORDS_WIDTH, RECORDS_HEIGHT):
                    print("returning records state")
                    return RECORDS_OPTIONS_STATE
                if self.check_state(event, 'Competitive', COMPETITIVE_X, COMPETITIVE_Y, COMPETITIVE_WIDTH,
                                    COMPETITIVE_HEIGHT):
                    return COMPETITIVE_STATE
                if self.check_state(event, 'Campaign', CAMPAIGN_X, CAMPAIGN_Y, CAMPAIGN_WIDTH, CAMPAIGN_HEIGHT):
                    return STAGES_MENU_STATE
                if self.check_state(event, 'How to play', HOW_TO_PLAY_X, HOW_TO_PLAY_Y, HOW_TO_PLAY_WIDTH, HOW_TO_PLAY_HEIGHT):
                    return HOW_TO_PLAY_STATE

    def check_state(self, event, text, x, y, width, height):
        if self.is_mouse_in_area(x, y, width, height):
            self.show_text_colorful(text, x, y, height, BLUE, DARK_GRAY)
            pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                return True
        else:
            self.show_text_colorful(text, x, y, height, WHITE, DARK_GRAY)
        return False

    def account_screen(self, log_in):
        print("in create account")
        global font_color, font_size
        global account_response
        state = DEFAULT
        username_input, password_input = "", ""
        self.draw_account_screen(log_in)
        self.update_back_arrow()
        hide_password = True
        while True:
            for event in pygame.event.get():
                if state == QUIT_STATE or event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return QUIT_STATE
                if state == WELCOME_STATE:
                    return WELCOME_STATE
                is_on_back_arrow = self.update_back_arrow()
                if state == DEFAULT:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # print(pygame.mouse.get_pos())
                        if is_on_back_arrow:
                            return WELCOME_STATE
                        state = self.account_check_mouse()
                        if state == WELCOME_STATE:
                            return WELCOME_STATE
                # elif state == WELCOME_STATE:
                #    return WELCOME_STATE
                elif state == INSERTING_USER_NAME:
                    state, username_input = self.get_screen_input(USERNAME_X + 90, USERNAME_Y,
                                                                            MAX_USERNAME_LEN,
                                                                            username_input, hide_data=False)
                elif state == INSERTING_PASSWORD:
                    state, password_input = self.get_screen_input(PASSWORD_X + 90, PASSWORD_Y,
                                                                            MAX_PASSWORD_LEN,
                                                                            password_input, hide_data=hide_password)
                elif state == SHOW_HIDE_PASSWORD:
                    print("show hide pass")
                    hide_password = not hide_password
                    self.screen.fill(background_color, (SHOW_HIDE_PASSWORD_X - SHOW_HIDE_PASSWORD_WIDTH // 2,
                                                        SHOW_HIDE_PASSWORD_Y - SHOW_HIDE_PASSWORD_HEIGHT // 2,
                                                        SHOW_HIDE_PASSWORD_WIDTH, SHOW_HIDE_PASSWORD_HEIGHT + 3))
                    if hide_password:
                        self.show_text_colorful('Show Password', SHOW_HIDE_PASSWORD_X, SHOW_HIDE_PASSWORD_Y,
                                                MEDIUM_TEXT_SIZE, BLUE, WHITE)
                        hidden_data = '*' * len(password_input)
                        self.delete_input(PASSWORD_X + 90, PASSWORD_Y, MAX_USERNAME_LEN)
                        self.show_input(hidden_data, PASSWORD_X + 90, PASSWORD_Y, MAX_USERNAME_LEN)
                        pygame.display.flip()
                    else:
                        self.show_text_colorful('Hide Password', SHOW_HIDE_PASSWORD_X, SHOW_HIDE_PASSWORD_Y,
                                                MEDIUM_TEXT_SIZE, BLUE, WHITE)
                        self.delete_input(PASSWORD_X + 90, PASSWORD_Y, MAX_USERNAME_LEN)
                        self.show_input(password_input, PASSWORD_X + 90, PASSWORD_Y, MAX_USERNAME_LEN)
                        pygame.display.flip()
                    state = DEFAULT

                elif state == SUBMITTED:
                    print("username:", username_input)
                    print("password:", password_input)
                    error_str = self.check_username_and_password(username_input, password_input)
                    if error_str != "":
                        self.screen.fill(background_color, (0, 285, 700, 35))
                        self.show_text(error_str, ACCOUNT_RESULT_X, ACCOUNT_RESULT_Y)
                        state = DEFAULT

                    else:
                        global username, password
                        global login, create_account
                        account_response = ''
                        username = username_input
                        password = password_input
                        login = log_in
                        create_account = not log_in
                        while account_response == '':
                            time.sleep(0.01)
                        print("account response is not empty")
                        print("account response", account_response)
                        if account_response == "success":
                            print("success lets go!")
                            # self.screen.fill(background_color, (0, 285, 700, 35))
                            # self.show_text("success", ACCOUNT_RESULT_X, ACCOUNT_RESULT_Y)
                            return HOME_STATE
                        else:
                            self.draw_account_screen(log_in)
                            self.screen.fill(background_color, (0, 285, 700, 35))
                            self.show_text(account_response, ACCOUNT_RESULT_X, ACCOUNT_RESULT_Y)
                            state = DEFAULT
                            username_input, password_input = "", ""

    def draw_account_screen(self, log_in):
        global font_color, font_size
        font_size = MEDIUM_TEXT_SIZE
        font_color = WHITE
        self.screen.fill(BLACK)
        self.show_text_colorful('Username', USERNAME_X, USERNAME_Y, MEDIUM_TEXT_SIZE, WHITE, BLACK)
        self.show_text_colorful('Password', PASSWORD_X, PASSWORD_Y, MEDIUM_TEXT_SIZE, WHITE, BLACK)
        self.show_text_colorful('Submit', SUBMIT_X, SUBMIT_Y, MEDIUM_TEXT_SIZE, BLUE, WHITE)

        if log_in:
            self.show_text_colorful('Login', TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)
        else:
            self.show_text_colorful('Create new account', TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)
        self.show_text_colorful('Show Password', SHOW_HIDE_PASSWORD_X, SHOW_HIDE_PASSWORD_Y, MEDIUM_TEXT_SIZE, BLUE,
                                WHITE)
        pygame.draw.rect(self.screen, RED,
                         pygame.Rect(USERNAME_X + 90, USERNAME_Y - font_size * 2 // 3, MAX_USERNAME_LEN * font_size,
                                     USERNAME_FIELD_HEIGHT + font_size // 3), 5)  # 200, 40(field, height)
        pygame.draw.rect(self.screen, RED,
                         pygame.Rect(USERNAME_X + 90, PASSWORD_Y - font_size * 2 // 3, MAX_PASSWORD_LEN * font_size,
                                     PASSWORD_FIELD_HEIGHT + font_size // 3), 5)
        pygame.display.flip()

    def check_username_and_password(self, username, password):
        if len(username) < 4:
            return "username must be at least 4 chars long"
        if len(password) < 8:
            return "password must be at least 8 chars long"
        return ""

    def account_check_mouse(self):
        if self.is_mouse_in_rect(USERNAME_X + 90, USERNAME_Y - 15, USERNAME_X + 90 + USERNAME_FIELD_WIDTH,
                              USERNAME_Y - 15 + USERNAME_FIELD_HEIGHT):
            print("INSERTING_USER_NAME")
            return INSERTING_USER_NAME
        elif self.is_mouse_in_rect(USERNAME_X + 90, PASSWORD_Y - 15, USERNAME_X + 90 + PASSWORD_FIELD_WIDTH,
                                PASSWORD_Y - 15 + PASSWORD_FIELD_HEIGHT):
            print("INSERTING_PASSWORD")
            return INSERTING_PASSWORD
        elif self.is_mouse_in_area(SUBMIT_X, SUBMIT_Y, SUBMIT_WIDTH, SUBMIT_HEIGHT):
            print("SUBMITTED")
            return SUBMITTED
        elif self.is_mouse_in_area(SHOW_HIDE_PASSWORD_X, SHOW_HIDE_PASSWORD_Y, SHOW_HIDE_PASSWORD_WIDTH,
                                   SHOW_HIDE_PASSWORD_HEIGHT):
            print("SHOW/HIDE PASSWORD")
            return SHOW_HIDE_PASSWORD
        else:
            print("DEFAULT")
            return DEFAULT

    def is_mouse_in_area(self, x, y, width, height):
        return self.is_mouse_in_rect(x - width // 2, y - height // 2, x + width // 2, y + height // 2)

    def welcome_screen(self):
        global font_color, font_size
        font_size = BIG_TEXT_SIZE
        font_color = WHITE
        self.screen.fill(BLACK)
        self.show_lines_colorful(['Welcome to:', 'Find best route game'], TITLE_X, TITLE_Y, BIG_TEXT_SIZE, GREEN, BLACK)
        self.draw_welcome_create_new_account(WHITE, DARK_GRAY)
        self.draw_welcome_login(WHITE, DARK_GRAY)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return QUIT_STATE
                if self.is_mouse_in_area(WELCOME_CREATE_ACCOUNT_X, WELCOME_CREATE_ACCOUNT_Y,
                                         WELCOME_CREATE_ACCOUNT_WIDTH, BIG_TEXT_SIZE):
                    # self.show_text_colorful('Create new account', 300, WINDOW_HEIGHT//2, 44, BLUE, BLACK)
                    self.draw_welcome_create_new_account(BLUE, DARK_GRAY)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                        return CREATE_ACCOUNT_STATE
                else:
                    # self.show_text_colorful('Create new account', 300, WINDOW_HEIGHT//2, 44, WHITE, BLACK)
                    self.draw_welcome_create_new_account(WHITE, DARK_GRAY)
                if self.is_mouse_in_area(WELCOME_LOGIN_X, WELCOME_LOGIN_Y, WELCOME_LOGIN_WIDTH, BIG_TEXT_SIZE):
                    # self.show_text_colorful('Login', 700, WINDOW_HEIGHT//2, 44, BLUE, DARK_GRAY)
                    self.draw_welcome_login(BLUE, DARK_GRAY)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                        return LOGIN_STATE
                else:
                    # self.show_text_colorful('Login', 700, WINDOW_HEIGHT//2, 44, WHITE, DARK_GRAY)
                    self.draw_welcome_login(WHITE, DARK_GRAY)


    def get_screen_input(self, x_pos, y_pos, max_len, entered_data, hide_data):
        global font_color, font_size, background_color
        font_color = WHITE
        font_size = MEDIUM_TEXT_SIZE
        background_color = BLACK
        # self.screen.fill(GREEN, (x_pos - font_size//2, y_pos-MEDIUM_TEXT_SIZE//2, MEDIUM_TEXT_SIZE, MEDIUM_TEXT_SIZE))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return QUIT_STATE, ""
                if event.type == pygame.KEYDOWN:
                    # valid_str = string.printable
                    valid_str = string.ascii_letters + string.digits + string.punctuation
                    valid_str = valid_str.replace(",", "")
                    valid_str = valid_str.replace("\"", "")
                    valid_str = valid_str.replace("\"", "")
                    valid_list = list(valid_str)
                    if len(entered_data) < max_len and event.unicode in valid_list:
                        input_char = event.unicode
                        entered_data += input_char
                        self.delete_input(x_pos, y_pos, max_len)
                        if not hide_data:
                            self.show_input(entered_data, x_pos, y_pos, max_len)
                        else:
                            hidden_data = '*' * len(entered_data)
                            self.show_input(hidden_data, x_pos, y_pos, max_len)
                        # x_pos += font_size//2 + SMALL_SPACE
                    elif event.key == pygame.K_BACKSPACE and entered_data != "":
                        entered_data = entered_data[:-1]
                        self.delete_input(x_pos, y_pos, max_len)
                        if not hide_data:
                            self.show_input(entered_data, x_pos, y_pos, max_len)
                        else:
                            hidden_data = '*' * len(entered_data)
                            self.show_input(hidden_data, x_pos, y_pos, max_len)
                        # x_pos -= font_size // 2 + SMALL_SPACE
                    elif event.key == pygame.K_RETURN:  # and entered_data != "":
                        return DEFAULT, entered_data
                is_on_back_arrow = self.update_back_arrow()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if is_on_back_arrow:
                        print("returning welcome state")
                        return WELCOME_STATE, ''
                    state = self.account_check_mouse()
                    return state, entered_data

    def update_back_arrow(self):
        if self.is_mouse_in_rect(WINDOW_WIDTH - 100, WINDOW_HEIGHT - 79, WINDOW_WIDTH, WINDOW_HEIGHT):
            self.show_image(r'photos/cyan_arrow.PNG', WINDOW_WIDTH - 100, WINDOW_HEIGHT - 79)
            return True
        self.show_image(r'photos/gray_arrow.PNG', WINDOW_WIDTH - 100, WINDOW_HEIGHT - 79)
        return False

    def delete_input(self, x_pos, y_pos, max_len):
        global font_size, background_color
        self.screen.fill(background_color,
                         (x_pos + 7, y_pos - font_size // 2, font_size * max_len - 20, font_size + 2))

    def show_input(self, input, x_pos, y_pos, max_len):
        global font_size, background_color
        center_x = x_pos + max_len * font_size // 2
        self.show_text(input, center_x, y_pos)

    def is_mouse_in_rect(self, min_x, min_y, max_x, max_y):
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos[0], mouse_pos[1]
        if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
            return True
        return False

    def draw_welcome_create_new_account(self, color, background_color):
        self.show_text_colorful('Create new account', WELCOME_CREATE_ACCOUNT_X, WELCOME_CREATE_ACCOUNT_Y,
                                BIG_TEXT_SIZE, color, background_color)

    def draw_welcome_login(self, color, background_color):
        self.show_text_colorful('Login', WELCOME_LOGIN_X, WELCOME_LOGIN_Y, BIG_TEXT_SIZE, color, background_color)

    def show_lines_colorful(self, lines, x, y, size, font_color, background_color):
        for line in lines:
            self.show_text_colorful(line, x, y, size, font_color, background_color)
            y += size + 3

    def show_lines(self, lines, x, y):
        global font_size
        for line in lines:
            self.show_text(line, x, y)
            y += font_size + 3

    def show_text_colorful(self, text, x, y, size, font_color, background_color):
        font = pygame.font.Font(FONT, size)
        text_object = font.render(text, True, font_color, background_color)  # text, antialias, color, background
        text_rect = text_object.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_object, text_rect)
        pygame.display.flip()

    def show_text(self, text, x, y):
        global font_color, font_size, background_color
        font = pygame.font.Font(FONT, font_size)
        text_object = font.render(text, True, font_color, background_color)  # text, antialias, color, background
        text_rect = text_object.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_object, text_rect)
        pygame.display.flip()

    def show_image(self, img_dir, x, y):
        image = pygame.image.load(img_dir).convert()
        image.set_colorkey(PINK)  # 255, 20, 147
        image.set_colorkey(PINK)
        # print(PINK)
        self.screen.blit(image, (x, y))
        pygame.display.flip()


class CommunicationThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket()
        self.key = None
        # print("finished CommunicationThread init")

    def run(self):
        global locker
        ip = sys.argv[1]
        self.thread_started()
        self.sock.connect((ip, PORT))
        self.send_with_size("CLIENT_hello server")
        self.key = dh_aes.DiffieHelman_recieve_pg(self.sock)
        global login, create_account, username, password, account_response, did_quit
        account_response = ''
        while account_response != 'success':
            # account_response = ''
            while not login and not create_account:
                time.sleep(0.01)
                if did_quit:
                    break
            self.account_comm()
            if did_quit:
                return False
            login = False
            create_account = False
        # locker.release()
        print("account response is successfull")

        global bool_selected_stage, stage_only_presentation, passed_campaign_stage # campaign
        global need_comp_level, difficulty, finished_competitive  # competitive
        global stage_map_list  # both campaign and competitive
        while True:
            time.sleep(0.01)
            if bool_selected_stage:
                self.stage_map_comm(False)
            if passed_campaign_stage:
                self.passed_campaign_stage_comm()
            if need_comp_level:
                self.stage_map_comm(True)
                need_comp_level = False
            if finished_competitive:
                self.check_record_comm()
            if need_records:
                self.records_comm()
            if did_quit:
                self.send_with_size('DISCONN')
                break
    def records_comm(self):
        global records, need_records, records_time
        self.send_with_size('RECORDS' + str(records_time))
        msg_type, msg_body = self.receive_by_protocol()
        if msg_type != 'RECORDS':
            print("wrong protocol")
            records = 'none'
        else:
            records = msg_body
        need_records = False

    def check_record_comm(self):
        global comp_stage, time_limit, record_broken, finished_competitive
        self.send_with_size('STATIME' + str(comp_stage) + '\n' + str(time_limit))
        msg_type, msg_body = self.receive_by_protocol()
        if msg_type == 'NEWRECO':
            print("broken record well played")
            record_broken = BROKEN
        elif msg_type == 'NOTRECO':
            print("didn't break a record")
            record_broken = NOT_BROKEN
        else:
            record_broken = NOT_BROKEN
            print("wrong protocol")
        finished_competitive = False


    def passed_campaign_stage_comm(self):
        global passed_campaign_stage
        self.send_with_size('BEATSTA' + str(stage_selected))
        passed_campaign_stage = False


    def stage_map_comm(self, is_competitive):
        global stage_only_presentation, stage_map_list, bool_selected_stage
        global need_comp_level, difficulty
        map_list = []
        if not is_competitive:
            self.send_with_size('GETSTAG' + str(stage_only_presentation))
        else:
            self.send_with_size('GETCOMP' + str(difficulty))
        msg_type, msg_body = self.receive_by_protocol()
        print('msg_type', msg_type)
        print('msg_body', msg_body)
        if not is_competitive:
            expected_msg_type = 'RETSTAG'
        else:
            expected_msg_type = 'RETCOMP'
        if msg_type == expected_msg_type:
            print("protocol correct")
            if msg_body == "none" or msg_body == "":
                print("error file not found in server")
                stage_map_list = [[0]]
            else:
                points = msg_body.split('\n')
                print("points", points)
                for p in points:
                    map_list.append(p.split(', '))
                for point in map_list:
                    point[0] = int(point[0])
                    point[1] = int(point[1])
                print("map list in comms", map_list)
                stage_map_list = map_list
        else:
            print("protocol error")
            stage_map_list = [[0]]

        if not is_competitive:
            bool_selected_stage = False
        else:
            need_comp_level = False

    def account_comm(self):
        global login, create_account, account_response, stage_reached, did_quit
        if did_quit:
            self.send_encrypted_msg("DISCONN")
            return False
        account_response = ''
        if create_account:
            msg_type = 'NEWUSER'
        else:
            msg_type = 'EXSUSER'
        data = msg_type + username + '\n' + password
        self.send_encrypted_msg(data)
        msg_type, msg_body = self.receive_by_protocol()
        if create_account:
            print('msg_type', msg_type)
            print('msg_body', msg_body)
            if msg_type == "NEWUSER":
                print("success")
                stage_reached = 1
                account_response = 'success'
            elif msg_type == 'ERRNEW_':
                print("failed")
                account_response = "Username already exists"
        if login:
            print('msg_type', msg_type)
            print('msg_body', msg_body)
            if msg_type == "EXSUSER":
                print("success")
                stage_reached = int(msg_body)
                print("stage_reached", stage_reached)
                account_response = 'success'
            elif msg_type == 'ERREXS_':
                print("failed")
                account_response = "Incorrect username or password"

    def receive_by_protocol(self):
        data = self.receive_by_size()
        msg_type = data[:MESSAGE_TYPE_LENGTH]
        msg_body = data[MESSAGE_TYPE_LENGTH:]
        return msg_type, msg_body

    def send_with_size(self, data):
        tcp_by_size.send_with_size(self.sock, data.encode())

    def receive_by_size(self):
        return tcp_by_size.recv_by_size(self.sock).decode()

    def send_encrypted_msg(self, msg):
        dh_aes.send_encrypted_data(self.sock, self.key, msg)

    def receive_encrypted_msg(self):
        return dh_aes.receive_encrypted_data(self.sock, self.key)


def main():

    screen_thread = ScreenThread()
    screen_thread.start()

    communication_thread = CommunicationThread()
    communication_thread.start()


if __name__ == '__main__':
    main()
