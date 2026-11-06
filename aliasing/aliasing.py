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

    def __init__(self, source_image: pg.Surface | None = None):
        """
        constructor of Aliasing class object
        """
        self.source_image = source_image
        self.rect_filter_val = False
        self.median_filter_val = False
        self.sigma_filter_val = False


    def get_ui(self, manager: pgui.UIManager, x = 20, y = 20, w = 600, h = 300) -> pgui.core.UIContainer:
        """
        ts returns container that contains ui
        """
        container = pgui.core.UIContainer(relative_rect=pg.Rect((x, y), (w, h)),
                                          manager = manager)

        # кнопочки 💅🏼
        rect_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x+10, y), (20,20)),
                                            text="Прямоугольный фильтр",
                                            container=container)
        median_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 210, y), (20,20)),
                                              text="Медианный фильтр",
                                              container=container)
        sigma_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 2 * 200, y), (20,20)),
                                             text="Сигма-фильтр",
                                             container=container)

        return container
        

    def apply_rectangle_filter_kernel_3(self, img : pg.Surface):
        """
        do smth with kernel 3
        """
        I_org = pg.surfarray.array3d(img)
        I = np.pad(I_org.astype('f'), ((1,1), (1,1), (0,0)), mode="edge")
        res = (
            I[:-2, :-2] + I[:-2, 1:-1] + I[:-2, 2:] +
            I[1:-1, :-2] + I[1:-1, 1:-1] + I[1:-1, 2:] +
            I[2:, :-2] + I[2:, 1:-1] + I[2:, 2:]
        )
        return (res/9).astype(int)
        
    def apply_median_filter(self, img : pg.Surface):
        """
        do smth
        """
        pass

    def apply_sigma_filter(self, img : pg.Surface):
        """
        do smth
        """
        pass