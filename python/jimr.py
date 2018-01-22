#! /usr/bin/env python3

import json
import sys

# print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# view dict as object
class objectview_recursive(object):
    def __init__(self, d):
        self.__dict__ = d
        for k in self.__dict__:
            if isinstance(self.__dict__[k], dict):
                self.__dict__[k] = objectview(self.__dict__[k])

# load json, return objectview
def jsonget(fspec):
    with open(fspec) as f:
        obj = objectview(json.load(f))
    return obj

# Given objectview, save json
def jsonput(obj, fspec):
    with open(fspec, 'w') as f:
        json.dump(obj.__dict__, f)

