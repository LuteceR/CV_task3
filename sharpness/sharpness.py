import pygame as pg
import pygame_gui as pgui


class Sharpness:
    """UI module for the sharpness mode."""

    def __init__(self, source_image: pg.Surface | None = None):
        self.source_image = source_image

    def get_ui(self, manager: pgui.UIManager, x=0, y=0, w=600, h=300) -> pgui.core.UIContainer:
        container = pgui.core.UIContainer(relative_rect=pg.Rect((x, y), (w, h)),
                                                  manager = manager)
        
        pgui.elements.UICheckBox(relative_rect=pg.Rect((x+10, y), (20,20)),
                                                text="sharpness",
                                                container=container)
        
        return container
