"""some class"""

import numpy as np
import pygame_gui as pgui
import pygame as pg

class Aliasing:
    """
    Factory class that creates the factory that's gotta smooth the images
    1. Rectangle filter
    2. Median filter
    3. Sigma filter
    """

    def __init__(self, *args, **kwargs):
        """
        constructor of Aliasing class object
        """
        self.rect_filter_val = False
        self.median_filter_val = False
        self.sigma_filter_val = False
        pass

    def get_ui(self, manager: pgui.UIManager, x = 20, y = 20, w = 600, h = 300) -> pgui.core.UIContainer:
        """
        ts returns ui
        """
        container = pgui.core.UIContainer(relative_rect=pg.Rect((x, y), (w, h)),
                                          manager = manager)

        # кнопочки 💅🏼
        rect_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x+10, y), (20,20)),
                                            text="Прямоугольный фильтр")
        median_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 210, y), (20,20)),
                                              text="Медианный фильтр")
        sigma_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 2 * 200, y), (20,20)),
                                             text="Сигма-фильтр")

        container.add_element(rect_btn)
        container.add_element(median_btn)
        container.add_element(sigma_btn)

        return container
        

    def apply_rectangle_filter(self, i, kernel_size = 3):
        """
        do smth
        """
        kernel = np.eye(kernel_size, kernel_size)
        return kernel
        
    def apply_median_filter(self):
        """
        do smth
        """
        pass

    def apply_sigma_filter(self):
        """
        do smth
        """
        pass