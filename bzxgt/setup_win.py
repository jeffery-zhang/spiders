import os
import sys
from cx_Freeze import setup, Executable

sys.path.append(os.path.abspath('./'))

# 目标文件
target_file = 'bzxgt/main.py'

build_exe_options = {
  'packages': ['os', 'sys', 'requests', 'bs4', 'threading', 'shutil', 'time', 'utils'],
  'include_files': [],
}

base = None

# 打包成exe
setup(name='MyScript',
    version='0.1',
    description='MyScript',
    options = {'build_exe': build_exe_options},
    executables = [Executable(target_name='main.exe', base=base, script=target_file)])