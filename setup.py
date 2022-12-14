import sys
import os
import subprocess

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

def ccmd():
    subprocess.run(["make", "clean"], cwd=(os.getcwd() + '/src/gym_duckietown/decision_logic'))
    subprocess.run(["make", "all"], cwd=(os.getcwd() + '/src/gym_duckietown/decision_logic'))

class CustomInstall(install):
    def run(self):
        install.run(self)
        ccmd()

class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        ccmd()

class CustomEggInfo(egg_info):
    def run(self):
        egg_info.run(self)
        ccmd()

    
def get_version(filename):
    import ast

    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith("__version__"):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError("No version found in %r." % filename)
    if version is None:
        raise ValueError(filename)
    return version


version = get_version(filename="src/gym_duckietown/__init__.py")

line = "daffy"

install_requires = [
    "gym>=0.17.1",
    "numpy>=1.10.0",
    "pyglet==1.5.11",
    "pyzmq>=16.0.0",
    "opencv-python>=3.4",
    "pyyaml>=3.11",
    f"duckietown-world-{line}",
    "PyGeometry-z6",
    "carnivalmirror==0.6.2",
    "zuper-commons-z6",
    "typing-extensions",
    "Pillow",
    "torch",
    "flask",
    "gevent",
    "eventlet",
    "flask_socketio",
    "torchvision",
    "tensorboard",
    "python-socketio[client]",
]

system_version = tuple(sys.version_info)[:3]

if system_version < (3, 7):
    install_requires.append("dataclasses")


setup(
    name=f"duckietown-gym-{line}",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    version=version,
    keywords="duckietown, environment, agent, rl, openaigym, openai-gym, gym",
    include_package_data=True,
    install_requires=install_requires,
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
        'egg_info': CustomEggInfo,
    },
    entry_points={
        "console_scripts": [
            "dt-check-gpu=gym_duckietown.check_hw:main",
        ],
    },
)
