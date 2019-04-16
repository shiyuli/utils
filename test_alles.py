# encoding: utf-8
# using Python 3.7

"""
@repo git.lishiyu.com/utils
@author lishiyu

@purpose
Test all python scripts, and replace os.system('pause') with print('pause') for CI reason.

@references
https://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
"""

from tempfile import mkstemp
from shutil import move, rmtree
from os import fdopen, getcwd, mkdir, chdir
from os.path import exists, join
from subprocess import Popen, PIPE

test_config = 'test.config'
test_dir = 'test'
replace_target_old = 'os.system(\'pause\')'
replace_target_new = 'print(\'pause\')'

def main():
    test_all()
    clean()

def test_all():
    global test_config, test_dir
    if not exists(test_dir):
        mkdir(test_dir)

    with open(test_config, 'r') as config_file:
        for script_name in config_file.readlines():
            script_name = script_name.replace('\n', '')
            print('testing', script_name)
            replace_pause(script_name)
            if test_one(script_name):
                print('pass')
            else:
                print('fail')

def test_one(filename):
    chdir(get_test_path())

    cmd = 'python ' + filename
    process = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    chdir('../')

    # when stderr is empty, return value is True, else False
    return not stderr

def clean():
    # remove test dir
    rmtree(get_test_path())

def replace_pause(filename):
    global replace_target_old, replace_target_new

    # create a temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(filename, 'r') as old_file:
            for line in old_file.readlines():
                if is_pause(line):
                    new_file.write(line.replace(replace_target_old, replace_target_new))
                else:
                    new_file.write(line)

    # move new file
    move(abs_path, join(get_test_path(), filename))

def is_pause(target):
    global replace_target_old
    return replace_target_old in target

def get_test_path():
    global test_dir
    return join(getcwd(), test_dir)

if __name__ == '__main__':
    main()
