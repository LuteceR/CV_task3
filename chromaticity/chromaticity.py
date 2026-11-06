import numpy as np
import pygame_gui as pgui
import pygame as pg


class Chromaticity:
    """
    Изменение яркости изображения
    * логарифмическое преобразование
    * степенное преобразование
    * бинарное преобразование
    * вырезание диапазона яркости
    """

    MODES = {
        "Логарифмическое преобразование": [], # не отображать
        "Степенное преобразование": [("Показатель степени", 1.0, (0.1, 10.0))],
        "Бинарное преобразование": [("Порог", 128, (0, 255))],
        "Вырезание диапазона яркости": [("Нижняя граница", 64, (0, 255)), 
                                        ("Верхняя граница", 192, (0, 255)),
                                        ("Заменить значением", -1, (-1, 255))],
    }

    def __init__(self, source_image: pg.Surface):
        self.source_image = source_image
        self.image = None
        self.mode_selector = None
        self.mode_panels = {}
        self.parameter_sliders = {}
        self.selected_mode = None

    def get_ui(self, manager: pgui.UIManager, x = 20, y = 20, w = 600, h = 300) -> pgui.core.UIContainer:
        container = pgui.core.UIContainer(
            relative_rect=pg.Rect((x, y), (w, h)),
            manager=manager,
        )

        self.mode_selector = pgui.elements.UIDropDownMenu(
            options_list=list(self.MODES),
            starting_option=next(iter(self.MODES)),
            relative_rect=pg.Rect((10, 4), (280, 24)),
            manager=manager,
            container=container,
        )

        self.image = pgui.elements.UIImage(
            relative_rect=pg.Rect((30, 50), self.source_image.get_size()),
            image_surface=self.source_image,
            manager=manager,
            container=container
        )

        self.mode_panels = {}
        self.parameter_sliders = {}
        for index, (mode, sliders) in enumerate(self.MODES.items()):
            panel = pgui.core.UIContainer(
                relative_rect=pg.Rect((290, 4), (w - 20, 150)),
                manager=manager,
                container=container,
            )
            if index != 0:
                panel.hide()
            self.mode_panels[mode] = panel

            self.parameter_sliders[mode] = []
            for index, slider in enumerate(sliders):
                pgui.elements.UILabel(
                    relative_rect=pg.Rect((0, 50 * index), (min(w - 30, 280), 20)),
                    text=slider[0],
                    manager=manager,
                    container=panel,
                )
                self.parameter_sliders[mode].append(pgui.elements.UIHorizontalSlider(
                        relative_rect=pg.Rect((0, 20 + 50 * index), (min(w - 30, 300), 30)),
                        start_value=slider[1],
                        value_range=slider[2],
                        manager=manager,
                        container=panel,
                    )
                )
           
        self.selected_mode = next(iter(self.MODES))
        self.redraw_image()
        return container


    def process_event(self, event: pg.event.Event):
        if (
            event.type == pgui.UI_DROP_DOWN_MENU_CHANGED
            and event.ui_element is self.mode_selector
            and event.text in self.mode_panels
        ):
            self.selected_mode = event.text
            self.redraw_image()
            for mode, panel in self.mode_panels.items():
                if mode == self.selected_mode:
                    panel.show()
                else:
                    panel.hide()
        elif (
            event.type == pgui.UI_HORIZONTAL_SLIDER_MOVED
            and event.ui_element in [slider for sliders in self.parameter_sliders.values() for slider in sliders]
        ):
            self.redraw_image()


    def rehide_panels(self):
        for mode, panel in self.mode_panels.items():
            if mode == self.selected_mode:
                panel.show()
            else:
                panel.hide()


    def redraw_image(self):
        image = self.source_image.copy()
        rgb = pg.surfarray.pixels3d(image)
        min_val = rgb.min()
        max_val = rgb.max()

        if self.selected_mode == "Логарифмическое преобразование":
            rgb[:] = ((rgb.astype(np.float32) - min_val) / max(max_val - min_val, 1)) * 255
            rgb[:] = np.clip(105.88 * np.log(1 + rgb.astype(np.int16)), 0, 255).astype(np.uint8)

        elif self.selected_mode == "Степенное преобразование":
            rgb[:] = ((rgb.astype(np.float32) - min_val) / max(max_val - min_val, 1)) * 255
            gamma = self.parameter_sliders[self.selected_mode][0].get_current_value()
            c = 255 / (255 ** gamma)
            rgb[:] = np.clip(c * np.power(rgb.astype(np.int16), gamma), 0, 255).astype(np.uint8)

        elif self.selected_mode == "Бинарное преобразование":
            threshold = self.parameter_sliders[self.selected_mode][0].get_current_value()
            rgb[:] = np.where(rgb > threshold, 255, 0).astype(np.uint8)

        elif self.selected_mode == "Вырезание диапазона яркости":
            gray = rgb.mean(axis=2)
            low = self.parameter_sliders[self.selected_mode][0].get_current_value()
            high = self.parameter_sliders[self.selected_mode][1].get_current_value()
            replace_value = self.parameter_sliders[self.selected_mode][2].get_current_value()
            rgb[(gray >= low) & (gray <= high)] = 0
            if replace_value >= 0:
                rgb[(gray < low) | (gray > high)] = replace_value 
        del rgb

        self.image.set_image(image)
