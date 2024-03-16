from labtools.defaults import *
import background

def convert_to_power(U):
    return U / 2.7

def temp_relation(preview, data_file=None):
    Il, Ul, U, R0, T0 = unpack_data(data_file['temperature'],
        ('Il', 'dIl'), ('Ul', 'dUl'), ('U', 'dU'), ('R0', 'dR0'), ('T0', 'dT'))

    correction = background.get_interpolation(data_file, 3, 4, len(U))
    U = U - correction
    P = convert_to_power(U)
    R = Ul / Il

    T0 += 271.15

    alpha = 4.82e-3
    beta = 6.76e-7

    p = (alpha / beta)
    q = ((1 / beta) - (R / (beta * R0)))


    T = T0 - (p / 2) + np.sqrt(sq(p / 2) - q)

    T = T[2:]
    P = P[2:]

    line = lambda x, a, b: a * x + b

    xs = np.log(T)
    ys = np.log(P)

    f, params = fit_func(line, xs, ys)

    note_var('a', params[0])
    note_var('b', params[1])

    sigma = 5.6704e-8
    epsilon = np.exp(params[1].value) / sigma

    note_var('epsilon', epsilon)

    plot = Plot(r'ln(T) [ln[K]]', r'$ln(\frac{\Phi}{A}) [ln(\frac{W}{m^2})]$')
    plot.title = 'Logarithmische Darstellung der Temperatur und Strahlungsleistung'
    plot.add_element(xs, ys, 'Messdaten')
    plot.add_element(f, 'gradenfit')
    plot.finish(preview, 'results/temp.png')

    table = {
        'U_l [V]': Ul,
        'I_l [A]': Il,
        r'R [\Omega]': R,
    }

    table_2 = {
        r'T [K]': T,
        r'\frac{\Phi}{A} [\frac{W}{m^2}]': P,
        r'ln(T) [ln[K]]': xs, 
        r'ln(\frac{\Phi}{A}) [ln(\frac{W}{m^2})]': ys
    }

    write_printable(table, 'results/temperature_1.csv')
    write_printable(table_2, 'results/temperature_2.csv')