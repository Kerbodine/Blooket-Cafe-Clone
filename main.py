# Importing modules
try:
     import pygame
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

import os
import sys
import csv
import random
import datetime

from pygame.constants import KEYDOWN, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN

# Setup
WIDTH, HEIGHT = 800,600
D_WIDTH, D_HEIGHT = 1600,1200
screen = pygame.display.set_mode((WIDTH,HEIGHT))
display = pygame.Surface((D_WIDTH, D_HEIGHT))
scale_factor = D_WIDTH / WIDTH
pygame.display.set_caption("Python - Blooket Café")
icon = pygame.image.load(os.path.join("assets", "icon.png"))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
quality = "Fancy"
FPS = 30

# File setup
quiz_config_list = []
with open("quiz_config.csv", "r") as quiz_config_file:
    quiz_config_reader = csv.reader(quiz_config_file)
    for line in quiz_config_reader:
        quiz_config_list.append(line)

questions_list = []
with open(f"quiz_files/{quiz_config_list[0][1]}.csv", "r") as questions_file:
    questions_reader = csv.reader(questions_file, delimiter="\t")
    for line in questions_reader:
        questions_list.append(line)

time_limit = int(quiz_config_list[1][1])  # Game length in minutes
time_limit_ticks = time_limit * 60 * FPS  # Adjusted game length in ticks

customer_interval = int(quiz_config_list[2][1])
reward_multiplier = int(quiz_config_list[3][1])

pygame.init()
pygame.mixer.init()

# Events
ADDCUSTOMER = pygame.USEREVENT
FINISHGAME = pygame.USEREVENT + 1

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (247,247,247)

YELLOW = (255,163,29)
BLUE = (50,120,255)
GREEN = (0,199,114)
RED = (255,71,43)

TEXT_RED = (196,60,54)
TEXT_GREEN = (81,196,54)

# Fonts
font_sourcesans_light_72 = pygame.font.Font("fonts/SourceSansPro-Light.ttf", 72)

font_sourcesans_regular_36 = pygame.font.Font("fonts/SourceSansPro-Regular.ttf", 36)
font_sourcesans_regular_50 = pygame.font.Font("fonts/SourceSansPro-Regular.ttf", 50)
font_sourcesans_regular_80 = pygame.font.Font("fonts/SourceSansPro-Regular.ttf", 80)

font_sourcesans_semi_bold_36 = pygame.font.Font("fonts/SourceSansPro-SemiBold.ttf", 36)

font_sourcesans_bold_36 = pygame.font.Font("fonts/SourceSansPro-Bold.ttf", 36)
font_sourcesans_bold_64 = pygame.font.Font("fonts/SourceSansPro-Bold.ttf", 64)

# Importing sounds
background_track1 = pygame.mixer.Sound("sound/Airport_Lounge.mp3")
background_track2 = pygame.mixer.Sound("sound/Apero_Hour.mp3")
background_track3 = pygame.mixer.Sound("sound/Bossa_Antigua.mp3")

sfx_pay = pygame.mixer.Sound("sound/pay.wav")
sxf_upgrade = pygame.mixer.Sound("sound/upgrade.wav")
sxf_correct = pygame.mixer.Sound("sound/correct.wav")
sxf_wrong = pygame.mixer.Sound("sound/wrong.wav")

pygame.mixer.Sound.set_volume(background_track1, 0.5)
pygame.mixer.Sound.set_volume(background_track2, 0.5)
pygame.mixer.Sound.set_volume(background_track3, 0.5)
pygame.mixer.Sound.set_volume(sfx_pay, 0.5)
pygame.mixer.Sound.set_volume(sxf_upgrade, 0.5)
pygame.mixer.Sound.set_volume(sxf_correct, 0.5)
pygame.mixer.Sound.set_volume(sxf_wrong, 0.5)

background_sound = [background_track1, background_track2, background_track3]

