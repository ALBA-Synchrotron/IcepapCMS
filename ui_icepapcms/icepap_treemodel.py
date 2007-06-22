#!/usr/bin/env python

"""***************************************************************************
**
** Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
**
** This file is part of the example classes of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
***************************************************************************"""

import sys
from PyQt4 import QtCore, QtGui
from lib_icepapcms import IcepapSystem, IcepapDriver, Conflict



class IcepapTreeModel(QtCore.QAbstractItemModel):
    SYSTEM, DRIVER, SYSTEM_WARNING, DRIVER_WARNING, SYSTEM_ERROR, DRIVER_ERROR, CRATE, DRIVER_NEW, ROOT = range(9)
    def __init__(self, IcepapsList, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        
        #self.item_dict = {}
        self.item_location = {}
        
        rootData = [QtCore.QVariant("Icepaps"), QtCore.QVariant("Description")]
        self.rootItem = TreeItem(rootData, IcepapTreeModel.ROOT, "")
        self.setupModelData(IcepapsList, self.rootItem)
        self._dec_roles = (QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapsys.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdriver.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapsyswarning.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdriverwarning.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapsyserror.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdrivererror.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapcrate.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdrivernew.png"))
        
    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()
        
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            item = index.internalPointer()
            return QtCore.QVariant(item.data(index.column()))
        elif role == QtCore.Qt.DecorationRole:
            if (index.column() == 0):
                item = index.internalPointer()
                return QtCore.QVariant(self._dec_roles[item.role])
            else:
                return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
    
    def item_data(self, index):
        item = index.internalPointer()
        return item.itemData
    
    def item(self, index):
        item = index.internalPointer()
        return item
        
    
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)
        
        return QtCore.QVariant()
    
    def index(self, row, column, parent=QtCore.QModelIndex()):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()
        
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
        
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentItem.row(), 0, parentItem)
    
    def rowCount(self, parent = QtCore.QModelIndex()):
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        
        return parentItem.childCount()
        
    def setupModelData(self, IcepapsList, parent):
        for icepap_name, icepap_system in IcepapsList.items():
            self.addIcepapSysten(icepap_name, icepap_system, parent)
            
    def addIcepapSysten(self, icepap_name, icepap_system, parent = None):
        if parent == None:
            parent = self.rootItem
        crate = -1
        location = icepap_name
        new_item_system = self.addItem([QtCore.QVariant(icepap_name), QtCore.QVariant(icepap_system.description)], IcepapTreeModel.SYSTEM, location, icepap_system, parent)
        if icepap_system.conflict == Conflict.NO_CONNECTION:
            return
        for addr, driver in sorted(icepap_system.IcepapDriverList.items()):
            if driver.cratenr  <> crate:
                crate = driver.cratenr
                location = "%s/%s" % (icepap_name, crate)
                new_item_crate = self.addItem([QtCore.QVariant(driver.cratenr), QtCore.QVariant("")], IcepapTreeModel.CRATE, location,None, new_item_system)
            location = "%s/%s/%s" % (icepap_name, crate, addr)    
            self.addItem([QtCore.QVariant(addr), QtCore.QVariant(driver.name)], IcepapTreeModel.DRIVER, location, driver, new_item_crate)    
            
    
    def addItem(self, labels, role, location, data, parent):
        new_item = TreeItem(labels, role, location, data, parent)
        #self.item_dict[id(new_item)] = new_item
        self.item_location[location] = new_item
        parent.appendChild(new_item)
        return new_item
    
    def indexByLocation(self, location):
        if self.item_location.has_key(location):
            item = self.item_location[location]
            if item:
                return self.createIndex(item.row(), 0, item)
            else:
                None
        else:
            return None
    
    def itemByLocation(self, location):
        if self.item_location.has_key(location):
            return self.item_location[location]
        else:
            return None
        
    def deleteIcepapSystem(self, icepap_name):
        item = self.itemByLocation(icepap_name)
        self.deleteItem(item)
    
    def deleteItem(self, item):
        index = self.indexByLocation(item.location)
        self.beginRemoveRows(self.parent(index), index.row(), index.row())
        #del self.item_dict[id(item)]
        del self.item_location[item.location]
        item.parentItem.removeChild(index.row())
        self.endRemoveRows()
            
       

class TreeItem:
    def __init__(self, label, role, location, data= None, parent=None):
        self.childItems = []
        self.itemLabel = label
        self.role = role
        if role == IcepapTreeModel.SYSTEM:
            if data.conflict == Conflict.NO_CONNECTION:
                self.role = IcepapTreeModel.SYSTEM_ERROR
            elif data.child_conflicts > 0:
                self.role = IcepapTreeModel.SYSTEM_WARNING
        elif role == IcepapTreeModel.DRIVER:
            if data.conflict == Conflict.DRIVER_NOT_PRESENT:
                self.role = IcepapTreeModel.DRIVER_ERROR
            elif data.conflict == Conflict.NEW_DRIVER:
                self.role = IcepapTreeModel.DRIVER_NEW
            elif data.conflict == Conflict.DRIVER_CHANGED:
                self.role = IcepapTreeModel.DRIVER_WARNING
        self.parentItem = parent
        self.itemData = data
        self.location = location
        
    def appendChild(self, child):
        self.childItems.append(child)
        
    def removeChild(self, row):
        del self.childItems[row]
        
    def child(self, row):
        return self.childItems[row]
    
    def childCount(self):
        return len(self.childItems)
    
    def columnCount(self):
        return len(self.itemLabel)
    
    def data(self, column):
        return self.itemLabel[column]
    
    def parent(self):
        return self.parentItem
    
    def changeLabel(self, labels):
        self.itemLabel = labels

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0
    
    def solveConflict(self):
        if self.role == IcepapTreeModel.DRIVER_WARNING:
            self.role = IcepapTreeModel.DRIVER
            self.itemData.conflict = Conflict.NO_CONFLICT
            self.parentItem.notifySolvedConflict()
        elif self.role == IcepapTreeModel.DRIVER_ERROR:
            self.parentItem.notifySolvedConflict()
   
    def notifySolvedConflict(self):
        if self.role == IcepapTreeModel.SYSTEM_WARNING:
            self.itemData.child_conflicts -= 1
            if self.itemData.child_conflicts == 0:
                self.role = IcepapTreeModel.SYSTEM
        elif self.role ==  IcepapTreeModel.CRATE:
            self.parentItem.notifySolvedConflict()
        
    def getIcepapSystem(self):
        
        if self.role == IcepapTreeModel.SYSTEM or self.role == IcepapTreeModel.SYSTEM_WARNING or self.role == IcepapTreeModel.SYSTEM_ERROR:
            return self.itemData
        if self.role ==  IcepapTreeModel.CRATE:
            return self.parentItem.getIcepapSystem()
        else:
            return self.parentItem.getIcepapSystem()