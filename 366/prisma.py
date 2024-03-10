from labtools.defaults import *
import scipy
from kafe2 import XYContainer, Fit, ContoursProfiler



y = lambda x: x
gamma = 1.0


def convert(deg, arc_min, zero, error):
    a = deg + arc_min / 60
    a += zero
    if (np.max(a) > 180.0):
        a = 360 - a

    a = ev(a, error / 60)

    rad_a = a * np.pi / 180

    return a, rad_a



def calibration(preview, data_file=None):
    zero = unpack_data(data_file['calibration'], 'zero')[0]
    a1, a1_min, a2, a2_min, da = unpack_data(
        data_file['calibration'], 
        'a1', 'a1_min', 'a2', 'a2_min', 'da')

    a1 = ev((a1 + zero + a1_min / 60), da / 60)
    a2 = ev((a2 + zero + a2_min / 60), da / 60)

    a2 = a2 - 360

    global gamma
    gamma = 0.5 * (a1 - a2)
    note_var('gamma', gamma)


def hg_cd_curve(preview, data_file=None):
    deg_data, min_data, dangle = unpack_data(
        data_file['baseline'], 
        'deg', 'minutes', 'dangle')
    zero = data_file['calibration']['zero']

    hg, cd = unpack_data(data_file['reference'], 'hg', 'cd')
    reference = np.flip(np.sort(np.append(hg, cd))) # sort from red to blue

    _, delta = convert(deg_data, min_data, zero, dangle)

    global gamma
    rad_gamma = gamma.value * np.pi / 180


    fit_func = lambda x, k0, k1: np.sqrt(k1 / ( (np.sin((x + rad_gamma) / 2) / np.sin(rad_gamma / 2)) - k0))
    res, cov = scipy.optimize.curve_fit(fit_func, delta, reference)
    err = np.sqrt(np.diag(cov))

    k0 = ev(res[0], err[0])
    k1 = ev(res[1], err[1])
    note_var('k0', k0.value)
    note_var('dk0', k0.error)
    note_var('k1', k1)

    fit = Fit(data=[delta, reference], model_function=fit_func)


    fit.add_error(axis='x', err_val=error(delta))  # add the x-error to the fit
    fit.add_error(axis='y', err_val=0)  # add the y-errors to the fit
    fit.do_fit()
#    fit.report()

    res = fit.parameter_values
    errs = fit.parameter_errors

    global y
    y = lambda x: fit_func(x, *res)

    plot = Plot(r'$\delta$ [rad]', r'$\lambda$ [nm]')
    plot.title = 'Kurvenfit'
    calibration_curve = plot.add_element(delta, reference, 'gemessenes Spektrum')
    plot.add_element(y, 'fit')
    plot.finish(preview, 'results/plot.png')

    spec_bad = Plot(r'$\lambda$ [nm]', '')
    spec_bad.title = "Repliziertes Spektrum der Hg-Cd Lampe"
    spec_bad.add_element('spectrum', y(delta))
    spec_bad.finish(preview, 'results/fit_spectrum.png')

    table = {
        r'\delta [rad]': np.round(value(delta), 3),
        r'\Delta\delta [rad]': np.round(error(delta), 3),
        r'\lambda [nm]': y(delta),
    }
    write_printable(table, 'results/repliziertes_hg_cd_spektrum.csv', 3)


def detect_element(preview, data_file=None):
    deg_data, min_data, dangle = unpack_data(
        data_file['measurement'], 
        'deg', 'minutes', 'dangle')
    zero = data_file['calibration']['zero']

    w_deg_data, w_min_data, w_dangle = unpack_data(
        data_file['measurement'], 
        'weak_deg', 'weak_min', 'dangle')


    a, delta = convert(deg_data, min_data, zero, dangle)
    w_a, w_delta = convert(w_deg_data, w_min_data, zero, dangle)


    plot = Plot(r'$\lambda$', '')

    plot.add_element('spectrum', y(delta))
    plot.add_element('spectrum_w', y(w_delta))
    plot.title = 'Unbekanntes Element'
    plot.finish(preview, 'results/unknown_spectrum.png')

    table = {
        r'\delta [rad]': np.round(value(delta), 3),
        r'\Delta\delta [rad]': np.round(error(delta), 3),
        r'\lambda [nm]': y(delta),
    }
    write_printable(table, 'results/unbekanntes_element.csv', 3)

    table = {
        r'\delta [rad]': np.round(value(w_delta), 3),
        r'\Delta\delta [rad]': np.round(error(w_delta), 3),
        r'\lambda [nm]': y(w_delta),
    }
    write_printable(table, 'results/unbekanntes_element_schwach.csv', 3)



