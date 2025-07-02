import os
import subprocess
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

class MakeLibCommand(build_ext):
    def run(self):
        subprocess.check_call(["make", "libtof"], cwd="STSW-IMG013/user_lib", env=os.environ)
        os.makedirs("vl53l1", exist_ok=True)
        self.copy_file("STSW-IMG013/libtof.so", "tof/libtof.so")
        super().run()

setup(
    name="vl53l1",
    version="0.1.0",
    packages=["vl53l1"],
    cmdclass={"build_ext": MakeLibCommand},
)
