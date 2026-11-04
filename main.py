"""
main file
"""

from pathlib import Path

import pygame as pg
import pygame_gui
import matplotlib
from PIL import Image

from aliasing.aliasing import Aliasing

matplotlib.use("Agg")

IMAGE = "resting_knight.png"
ZOOM_SCALE = 12
BASE_DIR = Path(__file__).resolve().parent

with Image.open(IMAGE) as img:
    SIZE_SCREEN = (img.width, img.height)

def main():
    """
    main function of app
    """

    aliasing_obj = Aliasing()

    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None    # Основной цикл отрисовки
    
    pg.display.set_caption("python gaming 8kก็็็็็็็็็็็็็็็็็็")

    screen = pg.display.set_mode(SIZE_SCREEN)
    
    mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")
    nav = pygame_gui.elements.UITabContainer(relative_rect=pg.Rect((0, 0), SIZE_SCREEN),
                                             manager=mode_manager)

    aliasing_ui_container = aliasing_obj.get_ui(manager=mode_manager,
                                             x=0,
                                             y=40,
                                             w=SIZE_SCREEN[0],
                                             h=SIZE_SCREEN[1])
    
    nav.add_tab("Цветность", "#Цветность")
    nav.add_tab("Сглаживание", "#Сглаживание")
    nav.add_tab("Резкость", "#Резкость")

    # convert_alpha - замена прозрачных частей на черный
    main_image = pg.image.load(BASE_DIR / IMAGE).convert_alpha()
    
    # main_image не трогаем дабы не портить ориг
    image_al = main_image.copy()
    image_ch = main_image.copy()
    image_sh = main_image.copy()
    
    # сюда складируем UI для каждой вкладки
    chrom_container = nav.get_tab_container(0)
    aliasing_container = nav.get_tab_container(1)
    sharp_container = nav.get_tab_container(2)

    #  вот так добавляем фон для табов
    aliasing_container.add_background_image(image_al)
    aliasing_container.set_container(aliasing_ui_container)

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
                    print(image_al)
            mode_manager.process_events(event)
        mode_manager.update(time_delta)
        mode_manager.draw_ui(screen)
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pg.quit()