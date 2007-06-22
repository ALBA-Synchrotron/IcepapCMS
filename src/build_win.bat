move setup.cfg setup.bak
python setup.py py2exe --includes sip,ExtensionClass
move setup.bak setup.cfg