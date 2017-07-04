#!/bin/sh
#rm *.py
#rm *~
pyrcc4 icepapcms.qrc -o qrc_icepapcms.py

/usr/bin/pyuic4  ipaptestpage.ui -o ui_ipaptestpage.py
/usr/bin/pyuic4  dialogaddicepap.ui -o ui_dialogaddicepap.py
/usr/bin/pyuic4  dialogaddlocation.ui -o ui_dialogaddlocation.py
/usr/bin/pyuic4  dialogsystemscan.ui -o ui_dialogsystemscan.py
/usr/bin/pyuic4  dialogdriverconflict.ui -o ui_dialogdriverconflict.py
/usr/bin/pyuic4  dialoghistoriccfg.ui -o ui_dialoghistoriccfg.py
/usr/bin/pyuic4  dialogpreferences.ui -o ui_dialogpreferences.py
/usr/bin/pyuic4  dialogipapprogram.ui -o ui_dialogipapprogram.py
/usr/bin/pyuic4  pageipapdriver.ui -o ui_pageipapdriver.py
/usr/bin/pyuic4  icepapcms.ui -o ui_icepapcms.py
/usr/bin/pyuic4  ipapconsole.ui -o ui_ipapconsole.py
/usr/bin/pyuic4  historiccfgwidget.ui -o ui_historiccfgwidget.py

/usr/bin/pyuic4  axis.ui -o ui_axis.py
/usr/bin/pyuic4  motor.ui -o ui_motor.py
/usr/bin/pyuic4  encoders.ui -o ui_encoders.py
/usr/bin/pyuic4  closedloop.ui -o ui_closedloop.py
/usr/bin/pyuic4  homing.ui -o ui_homing.py
/usr/bin/pyuic4  io.ui -o ui_io.py

/usr/bin/pyuic4 dialogconflictdriver_nonexpert.ui -o ui_dialogconflictdriver_nonexpert.py
/usr/bin/pyuic4 dialogconflictdriver_expert.ui -o ui_dialogconflictdriver_expert.py
/usr/bin/pyuic4 dialognewdriver.ui -o ui_dialognewdriver.py

DIR_DRIVERWIDGET=icepapdriver_widget
/usr/bin/pyuic4 $DIR_DRIVERWIDGET/icepapdriverwidget.ui -o $DIR_DRIVERWIDGET/ui_icepapdriverwidget.py
/usr/bin/pyuic4 $DIR_DRIVERWIDGET/icepapdriverwidgetsmall.ui -o $DIR_DRIVERWIDGET/ui_icepapdriverwidgetsmall.py

pushd ..
rm ui*py
rm $DIR_DRIVERWIDGET/ui*py
rm qrc_icepapcms.py
rm icepapcms_rc.py

mv qt_designer_files/ui*py .
mv qt_designer_files/$DIR_DRIVERWIDGET/ui*py $DIR_DRIVERWIDGET/

mv qt_designer_files/qrc_icepapcms.py .
ln -s qrc_icepapcms.py icepapcms_rc.py
popd

#gedit ui_icepapdriverwidget.py &
