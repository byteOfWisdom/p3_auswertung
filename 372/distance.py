from labtools.defaults import *
import background

def convert_to_power(U):
    return U / 2.7

def distance_curve(preview, data_file=None):
    s, x, U = unpack_data(data_file['distance'],
        's', ('x', 'dx'), ('U', 'dU'))

    r = s - x
    r *= 1e-3

    P = convert_to_power(U)

    poly = lambda x, a, b, c: (a / sq(x)) + (b / x)+ c
    f, params = fit_func(poly, r, P)

    note_var('a', params[0])
    note_var('b', params[1])
    note_var('c', params[2])

    plot = Plot(r'r [mm]', r'$\frac{\Phi}{A} [\frac{W}{m^2}]$')
    plot.title = 'Leistung gegen Abstand'
    plot.add_element(r, P, 'Daten')
    plot.add_element(f, 'Fit')
    plot.finish(preview, 'results/distance.png')

    table = {
        r'r [mm]': r,
        r'\frac{\Phi}{A} [\frac{W}{m^2}]': P,
    }

    write_printable(table, 'results/distance.csv')