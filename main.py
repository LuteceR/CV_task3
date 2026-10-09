import pygame

import numpy as np

pygame.init()

screen = pygame.display.set_mode((750, 600))

main_image = pygame.image.load("C:\\Users\\kb123\\Documents\\MTGO\\task_7\\img.png").convert_alpha()
pixels = pygame.surfarray.pixels3d(main_image)
image_rect = main_image.get_rect()
print(main_image.get_at((125, 125)))


gray = ((pixels[:, :, 0] + pixels[:, :, 1] + pixels[:, :, 2]) // 3).astype(np.uint8)
gray_image = pygame.surfarray.make_surface(np.repeat(gray[:, :, np.newaxis], 3, axis=2))
print(gray_image.get_at((125, 125)))


red_image = pygame.surfarray.make_surface(np.repeat(pixels[:, :, 0:1].astype(np.uint8), 3, axis=2))
print(main_image.get_at((125, 125)))
print(pixels[125, 125, :])
print(red_image.get_at((125, 125)))

green_image = pygame.surfarray.make_surface(np.repeat(pixels[:, :, 1:2].astype(np.uint8), 3, axis=2))
blue_image = pygame.surfarray.make_surface(np.repeat(pixels[:, :, 2:3].astype(np.uint8), 3, axis=2))
del pixels

clock = pygame.time.Clock()
font = pygame.font.Font()



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