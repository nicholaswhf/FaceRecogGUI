from ChildrenForm3 import Ui_Form3


class ChildrenForm3_Busi(Ui_Form3):
    def setupBusi(self, Form):
        # 下面是该类的一些具体动作
        # self.retranslateUi(Dialog)  # 调用自定义的方法“retranslateUi”（详细内容见下面），参数是窗口名称，作用是修改相关窗口部件的显示名称
        self.pushButton.clicked.connect(self.lineEdit.clear)