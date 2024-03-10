#!python3
import labtools
from labtools.defaults import *

def arc_angle(offset):
    offset = offset * 1e-3
    d = np.array([3.0, 2.0, 1.0, 0.6]) * 1e-3 # convert to meter
    b = np.array([74.0, 70.0, 58.0, 41.0]) * 1e-3 # convert to meter
    b = ev(b, 1e-3) # iirc war das die kleinste schrittgroesse

    dwand = ev(6750.0, 20.0) * 1e-3 # convert to meter
    segmente = 36

    #offset = ev(76.0, 0.0) * 1e-3 # convert to meter
    r = (-1 * b) + offset
    arc = r * 2 * np.pi / segmente
    alpha = arc / dwand

    return alpha

def task():
    #_ = list(map(print, arc_angle(76)))

    table = {
        r'Blendendurchmesser [mm]': [3.0, 2.0, 1.0, 0.6],
        r'\alpha (79mm)': arc_angle(79),
        r'\alpha (84mm)': arc_angle(84),
        r'\alpha (89mm)': arc_angle(89),
        r'\alpha (94mm)': arc_angle(94),
    }

    alpha = arc_angle(84)
    d = np.array([3.0, 2.0, 1.0, 0.6]) * 1e-3 # convert to meter

    p = Plot()
    p.title = r'Effektive Wellenlänge'
    x = 1 / d
    p1 = p.add_element(x, alpha, 'Messpunkte')
    p.ylabel = r"$\alpha$ [rad]"
    p.xlabel = r"$\frac{1}{D}$ $[m^{-1}]$"
    m, n, dm, dn = p.linear_fit(p1)
    m = ev(m, dm)
    n = ev(n, dn)
    print(m)
    print(n)
    p.add_element(lambda x: m.value * x + n.value, 'Gradenfit')
    p.finish(False, 'results/lambda.png')

    print(m / 1.22)

    write_printable(table, 'results/winkel.csv')
    labtools.easyparse.merge_all()

def main():
    task()

if __name__ == '__main__':
    main()