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


from PyQt5 import QtCore, QtGui
from icepap import Mode
import logging
from ..helpers import loggingInfo
from ..lib import Conflict


class IcepapTreeModel(QtCore.QAbstractItemModel):
    SYSTEM, DRIVER, SYSTEM_WARNING, DRIVER_WARNING, SYSTEM_ERROR, \
        DRIVER_ERROR, CRATE, DRIVER_NEW, DRIVER_CFG, \
        SYSTEM_OFFLINE, DRIVER_MOVED, ROOT = list(range(12))

    log = logging.getLogger('{}.IcepapTreeModel'.format(__name__))

    @loggingInfo
    def __init__(self, IcepapsList, no_expand=False, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self.item_location = {}

        rootData = [QtCore.QVariant("IcepapCMS DB")]
        self.rootItem = TreeItem(rootData, IcepapTreeModel.ROOT, "DB")

        self.setupModelData(IcepapsList, self.rootItem, no_expand)
        self._dec_roles = (QtGui.QPixmap(":/icons/icons/ipapsys.png"),
                           QtGui.QPixmap(":/icons/icons/ipapdriver.png"),
                           QtGui.QPixmap(":/icons/icons/ipapsyswarning.png"),
                           QtGui.QPixmap(
                               ":/icons/icons/ipapdriverwarning.png"),
                           QtGui.QPixmap(":/icons/icons/ipapsyserror.png"),
                           QtGui.QPixmap(":/icons/icons/ipapdrivererror.png"),
                           QtGui.QPixmap(":/icons/icons/ipapcrate.png"),
                           QtGui.QPixmap(":/icons/icons/ipapdrivernew.png"),
                           QtGui.QPixmap(":/icons/icons/ipapdrivercfg.png"),
                           QtGui.QPixmap(":/icons/icons/ipapsysoffline.png"),
                           QtGui.QPixmap(":/icons/icons/ipapdrivermoved.png"),
                           QtGui.QPixmap(":/icons/icons/gnome-nettool.png"))

    @loggingInfo
    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    @loggingInfo
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

    @loggingInfo
    def item_data(self, index):
        item = index.internalPointer()
        return item.itemData

    @loggingInfo
    def item(self, index):
        item = index.internalPointer()
        return item

    @loggingInfo
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    @loggingInfo
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and \
                role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    @loggingInfo
    def index(self, row, column, parent=QtCore.QModelIndex()):
        if row < 0 or column < 0 or row >= self.rowCount(
                parent) or column >= self.columnCount(parent):
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

    @loggingInfo
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    @loggingInfo
    def rowCount(self, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    @loggingInfo
    def setupModelData(self, IcepapsList, parent, no_expand):
        keys = sorted(IcepapsList.keys())
        for icepap_name in keys:
            self.addIcepapSystem(
                icepap_name,
                IcepapsList.get(icepap_name),
                no_expand,
                parent)

    @loggingInfo
    def addIcepapSystem(self, icepap_name, icepap_system,
                        no_expand, parent=None, index=None):
        """ TO-DO STORM review"""
        if parent is None:
            parent = self.rootItem
        crate = -1
        location = icepap_name
        role = IcepapTreeModel.SYSTEM
        if no_expand:
            role = IcepapTreeModel.SYSTEM_OFFLINE

        new_item_system =\
            self.addItem(
                [QtCore.QVariant(icepap_name),
                 QtCore.QVariant(icepap_system.description)],
                role, location, icepap_system, parent, index)

        if icepap_system.conflict == Conflict.NO_CONNECTION or no_expand:
            return
        drivers = sorted(icepap_system.getDrivers(in_memory=True))
        for driver in drivers:
            addr = driver.addr
            if driver.cratenr != crate:
                crate = driver.cratenr
                location = "%s/%s" % (icepap_name, crate)
                new_item_crate = self.addItem([QtCore.QVariant(
                    driver.cratenr)], IcepapTreeModel.CRATE, location, None,
                    new_item_system)
            location = "%s/%s/%s" % (icepap_name, crate, addr)
            self.addItem([QtCore.QVariant(str(addr) + " " + driver.name)],
                         IcepapTreeModel.DRIVER, location, driver,
                         new_item_crate)

    @loggingInfo
    def deleteIcepapSystem(self, icepap_name):
        item = self.itemByLocation(icepap_name)
        self.deleteItem(item)
        return item

    @loggingInfo
    def updateIcepapSystem(self, icepap_system, no_expand=False):
        index = self.indexByLocation(icepap_system.name)
        item = self.deleteIcepapSystem(icepap_system.name)
        self.addIcepapSystem(
            icepap_system.name,
            icepap_system,
            no_expand,
            item.parent(),
            index)

    @loggingInfo
    def addItem(self, labels, role, location, data, parent, tree_index=None):
        new_item = TreeItem(labels, role, location, data, parent)
        parent.appendChild(new_item, tree_index)

        self.item_location[location] = new_item
        index = self.indexByLocation(location)
        self.beginInsertRows(self.parent(index), index.row(), index.row())
        self.endInsertRows()
        return new_item

    @loggingInfo
    def indexByLocation(self, location):
        if location in self.item_location:
            item = self.item_location[location]
            if item:
                return self.createIndex(item.row(), 0, item)
            else:
                None
        else:
            return None

    @loggingInfo
    def itemByLocation(self, location):
        if location in self.item_location:
            return self.item_location[location]
        else:
            return None

    @loggingInfo
    def deleteItem(self, item):
        index = self.indexByLocation(item.location)
        self.beginRemoveRows(self.parent(index), index.row(), index.row())
        del self.item_location[item.location]
        item.parentItem.removeChild(index.row())
        self.endRemoveRows()

    @loggingInfo
    def changeItemIcon(self, location, role):
        index = self.indexByLocation(location)
        if index is not None:
            modelitem = self.item(index)
            modelitem.role = role
            self.dataChanged.emit(index, index)


class TreeItem:
    log = logging.getLogger('{}.TreeItem'.format(__name__))

    @loggingInfo
    def __init__(self, label, role, location, data=None, parent=None):
        self.childItems = []
        self.description = None
        self.itemLabel = [label[0]]
        if len(label) > 1:
            if str(label[1].value()) != "":
                self.description = str(label[1].value)
        self.role = role
        self.itemData = data
        self.updateRole()
        self.parentItem = parent
        self.location = location

    @loggingInfo
    def updateRole(self):
        if self.role == IcepapTreeModel.SYSTEM:
            if self.itemData.conflict == Conflict.NO_CONNECTION:
                self.role = IcepapTreeModel.SYSTEM_ERROR
            elif self.itemData.child_conflicts > 0:
                self.role = IcepapTreeModel.SYSTEM_WARNING
        elif self.role == IcepapTreeModel.DRIVER or \
                self.role == IcepapTreeModel.DRIVER_CFG:
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
            elif self.itemData.mode == Mode.CONFIG:
                self.role = IcepapTreeModel.DRIVER_CFG
        return self.role

    @loggingInfo
    def appendChild(self, child, index=None):
        if index is None:
            self.childItems.append(child)
        else:
            self.childItems.insert(index.row(), child)

    @loggingInfo
    def removeChild(self, row):
        del self.childItems[row]

    @loggingInfo
    def child(self, row):
        return self.childItems[row]

    @loggingInfo
    def childCount(self):
        return len(self.childItems)

    @loggingInfo
    def columnCount(self):
        return len(self.itemLabel)

    @loggingInfo
    def data(self, column):
        return self.itemLabel[column]

    @loggingInfo
    def parent(self):
        return self.parentItem

    @loggingInfo
    def changeLabel(self, label):
        if len(label) > 1:
            if label[1] != "":
                self.description = label[1]

        self.itemLabel = [label[0]]

    @loggingInfo
    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    @loggingInfo
    def solveConflict(self):
        if self.role == IcepapTreeModel.DRIVER_WARNING or \
                self.role == IcepapTreeModel.DRIVER_NEW:
            self.role = IcepapTreeModel.DRIVER
            self.itemData.conflict = Conflict.NO_CONFLICT
            self.parentItem.notifySolvedConflict()
        elif self.role == IcepapTreeModel.DRIVER_ERROR:
            self.parentItem.notifySolvedConflict()

    @loggingInfo
    def notifySolvedConflict(self):
        if self.role == IcepapTreeModel.SYSTEM_WARNING:
            self.itemData.child_conflicts -= 1
            if self.itemData.child_conflicts == 0:
                self.role = IcepapTreeModel.SYSTEM
        elif self.role == IcepapTreeModel.CRATE:
            self.parentItem.notifySolvedConflict()

    @loggingInfo
    def getIcepapSystem(self):
        if self.role == IcepapTreeModel.SYSTEM or \
                self.role == IcepapTreeModel.SYSTEM_WARNING or \
                self.role == IcepapTreeModel.SYSTEM_ERROR or \
                self.role == IcepapTreeModel.SYSTEM_OFFLINE:
            return self.itemData
        if self.role == IcepapTreeModel.CRATE:
            return self.parentItem.getIcepapSystem()
        else:
            return self.parentItem.getIcepapSystem()
