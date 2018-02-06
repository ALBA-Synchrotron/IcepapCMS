#!/usr/bin/env python

# ------------------------------------------------------------------------------
# This file is part of icepapCMS (https://github.com/ALBA-Synchrotron/icepapcms)
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# ------------------------------------------------------------------------------


from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextEdit, QTextCursor
from PyQt4.QtCore import Qt
import os

            

class PyConsoleText(QTextEdit):
    __pyqtSignals__ = ("commandReceived(const QString &)")
    
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        
        #self.colorizer = SyntaxColor()

        # to exit the main interpreter by a Ctrl-D if PyCute has no parent
        if parent is None:
            self.eofKey = Qt.Key_D
        else:
            self.eofKey = None
        self.prompt = ""
        # last line + last incomplete lines
        self.line    = QtCore.QString()
        self.lines   = []
        # the cursor position in the last line
        self.point   = 0
        # flag: the interpreter needs more input to run the last lines. 
        self.more    = 0
        # flag: readline() is being used for e.g. raw_input() and input()
        self.reading = 0
        # history
        self.history = []
        self.pointer = 0
        self.cursor_pos   = 0

        # user interface setup
        #self.setTextFormat(Qt.PlainText)
        
        self.setLineWrapMode(QTextEdit.NoWrap)
        #self.setCaption('Python Shell')

        
    def setPrompt(self, text):
        self.prompt = text
        
    def flush(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        pass



    def readline(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        self.reading = 1
        self.__clearLine()
        self.moveCursor(QTextCursor.End)
        while self.reading:
            qApp.processOneEvent()
        if self.line.length() == 0:
            return '\n'
        else:
            return str(self.line)
     

    
    def write(self, text):
    
        # The output of self.append(text) contains to many newline characters,
        # so work around QTextEdit's policy for handling newline characters.

        cursor = self.textCursor()

        cursor.movePosition(QTextCursor.End)

        pos1 = cursor.position()
        cursor.insertText(text)

        self.cursor_pos = cursor.position()
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

        # Set the format
        cursor.setPosition(pos1, QTextCursor.KeepAnchor)

        #format = cursor.charFormat()
        #format.setForeground( QtGui.QBrush(QtGui.QColor(255,255,255)))
        #cursor.setCharFormat(format)

            
    def __run(self):
        """
        Append the last line to the history list, let the interpreter execute
        the last line(s), and clean up accounting for the interpreter results:
        (1) the interpreter succeeds
        (2) the interpreter fails, finds no errors and wants more line(s)
        (3) the interpreter fails, finds errors and writes them to sys.stderr
        """
        self.pointer = 0
        self.history.append(QtCore.QString(self.line))
        try:
            self.lines.append(str(self.line))
        except Exception,e:
            print e

        source = '\n'.join(self.lines)

        self.emit(QtCore.SIGNAL("commandReceived(const QString &)"), QtCore.QString(source))
        self.lines = []
        self.__clearLine()
        self.write(self.prompt)

        
    def __clearLine(self):
        """
        Clear input line buffer
        """
        self.line.truncate(0)
        self.point = 0

        
    def __insertText(self, text):
        """
        Insert text at the current cursor position.
        """

        self.line.insert(self.point, text)
        self.point += text.length()

        cursor = self.textCursor()
        cursor.insertText(text)
        self.update()
        #self.color_line()


    def keyPressEvent(self, e):
        """
        Handle user input a key at a time.
        """
        text  = e.text()
        key   = e.key()

        if key == Qt.Key_Backspace:
            if self.point:
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
                #self.color_line()
            
                self.point -= 1 
                self.line.remove(self.point, 1)

        elif key == Qt.Key_Delete:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            #self.color_line()
                        
            self.line.remove(self.point, 1)
            
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.write('\n')
            if self.reading:
                self.reading = 0
            else:
                self.__run()
                
        elif key == Qt.Key_Tab:
            self.__insertText(text)
        elif key == Qt.Key_Left:
            if self.point : 
                self.moveCursor(QTextCursor.Left)
                self.point -= 1 
        elif key == Qt.Key_Right:
            if self.point < self.line.length():
                self.moveCursor(QTextCursor.Right)
                self.point += 1 

        elif key == Qt.Key_Home:
            cursor = self.textCursor ()
            cursor.setPosition(self.cursor_pos)
            self.setTextCursor (cursor)
            self.point = 0 

        elif key == Qt.Key_End:
            self.moveCursor(QTextCursor.EndOfLine)
            self.point = self.line.length() 

        elif key == Qt.Key_Up:

            if len(self.history):
                if self.pointer == 0:
                    self.pointer = len(self.history)
                self.pointer -= 1
                self.__recall()
                
        elif key == Qt.Key_Down:
            if len(self.history):
                self.pointer += 1
                if self.pointer == len(self.history):
                    self.pointer = 0
                self.__recall()

        elif text.length():
            self.__insertText(text)
            return

        else:
            e.ignore()
        self.update()


    def __recall(self):
        """
        Display the current item from the command history.
        """
        cursor = self.textCursor ()
        cursor.select( QtGui.QTextCursor.LineUnderCursor )
        cursor.removeSelectedText()
        self.__clearLine()
        self.write(self.prompt)
        self.__insertText(self.history[self.pointer])

        
#     def focusNextPrevChild(self, next):
#         """
#         Suppress tabbing to the next window in multi-line commands. 
#         """
#         if next and self.more:
#             return 0
#         return QTextEdit.focusNextPrevChild(self, next)

    def mousePressEvent(self, e):
        """
        Keep the cursor after the last prompt.
        """
        if e.button() == Qt.LeftButton:
            self.moveCursor(QTextCursor.End)
            
    def contentsContextMenuEvent(self,ev):
        """
        Suppress the right button context menu.
        """
        pass

#    
#    def color_line(self):
#        """ Color the current line """
#        
#        cursor = self.textCursor()
#        cursor.movePosition(QTextCursor.StartOfLine)
#
#        newpos = cursor.position()
#        pos = -1
#        
#        while(newpos != pos):
#            cursor.movePosition(QTextCursor.NextWord)
#
#            pos = newpos
#            newpos = cursor.position()
#
#            cursor.select(QTextCursor.WordUnderCursor)
#            word = str(cursor.selectedText ().toAscii())
#
#            if(not word) : continue
#            
#            (R,G,B) = self.colorizer.get_color(word)
#            
#            format = cursor.charFormat()
#            format.setForeground( QtGui.QBrush(QtGui.QColor(R,G,B)))
#            cursor.setCharFormat(format)
            




class SyntaxColor:
    """ Allow to color python keywords """

    keywords = set(["and", "del", "from", "not", "while",
                "as", "elif", "global", "or", "with",
                "assert", "else", "if", "pass", "yield",
                "break", "except", "import", "print",
                "class", "exec", "in", "raise",              
                "continue", "finally", "is", "return",
                "def", "for", "lambda", "try"])

    def __init__(self):
        pass
        

    def get_color(self, word):
        """ Return a color tuple (R,G,B) depending of the string word """

        stripped = word.strip()
        
        if(stripped in self.keywords):
            return (255, 132,0) # orange
        
        elif(self.is_python_string(stripped)):
            return (61, 120, 9) # dark green
        
        else:
            return (255,255,255)

    def is_python_string(self, str):
        """ Return True if str is enclosed by a string mark """

#         return (
#             (str.startswith("'''") and str.endswith("'''")) or
#             (str.startswith('"""') and str.endswith('"""')) or
#             (str.startswith("'") and str.endswith("'")) or
#             (str.startswith('"') and str.endswith('"')) 
#             )
        return False
        
        