# Importing images
ui_scene_main = pygame.image.load(os.path.join("assets", "ui_scene_main.png")).convert()
ui_scene_question = pygame.image.load(os.path.join("assets", "ui_blooket_question.png")).convert()
ui_scene_correct = pygame.image.load(os.path.join("assets", "ui_correct.png")).convert()
ui_scene_incorrect = pygame.image.load(os.path.join("assets", "ui_incorrect.png")).convert()
ui_scene_end = pygame.image.load(os.path.join("assets", "ui_endscreen.png")).convert()
ui_store = pygame.image.load(os.path.join("assets", "ui_store.png")).convert()

ui_plate_normal = pygame.image.load(os.path.join("assets", "ui_items","plate_normal.png")).convert_alpha()
ui_plate_locked = pygame.image.load(os.path.join("assets", "ui_items","plate_locked.png")).convert_alpha()
ui_textbubble = pygame.image.load(os.path.join("assets", "ui_items","ui_textbubble.png")).convert_alpha()

ui_sound = pygame.image.load(os.path.join("assets", "ui_items","ui_sound.png")).convert()
ui_mute = pygame.image.load(os.path.join("assets", "ui_items","ui_mute.png")).convert()

ui_toast_small = pygame.image.load(os.path.join("assets", "ui_items","toast_small.png")).convert_alpha()
ui_cereal_small = pygame.image.load(os.path.join("assets", "ui_items","cereal_small.png")).convert_alpha()
ui_yogurt_small = pygame.image.load(os.path.join("assets", "ui_items","yogurt_small.png")).convert_alpha()
ui_breakfast_combo_small = pygame.image.load(os.path.join("assets", "ui_items","breakfast_combo_small.png")).convert_alpha()
ui_orange_juice_small = pygame.image.load(os.path.join("assets", "ui_items","orange_juice_small.png")).convert_alpha()
ui_milk_small = pygame.image.load(os.path.join("assets", "ui_items","milk_small.png")).convert_alpha()
ui_waffle_small = pygame.image.load(os.path.join("assets", "ui_items","waffle_small.png")).convert_alpha()
ui_pancakes_small = pygame.image.load(os.path.join("assets", "ui_items","pancakes_small.png")).convert_alpha()
ui_french_toast_small = pygame.image.load(os.path.join("assets", "ui_items","french_toast_small.png")).convert_alpha()

ui_toast_normal = pygame.image.load(os.path.join("assets", "ui_items","toast_normal.png")).convert_alpha()
ui_cereal_normal = pygame.image.load(os.path.join("assets", "ui_items","cereal_normal.png")).convert_alpha()
ui_yogurt_normal = pygame.image.load(os.path.join("assets", "ui_items","yogurt_normal.png")).convert_alpha()
ui_breakfast_combo_normal = pygame.image.load(os.path.join("assets", "ui_items","breakfast_combo_normal.png")).convert_alpha()
ui_orange_juice_normal = pygame.image.load(os.path.join("assets", "ui_items","orange_juice_normal.png")).convert_alpha()
ui_milk_normal = pygame.image.load(os.path.join("assets", "ui_items","milk_normal.png")).convert_alpha()
ui_waffle_normal = pygame.image.load(os.path.join("assets", "ui_items","waffle_normal.png")).convert_alpha()
ui_pancakes_normal = pygame.image.load(os.path.join("assets", "ui_items","pancakes_normal.png")).convert_alpha()
ui_french_toast_normal = pygame.image.load(os.path.join("assets", "ui_items","french_toast_normal.png")).convert_alpha()

ui_characters = []
for i in range(40):
    ui_characters.append(pygame.image.load(os.path.join("assets", "ui_characters", "character" + str(i + 1) + ".png")).convert_alpha())

