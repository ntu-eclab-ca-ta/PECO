import argparse

from process import process_tasks
from report import report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # the argument "config", or short in "c", is the path of the config file, the config file is a yaml file
    parser.add_argument('-c', '--config', help='the path of the config file', required=True, type=str)

    # the argument "quiet", or short in "q", is a flag, if it is set, the report will not contain the log of the commands and without colors
    parser.add_argument('-q', '--quiet', help='quiet mode, do not print the log of the commands', action='store_true', default=False)

    parser.add_argument('-d', '--dict', help='report as a dict', action='store_true', default=False)

    args = parser.parse_args()

    results = process_tasks(args.config)

    if args.dict:
        print(results)
    else:
        print(report(results, verbose = not args.quiet))

    all_clear = all(value is None for value in results.values())
    exit_code = 0 if all_clear else 1
    exit(exit_code)