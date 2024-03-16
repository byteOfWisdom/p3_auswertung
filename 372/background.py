from labtools.defaults import *

def get_background(data_file, bg_index):
    U_n = unpack_data(data_file['background'], 
        ('U'+str(bg_index), 'dU'))[0]

    return np.sum(U_n) / U_n.size


def get_interpolation(data_file, bg_1, bg_2, num_data):
    return np.interp(
        list(range(1, num_data + 1)), 
        [0, num_data + 1],
        [float(get_background(data_file, bg_1)), float(get_background(data_file, bg_2))])