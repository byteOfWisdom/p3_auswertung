from labtools.defaults import *

def power_curve(preview, data_file=None):
    p_angle, a_angle, voltage, U_dark = unpack_data(data_file['malus'], 
        'pangle', 'angles', ('voltages', 'dU'), 'U_dark')

    voltage = voltage - U_dark

    angle = []
    for p in p_angle:
        for a in a_angle:
            angle.append(p - a)
    angle = np.array(angle)
    angle = np.radians(angle)

    write_printable({
        r'\varphi - \varphi_0': np.round(angle, 2),
        r'U [V]': voltage,
        }, 'results/malus.csv')

    I = lambda x, I0, phi_0, offset: I0 * sq(np.cos(x - phi_0)) + offset

    f, params = fit_func(I, angle, voltage)

    note_var('I0', params[0])
    note_var('phi_0', params[1])
    note_var('offset', params[2])

    U_max = max(voltage)
    U_min = min(voltage)

    PG = (U_max - U_min) / (U_max + U_min)
    note_var('U_max', U_max)
    note_var('U_min', U_min)
    note_var('PG', PG)

    plot = Plot(r'$\varphi - \varphi_0$ [rad]', 'Intensität [V]')
    plot.title = 'Malussches Gesetz'
    plot.add_element(angle, voltage, 'Messdaten')
    plot.add_element(f, 'Kurvenfit')

    plot.finish(preview, 'results/malus.png')