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

from typing import Tuple
from tempfile import mkstemp
from shutil import move, rmtree
from os import fdopen, getcwd, mkdir, chdir
from os.path import exists, join
from subprocess import Popen, PIPE

from core.types import Line, Stream

test_config: str = 'test.config'
test_dir: str = '.test'
replace_target_old: str = 'os.system(\'pause\')'
replace_target_new: str = 'print(\'pause\')'

"""
test all scripts
"""
def test_all() -> None:
    global test_config, test_dir

    with open(test_config, 'r') as config_file:
        for filename in config_file.readlines():
            filename = filename.replace('\n', '')

            if test_one(filename):
                print('pass')
            else:
                print('fail')

"""
test one script
"""
def test_one(filename: str) -> bool:
    test_filename = make_copy(filename)
    print('testing', test_filename)

    data: Stream = Stream(test_filename)
    replace_pause(data)
    data.save()

    chdir(get_test_path())

    cmd = f'python -m py_compile {test_filename}'
    # cmd_run = f'python {test_filename}'

    _, err = run(cmd)

    # when stderr is empty, return value is True, else False
    result: bool = not err
    if not result:
        print(err)

    chdir('../')
    return result

def run(cmd: str) -> Tuple[str, str]:
    process = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
    return process.communicate()

"""
make a copy of origin file, stored in test dir
"""
def make_copy(filename: str) -> str:
    # create a temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(filename, 'r') as old_file:
            new_file.writelines(old_file.readlines())

    pure_filename, path = parse_filename(filename)
    test_filename: str = get_test_file(pure_filename)

    # move new file
    move(abs_path, test_filename)

    return test_filename

"""
clean test dir
"""
def clean() -> None:
    # remove test dir
    rmtree(get_test_path())

"""
replace pause segment
"""
def replace_pause(data: Stream) -> None:
    global replace_target_old, replace_target_new

    for line in data.raw.raw:
        if is_pause(line.raw):
            line.replace(line.raw.replace(replace_target_old, replace_target_new))

"""
check if the target include pause segment
"""
def is_pause(target: str) -> bool:
    global replace_target_old
    return replace_target_old in target

"""
get test file in test dir
"""
def get_test_file(filename: str) -> str:
    return join(get_test_path(), filename)

"""
get test dir path
"""
def get_test_path() -> str:
    global test_dir

    test_path: str = join(getcwd(), test_dir)
    if not exists(test_path):
        mkdir(test_path)

    return test_path

"""
separate filename into pure filename and its path
"""
def parse_filename(filename: str) -> Tuple[str, str]:
    index: int = filename.rfind('/')
    if index is -1:
        return filename, ''

    path: str = filename[:index]
    filename = filename[index+1:]

    return filename, path

def main() -> None:
    test_all()
    clean()

if __name__ == '__main__':
    main()