# Unlocked dishes
unlocked_items = {
    "Toast": True,
    "Cereal": False,
    "Yogurt": False,
    "Breakfast_combo": False,
    "Orange_juice": False,
    "Milk": False,
    "Waffle": False,
    "Pancakes": False,
    "French_toast": False,
}
# Inventory count
item_counts = {
    "Toast": 0,
    "Cereal": 0,
    "Yogurt": 0,
    "Breakfast_combo": 0,
    "Orange_juice": 0,
    "Milk": 0,
    "Waffle": 0,
    "Pancakes": 0,
    "French_toast": 0,
}
# Food item levels
item_levels = {
    "Toast": 1,
    "Cereal": 0,
    "Yogurt": 0,
    "Breakfast_combo": 0,
    "Orange_juice": 0,
    "Milk": 0,
    "Waffle": 0,
    "Pancakes": 0,
    "French_toast": 0,
}
# Price at level 1
item_price = {
    "Toast": 25,
    "Cereal": 30,
    "Yogurt": 35,
    "Breakfast_combo": 40,
    "Orange_juice": 45,
    "Milk": 50,
    "Waffle": 55,
    "Pancakes": 60,
    "French_toast": 65,
}
# Prices given level
item_price_adjusted = {
    "Toast": None,
    "Cereal": None,
    "Yogurt": None,
    "Breakfast_combo": None,
    "Orange_juice": None,
    "Milk": None,
    "Waffle": None,
    "Pancakes": None,
    "French_toast": None,
}
# Customer demand images
small_item_images = {
    "Toast": ui_toast_small,
    "Cereal": ui_cereal_small,
    "Yogurt": ui_yogurt_small,
    "Breakfast_combo": ui_breakfast_combo_small,
    "Orange_juice": ui_orange_juice_small,
    "Milk": ui_milk_small,
    "Waffle": ui_waffle_small,
    "Pancakes": ui_pancakes_small,
    "French_toast": ui_french_toast_small,
}
# Item index to item name dictionary
item_number_to_name = {
    1: "Toast",
    2: "Cereal",
    3: "Yogurt",
    4: "Breakfast_combo",
    5: "Orange_juice",
    6: "Milk",
    7: "Waffle",
    8: "Pancakes",
    9: "French_toast",
}
# Food plate images
normal_item_images = {
    1: ui_toast_normal,
    2: ui_cereal_normal,
    3: ui_yogurt_normal,
    4: ui_breakfast_combo_normal,
    5: ui_orange_juice_normal,
    6: ui_milk_normal,
    7: ui_waffle_normal,
    8: ui_pancakes_normal,
    9: ui_french_toast_normal,
}

question_text_list = []
for item in questions_list:
    question_text_list.append(item[0])

answers_list = []
for item in questions_list:
    answers_list.append(item[1])

# Customer class
class Customer:
    def __init__(self, type, request_items, cash):
        self.type = type
        self.request_items = request_items
        self.temp_cash = cash

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

# Wrapping text in a paragraph
def render_textrect(string, font, rect, text_color, background_color, justification=0):

    final_lines = []

    requested_lines = string.splitlines()

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # for word in words:
            #     if font.size(word)[0] >= rect.width:
            #         raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        # if accumulated_height + font.size(line)[1] >= rect.height:
        #     raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            # else:
            #     raise TextRectException("Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface

