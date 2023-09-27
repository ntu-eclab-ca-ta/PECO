import os
import re
import more_itertools

import variable

class IndexedFile:
    def __init__(self, index, name):
        self.index = index
        self.name = name

    def __lt__(self, other):
        return self.index < other.index

class FileMiss(Exception):
    def __init__(self, format_type, index):
        super().__init__(f'File in "{format_type}" type with index "{index}" is missing')

def build_tasks(files_info):
    keys = list(files_info.keys())
    indices = [file.index for file in files_info[keys[0]]] if len(keys) > 0 else []
    tasks = []

    for i, index in enumerate(indices):
        tasks.append((index, {key: files_info[key][i].name for key in keys}))

    return tasks

def check_tasks(files_info):
    keys = list(files_info.keys())

    # If there is only one type of file, we don't need to check
    if len(keys) < 2:
        return

    files_mx_cnt = max([len(files_info[key]) for key in keys])

    # Check that every type of file has the same index
    for i in range(files_mx_cnt):
        for (pre, cur) in list(more_itertools.windowed(keys, 2)):
            if files_info[pre][i].index < files_info[cur][i].index:
                raise FileMiss(cur, files_info[pre][i].index)
            elif files_info[pre][i].index > files_info[cur][i].index:
                raise FileMiss(pre, files_info[cur][i].index)

def list_tasks(config):
    tasks = config['tasks']
    tasks_path = config['root'] + '/' + variable.solve_string(config, tasks['path'])
    tasks_format = tasks['format']

    files_path = list_files_recursively(tasks_path)
    files_info = {}
    for format_type in tasks_format:
        if format_type == 'index':
            continue
        format_re = variable.solve_string(config, tasks_format[format_type], prefix='(', postfix=')')
        # In some cases, the format is representing a directory rather than a file
        # Add the '$' to the end of the format to make sure there is no postfix after the format
        # Otherwise, the format might mathes the files within the directory
        format_re = f'{format_re}$'
        format_list = list_matched_files(files_path, format_re)
        files_info[format_type] = sorted(format_list)

    check_tasks(files_info)
    return build_tasks(files_info)

def list_files_recursively(path):
    result = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            result.append(dir_path)
        for file in files:
            file_path = os.path.join(root, file)
            result.append(file_path)
    return result

def list_matched_files(files, format):
    # Filter the files
    format = re.compile(format)
    indexed_files = [(file, format.findall(file)) for file in files]
    # Since we have '$' at the end of the format, the format should be unique. So the matched index should be either [] or [index]
    return [IndexedFile(index[0], file) for file, index in indexed_files if index != []]