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

    preview = tools.task_list.run_task_list(tasks)

    if not preview:
        tools.defaults.write_notes('results/notes.txt')
    else:
        tools.defaults.print_notes()

    tools.easyparse.merge_all()


if __name__ == '__main__':
    main()
