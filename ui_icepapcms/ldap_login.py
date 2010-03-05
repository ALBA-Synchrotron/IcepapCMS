from PyQt4 import Qt, QtGui
import sys
import ldap

__LDAP_SERVER__ = 'ldap01.cells.es'
__LDAP_WHO_TEMPLATE__ = 'uid=%s,ou=People,dc=CELLS,dc=ES'

class InputLineEdit(Qt.QWidget):
    def __init__(self, parent, row, text, echo_mode=Qt.QLineEdit.Normal):
        Qt.QWidget.__init__(self, parent)
        #self.parent = parent

        self.label = Qt.QLabel(text)
        self.line_edit = Qt.QLineEdit()
        self.line_edit.setEchoMode(echo_mode)

        self.parent().layout().addWidget(self.label, row, 0)
        self.parent().layout().addWidget(self.line_edit, row, 1)

class LdapLogin(Qt.QDialog):
    def __init__(self, parent=None):
        Qt.QDialog.__init__(self, parent)
        self.username = ''

        self.setLayout(Qt.QGridLayout())
        message = 'IcepapCMS Login\n\nPlease enter your user name\nand password\n'
        self.layout().addWidget(Qt.QLabel(message),0,0,1,2)

        self.user = InputLineEdit(self, 1, 'User', Qt.QLineEdit.Normal)
        self.password = InputLineEdit(self, 2, 'Password', Qt.QLineEdit.Password)
        
        self.connect(self.password.line_edit, Qt.SIGNAL('returnPressed()'), self.validate)
        self.connect(self, Qt.SIGNAL('finished(int)'), self.erasePassword)

    def validate(self):
        user = str(self.user.line_edit.text())
        passwd = str(self.password.line_edit.text())
        try:
            l = ldap.open(__LDAP_SERVER__)
            who = __LDAP_WHO_TEMPLATE__ % user
            l.bind_s(who, passwd)
            self.username = user
            self.done(Qt.QDialog.Accepted)
        except:
            self.password.label.setStyleSheet('QLabel { color: red }')
            self.password.line_edit.selectAll()

    def erasePassword(self):
        # PLEASE, DO NOT HACK IN HERE...
        self.password.line_edit.setText('Forget it!')
