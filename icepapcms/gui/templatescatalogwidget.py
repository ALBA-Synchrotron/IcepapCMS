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


import os
from PyQt5 import Qt, QtCore, QtWidgets
from xml.dom import minidom
import logging
from ..lib import ConfigManager
from ..helpers import loggingInfo

##########################################################################
# Templates Catalog Widget
# based on http://doc.trolltech.com/4.2/itemviews-basicsortfiltermodel.html
#
##########################################################################

CATALOG_PARAMS = ['MOTPHASES', 'MOTPOLES', 'MREGMODE', 'NVOLT', 'IVOLT',
                  'NCURR', 'CURRGAIN', 'MREGP', 'MREGI', 'MREGD', 'ANTURN',
                  'ANSTEP']

# 080731: jlidon considers that ICURR and BCURR are not needed
# 080731: jlidon considers that ANTURN adn ANSTEP must be part of the
#         catalog entries
# 090717: gcuni considers that catalogs should be param-free so any param
#         is possible


class TemplatesCatalogWidget(QtWidgets.QDialog):
    log = logging.getLogger('{}.TemplatesCatalogWidget'.format(__name__))

    @loggingInfo
    def __init__(self, master_catalog_file, pageipapdriver, parent=None):

        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.Window)

        self.pageipapdriver = pageipapdriver

        # BUILD THE CATALOG
        self.catalog = {}
        self.buildCatalog(master_catalog_file)
        config = ConfigManager()
        local_templates_dir = config.config[config.icepap]['templates_folder']
        prefix = local_templates_dir + os.sep
        local_templates = os.listdir(local_templates_dir)
        for local_template in local_templates:
            try:
                self.buildCatalog(prefix + local_template)
            except Exception:
                pass

        self.proxyModel = Qt.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.createModel())

        self.proxyGroupBox = QtWidgets.QGroupBox()
        self.proxyGroupBox.setFlat(True)

        self.proxyView = QtWidgets.QTreeView()
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)
        self.proxyView.setSortingEnabled(True)
        # AT THE ISG LAB, THIS METHOD IS NOT AVAILABLE...
        self.proxyView.doubleClicked.connect(self.rowDoubleClicked)

        self.filterPatternLineEdit = QtWidgets.QLineEdit()
        self.filterPatternLabel = QtWidgets.QLabel("&Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)
        self.filterPatternLineEdit.textChanged.connect(
            self.filterRegExpChanged)

        self.filterColumnComboBox = QtWidgets.QComboBox()
        # ITEMS HAVE BEEN FILLED AT THE self.buildCatalog CALL
        model = self.proxyModel.sourceModel()
        for column in range(model.columnCount()):
            self.filterColumnComboBox.addItem(
                model.horizontalHeaderItem(column).text())
        self.filterColumnLabel = QtWidgets.QLabel("Filter &column:")
        self.filterColumnLabel.setBuddy(self.filterColumnComboBox)
        self.filterColumnComboBox.currentIndexChanged.connect(
            self.filterColumnChanged)

        self.chkAutoClose = QtWidgets.QCheckBox("Auto close")
        self.chkAutoClose.setChecked(True)

        self.proxyLayout = QtWidgets.QGridLayout()

        self.proxyLayout.addWidget(self.filterColumnLabel, 0, 0)
        self.proxyLayout.addWidget(self.filterColumnComboBox, 0, 1)
        self.proxyLayout.addWidget(self.filterPatternLineEdit, 0, 2, 1, 2)
        self.proxyLayout.addWidget(self.chkAutoClose, 0, 4)

        self.proxyLayout.addWidget(self.proxyView, 1, 0, 1, 5)

        self.proxyGroupBox.setLayout(self.proxyLayout)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.proxyGroupBox)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("IcepaCMS Templates Catalog")
        self.resize(750, 600)

        self.proxyView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.proxyView.setColumnWidth(0, 220)

        # BETTER FILTER ON DESCRIPTION BY DEFAULT
        self.filterColumnComboBox.setCurrentIndex(1)

        self.filterPatternLineEdit.setText("")

    @loggingInfo
    def rowDoubleClicked(self, modelindex):
        row = modelindex.row()
        # FIRST IT WAS DESIGNED TO NOT CLOSE
        # NOW, WE SHOULD RELY ON THE VALUE OF THE CHECKBOX
        # SO THE OPTION PARAMETER COULD BE REMOVED

        template_name = str(modelindex.sibling(row, 0).data())

        params = self.catalog.get(template_name)
        self.pageipapdriver.setTemplateParams(template_name, params)
        if self.chkAutoClose.isChecked():
            self.close()

    @loggingInfo
    def buildCatalog(self, catalog):
        doc = minidom.parse(catalog)
        root = doc.documentElement
        for template_node in root.getElementsByTagName('template'):
            template_name = template_node.attributes.get('template_name').value
            params = {}
            description = ""
            desc_node = template_node.getElementsByTagName('description')[
                0].firstChild
            if desc_node is not None:
                description = str(desc_node.data)
            params['description'] = description

            for param in list(template_node.attributes.keys()):
                param_value_instance = template_node.attributes.get(param)
                params[param] = param_value_instance.value
            self.catalog[str(template_name)] = params

    @loggingInfo
    def createModel(self, parent=None):
        model = Qt.QStandardItemModel(0, 2, self)
        model.setHeaderData(0, QtCore.Qt.Horizontal,
                            QtCore.QVariant("Template"))
        model.setHeaderData(1, QtCore.Qt.Horizontal,
                            QtCore.QVariant("Description"))

        for template_name in list(self.catalog.keys()):
            self.addTemplate(model, template_name,
                             self.catalog[template_name]['description'])

        return model

    @loggingInfo
    def addTemplate(self, model, template_name, description):
        model.insertRow(0)
        model.setData(model.index(0, 0), QtCore.QVariant(template_name))
        model.setData(model.index(0, 1), QtCore.QVariant(description))
        model.item(0, 0).setFlags(Qt.Qt.ItemIsSelectable)
        model.item(0, 1).setFlags(Qt.Qt.ItemIsSelectable)

    @loggingInfo
    def filterRegExpChanged(self):
        caseSensitivity = QtCore.Qt.CaseInsensitive
        syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.RegExp)
        # Requested to use 'space' for joining words in an 'OR' operator
        filtertext = str(self.filterPatternLineEdit.text())
        filtertext = filtertext.lstrip().rstrip()
        words = filtertext.split(' ')
        if len(words) > 1:
            filtertext = '(' + ' | '.join(words) + ')'
        regExp = QtCore.QRegExp(str(filtertext), caseSensitivity, syntax)

        self.proxyModel.setFilterRegExp(regExp)
        # In case of just one match, auto-select it
        if self.proxyView.model().rowCount() == 1:
            self.proxyView.selectAll()
        else:
            self.proxyView.selectionModel().clear()

    @loggingInfo
    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(
            self.filterColumnComboBox.currentIndex())

    @loggingInfo
    def closeEvent(self, event):
        self.close()
        event.accept()


if __name__ == '__main__':
    import sys
    from pkg_resources import resource_filename
    app = QtWidgets.QApplication(sys.argv)
    file_name = resource_filename('icepapcms.templates',
                                  'catalog.xml')
    w = TemplatesCatalogWidget(file_name, None)
    w.show()
    sys.exit(app.exec_())