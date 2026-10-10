import pygame
import matplotlib
matplotlib.use("Agg") # зачем это? (надо чекнуть)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

import numpy as np

# Добавление картинки в движок происходит через make_surface()
# Картинка хранится в 3-мерном массиве [x, y, c] c - канал RGB
# Данные находятся в диапазоне uint8: 0 - 255
# screen.fill(color) - заполнить экран цветом
# screen.blit(element) - нарисовать элемент (картинку/график) на экране
# Позиция и цвет часто передаются как питоновского набора, например (1, 2, 3)

pygame.init()

screen = pygame.display.set_mode((750, 750))

# convert_alpha замена прозрачных частей на черный
main_image = pygame.image.load("C:\\Users\\kb123\\Documents\\MTGO\\task_7\\img.png").convert_alpha()
pixels = pygame.surfarray.pixels3d(main_image)
image_rect = main_image.get_rect()

# ч/б вариант
gray = pixels[:, :, :3].astype(np.uint16).sum(axis=2) // 3
gray_image = pygame.surfarray.make_surface(np.repeat(gray[:, :, np.newaxis], 3, axis=2))

# RGB каналы
red = np.zeros_like(pixels, dtype=np.uint8)
red[:, :, 0] = pixels[:, :, 0]
red_image = pygame.surfarray.make_surface(red)

green = np.zeros_like(pixels, dtype=np.uint8)
green[:, :, 1] = pixels[:, :, 1]
green_image = pygame.surfarray.make_surface(green)

blue = np.zeros_like(pixels, dtype=np.uint8)
blue[:, :, 2] = pixels[:, :, 2]
blue_image = pygame.surfarray.make_surface(blue)
del pixels # нужно удалить чтобы разблокировать изображение main_image

clock = pygame.time.Clock()
font = pygame.font.Font()

# ====== Гистограммы =========
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

# Основной цикл отрисовки
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    screen.blit(main_image, image_rect)
    screen.blit(gray_image, (250, 0), image_rect)

    screen.blit(red_image, (0, 250), image_rect)
    screen.blit(green_image, (250, 250), image_rect)
    screen.blit(blue_image, (500, 250), image_rect)

    screen.blit(hist_red_surf, (10, 500))
    screen.blit(hist_green_surf, (260, 500))
    screen.blit(hist_blue_surf, (510, 500))

    # Отслеживание положенияя мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if image_rect.collidepoint(mouse_x, mouse_y):
        image_x = mouse_x - image_rect.x
        image_y = mouse_y - image_rect.y

        color = main_image.get_at((image_x, image_y))
        text = font.render(f"R: {color.r} G: {color.g} B: {color.b}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()