# Main page
def main():
    
    cash = 0

    background_track_num = random.randint(1,3)
    background_track = background_sound[background_track_num - 1]
    background_track.play()

    run = True
    customers_list = []
    question_page = False
    guessed = True
    
    mute = False

    active_time = 0
    active_time_customer = 0

    display_correct = False
    display_incorrect = False
    store = False

    plate = None

    correct_answers = 0
    incorrect_answers = 0

    mute_rect = pygame.Rect(1500,20,80,80)
    mute_icon_rect = pygame.Rect(1505,25,70,70)

    plates_rect = pygame.Rect(200,530,1200,490)

    answer1_rect = pygame.Rect(20,640,770,260)
    answer2_rect = pygame.Rect(810,640,770,260)
    answer3_rect = pygame.Rect(20,920,770,260)
    answer4_rect = pygame.Rect(810,920,770,260)

    answer1_text_rect = pygame.Rect(40,660,730,200)
    answer2_text_rect = pygame.Rect(835,660,730,200)
    answer3_text_rect = pygame.Rect(40,940,730,200)
    answer4_text_rect = pygame.Rect(835,940,730,200)

    plate1_rect = pygame.Rect(220,560,200,200)
    plate2_rect = pygame.Rect(460,560,200,200)
    plate3_rect = pygame.Rect(700,560,200,200)
    plate4_rect = pygame.Rect(940,560,200,200)
    plate5_rect = pygame.Rect(1180,560,200,200)
    plate6_rect = pygame.Rect(340,760,200,200)
    plate7_rect = pygame.Rect(580,760,200,200)
    plate8_rect = pygame.Rect(820,760,200,200)
    plate9_rect = pygame.Rect(1060,760,200,200)

    customer1_rect = pygame.Rect(40,296,160,184)
    customer2_rect = pygame.Rect(560,296,160,184)
    customer3_rect= pygame.Rect(1080,296,160,184)

    customer1_text_rect = pygame.Rect(260,160,260,320)
    customer2_text_rect = pygame.Rect(780,160,260,320)
    customer3_text_rect = pygame.Rect(1300,160,260,320)

    item1_store_rect = pygame.Rect(160,200,400,200)
    item2_store_rect = pygame.Rect(600,200,400,200)
    item3_store_rect = pygame.Rect(1040,200,400,200)
    item4_store_rect = pygame.Rect(160,440,400,200)
    item5_store_rect = pygame.Rect(600,440,400,200)
    item6_store_rect = pygame.Rect(1040,440,400,200)
    item7_store_rect = pygame.Rect(160,680,400,200)
    item8_store_rect = pygame.Rect(600,680,400,200)
    item9_store_rect = pygame.Rect(1040,680,400,200)

    button_restock_food = pygame.Rect(600,1040,400,120)
    button_store = pygame.Rect(1320,1040,240,120)
    button_store_back = pygame.Rect(40,1040,240,120)

    def draw_sound(mute):
        if mute:
            display.blit(ui_mute, mute_icon_rect)
            pygame.mixer.Sound.set_volume(background_track1, 0)
            pygame.mixer.Sound.set_volume(background_track2, 0)
            pygame.mixer.Sound.set_volume(background_track3, 0)
            pygame.mixer.Sound.set_volume(sfx_pay, 0)
            pygame.mixer.Sound.set_volume(sxf_upgrade, 0)
            pygame.mixer.Sound.set_volume(sxf_correct, 0)
            pygame.mixer.Sound.set_volume(sxf_wrong, 0)

        else:
            display.blit(ui_sound, mute_icon_rect)
            pygame.mixer.Sound.set_volume(background_track1, 0.5)
            pygame.mixer.Sound.set_volume(background_track2, 0.5)
            pygame.mixer.Sound.set_volume(background_track3, 0.5)
            pygame.mixer.Sound.set_volume(sfx_pay, 0.5)
            pygame.mixer.Sound.set_volume(sxf_upgrade, 0.5)
            pygame.mixer.Sound.set_volume(sxf_correct, 0.5)
            pygame.mixer.Sound.set_volume(sxf_wrong, 0.5)

    def draw_time(active_time):
        time_remaining = round((time_limit_ticks - active_time) / FPS)
        time_converted = str(datetime.timedelta(seconds=time_remaining))
        time_text = font_sourcesans_regular_50.render(time_converted, True, BLACK)
        time_rect = time_text.get_rect(topleft = (40,160))
        display.blit(time_text, time_rect)

    def update_prices(item_price_adjusted):
        for key in list(item_price_adjusted):
            item_price_adjusted[key] = item_price[key] * (item_levels[key] ** 2 / 2)

    def draw_customers(customers_list):
        
        starting_x = 40
        x_distance = 520
        x_offset = 0

        starting_y = 190
        y_distance = 89
        y_offset = 0

        for customer in customers_list:
            character_type = int(customer.type)
            display.blit(ui_characters[character_type - 1],(starting_x + x_offset, 296))
            display.blit(ui_textbubble,(starting_x + x_offset + 180, 160))
            
            for _ in customer.request_items:
                for item in list(customer.request_items):
                    if customer.request_items[item] != 0:
                        display.blit(small_item_images[item], (starting_x + x_offset + 250, starting_y + y_offset))
                        text_rect = pygame.Rect(starting_x + x_offset + 330, starting_y + y_offset, 80, 50)
                        text_surface = font_sourcesans_bold_64.render("x" + str(customer.request_items[item]), True, BLACK)
                        display.blit(text_surface, text_rect)
                        y_offset += y_distance
                y_offset = 0
            
            y_offset = 0
            x_offset += x_distance

    def draw_cash(cash):
        cash_surface = font_sourcesans_light_72.render("Cash: " + str(cash), True, BLACK)
        cash_rect = cash_surface.get_rect(topright = (1460,15))
        display.blit(cash_surface, cash_rect)

    def draw_plates(unlocked_items):
        plate_starting_x_top = 220
        plate_starting_x_bottom = 340
        plate_x_distance = 240
        plate_x_offset_top = 0
        plate_x_offset_bottom = 0

        for i, item in enumerate(unlocked_items):
            if i < 5:
                if unlocked_items[item] == True:
                    display.blit(ui_plate_normal,(plate_starting_x_top + plate_x_offset_top, 560))
                    if item_counts[item] > 0:
                        display.blit(normal_item_images[i + 1],(plate_starting_x_top + plate_x_offset_top + 50, 610))

                    text_surf = font_sourcesans_bold_36.render(str(item_counts[item]), True, WHITE)
                    text_rect = text_surf.get_rect(center=(plate_starting_x_top + plate_x_offset_top + 180, 730))
                    display.blit(text_surf,text_rect)

                elif unlocked_items[item] == False:
                    display.blit(ui_plate_locked,(plate_starting_x_top + plate_x_offset_top, 560))
                plate_x_offset_top += plate_x_distance

            elif i >= 5:
                if unlocked_items[item] == True:
                    display.blit(ui_plate_normal,(plate_starting_x_bottom + plate_x_offset_bottom, 760))
                    if item_counts[item] > 0:
                        display.blit(normal_item_images[i + 1],(plate_starting_x_bottom + plate_x_offset_bottom + 50, 810))

                    text_surf = font_sourcesans_bold_36.render(str(item_counts[item]), True, WHITE)
                    text_rect = text_surf.get_rect(center=(plate_starting_x_bottom + plate_x_offset_bottom + 180, 930))
                    display.blit(text_surf,text_rect)

                elif unlocked_items[item] == False:
                    display.blit(ui_plate_locked,(plate_starting_x_bottom + plate_x_offset_bottom, 760))
                plate_x_offset_bottom += plate_x_distance

    def draw_question_page():
        display.blit(ui_scene_question, (0,0))
        
        title_text_rect = pygame.Rect(40, 270, 1520, 330)
        title_text = render_textrect(str(chosen_question_text), font_sourcesans_regular_80, title_text_rect, BLACK, BACKGROUND, 1)
        display.blit(title_text, title_text_rect)

        answer1_text = render_textrect(answer_text_dict["answer1"], font_sourcesans_semi_bold_36, answer1_text_rect, WHITE, YELLOW, 1)
        answer2_text = render_textrect(answer_text_dict["answer2"], font_sourcesans_semi_bold_36, answer2_text_rect, WHITE, BLUE, 1)
        answer3_text = render_textrect(answer_text_dict["answer3"], font_sourcesans_semi_bold_36, answer3_text_rect, WHITE, GREEN, 1)
        answer4_text = render_textrect(answer_text_dict["answer4"], font_sourcesans_semi_bold_36, answer4_text_rect, WHITE, RED, 1)

        display.blit(answer1_text, answer1_text_rect)
        display.blit(answer2_text, answer2_text_rect)
        display.blit(answer3_text, answer3_text_rect)
        display.blit(answer4_text, answer4_text_rect)

    def check_answer(mouse_x, mouse_y):
        if answer1_rect.collidepoint((mouse_x, mouse_y)):
            return 1
        elif answer2_rect.collidepoint((mouse_x, mouse_y)):
            return 2
        elif answer3_rect.collidepoint((mouse_x, mouse_y)):
            return 3
        elif answer4_rect.collidepoint((mouse_x, mouse_y)):
            return 4
        else:
            return None

    def check_plates(mouse_x, mouse_y):
        if plate1_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Toast"] == True:
            return "Toast"
        elif plate2_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Cereal"] == True:
            return "Cereal"
        elif plate3_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Yogurt"] == True:
            return "Yogurt"
        elif plate4_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Breakfast_combo"] == True:
            return "Breakfast_combo"
        elif plate5_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Orange_juice"] == True:
            return "Orange_juice"
        elif plate6_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Milk"] == True:
            return "Milk"
        elif plate7_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Waffle"] == True:
            return "Waffle"
        elif plate8_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["Pancakes"] == True:
            return "Pancakes"
        elif plate9_rect.collidepoint((mouse_x, mouse_y)) and unlocked_items["French_toast"] == True:
            return "French_toast"
        else:
            return None

    def check_buy_item(mouse_x, mouse_y):
        if item1_store_rect.collidepoint((mouse_x, mouse_y)):
            return 1
        elif item2_store_rect.collidepoint((mouse_x, mouse_y)):
            return 2
        elif item3_store_rect.collidepoint((mouse_x, mouse_y)):
            return 3
        elif item4_store_rect.collidepoint((mouse_x, mouse_y)):
            return 4
        elif item5_store_rect.collidepoint((mouse_x, mouse_y)):
            return 5
        elif item6_store_rect.collidepoint((mouse_x, mouse_y)):
            return 6
        elif item7_store_rect.collidepoint((mouse_x, mouse_y)):
            return 7
        elif item8_store_rect.collidepoint((mouse_x, mouse_y)):
            return 8
        elif item9_store_rect.collidepoint((mouse_x, mouse_y)):
            return 9
        else:
            return None

    def draw_store(unlocked_items, item_price_adjusted, item_levels):
        level_start_x = 320
        level_x_distance = 440
        x_offset = 0

        level_start_y = 280
        level_y_distance = 240
        y_offset = 0

        for i in range (9):
            item_name = item_number_to_name[i + 1]

            # Drawing level tags for all items
            if unlocked_items[item_name] == True:
                text = f"Level: {str(item_levels[item_name])}"
            else:
                text = "Locked"
            level_text = font_sourcesans_regular_36.render(text, True, BLACK)
            level_rect = pygame.Rect(level_start_x + x_offset, level_start_y + y_offset, 120, 30)
            display.blit(level_text, level_rect)

            # Drawing price tags for all items
            price = item_price_adjusted[item_name] * 4
            if item_levels[item_name] == 5:
                price = "Max level"
            elif price == 0:
                price = (item_price[item_name] ** 2) / 5
            if price == "Max level":
                price_text = font_sourcesans_bold_36.render(f"Max level", True, BLACK)
            elif cash >= price:
                price_text = font_sourcesans_bold_36.render(f"${price}", True, TEXT_GREEN)
            else:
                price_text = font_sourcesans_bold_36.render(f"${price}", True, TEXT_RED)
            price_rect = price_text.get_rect(topright=(level_start_x + x_offset + 220, level_start_y + y_offset + 60))
            display.blit(price_text, price_rect)

            x_offset += level_x_distance
            if (i + 1) % 3 == 0:
                x_offset = 0
                y_offset += level_y_distance

    while run:

        update_prices(item_price_adjusted)

        if active_time >= time_limit_ticks:
            pygame.event.post(pygame.event.Event(FINISHGAME))

        if active_time_customer / FPS >= customer_interval:
            active_time_customer = 0
            pygame.event.post(pygame.event.Event(ADDCUSTOMER))

        if guessed:
            chosen_question = random.randint(0,len(question_text_list) - 1)
            chosen_question_text = question_text_list[chosen_question]

            chosen_answer = answers_list[chosen_question]
            answer_slot = random.randint(1,4)
            guessed = False

            answer_dict = {
                "answer1": False,
                "answer2": False,
                "answer3": False,
                "answer4": False,
                }

            answer_dict["answer" + str(answer_slot)] = True

            answers_list_temp = answers_list.copy()
            answers_list_temp.remove(chosen_answer)

            answer_text_dict = {
                "answer1": None,
                "answer2": None,
                "answer3": None,
                "answer4": None,
            }

            answer_text_dict["answer" + str(answer_slot)] = chosen_answer
            
            for key in list(answer_text_dict):
                if answer_text_dict[key] == None:
                    temp_answer = random.choice(answers_list_temp)
                    answer_text_dict[key] = temp_answer
                    answers_list_temp.remove(temp_answer)
        
        if store == True:
            display.blit(ui_store, (0,0))
            draw_store(unlocked_items, item_price_adjusted, item_levels)
            draw_cash(cash)
            draw_sound(mute)

        elif not question_page:
            display.blit(ui_scene_main,(0,0))
            draw_time(active_time)
            draw_plates(unlocked_items)
            draw_customers(customers_list)
            draw_cash(cash)
            draw_sound(mute)

        elif display_correct:
            display.blit(ui_scene_correct, (0,0))
            draw_sound(mute)

        elif display_incorrect:
            display.blit(ui_scene_incorrect, (0,0))
            draw_sound(mute)

        else:
            draw_question_page()
            draw_cash(cash)
            draw_sound(mute)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = mouse_pos
                mouse_x *= scale_factor
                mouse_y *= scale_factor

                if mute_rect.collidepoint((mouse_x, mouse_y)):
                    mute = not mute

                elif store == True:
                    buy_item = check_buy_item(mouse_x, mouse_y)
                    if buy_item != None:
                        item_name = item_number_to_name[buy_item]
                        unlock_price = (item_price[item_name] ** 2) / 5
                        # Check if not unlocked and enough cash
                        if unlocked_items[item_name] == False:
                            if cash >= unlock_price:
                                unlocked_items[item_name] = True
                                item_levels[item_name] = 1
                                cash -= unlock_price
                                sxf_upgrade.play()
                        elif item_levels[item_name] == 5:
                            pass
                        elif cash >= item_price_adjusted[item_name] * 4:
                            item_levels[item_name] += 1
                            cash -= item_price_adjusted[item_name] * 4
                            sxf_upgrade.play()

                elif question_page == False and store == False and display_correct == False and display_incorrect == False:

                    if customer1_rect.collidepoint((mouse_x, mouse_y)) or customer1_text_rect.collidepoint((mouse_x, mouse_y)):
                        if plate != None:
                            try:
                                plate_number = customers_list[0].request_items[plate]
                                for _ in range(plate_number):
                                    if item_counts[plate] > 0:
                                        item_counts[plate] -= 1
                                        customers_list[0].request_items[plate] -= 1
                                        customers_list[0].temp_cash += item_price_adjusted[plate] * reward_multiplier
                            except:
                                pass

                    if customer2_rect.collidepoint((mouse_x, mouse_y)) or customer2_text_rect.collidepoint((mouse_x, mouse_y)):
                        if plate != None:
                            try:
                                plate_number = customers_list[1].request_items[plate]
                                for _ in range(plate_number):
                                    if item_counts[plate] > 0:
                                        item_counts[plate] -= 1
                                        customers_list[1].request_items[plate] -= 1
                                        customers_list[1].temp_cash += item_price_adjusted[plate] * reward_multiplier
                            except:
                                pass

                    if customer3_rect.collidepoint((mouse_x, mouse_y)) or customer3_text_rect.collidepoint((mouse_x, mouse_y)):
                        if plate != None:
                            try:
                                plate_number = customers_list[2].request_items[plate]
                                for _ in range(plate_number):
                                    if item_counts[plate] > 0:
                                        item_counts[plate] -= 1
                                        customers_list[2].request_items[plate] -= 1
                                        customers_list[2].temp_cash += item_price_adjusted[plate] * reward_multiplier
                            except:
                                pass

                elif question_page == True and display_correct == False and display_incorrect == False:
                    answer_number = check_answer(mouse_x, mouse_y)
                    if answer_number == answer_slot:
                        guessed = True
                        print("Correct")
                        correct_answers += 1
                        display_correct = True
                        sxf_correct.play()
                        for item in unlocked_items:
                            if unlocked_items[item] == True:
                                item_counts[item] += 1

                    elif answer_number != None:
                        guessed = True
                        incorrect_answers += 1
                        print("Incorrect")
                        display_incorrect = True
                        sxf_wrong.play()

                if button_restock_food.collidepoint((mouse_x, mouse_y)) and question_page == False:
                    question_page = True

                if button_store.collidepoint((mouse_x, mouse_y)) and question_page == False and store == False:
                    store = True

                if button_store_back.collidepoint((mouse_x, mouse_y)) and store == True:
                    store = False

                elif not question_page:
                    if plates_rect.collidepoint((mouse_x, mouse_y)):
                        plate = check_plates(mouse_x, mouse_y)

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if display_correct == True:
                        display_correct = False
                        question_page = False
                    elif display_incorrect == True:
                        display_incorrect = False
                        question_page = False
                    else:
                        question_page = True
                elif event.key == K_ESCAPE:
                    question_page = False

            elif event.type == ADDCUSTOMER:
                if len(customers_list) < 3:
                    request_choices = {}
                    for item in unlocked_items:
                        if unlocked_items[item] == True:
                            request_choices[str(item)] = 0
                    items_requested = random.randint(1,3)
                    for _ in range(items_requested):
                        item = random.choice(list(request_choices))
                        request_choices[item] = random.randint(1,3)
                    print(request_choices)

                    for item in list(request_choices):
                        if request_choices[item] == 0:
                            request_choices.pop(item)
                    print(request_choices)

                    customer_type = random.randint(1,len(ui_characters))
                    customer = Customer(customer_type,request_choices, 0)
                    customers_list.append(customer)
            
            elif event.type == FINISHGAME:
                run = False
                end_menu(correct_answers, incorrect_answers, cash)
        
        for i, customer in enumerate(customers_list):
            pop_list = []
            for key in list(customers_list[i-1].request_items):
                if customers_list[i-1].request_items[key] == 0:
                    pop_list.append("Empty")
                else:
                    pop_list.append("Full")
            
            for item in pop_list:
                if item == "Empty":
                    pop_list.remove("Empty")

            if "Full" not in pop_list:
                cash += customers_list[i-1].temp_cash
                customers_list.pop(i-1)
                sfx_pay.play()
            
        if quality == "Fancy":
            surf = pygame.transform.smoothscale(display, (WIDTH, HEIGHT))
        else:
            surf = pygame.transform.scale(display, (WIDTH, HEIGHT))
        screen.blit(surf,(0,0))
        pygame.display.update()
        clock.tick(FPS)
        active_time += 1
        active_time_customer += 1

