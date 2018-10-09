move setup.cfg setup.bak
;python setup.py py2exe --includes sip,ExtensionClass
; the includes are defined inside the setup.py configuration
python setup.py py2exe
move setup.bak setup.cfg