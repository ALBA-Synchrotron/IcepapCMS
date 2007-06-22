#!/bin/sh
rm *.py
rm *~
pyuic4 -x icepapdriverwidget.ui -o ui_icepapdriverwidget.py
pyuic4 -x icepapdriverwidgetsmall.ui -o ui_icepapdriverwidgetsmall.py

