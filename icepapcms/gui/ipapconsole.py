from PyQt5 import QtCore, QtWidgets


class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, command=""):
        super(EmbTerminal, self).__init__()
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.terminal)

        self.process.start('xterm', ['-into', str(int(self.winId())),
                                     '-bg', 'black', '-fg', 'gray',
                                     '-rightbar', '-geom', '150x40',
                                     '-e', command])
        self.setFixedSize(800, 480)


class IcepapConsole(QtWidgets.QDialog):
    def __init__(self, parent=None, addr=None):
        if addr is None:
            return
        QtWidgets.QDialog.__init__(self, parent)
        lay = QtWidgets.QVBoxLayout()
        self.setLayout(lay)
        cmd = 'icepapctl {}'.format(addr)
        self.terminal = EmbTerminal(cmd)
        self.terminal.process.finished.connect(self.close)
        lay.addWidget(self.terminal)
        self.setWindowTitle('Icepap Console <{}>'.format(addr))


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    console = IcepapConsole(app, 'icepapspare15')
    console.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()