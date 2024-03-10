from labtools.defaults import *

def massstab(preview, data_file=None):
    b, B, G, f3, B2 = unpack_data(data_file['projector'], ('b', 'db'), ('B', 'dB'), 'G', 'f3', ('B2', 'dB'))

    gamma_1 = b / f3
    gamma_2 = B / G
    gamma_3 = B2 / G

    note_var('gamma_1', gamma_1)
    note_var('gamma_2', gamma_2)
    note_var('gamma_3', gamma_3)


def ausleuchtung_1(preview, data_file=None):
    bg, grid_x, grid_y, light_1, light_2, light_3 = unpack_data(data_file['projector'],
        ('bgl', 'dl'),
        'grid_x',
        'grid_y',
        'light_1',
        'light_2',
        'light_3'
        )

    background = sum(bg) / len(bg)


    light_1 = light_1 * 0.1 - background
    light_2 = light_2 * 0.1
    light_3 = light_3 * 0.1
    light_2[light_2 == 0.0] = background
    light_3[light_3 == 0.0] = background

    light_2 = light_2 - background
    light_3 = light_3 - background

    plot = Plot()
    plot.title = 'Bildfeldausleuchtung Aufbau 1'
    plot.add_element('heatmap', grid_x - 1, grid_y - 1, light_1, label='Lux')
    plot.finish(preview, 'results/heatmap_1.png')

    plot = Plot()
    plot.title = 'Bildfeldausleuchtung Kondensor verdreht'
    plot.add_element('heatmap', grid_x - 1, grid_y - 1, light_2, label='Lux')
    plot.finish(preview, 'results/heatmap_2.png')

    plot = Plot()
    plot.title = 'Bildfeldausleuchtung plankonvexes Objektiv'
    plot.add_element('heatmap', grid_x - 1, grid_y - 1, light_3, label='Lux')
    plot.finish(preview, 'results/heatmap_3.png')
