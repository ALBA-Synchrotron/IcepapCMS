#!/usr/bin/env python
DISTUTILS_DEBUG=1
from distutils.core import setup
import glob
import os

if os.name == 'nt': #sys.platform == 'win32':
    import py2exe

setup(name = "icepapcms",
      version = "1.16",
      description = "Icepap Configuration Management System and Test Tool",
      author = "Guifre Cuni",
      author_email = "gcuni@cells.es",
      url = "http://www.cells.es",
      #packages = ["storm", "storm.databases", "lib_icepapcms", "lib_icepapcms/PyQt4", "lib_icepapcms/serial", "lib_icepapcms/pyIcePAP", "lib_icepapcms.icepapzodb", "ui_icepapcms", "ui_icepapcms.icepapdriver_widget", "ui_icepapcms.Led"],
      #packages = ["storm", "storm.databases", "lib_icepapcms", "lib_icepapcms.icepapzodb", "ui_icepapcms", "ui_icepapcms.icepapdriver_widget", "ui_icepapcms.Led"],
      packages = ["storm", "storm.databases", "lib_icepapcms", "lib_icepapcms.icepapzodb", "lib_icepapcms.IPy", "ui_icepapcms", "ui_icepapcms.icepapdriver_widget", "ui_icepapcms.icepapdriver_widget.Led", "ui_icepapcms.Led"],
      data_files = [('doc', glob.glob("doc/*.*")),
                    ('db', glob.glob("db/*.sql")),
                    ('templates', glob.glob("templates/*.*"))
                    ],
      
      scripts = ["icepapcms","icepapcms.py"],
	  console = ["icepapcms.py"],
	  windows = [
        {
            "script": "icepapcms.py",
            "icon_resources": [(1, "icepapcms.ico")]
        }
      ],
      long_description = "IcepapCfg is a configuration and test tool for the Icepap motor controller",
      options={"py2exe":{"includes":["sip","PyQt4._qt","serial","pyIcePAP"]}})
