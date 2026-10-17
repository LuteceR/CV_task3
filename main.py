import pygame
import pygame_gui
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image

from pathlib import Path
import numpy as np
import math
# =================================  НА КНОПКУ "0" ПЕРЕКЛЮЧЕНИЕ РЕЖИМОВ  ==========================
from ui import create_sliders
import kernel_operations

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
mode_channels = "channels"
mode_effects = "effects"
mode_cont_map = "constrast_map"
showmodes = [mode_channels, mode_effects, mode_cont_map]
cur_showmode = mode_channels

d = 1

four_conn = False
ate_conn = False

# значения окна W
avg_r = 0
avg_g = 0
avg_b = 0
avg_a = 0
avg_all = 0

with Image.open(IMAGE) as img:
    SIZE_SCREEN = (max(800, img.width + 10), max(800, img.height + 120))

pygame.init()
pygame.display.set_caption("python gaming 4k")
screen = pygame.display.set_mode(SIZE_SCREEN)
clock = pygame.time.Clock()

channel_mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")
effects_mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")
cont_map_mode_manager = pygame_gui.UIManager(SIZE_SCREEN, BASE_DIR / "theme.json")

# convert_alpha замена прозрачных частей на черный
main_image = pygame.image.load(BASE_DIR / IMAGE).convert_alpha()
display_image = main_image.copy()
image_rect = main_image.get_rect(topleft=(5, 180))
rgb = pygame.surfarray.array3d(main_image)
print(f"rgb shape: {rgb.shape}")
mean_rgb = rgb.mean(axis=(0, 1))
mean_all = rgb.mean()


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

grayscale_image = np.mean(pixels[..., :3], axis=-1)
del pixels

fig_red, ax_red = plt.subplots(figsize=(2, 2), dpi=100)
ax_red.hist(red[:, :, 0].flatten(), color='red', bins=256, density=True)
ax_red.grid(True)
hist_red = FigureCanvasAgg(fig_red)
hist_red.draw()
hist_red_surf = pygame.image.frombytes(
    hist_red.buffer_rgba().tobytes(),
    hist_red.get_width_height(),
    "RGBA",
)

fig_green, ax_green = plt.subplots(figsize=(2, 2), dpi=100)
ax_green.hist(green[:, :, 1].flatten(), color='green', bins=256, density=True)
ax_green.grid(True)
hist_green = FigureCanvasAgg(fig_green)
hist_green.draw()
hist_green_surf = pygame.image.frombytes(
    hist_green.buffer_rgba().tobytes(),
    hist_green.get_width_height(),
    "RGBA",
)

fig_blue, ax_blue = plt.subplots(figsize=(2, 2), dpi=100)
ax_blue.hist(blue[:, :, 2].flatten(), color='blue', bins=256, density=True)
ax_blue.grid(True)
hist_blue = FigureCanvasAgg(fig_blue)
hist_blue.draw()
hist_blue_surf = pygame.image.frombytes(
    hist_blue.buffer_rgba().tobytes(),
    hist_blue.get_width_height(),
    "RGBA",
)

fig_line, ax_line = plt.subplots(figsize=(3, 2), dpi=100)
ax_line.plot(grayscale_image[:, 0])
ax_line.grid(True)
plot_line = FigureCanvasAgg(fig_line)
plot_line.draw()
plot_line_surf = pygame.image.frombytes(
    plot_line.buffer_rgba().tobytes(),
    plot_line.get_width_height(),
    "RGBA",
)

# UI элементы

modes_button = pygame_gui.elements.UIDropDownMenu(options_list=COLOR_MODES,
                                                  starting_option=COLOR_MODES[0],
                                                  relative_rect=pygame.Rect((20, 30), (100, 30)),
                                                  manager=channel_mode_manager)

compare_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((140, 30), (250, 30)),
                                                    start_value=slider_value,
                                                    value_range=(slider_value, img.width),
                                                    manager=channel_mode_manager)

d_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((140, 0), (100, 30)),
                                                    start_value=d,
                                                    value_range=(1, 10),
                                                    manager=channel_mode_manager)

four_checkbox = pygame_gui.elements.UICheckBox(text="4-связность",
                                                relative_rect=pygame.Rect((390, 30), (30, 30)),
                                                manager=channel_mode_manager)

ate_checkbox = pygame_gui.elements.UICheckBox(text="8-связность",
                                                relative_rect=pygame.Rect((510, 30), (30, 30)),
                                                manager=channel_mode_manager)

HandmadeFilter_checkbox = pygame_gui.elements.UICheckBox(text="wierd filter",
                                                        relative_rect=pygame.Rect((390, 2), (30, 30)),
                                                        manager=channel_mode_manager)

