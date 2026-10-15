import pygame
import pygame_gui
from PIL import Image

from pathlib import Path
import numpy as np
def create_sliders(manager, screen_size):
    r_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 10), (190, 30)),
                                                                start_value=100,
                                                                value_range=(0, 200),
                                                                manager=manager)

    g_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 60), (190, 30)),
                                                                start_value=100,
                                                                value_range=(0, 200),
                                                                manager=manager)

    b_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 110), (190, 30)),
                                                                start_value=100,
                                                                value_range=(0, 200),
                                                                manager=manager)

    contrast_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 160), (190, 30)),
                                                                start_value=100,
                                                                value_range=(0, 200),
                                                                manager=manager)

    CHANNELS = ["Red", "Green", "Blue"]
    select_r_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[0],
                                                      relative_rect=pygame.Rect((screen_size[0] - 200, 210), (60, 30)),
                                                      manager=manager)

    select_g_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[1],
                                                      relative_rect=pygame.Rect((screen_size[0] - 140, 210), (60, 30)),
                                                      manager=manager)

    select_b_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[2],
                                                      relative_rect=pygame.Rect((screen_size[0] - 80, 210), (60, 30)),
                                                      manager=manager)

    mirror_v = pygame_gui.elements.UICheckBox(text="Mirror vertical",
                                              relative_rect=pygame.Rect((screen_size[0] - 200, 250), (30, 30)),
                                              manager=manager)

    mirror_h = pygame_gui.elements.UICheckBox(text="Mirror horizontal",
                                              relative_rect=pygame.Rect((screen_size[0] - 200, 290), (30, 30)),
                                              manager=manager)

    # 2 галочки - удаление шума 4- и 8-связностью
    # "Идея Сьюзи" (что-то своё)
    # график яркости по строке (граф + слайдер)
    # 2 галочки - карта контрастности 4- и 8-связностью + поле для воода размера окна



    return (r_level_slider, g_level_slider, b_level_slider,
            contrast_slider,
            select_r_source, select_g_source, select_b_source,
            mirror_v, mirror_h)