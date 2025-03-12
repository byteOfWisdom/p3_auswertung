#!python3

from labtools import *
import response
import leslie
import temperature
import distance

from matplotlib import pyplot as plt

def main():
    tasks = {
        'a': response.response_time,
        'b': leslie.leslie_cube,
        'c': distance.distance_curve,
        'd': temperature.temp_relation,
    }

    preview = run_task_list(tasks)

    if not preview:
        write_notes('results/notes.txt')
    else:
        print_notes()

    merge_all()


if __name__ == '__main__':
    main()