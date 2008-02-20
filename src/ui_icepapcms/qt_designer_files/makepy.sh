#!/bin/sh
#rm *.py
#rm *~
pyrcc4 icepapcms.qrc -o ../qrc_icepapcms.py
/usr/bin/pyuic4  ipaptestpage.ui -o ../ui_ipaptestpage.py
/usr/bin/pyuic4  dialogaddicepap.ui -o ../ui_dialogaddicepap.py
/usr/bin/pyuic4  dialogaddlocation.ui -o ../ui_dialogaddlocation.py
/usr/bin/pyuic4  dialogsystemscan.ui -o ../ui_dialogsystemscan.py
/usr/bin/pyuic4  dialogdriverconflict.ui -o ../ui_dialogdriverconflict.py
/usr/bin/pyuic4  dialoghistoriccfg.ui -o ../ui_dialoghistoriccfg.py
/usr/bin/pyuic4  dialogpreferences.ui -o ../ui_dialogpreferences.py
/usr/bin/pyuic4  dialogipapprogram.ui -o ../ui_dialogipapprogram.py
/usr/bin/pyuic4  pageipapdriver.ui -o ../ui_pageipapdriver.py
/usr/bin/pyuic4  icepapcms.ui -o ../ui_icepapcms.py
/usr/bin/pyuic4  ipapconsole.ui -o ../ui_ipapconsole.py
/usr/bin/pyuic4  historiccfgwidget.ui -o ../ui_historiccfgwidget.py


#gedit ui_icepapdriverwidget.py &
