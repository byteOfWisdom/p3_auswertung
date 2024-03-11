from labtools.defaults import *

def quarz(preview, data_file=None):
    wl, angle_series, dangle, polarizer = unpack_data(data_file['quarz'], 
        'wavelength', 'angles', 'dangle', 'polarizer')

    #mod_plot_num()
    angles = []
    for series in angle_series:
        series = series - polarizer
        angles.append(sum(ev(series, dangle)) / len(series))

    angles = np.array(angles)
    #angles = np.radians(angles)

    mod_angles = []
    for series in angle_series:
        series = series - 90
        mod_angles.append(sum(ev(series, dangle)) / len(series))

    mod_angles = np.array(mod_angles)

    write_printable(
        {r'\frac{1}{\lambda} [nm^{-2}]': 1 / sq(wl), 
        r'\varphi': angles, 
        r"\varphi' (\varphi_0 = 90^{\circ})": mod_angles,
        }, 
        'results/quarz.csv')

    biot = lambda x, a, b: a + b * x
    biot_plot, params = fit_func(biot, 1 / sq(wl), angles)

    note_var('A', params[0])
    note_var('B', params[1])

    alpha = lambda x: (params[0] / 4) + (params[1] / (4 * sq(x)))

    note_var('alpha(410.2nm)', alpha(410.2))
    note_var('alpha(589.3.2nm)', alpha(589.3))
    note_var('alpha(728.1nm)', alpha(728.1))

    plot = Plot(r'$\frac{1}{\lambda^2}$ $[nm^{-2}]$', r'Drehvermögen [grad]')
    plot.title = 'Drehvermögen von quarz'
    plot.add_element(1 / sq(wl), angles, 'Messwerte')
    plot.add_element(biot_plot, 'Fit-Grade')
    plot.finish(preview, 'results/quarz')