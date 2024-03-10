#!python3

import labtools as tools
import abbe
import projector

def main():
    tasks = {
        'a': abbe.abbe,
        'b': projector.ausleuchtung_1,
        'c': projector.massstab,
    }

    preview = tools.task_list.run_task_list(tasks)

    if not preview:
        tools.notes.write_notes('results/notes.txt')
    else:
        tools.notes.print_notes()

    tools.easyparse.merge_all()


if __name__ == '__main__':
    main()