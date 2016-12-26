'''
    Setup options & Meta-data for sclib program
    Copyright (c) 2016 AU MIT Students
'''

from setuptools import setup

setup(
    name='sclib',
    version='1.0.ocr0.9',
    py_modules=['sclib'],
    install_requires=[
        'Click',
        'ruamel.yaml',
        'paramiko',
    ],
    entry_points='''
        [console_scripts]
        sclib=sclib:syLib
    ''',
)