from labtools.defaults import *
from fuckoff import carr

def calc_g(data):
    x, x0 = unpack_data(data['konstante'], ('x', 'dx'), 'x0')
    m = np.arange(1, 1 + len(x))

    x = x - x0

    r = 100
    green = 546.07 #converted to nm
    angle = x / r

    g = m * green / (2 * np.sin(angle / 2))

    g_bar = sum(g) / len(g)
    return g_bar, g


def konstante(preview, data=None):
    g_bar, g = calc_g(data)

    x, x0 = unpack_data(data['konstante'], ('x', 'dx'), 'x0')
    m = np.arange(1, 1 + len(x))
    x = x - x0
    r = 100
    angle = x / r

    note_var('g_bar', g_bar)

    table = {
        'Ordnung': m,
        r'\varphi [rad]': angle,
        'g [nm]': g,
    }

    write_printable(table, 'results/gitter_konstante.csv')


def blue_line(preview, data=None):
    x_blue, x0 = unpack_data(data['blue'], ('x', 'dx'), 'x0')
    x_blue = x_blue - x0

    m = np.arange(1, 1 + len(x_blue))
    r = 100
    angle = x_blue / r

    g_bar, _ = calc_g(data)

    l_blue = g_bar * np.sin(angle / 2) * 2 / m

    _ = list(map(lambda x: note_var('lambda', x), l_blue))

    note_var('l_bar', sum(l_blue) / len(l_blue))

    table = {
        'Ordnung': m,
        r'\varphi [rad]': angle,
        r'\lambda': l_blue,
    }

    write_printable(table, 'results/blue.csv')


def resolution(preview, data=None):
    g, _ = calc_g(data)

    b, s, B = unpack_data(data['resolution'], ('b', 'db'), ('g', 'dg'), ('B', 'dB'))
    D = s * B / b # cm
    D = 1e7 * D # nm

    N = D / g

    print(N)

    A_2 = 2 * N
    A_4 = 4 * N
    A_6 = 6 * N

    l = 578.01

    dl_2 = l / A_2
    dl_4 = l / A_4
    dl_6 = l / A_6

    table = {
        'Verschwunde  Ordnung': np.array(['keine', '2.', '4.', '6.']),
        'D': D,
        'N': N,
    }

    table_2 = {
        'N': N,
        'A (m=2)': A_2,
        'A (m=4)': A_4,
        'A (m=6)': A_6,
    }

    table_3 = {
        'Verschwunde  Ordnung': np.array(['keine', '2.', '4.', '6.']),
        'N': N,
        r'\Delta\lambda(m=2)': dl_2,
        r'\Delta\lambda(m=4)': dl_4,
        r'\Delta\lambda(m=6)': dl_6,
    }

    write_printable(table, 'results/spaltzahlen.csv')
    write_printable(table_2, 'results/aufloesugen.csv')
    write_printable(table_3, 'results/delta_lambda.csv')