def task_e(preview, data_file=None):
    deg_data, min_data, dangle = unpack_data(
        data_file['baseline'], 
        'deg', 'minutes', 'dangle')
    zero = data_file['calibration']['zero']

    hg, cd = unpack_data(data_file['reference'], 'hg', 'cd')
    reference = np.flip(np.sort(np.append(hg, cd))) # sort from red to blue

    a, delta = convert(deg_data, min_data, zero, dangle)

    global gamma
    rad_gamma = gamma.value * np.pi / 180

    n = np.sin((delta + rad_gamma) / 2) / np.sin(rad_gamma / 2)

    lambda_sq = 1 / (reference ** 2)

    plot = Plot( r'$\frac{1}{\lambda^2}$ $[nm^{-2}]$', 'n')
    p1 = plot.add_element( lambda_sq, n, 'Berechnete n')
    k0, k1, dk0, dk1 = plot.linear_fit(p1)
    note_var('k0', ev(k0, dk0))
    note_var('k1', k1)
    note_var('dk1', dk1)
    plot.add_element(lambda x: x * k0 + k1, 'fit')
    plot.title = 'Brechungsindex'
    plot.finish(preview, 'results/plot_e.png')

    table = {
        r'\lambda [nm]': reference,
        r'\frac{1}{\lambda^2} [nm^{-2}]': np.round(lambda_sq, 8),
        'n': n,
    }

    write_printable(table, 'results/task_e.csv')


def misc_spectra(preview, data_file=None):
    hg, cd = unpack_data(data_file['reference'], 'hg', 'cd')
    reference = np.flip(np.sort(np.append(hg, cd))) # sort from red to blue

    spec = Plot(r'$\lambda$ [nm]', '')
    spec.title = "Referenz-Spektrum der Hg-Cd Lampe"
    spec.add_element('spectrum', reference)
    spec.finish(preview, 'results/hg_cd_spectrum.png')
    
    spec = Plot(r'$\lambda$ [nm]', '')
    spec.title = "Zink Spektrum"
    zn, zn_w = unpack_data(data_file['reference'], 'Zn', 'Zn_weak')
    spec.add_element('spectrum', zn)
    spec.add_element('spectrum_w', zn_w)
    spec.finish(preview, 'results/zink.png')

    spec = Plot(r'$\lambda$ [nm]', '')
    spec.title = "Cadmium Spektrum"
    cd, cd_w = unpack_data(data_file['reference'], 'cd', 'cd_weak')
    spec.add_element('spectrum', cd)
    spec.add_element('spectrum_w', cd_w)
    spec.finish(preview, 'results/cd_spectrum.png')


def A(wl):
#    wl *= 1e-9
    gamma = ev(60.04, 0.06)
    delta = ev(0.852, 0.001)
    d0 = ev(11 * 1e3, 1e3)
    k1 = ev(123.4e2, 5.6e2)# * 1e-18
    k1_ = ev(109.0e2, 1.7e2)# * 1e-18

    rad_gamma = gamma * np.pi / 180
    b = (2 * np.sin(rad_gamma / 2) * d0) / np.cos((rad_gamma + delta) / 2)
    temp = 2 * b / (wl ** 3)
    return temp * k1, temp * k1_



def resolution(preview, data_file=None):
    note_var('A(400)', A(400)[0].value)
    note_var('dA(400)', A(400)[0].error)
    note_var('A(500)', A(500)[0].value)
    note_var('dA(500)', A(500)[0].error)
    note_var('A(600)', A(600)[0].value)
    note_var('dA(600)', A(600)[0].error)

    note_var('A(400)', A(400)[1].value)
    note_var('dA(400)', A(400)[1].error)
    note_var('A(500)', A(500)[1].value)
    note_var('dA(500)', A(500)[1].error)
    note_var('A(600)', A(600)[1].value)
    note_var('dA(600)', A(600)[1].error)

    note_var('delta lambda', 400 / A(400)[0])
    note_var('delta lambda', 500 / A(500)[0])
    note_var('delta lambda', 600 / A(600)[0])
