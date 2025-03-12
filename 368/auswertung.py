#!python3

import labtools as tools
import spalt
import gitter
from matplotlib import rc
from matplotlib import pyplot as plt

def main():
    tasks = {
        'a': spalt.spalt,
        'b': spalt.d0,
        'c': gitter.konstante,
        'd': gitter.blue_line,
        'e': gitter.resolution,
    }

#    plt.xkcd()
#    rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#    rc('font',**{'family':'serif','serif':['Times']})
#    rc('font', **{'family':'fantasy','fantasy':['xkcd script']})
    rc('text', usetex=True)
#    plt.rcParams['font.family'] = 'fantasy'
#    plt.rcParams['font.fantasy'] = 'xkcd script'
    plt.rcParams['text.latex.preamble'] = r'\usepackage{comicsans}'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Comic Sans MS'
#    plt.rcParams['text.usetex'] = True

    preview = tools.task_list.run_task_list(tasks)

    if not preview:
        tools.defaults.write_notes('results/notes.txt')
    else:
        tools.defaults.print_notes()

    tools.easyparse.merge_all()


if __name__ == '__main__':
    main()
