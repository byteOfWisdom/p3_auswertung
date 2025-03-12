#!python3

import labtools as tools
import prisma

def main():
    #tools.defaults.mod_plot_num()
    tasks = {
        'a': prisma.calibration,
        'b': prisma.hg_cd_curve,
        'c': prisma.misc_spectra,
        'd': prisma.detect_element,
        'e': prisma.task_e,
        'f': prisma.resolution,
    }

    preview = tools.task_list.run_task_list(tasks)

    if not preview:
        tools.defaults.write_notes('results/notes.txt')
    else:
        tools.defaults.print_notes()
    tools.defaults.merge_all()



if __name__ == '__main__':
    main()
