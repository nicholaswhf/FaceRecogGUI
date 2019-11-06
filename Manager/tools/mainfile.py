from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication,
                             QToolBox, QPushButton, QLabel,
                             QTreeWidget, QTreeWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from MainForm import Ui_MainWindow
from ChildrenForm import Ui_Form
from ChildrenForm2 import Ui_Form2
from ChildrenForm3_yewuwenjian import ChildrenForm3_Busi

import sys

class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()

        # 主窗口初始化时实现主窗口布局
        self.setupUi(self)

        # 创建一个QTreeWidget部件
        self.tree = QTreeWidget()
        # 设置部件的列数为1
        self.tree.setColumnCount(1)
        # 设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        # self.tree.setHeaderLabels(['节点名称'])
        # 设置表头信息：隐藏表头
        self.tree.setHeaderHidden(1)
        # 设置root和root2为self.tree的子树，所以root和root2就是跟节点
        root = QTreeWidgetItem(self.tree)
        root2 = QTreeWidgetItem(self.tree)

        # 设置root节点的打开/关闭状态下的不同的图片
        icon = QIcon()
        # 节点打开状态
        icon.addPixmap(QPixmap("./folder open.png"), QIcon.Normal, QIcon.On)
        # 节点关闭状态　　
        icon.addPixmap(QPixmap("./folder closed.png"), QIcon.Normal, QIcon.Off)
        root.setIcon(0, icon)

        # 设置根节点的名称
        root.setText(0, '第一节点')
        root2.setText(0, '第二节点')

        # 为root节点设置子结点
        child1 = QTreeWidgetItem(root)

        # 设置child1节点的图片
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("./Original Point.png"), QIcon.Normal)
        child1.setIcon(0, icon2)

        child1.setText(0, 'child1')
        # child1.setText(1, 'name1')
        child2 = QTreeWidgetItem(root)
        # 设置child2节点的图片
        child2.setIcon(0, icon2)
        child2.setText(0, 'child2')
        # child2.setText(1, 'name2')
        child3 = QTreeWidgetItem(root)

        # 设置child3节点的打开 / 关闭状态下的不同的图片
        child3.setIcon(0, icon)

        child3.setText(0, 'child3')
        child4 = QTreeWidgetItem(child3)
        # 设置child4节点的图片
        child4.setIcon(0, icon2)
        child4.setText(0, 'child4')
        # child4.setText(1, 'name4')

        # 为root2节点设置子结点
        child1 = QTreeWidgetItem(root2)
        child1.setText(0, 'child1')
        # child1.setText(1, 'name1')
        child2 = QTreeWidgetItem(root2)
        child2.setText(0, 'child2')
        # child2.setText(1, 'name2')
        child3 = QTreeWidgetItem(root2)
        child3.setText(0, 'child3')
        child4 = QTreeWidgetItem(child3)
        child4.setText(0, 'child4')

        # 实例化QToolBox
        self.toolBox = QToolBox()

        #  设置左侧导航栏 toolBox 初始化时的宽度
        # self.toolBox.setStyleSheet("QToolBoxButton { min-width:180px;}")

        # 设置左侧导航栏 toolBox 在左右拉拽时的最小宽度
        self.toolBox.setMinimumWidth(100)

        # 给QToolBox添加子项目；添加了3个子项目
        self.toolBox.addItem(self.tree, QIcon('snapshot.png'), "设置")
        self.toolBox.addItem(QPushButton("Tab1 "), "数据分析")
        self.toolBox.addItem(QLabel("Tab2 "), "生产动态分析测试与建模")

        self.toolBox.setCurrentIndex(0)  # 设置软件启动时默认打开导航栏的第几个 Item；这里设置的是打开第1个 Item。

        # 给QSsplitter添加第一个窗体（QToolBox）
        self.splitter.addWidget(self.toolBox)

        # self.verticalLayout.addWidget(self.toolBox)


        # QToolBox 的 QToolBoxButton 按钮切换时发出的信号；也是信号与槽的连接
        self.toolBox.currentChanged.connect(self.mylinktowindows)



        # 主窗口初始化时实例化子窗口1和子窗口2
        self.child = ChildrenForm()
        self.child2 = ChildrenForm2()
        self.child3 = ChildrenForm3()

        # 在主窗口的QSplitter里添加子窗口
        self.splitter.addWidget(self.child)

        # 设置分割器QSplitter初始化时各个子窗体的大小；下面是两个子窗体。
        self.splitter.setSizes([180, 700])


        #  下面一行为设置 QSplitter 分割器伸缩大小因子，但是这样设置全屏后导航栏放大了比较好看；不清楚原因。
        self.splitter.setStretchFactor(0, 0)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。
        self.splitter.setStretchFactor(1, 1)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。

        #  设置 QSplitter 分割器各部分最小化时的情况，设置为“False”意味着左右拉动分隔栏时各部分不会消失；此设置也可以在界面设计时在 QtDesigner 里设置。
        self.splitter.setChildrenCollapsible(False)

        #  设置 QSplitter 分割器随主窗口自适应大小变化。此设置也可以在界面设计时在 QtDesigner 里设置。
        self.splitter.setAutoFillBackground(True)

        # 隐藏QSplitter里的窗体；下面代码里的“widget(0)”表示隐藏第1个窗体，“widget(1)”则表示隐藏第2个窗体。
        # self.splitter.widget(1).hide()
        # self.splitter.widget(1).setVisible(1)  # setVisible(1) 里面的数字 1 表示真；数字 0 表示假。

        # 删除（隐藏？）QSplitter里的窗体；下面代码里的“widget(0)”表示隐藏第1个窗体，“widget(1)”则表示隐藏第2个窗体。
        # self.splitter.widget(1).setParent(None)
        # self.splitter.widget(1).deleteLater()

        # 在QSplitter的指定位置载入新窗体，但要先用上面的“self.splitter.widget(1).setParent(None)”命令。
        # self.splitter.insertWidget(1, self.child)

    def mylinktowindows(self):

         if self.toolBox.currentIndex() == 0:
             # 把QSplitter的指定位置的窗体从QSplitter中剥离
             self.splitter.widget(1).setParent(None)
             # 在QSplitter的指定位置载入新窗体，但要先用上面的“self.splitter.widget(1).setParent(None)”命令。
             self.splitter.insertWidget(1, self.child)
             self.splitter.setStretchFactor(0, 0)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。
             self.splitter.setStretchFactor(1, 1)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。
             #  设置 QSplitter 分割器各部分最小化时的情况，设置为“False”意味着左右拉动分隔栏时各部分不会消失；此设置也可以在界面设计时在 QtDesigner 里设置。
             self.splitter.setChildrenCollapsible(False)
             #  设置 QSplitter 分割器随主窗口自适应大小变化。此设置也可以在界面设计时在 QtDesigner 里设置。
             self.splitter.setAutoFillBackground(True)
         elif self.toolBox.currentIndex() == 1:
             self.splitter.widget(1).setParent(None)
             # 在QSplitter的指定位置载入新窗体，但要先用上面的“self.splitter.widget(1).setParent(None)”命令。
             self.splitter.insertWidget(1, self.child2)
             self.splitter.setStretchFactor(0, 0)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。
             self.splitter.setStretchFactor(1, 1)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。
             #  设置 QSplitter 分割器各部分最小化时的情况，设置为“False”意味着左右拉动分隔栏时各部分不会消失；此设置也可以在界面设计时在 QtDesigner 里设置。
             self.splitter.setChildrenCollapsible(False)
             #  设置 QSplitter 分割器随主窗口自适应大小变化。此设置也可以在界面设计时在 QtDesigner 里设置。
             self.splitter.setAutoFillBackground(True)
         elif self.toolBox.currentIndex() == 2:
             self.splitter.widget(1).setParent(None)
             # 在QSplitter的指定位置载入新窗体，但要先用上面的“self.splitter.widget(1).setParent(None)”命令。
             self.splitter.insertWidget(1, self.child3)
             self.splitter.setStretchFactor(0, 0)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。
             self.splitter.setStretchFactor(1, 1)  # 此函数用于设定：控件是否可伸缩。第一个参数用于指定控件的序号。第二个函数大于0时，表示控件可伸缩，小于0时，表示控件不可伸缩。
             #  设置 QSplitter 分割器各部分最小化时的情况，设置为“False”意味着左右拉动分隔栏时各部分不会消失；此设置也可以在界面设计时在 QtDesigner 里设置。
             self.splitter.setChildrenCollapsible(False)
             #  设置 QSplitter 分割器随主窗口自适应大小变化。此设置也可以在界面设计时在 QtDesigner 里设置。
             self.splitter.setAutoFillBackground(True)


class ChildrenForm(QWidget, Ui_Form):
    def __init__(self):
        super(ChildrenForm, self).__init__()

        # 子窗口初始化时实现子窗口布局
        self.setupUi(self)


class ChildrenForm2(QWidget, Ui_Form2):
    def __init__(self):
        super(ChildrenForm2, self).__init__()

        # 子窗口初始化时实现子窗口布局
        self.setupUi(self)

class ChildrenForm3(QWidget, ChildrenForm3_Busi):
    def __init__(self):
        super(ChildrenForm3, self).__init__()

        # 子窗口初始化时实现子窗口布局
        self.setupUi(self)
        self.setupBusi(self)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    myshow = MainForm()
    myshow.show()
    sys.exit(app.exec_())