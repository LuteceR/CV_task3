import pygame
import pygame_gui
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image

from pathlib import Path
import numpy as np
# ================================= !!!! НА КНОПКУ "0" ПЕРЕКЛЮЧЕНИЕ РЕЖИМОВ !!!!!! ==========================
from ui import create_sliders

# Добавление картинки в движок происходит через make_surface()
# Картинка хранится в 3-мерном массиве [x, y, c] c - канал RGB
# Данные находятся в диапазоне uint8: 0 - 255
# screen.fill(color) - заполнить экран цветом
# screen.blit(element) - нарисовать элемент (картинку/график) на экране
# Позиция и цвет часто передаются как питоновского набора, например (1, 2, 3)

SIZE_SCREEN = (0, 0)
IMAGE = "img.png"
ZOOM_SCALE = 12
BASE_DIR = Path(__file__).resolve().parent
COLOR_MODES = [
    "Original",
    "Red",
    "Blue",
    "Green",
    "Gray"
]
slider_value = 0
M_CHANNELS = "channels"
M_EFFECTS = "effects"
showmode = M_CHANNELS

# значения окна W
avg_r = 0
avg_g = 0
avg_b = 0
avg_a = 0
avg_all = 0

with Image.open(IMAGE) as img:
    SIZE_SCREEN = (max(700, img.width + 10), max(800, img.height + 120))

pygame.init()
pygame.display.set_caption("python gaming 4k")
screen = pygame.display.set_mode(SIZE_SCREEN)

channel_mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")
effects_mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")

# convert_alpha замена прозрачных частей на черный
main_image = pygame.image.load(BASE_DIR / IMAGE).convert_alpha()
display_image = main_image.copy()
image_rect = main_image.get_rect(topleft=(5, 120))
rgb = pygame.surfarray.array3d(main_image)
alpha = pygame.surfarray.array_alpha(main_image)

mean_rgb = rgb.mean(axis=(0, 1))
mean_all = rgb.mean()
print(mean_rgb, mean_all)

clock = pygame.time.Clock()
font = pygame.font.Font()

# ====== Гистограммы =========
pixels = pygame.surfarray.pixels3d(main_image)

# RGB каналы
red = np.zeros_like(pixels, dtype=np.uint8)
red[:, :, 0] = pixels[:, :, 0]

green = np.zeros_like(pixels, dtype=np.uint8)
green[:, :, 1] = pixels[:, :, 1]

blue = np.zeros_like(pixels, dtype=np.uint8)
blue[:, :, 2] = pixels[:, :, 2]
del pixels

fig_red, ax_red = plt.subplots(figsize=(2, 2), dpi=100)
ax_red.hist(red[:, :, 0].flatten(), bins=256, density=True)
ax_red.grid(True)

# Добавление в окно pygame
hist_red = FigureCanvasAgg(fig_red)
hist_red.draw()
hist_red_surf = pygame.image.frombytes(
    hist_red.buffer_rgba().tobytes(),
    hist_red.get_width_height(),
    "RGBA",
)

fig_green, ax_green = plt.subplots(figsize=(2, 2), dpi=100)
ax_green.hist(green[:, :, 1].flatten(), bins=256, density=True)
ax_green.grid(True)
hist_green = FigureCanvasAgg(fig_green)
hist_green.draw()
hist_green_surf = pygame.image.frombytes(
    hist_green.buffer_rgba().tobytes(),
    hist_green.get_width_height(),
    "RGBA",
)

fig_blue, ax_blue = plt.subplots(figsize=(2, 2), dpi=100)
ax_blue.hist(blue[:, :, 2].flatten(), bins=256, density=True)
ax_blue.grid(True)
hist_blue = FigureCanvasAgg(fig_blue)
hist_blue.draw()
hist_blue_surf = pygame.image.frombytes(
    hist_blue.buffer_rgba().tobytes(),
    hist_blue.get_width_height(),
    "RGBA",
)

modes_button = pygame_gui.elements.UIDropDownMenu(options_list=COLOR_MODES,
                                                  starting_option=COLOR_MODES[0],
                                                  relative_rect=pygame.Rect((20, 30), (100, 30)),
                                                  manager=channel_mode_manager)

compare_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((140, 30), (250, 30)),
                                                        start_value=slider_value,
                                                        value_range=(slider_value, img.width),
                                                        manager=channel_mode_manager)

(r_level_slider, g_level_slider, b_level_slider,
            contrast_slider,
            select_r_source, select_g_source, select_b_source,
            mirror_v, mirror_h) = create_sliders(effects_mode_manager, SIZE_SCREEN) # Слайдеры для эффектов