save_button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((510, 70), (110, 30)),
                                           text="Save image", 
                                           manager=channel_mode_manager)

(r_level_slider, g_level_slider, b_level_slider,
    contrast_slider,
    select_r_source, select_g_source, select_b_source,
    r_level_inv, g_level_inv, b_level_inv,
    mirror_v, mirror_h, line_slider_for_graph,
    four_conn_checkbox, eight_conn_checkbox, window_size_slider,
    save_button2, save_button3) = create_sliders(effects_mode_manager, cont_map_mode_manager, SIZE_SCREEN)

# изменения цвета изображения в зависимости от выбранного режима
def process(rgb_image, mode):
    if mode == "Gray":
        rgb_image = rgb_image.astype(np.float32)
        grayscale_image = np.dot(rgb_image[..., :3], [0.2989, 0.5870, 0.1140])
        return np.repeat(grayscale_image[:, :, np.newaxis], 3, axis=2) # np.mean(rgb_image[..., :3], axis=-1) # для усредн. серого
    rgb_image = rgb_image.astype(np.uint8)
    if mode == "Red":
        rgb_image[:, :, 1:] = 0
    elif mode == "Green":
        rgb_image[:, :, [0, 2]] = 0
    elif mode == "Blue":
        rgb_image[:, :, :2] = 0
    return rgb_image


def update_image():
    if cur_showmode == mode_channels:
        update_image_with_channels()
    elif cur_showmode == mode_effects:
        update_image_with_effects()
    elif cur_showmode == mode_cont_map:
        update_image_with_cont_map()

# обновление изображения на экране в зависимости от положения слайдера
def update_image_with_channels():
    global display_image
    rgb_filtered = rgb.copy()
    if four_checkbox.get_state():
        rgb_filtered = kernel_operations.the_four_connectivity(rgb)
    elif ate_checkbox.get_state():
        rgb_filtered = kernel_operations.the_eight_connectivity(rgb)
    elif HandmadeFilter_checkbox.get_state():
        rgb_filtered = kernel_operations.drunk_filter(rgb, d)
    x = int(slider_value)
    image = rgb_filtered
    image[:x] = process(rgb[:x], modes_button.selected_option[0])
    surf = pygame.surfarray.make_surface(image).convert_alpha()
    display_image = surf


def update_image_with_effects():
    global display_image, plot_line_surf, fig_line, ax_line, plot_line

    image = rgb.astype(np.float32)

    # Смена источников RGB-каналов
    CHANNELS = ["Red", "Green", "Blue"]
    r_source = CHANNELS.index(select_r_source.selected_option[0])
    g_source = CHANNELS.index(select_g_source.selected_option[0])
    b_source = CHANNELS.index(select_b_source.selected_option[0])
    image = image[:, :, [r_source, g_source, b_source]]

    # Усиление/ослабление
    channel_levels = np.array([
        r_level_slider.get_current_value(),
        g_level_slider.get_current_value(),
        b_level_slider.get_current_value(),
    ], dtype=np.float32)

    image *= channel_levels

    # Инвертирование
    if r_level_inv.get_state():
        image[:, :, 0] = 255 - image[:, :, 0]

    if g_level_inv.get_state():
        image[:, :, 1] = 255 - image[:, :, 1]

    if b_level_inv.get_state():
        image[:, :, 2] = 255 - image[:, :, 2]

    # Контраст
    contrast = contrast_slider.get_current_value()
    image = 256 / (1 + np.exp(contrast * (1/2 - (image/256.))))

    image = np.clip(np.rint(image), 0, 255).astype(np.uint8)

    # отражение
    flip_h = mirror_h.get_state()
    flip_v = mirror_v.get_state()

    if flip_h:
        image = image[::-1, :, :]

    if flip_v:
        image = image[:, ::-1, :]

    surf = pygame.surfarray.make_surface(
        np.ascontiguousarray(image)
    )

    display_image = surf

    # График профиля по строке
    rgb_image = rgb.copy()
    grayscale_image = np.mean(rgb_image[..., :3], axis=-1)

    ax_line.clear() 
    line = math.floor(line_slider_for_graph.get_current_value() * (img.height - 1))
    ax_line.plot(grayscale_image[:, line])
    ax_line.grid(True)
    ax_line.set_ylim(0, 255)
    plot_line.draw()
    plot_line_surf = pygame.image.frombytes(
        plot_line.buffer_rgba().tobytes(),
        plot_line.get_width_height(),
        "RGBA",
    )

