"""some class"""

import numpy as np
import pygame_gui as pgui
import pygame as pg

class Aliasing:
    """
    Factory class that creates the factory that's gotta smooth the images
    1. Rectangle filter
    2. Median filter
    3. Sigma filter
    """
    rect_btn: pgui.elements.UICheckBox = None
    median_btn: pgui.elements.UICheckBox = None
    sigma_btn: pgui.elements.UICheckBox = None
    img_ui: pgui.elements.UIImage = None
    image_surf: pg.Surface = None
    img_org: pg.Surface = None

    ZOOM_SCALE = 12
    SIZE_SCREEN = None

    def __init__(self):
        """
        constructor of Aliasing class object
        """

    def get_ui(self, 
               manager: pgui.UIManager, 
               img: pg.surface, 
               x = 20, 
               y = 20, 
               w = 600, 
               h = 300) -> pgui.core.UIContainer:
        """
        ts returns container that contains ui
        """
        container = pgui.core.UIContainer(relative_rect=pg.Rect((x, y), (w, h)),
                                          manager = manager)

        # кнопочки 💅🏼
        rect_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x+10, y), (20,20)),
                                            text="Прямоугольный фильтр",
                                            container=container,
                                            object_id="#rect_filter")
        median_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 210, y), (20,20)),
                                              text="Медианный фильтр",
                                              container=container,
                                              object_id="#median_filter")
        sigma_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 2 * 200, y), (20,20)),
                                             text="Сигма-фильтр",
                                             container=container,
                                             object_id="#sigma_filter")
        gaussian_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 2 * 270, y), (20,20)),
                                                text="Гауссиан-фильтр",
                                                container=container,
                                                object_id="#gaussian_filter")

        abs_diff_btn = pgui.elements.UICheckBox(relative_rect=pg.Rect((x + 2 * 270, y + 20), (20,20)),
                                                text="Абсолютная разница",
                                                container=container,
                                                object_id="#abs_diff_filter")

        image_ui = pgui.elements.UIImage(relative_rect=pg.Rect((0, y + 50), (img.get_width(), img.get_height())),
                                         image_surface=img,
                                         container=container)
        
        self.rect_btn = rect_btn
        self.median_btn = median_btn
        self.sigma_btn = sigma_btn
        self.img_ui = image_ui
        self.image_surf = img.copy()
        self.img_org = img.copy()

        return container

    def zoom_thing(self, screen: pg.Surface, mouse: tuple[int, int]):
        """
        creates small zoom area to watch on pixels around the cursor
        """
        mouse_x, mouse_y = mouse
        image_rect = self.img_ui.get_abs_rect()
        image = self.image_surf

        if image_rect.collidepoint(mouse_x, mouse_y):
            image_x = (mouse_x - image_rect.x) * image.get_width() // image_rect.width
            image_y = (mouse_y - image_rect.y) * image.get_height() // image_rect.height

            area = pg.Rect(0, 0, self.ZOOM_SCALE, self.ZOOM_SCALE)
            area.center = (image_x, image_y)

            # обрезаем по границам картинки, чтобы не выйти за них
            area = area.clip(image.get_rect())

            if area.width > 0 and area.height > 0:
                piece = image.subsurface(area).copy()

                piece = pg.transform.scale(
                    piece, (area.width * self.ZOOM_SCALE, area.height * self.ZOOM_SCALE)
                )
                zoom_rect = piece.get_rect(topright=(screen.get_width() - 10, 100))
                screen.blit(piece, zoom_rect)
                pg.draw.rect(screen, (255, 255, 255), zoom_rect, 2)
        
    def process_event(self,
                      event: pg.event.Event,
                      manager: pgui.UIManager):
        """
        process events
        """
        if event.type == pgui.UI_CHECK_BOX_CHECKED:
            print(event.ui_object_id)
            if event.ui_object_id == "container.#rect_filter":
                self.img_ui.set_image(self.apply_rectangle_filter_kernel_3(self.image_surf))
            elif event.ui_object_id == "container.#median_filter":
                self.img_ui.set_image(self.apply_median_filter(self.image_surf))
            elif event.ui_object_id == "container.#sigma_filter":
                self.img_ui.set_image(self.apply_sigma_filter(self.image_surf))
            elif event.ui_object_id == "container.#gaussian_filter":
                self.img_ui.set_image(self.apply_gaussian_filter(self.image_surf))
            elif event.ui_object_id == "container.#abs_diff_filter":
                self.img_ui.set_image(self.apply_absolute_difference(self.img_ui.image, self.img_org))
        elif event.type == pgui.UI_CHECK_BOX_UNCHECKED:
            self.img_ui.set_image(self.image_surf)

    def apply_rectangle_filter_kernel_3(self, img_ui : pg.Surface):
        """
        rectantle filter with kernel 3x3
        looks like this thing:
            |1 1 1|
        K = |1 1 1| * 1/9
            |1 1 1|
        """
        I_org = pg.surfarray.array3d(img_ui)
        I = np.pad(I_org.astype('f'), ((1,1), (1,1), (0,0)), mode="edge")
        res = (
            I[:-2, :-2]     + I[:-2, 1:-1]      + I[:-2, 2:] +
            I[1:-1, :-2]    + I[1:-1, 1:-1]     + I[1:-1, 2:] +
            I[2:, :-2]      + I[2:, 1:-1]       + I[2:, 2:]
        )
        return pg.surfarray.make_surface((res/9).astype(int))
        
    def apply_median_filter(self, img_ui : pg.Surface):
        """
        rectantle filter with kernel 3x3
        looks like this thing:
                       |1 1 1|
        K = median of (|1 1 1|)
                       |1 1 1|
        """
        pixels = pg.surfarray.array3d(img_ui)
        width, height, _ = pixels.shape
        I = np.pad(pixels, ((1, 1), (1, 1), (0, 0)), mode="reflect")

        neighbors = np.stack([
            I[0:width,     0:height],
            I[0:width,     1:height+1],
            I[0:width,     2:height+2],
            I[1:width+1,   0:height],
            I[1:width+1,   1:height+1],
            I[1:width+1,   2:height+2],
            I[2:width+2,   0:height],
            I[2:width+2,   1:height+1],
            I[2:width+2,   2:height+2],
        ])

        return pg.surfarray.make_surface(
            np.median(neighbors, axis=0).astype(np.uint8)
        )

    def apply_gaussian_filter(self, img_ui : pg.Surface):
        """
        rectantle filter with kernel 3x3
        looks like this thing:
            |1 2 1|
        K = |2 4 2| * 1/16
            |1 2 1|
        """
        I_org = pg.surfarray.array3d(img_ui)
        I = np.pad(I_org.astype('f'), ((1,1), (1,1), (0,0)), mode="edge")
        neighbors = [
            I[:-2, :-2],
            I[:-2, 1:-1],
            I[:-2, 2:],
            I[1:-1, :-2],
            I[1:-1, 1:-1],
            I[1:-1, 2:],
            I[2:, :-2],
            I[2:, 1:-1],
            I[2:, 2:]
        ]
        res = (
            neighbors[0] + 2*neighbors[1] + neighbors[2] +
            2*neighbors[3] + 4*neighbors[4] + 2*neighbors[5] +
            neighbors[6] + 2*neighbors[7] + neighbors[8]
        )
        return pg.surfarray.make_surface((res/16).astype(np.uint8))
    
    def apply_sigma_filter(self, img_ui : pg.Surface):
        """
        rectantle filter with kernel 3x3
        looks like this thing:
            |1 2 1|
        K = |2 4 2| * 1/16
            |1 2 1|
        """
        sigma = 50
        I_org = pg.surfarray.array3d(img_ui)
        I = np.pad(I_org.astype('f'), ((1,1), (1,1), (0,0)), mode="edge")
        center = I[1:-1, 1:-1]
        neighbors = [
            I[:-2, :-2],
            I[:-2, 1:-1],
            I[:-2, 2:],
            I[1:-1, :-2],
            I[1:-1, 1:-1],
            I[1:-1, 2:],
            I[2:, :-2],
            I[2:, 1:-1],
            I[2:, 2:]
        ]

        masks = [
            np.max(np.abs(n - center), axis=2) <= sigma
            for n in neighbors
        ]
        
        total = sum(n * m[:, :, None] for n, m in zip(neighbors, masks))
        count = sum(masks)

        result = total / count[:, :, None]

        return pg.surfarray.make_surface(result.astype(np.uint8))
    
    def apply_absolute_difference(self, img_ui1: pg.Surface, img_ui2: pg.Surface):
        """
        find abs diff between original and filtered image
        """
        I1 = pg.surfarray.array3d(img_ui1).astype('f')
        I2 = pg.surfarray.array3d(img_ui2).astype('f')

        abs_diff = np.abs(I1 - I2)
        print(I1[0, 0], I2[0, 0], abs_diff[0, 0])

        return pg.surfarray.make_surface(abs_diff.astype(np.uint8))