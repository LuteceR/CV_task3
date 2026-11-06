"""
main file
"""

from pathlib import Path

import pygame as pg
import pygame_gui
import matplotlib # not used
from PIL import Image

from aliasing.aliasing import Aliasing
from chromaticity.chromaticity import Chromaticity
from sharpness.sharpness import Sharpness

matplotlib.use("Agg") # not used

IMAGE = "resting_knight.png"
ZOOM_SCALE = 12
BASE_DIR = Path(__file__).resolve().parent


def limit(val, min_val, max_val):
    """
    limit value to min and max
    """
    return max(min_val, min(val, max_val))


def main():
    """
    main function of app
    """

    pg.init()
    with Image.open(IMAGE) as img:
        infoObject = pg.display.Info()
        SIZE_SCREEN = (limit(img.width, 600, infoObject.current_w - 100),
                    limit(img.height, 600, infoObject.current_h - 100))

    pg.display.set_caption("python gaͥ̑͊͠₥ing 𝟠kก็็็็็็็็็็็็็็็็็็")

    screen = pg.display.set_mode(SIZE_SCREEN)
    
    mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")
    nav = pygame_gui.elements.UITabContainer(relative_rect=pg.Rect((0, 0), SIZE_SCREEN),
                                             manager=mode_manager)

    nav.add_tab("Цветность", "#Цветность")
    nav.add_tab("Сглаживание", "#Сглаживание")
    nav.add_tab("Резкость", "#Резкость")

    # convert_alpha - замена прозрачных частей на черный
    main_image = pg.image.load(BASE_DIR / IMAGE).convert_alpha()
    image_al = main_image.copy()

    chromaticity_obj = Chromaticity(main_image)
    aliasing_obj = Aliasing()
    sharpness_obj = Sharpness()

    chrom_ui_container = chromaticity_obj.get_ui(manager=mode_manager,
                                                      x=0,
                                                      y=40,
                                                      w=SIZE_SCREEN[0],
                                                      h=SIZE_SCREEN[1])
    
    aliasing_ui_container = aliasing_obj.get_ui(manager=mode_manager,
                                             img=image_al,
                                             x=0,
                                             y=30,
                                             w=SIZE_SCREEN[0],
                                             h=SIZE_SCREEN[1])

    sharp_ui_container = sharpness_obj.get_ui(manager=mode_manager,
                                                x=0,
                                                y=40,
                                                w=SIZE_SCREEN[0],
                                                h=SIZE_SCREEN[1])

    # сюда складируем UI для каждой вкладки
    chrom_container = nav.get_tab_container(0)
    aliasing_container = nav.get_tab_container(1)
    sharp_container = nav.get_tab_container(2)

    chrom_ui_container.set_container(chrom_container)
    aliasing_ui_container.set_container(aliasing_container)

    sharp_ui_container.set_container(sharp_container)

    clock = pg.time.Clock()

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    ind = 0 if nav.current_container_index is None else nav.current_container_index  
                    nav.switch_current_container((ind + 1)%3)
                    nav.rebuild()

            aliasing_obj.process_event(event, mode_manager)
            mode_manager.process_events(event)
            chromaticity_obj.process_event(event)

        
        mode_manager.update(time_delta)
        screen.fill((0, 0, 0))
        mode_manager.draw_ui(screen)
        if nav.current_container_index == 1:
            aliasing_obj.zoom_thing(screen, pg.mouse.get_pos())
        pg.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
    pg.quit()