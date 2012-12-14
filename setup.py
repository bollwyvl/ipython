# -*- coding: utf-8 -*-

from setuptools import (
    setup,
    find_packages,
    )

__version__ = 'undefined'

exec open('blockly/version.py')

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='blockly',
    version=__version__,
    description='A Blockly visual programming cell for the IPython web notebook',
    long_description=readme,
    author='Nicholas Bollweg',
    author_email='nick.bollweg@gmail.com',
    url='https://github.com/bollwyvl/ipython-blockly',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    entry_points={
        'ipnotebook': [
            'blockly = blockly:BlocklyNotebookExtension'
        ]
    }
)
