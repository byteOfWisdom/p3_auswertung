from labtools import *
import background

def response_time(preview, data_file=None):
    U = unpack_data(data_file['kalibration'], ('U', 'dU'))[0]

    correction = background.get_interpolation(data_file, 0, 1, len(U))
    U = U# - correction

    note_var('U0', background.get_background(data_file, 0))
    note_var('U1', background.get_background(data_file, 1))
    note_var('U2', background.get_background(data_file, 2))
    note_var('U3', background.get_background(data_file, 3))
    note_var('U4', background.get_background(data_file, 4))

    time = np.array(range(1, U.size + 1)) * 10

    plot = Plot('Zeit [s]', 'Spannung [mV]')
    plot.title = 'Ansprechzeit'
    data = plot.add_element(time, U, 'Messwerte')
    plot.mark_y(58.5, '90% des Maximalwertes')
    plot.mark_x(75)
    plot.finish(preview, 'results/response.png')