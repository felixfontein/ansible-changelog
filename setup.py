"""File Tree Subs"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ansible-changelog',
    version='0.0.1',
    description='Synchronize a file tree with text file substitutions',
    long_description=long_description,
    url='https://github.com/felixfontein/ansible-changlog',
    license='GPLv3+',
    author='Ansible Project',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='ansible changelog',
    packages=find_packages(),
    install_requires=['ansible>=2.9'],
    entry_points={
        'console_scripts': [
            'ansible-changelog = ansible_changelog:main',
        ],
    },
)
