from pathlib import Path

import pygame as pg
import pygame_gui
import matplotlib
from PIL import Image

import kernel_operations

matplotlib.use("Agg")

IMAGE = "resting_knight.png"
ZOOM_SCALE = 12
BASE_DIR = Path(__file__).resolve().parent

with Image.open(IMAGE) as img:
    SIZE_SCREEN = (img.width, img.height)

def update_image():
    """
    updates image
    """
    global display_image
    rgb_filtered = rgb.copy()
    if four_checkbox.get_state():
        rgb_filtered = kernel_operations.the_four_connectivity(rgb)
    elif ate_checkbox.get_state():
        rgb_filtered = kernel_operations.the_eight_connectivity(rgb)
    image = rgb_filtered
    surf = pg.surfarray.make_surface(image).convert_alpha()
    display_image = surf

def main():
    """
    main function of app
    """
    
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None    # Основной цикл отрисовки
    
    pg.display.set_caption("python gaming 8k")
    screen = pg.display.set_mode(SIZE_SCREEN)
    clock = pg.time.Clock()

    channel_mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")

    # convert_alpha замена прозрачных частей на черный
    main_image = pg.image.load(BASE_DIR / IMAGE).convert_alpha()
    display_image = main_image.copy()
    image_rect = main_image.get_rect()
    rgb = pg.surfarray.array3d(main_image)
    print(f"rgb shape: {rgb.shape}")
    mean_rgb = rgb.mean(axis=(0, 1))
    mean_all = rgb.mean()

    clock = pg.time.Clock()
    font = pg.font.Font()

    four_checkbox = pygame_gui.elements.UICheckBox(text="4-связность",
                                                relative_rect=pg.Rect((390, 30), (30, 30)),
                                                manager=channel_mode_manager)

    ate_checkbox = pygame_gui.elements.UICheckBox(text="8-связность",
                                                    relative_rect=pg.Rect((510, 30), (30, 30)),
                                                    manager=channel_mode_manager)

    save_button1 = pygame_gui.elements.UIButton(relative_rect=pg.Rect((510, 70), (110, 30)),
                                            text="Save image", 
                                            manager=channel_mode_manager)

    
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        screen.blit(display_image, image_rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_0:
                    update_image()
                elif event.key == pg.K_8:
                    ate_checkbox.set_state(not ate_checkbox.get_state())
                elif event.key == pg.K_4:
                    four_checkbox.set_state(not four_checkbox.get_state())

        channel_mode_manager.process_events(event)
        channel_mode_manager.update(time_delta)
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pg.quit()