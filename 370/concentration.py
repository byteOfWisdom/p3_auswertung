from labtools.defaults import *

def concentration(preview, data_file=None):
    conc, angle_series, dangle, unknown, phi_zero = unpack_data(data_file['concentration'], 
        'concentration', 'angles', 'dangle', 'unknown', 'zero')

    angles = []
    for series in angle_series:
        angles.append(sum(ev(series, dangle) - phi_zero) / len(series))

    angles = np.array(angles)
    #angles = np.radians(angles)

    write_printable({
        r'C [\frac{mol}{l}]': conc,
        r'\delta\varphi': angles,
        },'results/concentration.csv')

    unknown = (sum(unknown - phi_zero) / len(unknown))

    linear = lambda x, a, b: a * x + b
    calib, params = fit_func(linear, conc, angles)

    note_var('a', params[0])
    note_var('b', params[1])
    c_calc = (unknown - params[1]) / params[0]
    note_var('c', c_calc)


    plot = Plot(r'Konzentration $\frac{mol}{l}$', r'Drehwinkel [rad]')
    plot.title = 'Drehwinkel von Zuckerlösungen'
    plot.add_element(conc, angles, 'Messwerte')
    lin = plot.add_element(calib, 'Fit Grade')
    plot.mark_intersect(lin, unknown, 'unbekannte Loesung')
    plot.mark_y(unknown)
    plot.finish(preview, 'results/concentration.png')