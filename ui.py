import pygame
import pygame_gui
from PIL import Image

from pathlib import Path
import numpy as np

def create_sliders(mngr, screen_size):
    # Подписи надо: "источники каналов", "Усиление каналов", "Контрастность"
    CHANNELS = ["Red", "Green", "Blue"]
    select_r_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[0],
                                                      relative_rect=pygame.Rect((screen_size[0] - 200, 30), (60, 30)),
                                                      manager=mngr)

    select_g_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[1],
                                                      relative_rect=pygame.Rect((screen_size[0] - 140, 30), (60, 30)),
                                                      manager=mngr)

    select_b_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[2],
                                                      relative_rect=pygame.Rect((screen_size[0] - 80, 30), (60, 30)),
                                                      manager=mngr)
    
    r_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 80), (190, 30)),
                                                                start_value=1.0,
                                                                value_range=(0, 5),
                                                                manager=mngr)

    g_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 120), (190, 30)),
                                                                start_value=1.0,
                                                                value_range=(0, 5),
                                                                manager=mngr)

    b_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 160), (190, 30)),
                                                                start_value=1.0,
                                                                value_range=(0, 5),
                                                                manager=mngr)

    contrast_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((screen_size[0] - 200, 210), (190, 30)),
                                                                start_value=5.0,
                                                                value_range=(0, 50),
                                                                manager=mngr)



    mirror_v = pygame_gui.elements.UICheckBox(text="Mirror vertical",
                                              relative_rect=pygame.Rect((screen_size[0] - 200, 250), (30, 30)),
                                              manager=mngr)

    mirror_h = pygame_gui.elements.UICheckBox(text="Mirror horizontal",
                                              relative_rect=pygame.Rect((screen_size[0] - 200, 290), (30, 30)),
                                              manager=mngr)

    # 2 галочки - удаление шума 4- и 8-связностью
    # "Идея Сьюзи" (что-то своё)
    # ЗАДАНИЕ 6
    # график яркости по строке (граф + слайдер)
    # ЗАДАНИЕ 7
    # 2 галочки - карта контрастности (чё?) 4- и 8-связностью + поле для воода размера окна



    return (r_level_slider, g_level_slider, b_level_slider,
            contrast_slider,
            select_r_source, select_g_source, select_b_source,
            mirror_v, mirror_h)