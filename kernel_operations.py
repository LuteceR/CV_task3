import numpy as np

def the_eight_connectivity(rgb: np.ndarray) -> np.ndarray:
    filtered_rgb = np.pad(rgb.astype('f'), ((1, 1), (1, 1), (0, 0)), mode='edge') # добавление pad для фото, который является копией самих пикселей. Нужно для 4 и 8-ми связностей
    horizontal_neighbours = filtered_rgb[:, 2:] + filtered_rgb[:, 1:-1] + filtered_rgb[:, :-2]
    res = horizontal_neighbours[2:, :] + horizontal_neighbours[1:-1, :] + horizontal_neighbours[:-2, :]
    return (res/9).astype(rgb.dtype)

def the_four_connectivity(rgb: np.ndarray) -> np.ndarray:
    filtered_rgb = np.pad(rgb.astype('f'), ((1, 1), (1, 1), (0, 0)), mode='edge') # добавление pad для фото, который является копией самих пикселей. Нужно для 4 и 8-ми связностей
    res = (filtered_rgb[1:-1, 1:-1] +
           filtered_rgb[:-2,1:-1] +
           filtered_rgb[2:,1:-1] +
           filtered_rgb[1:-1,:-2] +
           filtered_rgb[1:-1,2:])
    return (res/5).astype(rgb.dtype)

def drunk_filter(rgb: np.ndarray, d: int) -> np.ndarray:
    filtered_rgb = np.pad(rgb.astype('f'), ((d, d), (d, d), (0, 0)), mode='edge') # добавление pad для фото, который является копией самих пикселей. Нужно для 4 и 8-ми связностей
    res = (filtered_rgb[2*d:, 2*d:] * 0.5 +
           filtered_rgb[:-2*d, :-2*d] * 0.5)
    return (res).astype(rgb.dtype)