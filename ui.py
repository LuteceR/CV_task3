import pygame
import pygame_gui
from PIL import Image

from pathlib import Path
import numpy as np

def create_sliders(eff_mngr, cn_map_mngr, screen_size):
    CHANNELS = ["Red", "Green", "Blue"]
    select_r_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[0],
                                                      relative_rect=pygame.Rect((30, 30), (80, 30)),
                                                      manager=eff_mngr)

    select_g_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[1],
                                                      relative_rect=pygame.Rect((120, 30), (80, 30)),
                                                      manager=eff_mngr)

    select_b_source = pygame_gui.elements.UIDropDownMenu(options_list=CHANNELS,
                                                      starting_option=CHANNELS[2],
                                                      relative_rect=pygame.Rect((210, 30), (80, 30)),
                                                      manager=eff_mngr)
    
    r_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((30, 80), (190, 30)),
                                                                start_value=1.0,
                                                                value_range=(0, 5),
                                                                manager=eff_mngr)

    r_level_inv = pygame_gui.elements.UICheckBox(text="",
                                                 relative_rect=pygame.Rect((230, 80), (30, 30)),
                                                    manager=eff_mngr)

    g_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((270, 80), (190, 30)),
                                                                start_value=1.0,
                                                                value_range=(0, 5),
                                                                manager=eff_mngr)
    
    g_level_inv = pygame_gui.elements.UICheckBox(text="",
                                                 relative_rect=pygame.Rect((470, 80), (30, 30)),
                                                    manager=eff_mngr)

    b_level_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((510, 80), (190, 30)),
                                                                start_value=1.0,
                                                                value_range=(0, 5),
                                                                manager=eff_mngr)

    b_level_inv = pygame_gui.elements.UICheckBox(text="",
                                                 relative_rect=pygame.Rect((710, 80), (30, 30)),
                                                    manager=eff_mngr)

    contrast_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((300, 30), (190, 30)),
                                                                start_value=5.0,
                                                                value_range=(0, 50),
                                                                manager=eff_mngr)

    mirror_v = pygame_gui.elements.UICheckBox(text="Mirror vertical",
                                              relative_rect=pygame.Rect((500, 30), (30, 30)),
                                              manager=eff_mngr)

    mirror_h = pygame_gui.elements.UICheckBox(text="Mirror horizontal",
                                              relative_rect=pygame.Rect((640, 30), (30, 30)),
                                              manager=eff_mngr)


    line_slider_for_graph = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((30, 140), (190, 30)),
                                                            start_value=0.0,
                                                            value_range=(0, 1),
                                                            manager=eff_mngr)

    save_button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((270, 140), (110, 30)),
                                           text="Save image",
                                           manager=eff_mngr)

    # ЗАДАНИЕ 7
    four_conn_checkbox = pygame_gui.elements.UICheckBox(text="4-связность",
                                            relative_rect=pygame.Rect((10, 10), (30, 30)),
                                            manager=cn_map_mngr)
    
    eight_conn_checkbox = pygame_gui.elements.UICheckBox(text="8-связность",
                                        relative_rect=pygame.Rect((10, 50), (30, 30)),
                                        manager=cn_map_mngr)
    
    
    window_size_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((120, 90), (190, 30)),
                                                        start_value=1,
                                                        value_range=(1, 8),
                                                        manager=cn_map_mngr)

    save_button3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((510, 70), (110, 30)),
                                           text="Save image",
                                           manager=cn_map_mngr)



    return (r_level_slider, g_level_slider, b_level_slider,
            contrast_slider,
            select_r_source, select_g_source, select_b_source,
            r_level_inv, g_level_inv, b_level_inv,
            mirror_v, mirror_h, line_slider_for_graph,
            four_conn_checkbox, eight_conn_checkbox, window_size_slider,
            save_button2, save_button3)