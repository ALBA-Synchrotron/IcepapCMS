#!/usr/bin/env python

from setuptools import setup, find_packages


long_description = """
IcepapCMS is a graphical configuration and test tool for the Icepap motor 
controller, base on icepap library. 

It allows to configure the electrical parameters, I/O interfaces, encoders, 
movement parameters, homing procedures. 

All changes are saved on a data base which allows to do easy rollbacks, 
identified changes and conflicts between the hardware configuration and the 
data base configuration. 

The program includes one graphical console to communicate with raw commands.  
"""

# The version is updated automatically with bumpversion
# Do not update manually
__version = '3.0.1'


# Setup
setup(
    name="icepapcms",
    version=__version,
    packages=find_packages(),
    description="Icepap Configuration Management System and Test Tool",
    long_description=long_description,
    author="Guifre Cuni et al.",
    author_email="ctbeamlines@cells.es",
    license="GPLv3",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
    ],
    entry_points={
        'gui_scripts': [
            'icepapcms = icepapcms.__main__:main',
            'ipapconsole = icepapcms.gui.ipapconsole:main'],
    },
    install_requires=[
        "storm>=0.23",
        "IPy>=0.62",
        "PyQt5",
        "icepap>=3.3.0",
        'configobj',
        'ldap3',
        'PyYAML',

    ],
    package_data={
        '': ['*.ui', '*.png', '*.svg', '*.gif', '*.xml', '*.txt', '*.sql',
             '*.pdf']
    },
    include_package_data=True,
    platforms=["Linux, Windows XP/Vista/7/8"],
    url="https://github.com/ALBA-Synchrotron/IcepapCMS",
    python_requires='>=3.5',
)