def update_image_with_cont_map():
    global display_image
    if four_conn_checkbox.get_state():
        kernel=np.array([[0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]])
    elif (eight_conn_checkbox.get_state()):
        kernel = np.ones((3, 3), dtype=np.uint8)
    else:
        kernel_size = window_size_slider.get_current_value() * 2 + 1
        kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)

    img = rgb.astype(np.float32)
    gray = np.mean(img[..., :3], axis=-1)

    kh, kw = kernel.shape
    pad = kh // 2
    padded = np.pad(gray, ((pad, pad), (pad, pad)), mode="edge")

    H, W = gray.shape
    contrast_map = np.zeros((H, W), dtype=np.float32)

    # создание набора масок
    windows = np.lib.stride_tricks.sliding_window_view( # нет Linux
        padded,
        (kh, kw)
    )
    # print(windows.shape) # выведет (img.w, img.h, kw, kh)

    # приведение ядра к бинарным значениям
    mask = kernel.astype(bool)

    values = windows[:, :, mask]
    means = values.mean(axis=-1)
    contrast_map = np.sqrt(np.mean((values - means[:, :, None]) ** 2, axis=-1))

    # for y in range(H):
    #     for x in range(W):
    #         y0 = y
    #         y1 = y + kh
    #         x0 = x
    #         x1 = x + kw

    #         window = padded[y0:y1, x0:x1]
    #         mask = kernel.astype(bool)
    #         values = window[mask]

    #         mean = np.mean(values)
    #         std = np.sqrt(np.mean((values - mean) ** 2))
    #         contrast_map[y, x] = std

    # нормализация в диапазон 0..255
    c_min = contrast_map.min()
    c_max = contrast_map.max()
    cont_map = (contrast_map - c_min) / (c_max - c_min) * 255.0
    cont_map = cont_map.astype(np.uint8)

    res_image = np.stack((cont_map, cont_map, cont_map), axis=-1)
    display_image = pygame.surfarray.make_surface(res_image).convert_alpha()


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

        color = display_image.get_at((image_x, image_y))

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

    channel_mode_manager.draw_ui(screen)


def draw_effects():
    # Делаем слайдеры для каждой настройки и разделители между ними в create_sliders()
    # НЕ УСЛОЖНЯЕМ ИНТЕРФЕЙС И СЕБЕ ЖИЗНЬ!!!🙏🙏🙏🙏🙏🙏

    screen.fill((30, 30, 30))

    # заголовки
    text = font.render(f"Источники цветов (каналы)", True, (255, 255, 255))
    screen.blit(text, (30, 10))

    text = font.render(f"Количество цветов", True, (255, 255, 255))
    screen.blit(text, (30, 65))

    text = font.render(f"Контрастность", True, (255, 255, 255))
    screen.blit(text, (300, 10))

    screen.blit(display_image, image_rect)

    cur_line = round(line_slider_for_graph.get_current_value() * img.height)
    slider_text = font.render(f"Строка {cur_line}", True, (255, 255, 255))
    screen.blit(slider_text, (30, 120))

    mouse_pos = pygame.mouse.get_pos()
    if line_slider_for_graph.rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (200, 200, 200, 128), (image_rect.left, image_rect.top + cur_line - 1, img.width, 3))

    screen.blit(plot_line_surf, (SIZE_SCREEN[1] - 330, 120))

    effects_mode_manager.draw_ui(screen)

def draw_cont_map():
    screen.fill((30, 30, 30))
    screen.blit(display_image, image_rect)
    screen.blit(font.render(f"Размер окна {window_size_slider.get_current_value() * 2 + 1}", True, (255, 255, 255)), (10, 100))

    cont_map_mode_manager.draw_ui(screen)

# Основной цикл отрисовки
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in [pygame_gui.UI_CHECK_BOX_CHECKED, 
                            pygame_gui.UI_CHECK_BOX_UNCHECKED, 
                            pygame_gui.UI_DROP_DOWN_MENU_CHANGED]:
            update_image()
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == compare_slider:
                slider_value = event.value
            elif (event.ui_element == d_slider):
                d = event.value
            update_image()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                cur_showmode = showmodes[(showmodes.index(cur_showmode) + 1) % 3]
                update_image()
            elif event.key == pygame.K_8:
                ate_checkbox.set_state(not ate_checkbox.get_state())
            elif event.key == pygame.K_4:
                four_checkbox.set_state(not four_checkbox.get_state())
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element in [save_button1, save_button2, save_button3]:
                pygame.image.save(display_image, "output_image.png")

        channel_mode_manager.process_events(event)
        effects_mode_manager.process_events(event)
        cont_map_mode_manager.process_events(event)

    if cur_showmode == mode_channels:
        draw_channels()
        channel_mode_manager.update(time_delta)
    elif cur_showmode == mode_effects:
        draw_effects()
        effects_mode_manager.update(time_delta)
    elif cur_showmode == mode_cont_map:
        draw_cont_map()
        cont_map_mode_manager.update(time_delta)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()