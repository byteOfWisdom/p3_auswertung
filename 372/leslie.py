from labtools.defaults import *
import background

def convert_to_power(U):
    return U / 2.7

def leslie_cube(preview, data_file=None):
    Um, Up, Ub, Uw = unpack_data(data_file['leslie'],
        ('U_matt', 'dU'), ('U_glanz', 'dU'), ('U_schwarz', 'dU'), ('U_weiss', 'dU'))

    Tm, Tp, Tb, Tw, T0 = unpack_data(data_file['leslie'],
        ('T_matt', 'dT'), ('T_glanz', 'dT'), ('T_schwarz', 'dT'), ('T_weiss', 'dT'), ('T0', 'dT'))

    sigma = 5.6704e-8

    correction = background.get_interpolation(data_file, 1, 2, 10)
    Um = Um - correction
    Up = Up - correction
    Ub = Ub - correction
    Uw = Uw - correction

    Tm += 271.15
    Tp += 271.15
    Tb += 271.15
    Tw += 271.15
    T0 += 271.15

    table_1 = {
        r'T_m [K]': Tm,
        r'U_m [mV]': Um,
        r'T_p [K]': Tp,
        r'U_p [mV]': Up,
    }

    table_2 = {
        r'T_b [K]': Tb,
        r'U_b [mV]': Ub,
        r'T_w [K]': Tw,
        r'U_w [mV]': Uw,
    }
    write_printable(table_1, 'results/leslie1.csv')
    write_printable(table_2, 'results/leslie2.csv')


    line = lambda x, a, b: a * x + b

    fm, params_m = fit_func(line, (Tm ** 4) - (T0 ** 4), convert_to_power(Um), False)
    fb, params_b = fit_func(line, (Tb ** 4) - (T0 ** 4), convert_to_power(Ub), False)
    fw, params_w = fit_func(line, (Tw ** 4) - (T0 ** 4), convert_to_power(Uw), False)
    fp, params_p = fit_func(line, (Tp ** 4) - (T0 ** 4), convert_to_power(Up), False)

    for res in [params_m, params_b, params_w, params_p]:
        note_var('a', res[0])
        note_var('b', res[1])
        note_var('epsilon', res[0] / sigma)

    plot = Plot(r'$T^4 - T_0^4 [K]$', r'$\frac{\Phi}{A}$ $\frac{W}{m^2}$')
    plot.title = 'Leslie Würfel'
    plot.add_element((Tm ** 4) - (T0 ** 4), convert_to_power(Um), 'Messwerte matte Seite', color='firebrick')
    plot.add_element((Tb ** 4) - (T0 ** 4), convert_to_power(Ub), 'Messwerte schwarze Seite', color='teal')
    plot.add_element((Tw ** 4) - (T0 ** 4), convert_to_power(Uw), 'Messwerte weisse Seite', color='plum')
    plot.add_element((Tp ** 4) - (T0 ** 4), convert_to_power(Up), 'Messwerte polierte Seite', color='darkkhaki')

    plot.add_element(fm, label='Fit matte Seite', color='firebrick')
    plot.add_element(fb, label='Fit schwarze Seite', color='teal')
    plot.add_element(fw, label='Fit weisse Seite', color='plum')
    plot.add_element(fp, label='Fit polierte Seite', color='darkkhaki')

    plot.add_element(lambda x: sigma * x, label='Schwarze Koerper', color='black')

    plot.finish(preview, 'results/leslie.png')