# изменения цвета изображения в зависимости от выбранного режима
def process(rgb_image, mode):
    if mode == "Gray":
        rgb_image = rgb_image.astype(np.float32)
        grayscale_image = np.dot(rgb_image[..., :3], [0.2989, 0.5870, 0.1140])
        return np.repeat(grayscale_image[:, :, np.newaxis], 3, axis=2)
    rgb_image = rgb_image.astype(np.uint8)
    if mode == "Red":
        rgb_image[:, :, 1:] = 0
    elif mode == "Green":
        rgb_image[:, :, [0, 2]] = 0
    elif mode == "Blue":
        rgb_image[:, :, :2] = 0
    return rgb_image

# обновление изображения на экране в зависимости от положения слайдера
def update_display_image():
    global display_image
    x = int(slider_value)
    image = rgb.copy()
    image[:x] = process(rgb[:x], modes_button.selected_option[0])
    surf = pygame.surfarray.make_surface(image).convert_alpha()
    pygame.surfarray.pixels_alpha(surf)[:] = alpha      # применение прозрачности
    display_image = surf

clock = pygame.time.Clock()


def draw_channels():
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (50, 50, 70), (0, 0, SIZE_SCREEN[0], 120))
    screen.blit(display_image, image_rect)

    screen.blit(hist_red_surf, (SIZE_SCREEN[0] - 250, 150))
    screen.blit(hist_green_surf, (SIZE_SCREEN[0] - 250, 350))
    screen.blit(hist_blue_surf, (SIZE_SCREEN[0] - 250, 550))

    # Отслеживание положения мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if image_rect.collidepoint(mouse_x, mouse_y):
        image_x = mouse_x - image_rect.x
        image_y = mouse_y - image_rect.y

        color = main_image.get_at((image_x, image_y))

        area = pygame.Rect(0, 0, ZOOM_SCALE, ZOOM_SCALE)
        area.center = (image_x, image_y)

        # обрезаем по границам картинки, чтобы не выйти за них
        area = area.clip(main_image.get_rect())

        if area.width > 0 and area.height > 0:
            piece = display_image.subsurface(area).copy()

            rgb_piece = pygame.surfarray.array3d(piece)
            r_channel = rgb_piece[:, :, 0]
            g_channel = rgb_piece[:, :, 1]
            b_channel = rgb_piece[:, :, 2]

            avg_r = r_channel.sum() / r_channel.size
            avg_g = g_channel.sum() / g_channel.size
            avg_b = b_channel.sum() / b_channel.size

            S_red = ((r_channel - avg_r) ** 2).sum() / r_channel.size
            S_green = ((g_channel - avg_g) ** 2).sum() / g_channel.size
            S_blue = ((b_channel - avg_b) ** 2).sum() / b_channel.size

            piece = pygame.transform.scale(
                piece, (area.width * ZOOM_SCALE, area.height * ZOOM_SCALE)
            )
            screen.blit(piece, (SIZE_SCREEN[0] - 170, 5))
            pygame.draw.rect(screen, (255, 255, 255), (*(SIZE_SCREEN[0] - 170, 5), *piece.get_size()), 2)

        text = font.render(f"R: {color.r} G: {color.g} B: {color.b}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        slider_text = font.render(
            f"Координаты p = {image_x, image_y} | Интенсивность : {round((color.r + color.g + color.b) / 3, 2)}\n" +
            f"μ_Wp(RED) = {round(r_channel.sum() / r_channel.size, 2)}, μ_Wp(GREEN) = {round(g_channel.sum() / g_channel.size, 2)}, μ_Wp(BLUE) = {round(b_channel.sum() / b_channel.size, 2)}\n" +
            f"S_Wp(RED) = {round(S_red, 2)}, S_Wp(GREEN) = {round(S_green, 2)}, S_Wp(BLUE) = {round(S_blue, 2)},",
            True, (255, 255, 255))
        screen.blit(slider_text, (10, 70))

    slider_text = font.render(f"Comparison", True, (255, 255, 255))
    screen.blit(slider_text, (140, 10))

    channel_mode_manager.draw_ui(screen)


def draw_effects():
    # Делаем слайдеры для каждой настройки и разделители между ними в create_sliders()
    # НЕ УСЛОЖНЯЕМ ИНТЕРФЕЙС И СЕБЕ ЖИЗНЬ!
    screen.fill((30, 30, 30))
    effects_mode_manager.draw_ui(screen)


# Основной цикл отрисовки
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            update_display_image()
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            slider_value = event.value
            update_display_image()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                showmode = M_EFFECTS if showmode == M_CHANNELS else M_CHANNELS
        channel_mode_manager.process_events(event)
        effects_mode_manager.process_events(event)

    if showmode == M_CHANNELS:
        channel_mode_manager.update(time_delta)
        draw_channels()
    else:
        draw_effects()
        effects_mode_manager.update(time_delta)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()