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
from lib_icepapcms import IcepapSystem, IcepapDriver, Conflict, IcepapMode



class IcepapTreeModel(QtCore.QAbstractItemModel):
    SYSTEM, DRIVER, SYSTEM_WARNING, DRIVER_WARNING, SYSTEM_ERROR, DRIVER_ERROR, CRATE, DRIVER_NEW, DRIVER_CFG, SYSTEM_OFFLINE, DRIVER_MOVED,ROOT = range(12)
    def __init__(self, IcepapsList, no_expand = False, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        
        #self.item_dict = {}
        self.item_location = {}
        
        #rootData = [QtCore.QVariant("Icepaps"), QtCore.QVariant("Description")]
        rootData = [QtCore.QVariant("IcepapCMS DB")]
        self.rootItem = TreeItem(rootData, IcepapTreeModel.ROOT, "DB")        
        
        self.setupModelData(IcepapsList, self.rootItem, no_expand)
        self._dec_roles = (QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapsys.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdriver.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapsyswarning.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdriverwarning.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapsyserror.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdrivererror.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapcrate.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdrivernew.png"), 
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdrivercfg.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapsysoffline.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/ipapdrivermoved.png"),
                           QtGui.QPixmap(":/icons/IcepapCfg Icons/gnome-nettool.png"))
        
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
                item.updateRole()
                return QtCore.QVariant(self._dec_roles[item.role])
            else:
                return QtCore.QVariant()
                
        elif role == QtCore.Qt.ToolTipRole:
            item = index.internalPointer()
            if item.description is None:
                return QtCore.QVariant()
            return QtCore.QVariant(item.description)
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
        
    def setupModelData(self, IcepapsList, parent, no_expand):
        #print str(type(IcepapsList))
        #print str(IcepapsList.keys())
        #for icepap_name, icepap_system in IcepapsList.items():
        keys = IcepapsList.keys()
        keys.sort()
        for icepap_name in keys:
            self.addIcepapSystem(icepap_name, IcepapsList.get(icepap_name), no_expand, parent)
            
    def addIcepapSystem(self, icepap_name, icepap_system, no_expand, parent = None, index = None):
        """ TO-DO STORM review"""
        if parent == None:
            parent = self.rootItem
        crate = -1
        location = icepap_name
        role = IcepapTreeModel.SYSTEM
        if no_expand:
            role = IcepapTreeModel.SYSTEM_OFFLINE            
        
        new_item_system = self.addItem([QtCore.QVariant(icepap_name), QtCore.QVariant(icepap_system.description)], role, location, icepap_system, parent, index)
        
        if icepap_system.conflict == Conflict.NO_CONNECTION or no_expand:
            return
        drivers = icepap_system.getDrivers(True)
        drivers.sort()
        for driver in drivers:
            addr = driver.addr
            if driver.cratenr  <> crate:
                crate = driver.cratenr
                location = "%s/%s" % (icepap_name, crate)
                new_item_crate = self.addItem([QtCore.QVariant(driver.cratenr)], IcepapTreeModel.CRATE, location,None, new_item_system)
            location = "%s/%s/%s" % (icepap_name, crate, addr)
            self.addItem([QtCore.QVariant(str(addr)+" "+driver.name)], IcepapTreeModel.DRIVER, location, driver, new_item_crate)
            
    def deleteIcepapSystem(self, icepap_name):
        item = self.itemByLocation(icepap_name)
        self.deleteItem(item)
        return item
    
    def updateIcepapSystem(self, icepap_system, no_expand = False):
        index = self.indexByLocation(icepap_system.name)
        item = self.deleteIcepapSystem(icepap_system.name)
        self.addIcepapSystem(icepap_system.name, icepap_system, no_expand,item.parent(),index)
        
    def addItem(self, labels, role, location, data, parent, tree_index = None):
        new_item = TreeItem(labels, role, location, data, parent)
        #self.item_dict[id(new_item)] = new_item
        
        #parent.appendChild(new_item)
        parent.appendChild(new_item,tree_index)
            

        self.item_location[location] = new_item
        index = self.indexByLocation(location)
        self.beginInsertRows(self.parent(index), index.row(), index.row())
        self.endInsertRows()
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
    
    
    def deleteItem(self, item):
        index = self.indexByLocation(item.location)
        self.beginRemoveRows(self.parent(index), index.row(), index.row())
        #del self.item_dict[id(item)]
        del self.item_location[item.location]
        item.parentItem.removeChild(index.row())
        self.endRemoveRows()
    
    def changeItemIcon(self, location, role):
        index = self.indexByLocation(location)
        if not index is None:
            modelitem = self.item(index)
            modelitem.role = role
            self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), index, index)

class TreeItem:
    def __init__(self, label, role, location, data= None, parent=None):
        self.childItems = []
        self.description = None
        self.itemLabel = [label[0]]
        if len(label) > 1:
            if label[1].toString() != "":
                self.description = label[1].toString() 
        self.role = role
        self.itemData = data
        self.updateRole()
        self.parentItem = parent        
        self.location = location
    
    def updateRole(self):
        if self.role == IcepapTreeModel.SYSTEM:
            if self.itemData.conflict == Conflict.NO_CONNECTION:
                self.role = IcepapTreeModel.SYSTEM_ERROR
            elif self.itemData.child_conflicts > 0:
                self.role = IcepapTreeModel.SYSTEM_WARNING
        elif self.role == IcepapTreeModel.DRIVER or self.role == IcepapTreeModel.DRIVER_CFG:
            if self.itemData.conflict == Conflict.NO_CONFLICT:
                self.role = IcepapTreeModel.DRIVER
            if self.itemData.conflict == Conflict.DRIVER_NOT_PRESENT:
                self.role = IcepapTreeModel.DRIVER_ERROR
            elif self.itemData.conflict == Conflict.NEW_DRIVER:
                self.role = IcepapTreeModel.DRIVER_NEW
            elif self.itemData.conflict == Conflict.DRIVER_CHANGED:
                self.role = IcepapTreeModel.DRIVER_WARNING
            elif self.itemData.conflict == Conflict.DRIVER_MOVED:
                self.role = IcepapTreeModel.DRIVER_MOVED
            elif self.itemData.mode == IcepapMode.CONFIG:
                self.role = IcepapTreeModel.DRIVER_CFG
        
        
    def appendChild(self, child, index = None):
        if index == None:
            self.childItems.append(child)
        else:
            self.childItems.insert(index.row(),child)
        
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
    
    def changeLabel(self, label):
        if len(label) > 1:
            if label[1] != "":
                self.description = label[1]
        
        self.itemLabel = [label[0]]

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0
    
    def solveConflict(self):
        if self.role == IcepapTreeModel.DRIVER_WARNING or self.role == IcepapTreeModel.DRIVER_NEW:
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
        if self.role == IcepapTreeModel.SYSTEM or self.role == IcepapTreeModel.SYSTEM_WARNING or self.role == IcepapTreeModel.SYSTEM_ERROR or self.role == IcepapTreeModel.SYSTEM_OFFLINE:
            return self.itemData
        if self.role ==  IcepapTreeModel.CRATE:
            return self.parentItem.getIcepapSystem()
        else:
            return self.parentItem.getIcepapSystem()
