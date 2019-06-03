# encoding: utf-8
# using Python 3.7

"""
@repo git.lishiyu.com/utils
@author lishiyu

@usage Put this script into directory that contains files, run it.
       And these files will be named to number+extension_name. (e.g. 0.dcm 1.dcm 2.dcm)
"""

import os
import random

script_name = None

def main():
    rename_random()
    rename_order()
    os.system('pause')

"""
prevent name conflict
"""
def rename_random():
    for file in os.listdir(os.getcwd()):
        if valid_filename(file):
            rename_core(file, str(random.random()))

def rename_order():
    i = 0
    for file in os.listdir(os.getcwd()):
        if valid_filename(file):
            rename_core(file, str(i))
            i += 1

    print('done!')

def rename_core(target, newname):
    exname_index = target.rfind('.')
    exname = target[exname_index:]
    os.rename(target, newname + exname)

def valid_filename(filename):
    global script_name
    if script_name is None:
        script_name = __file__.split('\\')[-1]

    return script_name not in filename

if __name__ == '__main__':
    main()
