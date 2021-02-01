#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapcms https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from PyQt5 import QtCore, QtGui, QtWidgets
import logging
from ..helpers import loggingInfo


class PyConsoleText(QtWidgets.QTextEdit):
    commandReceived = QtCore.pyqtSignal(str, name='commandReceived')
    log = logging.getLogger('{}.PyConsoleText'.format(__name__))

    @loggingInfo
    def __init__(self, parent=None):
        QtWidgets.QTextEdit.__init__(self, parent)

        # to exit the main interpreter by a Ctrl-D if PyCute has no parent
        if parent is None:
            self.eofKey = QtCore.Qt.Key_D
        else:
            self.eofKey = None
        self.prompt = ""
        # last line + last incomplete lines
        self.line = ""
        self.lines = []
        # the cursor position in the last line
        self.point = 0
        # flag: the interpreter needs more input to run the last lines.
        self.more = 0
        # flag: readline() is being used for e.g. raw_input() and input()
        self.reading = 0
        # history
        self.history = []
        self.pointer = 0
        self.cursor_pos = 0

        # user interface setup

        self.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

    @loggingInfo
    def setPrompt(self, text):
        self.prompt = text

    @loggingInfo
    def flush(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        pass

    @loggingInfo
    def readline(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        self.reading = 1
        self.__clearLine()
        self.moveCursor(QtGui.QTextCursor.End)
        if len(self.line) == 0:
            return '\n'
        else:
            return self.line

    @loggingInfo
    def write(self, text):

        # The output of self.append(text) contains to many newline characters,
        # so work around QTextEdit's policy for handling newline characters.

        cursor = self.textCursor()

        cursor.movePosition(QtGui.QTextCursor.End)

        pos1 = cursor.position()
        cursor.insertText(text)

        self.cursor_pos = cursor.position()
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

        # Set the format
        cursor.setPosition(pos1, QtGui.QTextCursor.KeepAnchor)

    @loggingInfo
    def __run(self):
        """
        Append the last line to the history list, let the interpreter execute
        the last line(s), and clean up accounting for the interpreter results:
        (1) the interpreter succeeds
        (2) the interpreter fails, finds no errors and wants more line(s)
        (3) the interpreter fails, finds errors and writes them to sys.stderr
        """
        self.pointer = 0
        self.history.append(self.line)
        try:
            self.lines.append(self.line)
        except Exception as e:
            self.log.error('Error on __run(): %s', e)

        source = '\n'.join(self.lines)

        self.commandReceived.emit(source)
        self.lines = []
        self.__clearLine()
        self.write(self.prompt)

    @loggingInfo
    def __clearLine(self):
        """
        Clear input line buffer
        """
        self.line = ""
        self.point = 0

    @loggingInfo
    def __insertText(self, text):
        """
        Insert text at the current cursor position.
        """

        self.line = self.line[:self.point] + text + self.line[self.point:]
        self.point += len(text)

        cursor = self.textCursor()
        cursor.insertText(text)
        self.update()

    @loggingInfo
    def keyPressEvent(self, e):
        """
        Handle user input a key at a time.
        """
        text = e.text()
        key = e.key()

        if key == QtCore.Qt.Key_Backspace:
            if self.point:
                cursor = self.textCursor()
                cursor.movePosition(
                    QtGui.QTextCursor.PreviousCharacter,
                    QtGui.QTextCursor.KeepAnchor)
                cursor.removeSelectedText()

                self.point -= 1
                self.line = self.line[:self.point] + self.line[self.point+1:]

        elif key == QtCore.Qt.Key_Delete:
            cursor = self.textCursor()
            cursor.movePosition(
                QtGui.QTextCursor.NextCharacter,
                QtGui.QTextCursor.KeepAnchor)
            cursor.removeSelectedText()

            self.line = self.line[:self.point] + self.line[self.point+1:]

        elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
            self.write('\n')
            if self.reading:
                self.reading = 0
            else:
                self.__run()

        elif key == QtCore.Qt.Key_Tab:
            self.__insertText(text)
        elif key == QtCore.Qt.Key_Left:
            if self.point:
                self.moveCursor(QtGui.QTextCursor.Left)
                self.point -= 1
        elif key == QtCore.Qt.Key_Right:
            if self.point < len(self.line):
                self.moveCursor(QtGui.QTextCursor.Right)
                self.point += 1

        elif key == QtCore.Qt.Key_Home:
            cursor = self.textCursor()
            cursor.setPosition(self.cursor_pos)
            self.setTextCursor(cursor)
            self.point = 0

        elif key == QtCore.Qt.Key_End:
            self.moveCursor(QtGui.QTextCursor.EndOfLine)
            self.point = len(self.line)

        elif key == QtCore.Qt.Key_Up:

            if len(self.history):
                if self.pointer == 0:
                    self.pointer = len(self.history)
                self.pointer -= 1
                self.__recall()

        elif key == QtCore.Qt.Key_Down:
            if len(self.history):
                self.pointer += 1
                if self.pointer == len(self.history):
                    self.pointer = 0
                self.__recall()

        elif len(text) > 0:
            self.__insertText(text)
            return

        else:
            e.ignore()
        self.update()

    @loggingInfo
    def __recall(self):
        """
        Display the current item from the command history.
        """
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        self.__clearLine()
        self.write(self.prompt)
        self.__insertText(self.history[self.pointer])

    @loggingInfo
    def mousePressEvent(self, e):
        """
        Keep the cursor after the last prompt.
        """
        if e.button() == QtCore.Qt.LeftButton:
            self.moveCursor(QtGui.QTextCursor.End)

    @loggingInfo
    def contentsContextMenuEvent(self, ev):
        """
        Suppress the right button context menu.
        """
        pass


class SyntaxColor:
    """ Allow to color python keywords """

    keywords = {"and", "del", "from", "not", "while", "as", "elif", "global",
                "or", "with", "assert", "else", "if", "pass", "yield", "break",
                "except", "import", "print", "class", "exec", "in", "raise",
                "continue", "finally", "is", "return", "def", "for", "lambda",
                "try"}

    def __init__(self):
        pass

    def get_color(self, word):
        """ Return a color tuple (R,G,B) depending of the string word """

        stripped = word.strip()

        if stripped in self.keywords:
            return 255, 132, 0  # orange

        elif self.is_python_string(stripped):
            return 61, 120, 9  # dark green

        else:
            return 255, 255, 255

    def is_python_string(self, str):
        """ Return True if str is enclosed by a string mark """

        return False
