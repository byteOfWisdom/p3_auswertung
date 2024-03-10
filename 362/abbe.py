from labtools.defaults import *

def abbe(preview, data_file=None):
    s, pg, pb, G, B = unpack_data(
        data_file['abbe'],
        ('s', 'ds'),
        ('pg', 'dp'),
        ('pb', 'dp'),
        ('G', 'dG'),
        ('B', 'dB')
    )

    s = np.full(len(list(pb)), s)

    xb = pb - s
    xg = s - pg
    gamma = B / G

    fit_g, params_g = fit_func(lambda x, a, b: a * x + b, 1 + 1 / gamma, xg)
    fit_b, params_b = fit_func(lambda x, a, b: a * x + b, 1 + gamma, xb)

    plot = Plot(r'$(1 + \frac{1}{\gamma})$', r'$x_g [cm]$')
    plot.title = 'Gegenstandsseite Abbe-Verfahren'
    plot.add_element(1 + 1 / gamma, xg, r'Messungen')
    plot.add_element(fit_g, 'Gradenfit')
    plot.finish(preview, 'results/abbe_full.png')


    plot = Plot(r'$(1 + \frac{1}{\gamma})$', r'$x_b [cm]$')
    plot.title = 'Bildseite Abbe-Verfahren'
    plot.add_element(1 + gamma, xb, r'Messungen')
    plot.add_element(fit_b, 'Gradenfit')
    plot.finish(preview, 'results/abbe_gegenstandsseite.png')

    note_var('f_b', params_b[0])
    note_var('h_b', params_b[1])
    note_var('f_g', params_g[0])
    note_var('h_g', params_g[1])

    table = {
        r'x [cm]': xb,
        r"x' [cm]": xg,
        r'\gamma': gamma
    }

    write_printable(table, 'results/abbe.csv')