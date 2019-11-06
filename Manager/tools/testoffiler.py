import random, sys
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import *
from PyQt5 import QtCore,QtGui,QtWidgets,QtSql
 
class NumberSortModel(QtSql.QSortFilterProxyModel):
 
    def lessThan(self, left, right):
        print("lvalue", left.data())
        print("lvalue", right.data())
        lvalue = left.data()
        rvalue = right.data()
        return lvalue < rvalue
 
 
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    model = QStandardItemModel(5, 5)
    random.seed()
    for i in range(5):
        for j in range(5):
            item = QStandardItem()
            item.setData(random.randint(-500, 500)/10.0, Qt.DisplayRole)
            model.setItem(i, j, item)
     
    proxy = NumberSortModel()
    proxy.setSourceModel(model)
     
    view = QTableView()
    view.setModel(proxy)
    view.setSortingEnabled(True)
    view.show()
    sys.exit(app.exec_())