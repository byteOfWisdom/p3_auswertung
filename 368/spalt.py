from labtools.defaults import *
from fuckoff import carr
from matplotlib import rcParams

def spalt(preview, data=None):
    D, f, xm, m = unpack_data(data['spalt'], ('D', 'dD'), ('f', 'df'), ('xm', 'dx'), 'm')

#    zero = np.sum(xm[np.abs(m) == 1]) / 2
    zero = np.sum((xm[:5] + xm[5:]) / 2) / 5
    xm = xm - zero

    alpha = np.arctan(xm / f)

    table = {
        'm': np.abs(m),
        r'x_m [mm]': xm,
        r'\alpha': alpha
    }
    write_printable(table, 'results/b.csv')

    line = lambda x, a, b: x * a + b
    fit, params = fit_func(line, m, xm)

    l1 = params[0] * D / f

    note_var('a', params[0])
    note_var('b', params[1])
    note_var('l1', l1)
    rcParams.update({"text.usetex": False})
    plot = Plot('m', r'$x_m [mm]$')
    plot.title = 'Lage der Beugungsminima'
    plot.add_element(m, xm, label='Lage der Minima', color=carr[0])
    plot.add_element(fit, label='Gradenfit', color=carr[1])
    plot.finish(preview, 'results/spalt.png')


def d0(preview, data=None):
    b, g, B = unpack_data(data['d0'], ('b', 'db'), ('g', 'dg'), ('B', 'dB'))
    note_var('G', g * B / b)
