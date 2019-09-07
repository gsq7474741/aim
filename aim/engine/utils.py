import os
from copy import deepcopy
from functools import reduce


def deep_merge(*dicts, update=False):
    """
    Merges dicts deeply
    """
    def merge_into(d1, d2):
        for key in d2:
            if key not in d1 or not isinstance(d1[key], dict):
                d1[key] = deepcopy(d2[key])
            else:
                d1[key] = merge_into(d1[key], d2[key])
        return d1

    if update:
        return reduce(merge_into, dicts[1:], dicts[0])
    else:
        return reduce(merge_into, dicts, {})


def is_path_creatable(path):
    """
    `True` if current user has sufficient permissions to create the passed
    path
    `False` otherwise.
    """
    dir_name = os.path.dirname(path)
    return os.access(dir_name, os.W_OK)


def ls_dir(paths):
    """
    List the files in directories
    """
    if len(paths) == 0:
        return []

    if os.path.isdir(paths[0]):
        ls_head = [os.path.join(paths[0], i) for i in os.listdir(paths[0])]
        return ls_dir(ls_head + (paths[1:] if len(paths) > 1 else []))
    else:
        return [paths[0]] + (ls_dir(paths[1:]) if len(paths) > 1 else [])
