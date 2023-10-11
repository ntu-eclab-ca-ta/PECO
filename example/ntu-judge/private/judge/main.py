import argparse
import os

import process

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src', type=str, required=True)
    parser.add_argument('-d', '--dst', type=str, default='./')
    parser.add_argument('--rename', action='store_true')
    parser.add_argument('--decompress', action='store_true')
    parser.add_argument('--judge', action='store_true')
    parser.add_argument('--case', type=str, default='')
    args = parser.parse_args()

    if os.path.isdir(args.src) and args.rename:
        filename = process.reformat_folder(args.src)
    elif os.path.isfile(args.src) and args.decompress:
        filename = process.decompress_file(args.src)
    elif os.path.isfile(args.src) and args.judge != "":
        process.judge(args.src, args.dst, args.case)