def end_menu(correct_answers, incorrect_answers, cash):

    run = True

    button_play_again = pygame.Rect(600,1040,400,120)

    total_answers = correct_answers + incorrect_answers
    try:
        correct_incorrect_percentage = round(correct_answers / total_answers * 100, 2)
    except ZeroDivisionError:
        correct_incorrect_percentage = round(correct_answers / 1 * 100, 2)

    questions_correct_rect = pygame.Rect(160,500,1280,50)
    correct_incorrect_percentage_rect = pygame.Rect(160,580,1280,50)
    total_cash_rect = pygame.Rect(160,660,1280,50)

    def draw_summary(correct_incorrect_percentage):
        questions_correct_text = font_sourcesans_regular_50.render("Questions correct: " + str(correct_answers), True, BLACK)
        display.blit(questions_correct_text, questions_correct_rect)

        correct_incorrect_percentage_text = font_sourcesans_regular_50.render("Correct percentage: " + str(correct_incorrect_percentage) + "%", True, BLACK)
        display.blit(correct_incorrect_percentage_text, correct_incorrect_percentage_rect)

        total_cash_text = font_sourcesans_regular_50.render("Final cash: $" + str(cash), True, BLACK)
        display.blit(total_cash_text, total_cash_rect)

    while run:
        display.blit(ui_scene_end, (0,0))
        draw_summary(correct_incorrect_percentage)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = mouse_pos
                mouse_x *= scale_factor
                mouse_y *= scale_factor

                if button_play_again.collidepoint((mouse_x, mouse_y)):
                    run = False
                    main()

        if quality == "Fancy":
            surf = pygame.transform.smoothscale(display, (WIDTH, HEIGHT))
        else:
            surf = pygame.transform.scale(display, (WIDTH, HEIGHT))
        screen.blit(surf,(0,0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
