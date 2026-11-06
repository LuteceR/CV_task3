import numpy as np
import pygame as pg
import pygame_gui as pgui


class Sharpness:
    """UI module for the sharpness mode."""

    def __init__(self, source_image: pg.Surface):
        self.source_image = source_image
        self.win_size_slider = None
        self.coef_slider = None
        self.image = None

    def get_ui(self, manager: pgui.UIManager, x=0, y=0, w=600, h=300) -> pgui.core.UIContainer:
        container = pgui.core.UIContainer(
                    relative_rect=pg.Rect((x, y), (w, h)),
                    manager=manager,
                )

        self.image = pgui.elements.UIImage(
                    relative_rect=pg.Rect((30, 50), self.source_image.get_size()),
                    image_surface=self.source_image,
                    manager=manager,
                    container=container
                )

        pgui.elements.UILabel(
                            relative_rect=pg.Rect((4, 4), (min(w - 30, 280), 20)),
                            text="Размер окна",
                            manager=manager,
                            container=container,
                        )

        self.win_size_slider = pgui.elements.UIHorizontalSlider(
                                relative_rect=pg.Rect((4, 28), (min(w - 30, 300), 30)),
                                start_value=1,
                                value_range=(1, 10),
                                manager=manager,
                                container=container,
                            )

        pgui.elements.UILabel(
                            relative_rect=pg.Rect((300, 4), (min(w - 30, 280), 20)),
                            text="Коэффициент",
                            manager=manager,
                            container=container,
                        )
        
        self.coef_slider = pgui.elements.UIHorizontalSlider(
                                relative_rect=pg.Rect((300, 28), (min(w - 30, 300), 30)),
                                start_value=0.0,
                                value_range=(0.0, 10.0),
                                manager=manager,
                                container=container,
                            )
        self.redraw_image()
        return container


    def process_event(self, event: pg.event.Event):
        if (
            event.type == pgui.UI_HORIZONTAL_SLIDER_MOVED
            and (event.ui_element in [self.win_size_slider, self.coef_slider])
        ):
            self.redraw_image()


    def redraw_image(self):
        image = self.source_image.copy()
        rgb = pg.surfarray.pixels3d(image)
        original = rgb.astype(np.float32)
        radius = round(self.win_size_slider.get_current_value())
        window_size = 2 * radius + 1
        coefficient = self.coef_slider.get_current_value()
        padded = np.pad(original,
            ((radius, radius), (radius, radius), (0, 0)),
            mode="edge",
        )

        windows = np.lib.stride_tricks.sliding_window_view(padded, (window_size, window_size), axis=(0, 1)) # shape = (224, 224, 3, window_size, window_size)
        blurred = windows.mean(axis=(-1, -2)) # Прямоугольный сглаживающий фильтр

        rgb[:] = np.clip((1 + coefficient) * original - coefficient * blurred, 0, 255).astype(np.uint8)
        del rgb

        self.image.set_image(image)
