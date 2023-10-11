import re
import os
import subprocess

def reformat_folder(path, pattern = '([a-zA-Z0-9]{9})#.*(\..*)'):
    files = os.listdir(path)
    new_filenames = []

    for filename in files:
        new_filename = reformat_file(os.path.join(path, filename), pattern)
        new_filenames.append(new_filename)
    
    return new_filenames

def reformat_file(filename, pattern = '([a-zA-Z0-9]{9})#.*(\..*)'):
    pat = re.compile(pattern)

    match = pat.findall(filename)
    if not os.path.isfile(filename) or len(match) == 0:
        return None
    else:
        path = os.path.split(filename)[0]
        id = match[0][0]           
        ext = match[0][1]
        new_filename = os.path.join(path, f'{id}{ext}')
        os.rename(filename, new_filename)
        return new_filename

def decompress_file(filename, dest='./'):
    if not os.path.isfile(filename):
        return None

    def build_command(command_list, file_name):
        return [c if c is not None else file_name for c in command_list]

    commands = {
        '.zip': ['unzip', None, '-d', dest]
    }

    name, ext = os.path.splitext(filename)
    if ext not in commands.keys():
        return None

    command = build_command(commands[ext], filename)
    ret = subprocess.run(command)

    if ret.returncode != 0:
        return None
    else:
        return name

def judge(filename, dst, case):
    correct = []

    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line == '':
                continue
            _, passed = line.split(':')
            correct.append(passed.strip() == 'Passed')
    
    with open(dst, 'a') as f:
        case = case.split('/')[-1].split('.')[0]
        f.write(f'{case}: {100.0 * sum(correct) / len(correct):.2f}\n')
