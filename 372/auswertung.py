#!python3

import labtools as tools
import response
import leslie
import temperature
import distance

def main():
    tasks = {
        'a': response.response_time,
        'b': leslie.leslie_cube,
        'c': distance.distance_curve,
        'd': temperature.temp_relation,
    }

    preview = tools.task_list.run_task_list(tasks)

    if not preview:
        tools.notes.write_notes('results/notes.txt')
    else:
        tools.notes.print_notes()

    tools.easyparse.merge_all()


if __name__ == '__main__':
    main()