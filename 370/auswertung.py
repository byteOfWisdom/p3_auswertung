#!python3

import labtools as tools
import malus
import concentration
import quarz

def main():
    tasks = {
        'a': malus.power_curve,
        'b': quarz.quarz,
        'c': concentration.concentration,
    }

    preview = tools.task_list.run_task_list(tasks)

    if not preview:
        tools.notes.write_notes('results/notes.txt')
    else:
        tools.notes.print_notes()

    tools.easyparse.merge_all()


if __name__ == '__main__':
    main()