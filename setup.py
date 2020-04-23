#!/usr/bin/env python

from setuptools import setup, find_packages


long_description = """IcepapCfg is a configuration and test tool for the
Icepap motor controller"""

# The version is updated automatically with bumpversion
# Do not update manually
__version = '2.3.6'


# Setup
setup(
    name="icepapCMS",
    version=__version,
    packages=find_packages(),
    description="Icepap Configuration Management System and Test Tool",
    long_description=long_description,
    author="Guifre Cuni",
    author_email="guifre.cuni@cells.es",
    entry_points={
        'gui_scripts': [
            'icepapcms = icepapCMS.ui_icepapcms.icepapcms:main',
            'ipapconsole = icepapCMS.ui_icepapcms.ipapconsole:main'],
    },
    # install_requires=[
    #     "storm==0.20",
    #     "IPy>=0.62",
    #     "PyQt4",
    #      MySQL-python
    #     "sqlite3", # or pysqlite2 (not in pypi)
    #     "pyicepap" #not in pypi
    #     "ldap" # needed by ldap_login (ALBA-Cells library)
    # ],
    include_package_data=True,
    platforms=["Linux, Windows XP/Vista/7/8"],
    url="http://computing.cells.es/products/icepap-cms"
)
