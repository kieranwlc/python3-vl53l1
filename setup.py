from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess
import os
import shutil

class CustomBuild(build_py):
    def run(self):
        build_dir = os.path.abspath('STSW-IMG013/user_lib')
        subprocess.check_call(['make', 'libtof'], cwd=build_dir)

        lib_path = os.path.join(build_dir, 'libtof.so')
        target_dir = os.path.join(self.build_lib, 'vl53l1')
        self.mkpath(target_dir)
        shutil.copy2(lib_path, target_dir)

        super().run()

setup(
    name='vl53l1',
    version='0.1',
    packages=find_packages(),
    package_data={
        'vl53l1': ['libtof.so'],
    },
    cmdclass={
        'build_py': CustomBuild,
    },
)
