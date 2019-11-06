import sys,os,subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore,QtGui,QtWidgets,QtSql
import qtawesome

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
    def initUI( self ):
        self.setFixedSize(1000,500)
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('FaceEntrance.sqlite')
        db.open()

        #设置全局布局为水平布局，设置标题与初始大小窗口
        self.hbox=QHBoxLayout()
        self.setWindowTitle("FaceEntrance Manager")
        self.setObjectName("MainWindow")
        #实例化QFrame控件
        self.topLeft=MenuFrame()
        self.topLeft.setFrameShape(QFrame.StyledPanel)
        self.topLeft.menu_add_member.clicked.connect(self.toaddmember)
        self.topLeft.menu_lookup_member.clicked.connect(self.tolookupmember)
       
        self.navigater=TopFrame()
        self.navigater.setObjectName("Navigater")
        self.navigater.btn_1.clicked.connect(self.tovisitor)
        self.navigater.btn_3.clicked.connect(self.tomember)
        bottom=QFrame()
        #bottom.setFrameShape()
        #实例化QSplitter控件并设置初始为水平方向布局
        self.splitter1=QSplitter(Qt.Horizontal)
        
        self.QueryMember=QueryFrame()

        self.AddMember=TextFrame()

        self.QueryRecord=RecordFrame()

        #recordleft
        self.record_manager_menu=RecordMenu()


        self.splitter1.addWidget(self.topLeft)
        self.splitter1.addWidget(self.AddMember)

        self.splitter1.setSizes([300,650])
        self.splitter2=QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.navigater)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(bottom)

        #设置窗体全局布局以及子布局的添加
        self.hbox.addWidget(self.splitter2)
        self.hbox.setContentsMargins(0,0,0,0)
        self.hbox.setSpacing(0)
        widget=QWidget()
        widget.setLayout(self.hbox)
        self.setCentralWidget(widget)
        self.setStyleSheet("#Navigater{background:white} #MainWindow{background:#e5e5e5}")
    def toaddmember(self):
        self.splitter1.widget(1).setParent(None)
        self.splitter1.insertWidget(1, self.AddMember)
    def tolookupmember(self):
        self.splitter1.widget(1).setParent(None)
        self.splitter1.insertWidget(1, self.QueryMember)
    def torecord(self):
        self.splitter1.widget(1).setParent(None)
        self.splitter1.insertWidget(1,self.QueryRecord)
    def tovisitor(self):
        self.splitter1.widget(1).setParent(None)
        self.splitter1.insertWidget(1,self.QueryRecord)
        self.splitter1.widget(0).setParent(None)
        self.splitter1.insertWidget(0,self.record_manager_menu)
    def tomember(self):
        self.splitter1.widget(1).setParent(None)
        self.splitter1.insertWidget(1,self.AddMember)
        self.splitter1.widget(0).setParent(None)
        self.splitter1.insertWidget(0,self.topLeft)
class TopFrame(QFrame):
    def __init__(self):
        super(TopFrame,self).__init__()
        self.initUi()
    def initUi(self):
        self.setFixedSize(1000,50)
        self.appname=QLabel("FaceEntrance",self)
        self.appname.setObjectName("AppName")
        self.appname.move(100,15)
        self.camera=QLabel('Video',self)
        self.camera.setObjectName('Camera')
        self.camera.setFixedSize(30,30)
        self.camera.setAutoFillBackground(True)
        self.camera.move(50,10)
        img = QImage("./A.png")
        size = QSize(30, 30)
        pixImg = QPixmap.fromImage(img.scaled(size, Qt.IgnoreAspectRatio))
        self.camera.setPixmap(pixImg)

        self.btn_1=QPushButton(qtawesome.icon('fa.bug',color='#5691d3'),"Visitor",self)
        self.btn_1.setObjectName("Visit")
        self.btn_1.move(350,0)
        self.btn_1.setFixedSize(125,50)
        self.btn_2=QPushButton(qtawesome.icon('fa.bomb',color='#5691d3'),"Setting",self)
        self.btn_2.setObjectName("Visit")
        self.btn_2.move(475,0)
        self.btn_2.setFixedSize(125,50)
        self.btn_3=QPushButton(qtawesome.icon('fa.adjust',color='#5691d3'),"Member",self)
        self.btn_3.setObjectName("Visit")
        self.btn_3.move(600,0)
        self.btn_3.setFixedSize(125,50)
        self.setStyleSheet('''QPushButton{border:none;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;;color:#5691d3} QPushButton:hover{background:#eef4fb;color:#5691d3;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}QLabel{background:#ffffff;color:#5691d3} ''')

class MenuFrame(QFrame):
    def __init__(self):
        super(MenuFrame,self).__init__()
        self.setFixedSize(300,388)
        self.setObjectName("Menu")
        self.setStyleSheet("#Menu{margin:20 50 0 50;background:white;border:none}QPushButton{margin:20 50 0 50;border:none;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;;color:#5691d3} QPushButton:hover{border-right:5px solid #5691d3;background:#eef4fb;color:#5691d3;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;}")
        self.menu_add_member=QPushButton("添加成员",self)
        self.menu_add_member.setFixedSize(300,70)
        self.menu_add_member.move(0,0)
        self.menu_lookup_member=QPushButton("查看成员",self)
        self.menu_lookup_member.setFixedSize(300,70)
        self.menu_lookup_member.move(0,50)

class RecordMenu(QFrame):
    def __init__(self):
        super(RecordMenu,self).__init__()
        self.setFixedSize(300,388)
        self.setObjectName("RecordMenu")
        self.setStyleSheet("#RecordMenu{margin:20 50 0 50;background:white;border:none}QPushButton{margin:20 50 0 50;border:none;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;;color:#5691d3} QPushButton:hover{border-right:5px solid #5691d3;background:#eef4fb;color:#5691d3;font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;}")
        self.menu_add_member=QPushButton("查看记录",self)
        self.menu_add_member.setFixedSize(300,70)
        self.menu_add_member.move(0,0)

class TextFrame(QFrame):
    def __init__(self):
        super(TextFrame,self).__init__()
        self.setFixedSize(650,388)
        self.setObjectName("Text")
        
        self.ins=QLabel("成员图像与信息输入",self)
        self.ins.setObjectName("Prompt")
        self.ins.move(20,40)
        self.ins.setFixedSize(600,20)
        
        self.name=QLabel("*成员姓名：",self)
        self.name.setObjectName("MemberName")
        self.name.move(144,80)
        #self.name.setFixedSize(60,17)
        self.namevalue=QLineEdit(self)
        self.namevalue.move(211,75)
        self.namevalue.setFixedSize(331,27)
        
        self.id=QLabel("*成员编号：",self)
        self.id.setObjectName("Id")
        self.id.move(144,125)
        #self.name.setFixedSize(60,17)
        self.idvalue=QLineEdit(self)
        self.idvalue.move(211,115)
        self.idvalue.setFixedSize(331,27)

        self.image=QLabel("*图像上传：",self)
        self.image.setObjectName("Image")
        self.image.move(144,170)

        self.imageValue=myLabel('Image',self)
        self.imageValue.setObjectName('ImageValue')
        self.imageValue.setFixedSize(50,50)
        self.imageValue.setAutoFillBackground(True)
        self.imageValue.move(220,155)
        img = QImage("./B.png")
        size = QSize(50, 50)
        pixImg = QPixmap.fromImage(img.scaled(size, Qt.IgnoreAspectRatio))
        self.imageValue.setPixmap(pixImg)
        self.imageValue.clicked.connect(self.select)

        self.imagetext=myLabel(" 上传图像",self)
        self.imagetext.setObjectName("ImageText")
        self.imagetext.setFixedSize(44,10)
        self.imagetext.move(223,190)
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.5)
        self.imagetext.setGraphicsEffect(op)
        self.imagetext.clicked.connect(self.select)

        #建议上传图片尺寸为640*640，大小不超过1M
        self.tiptext=QLabel("建议上传文件夹内包含20张图片,图片大小不超过1M",self)
        self.tiptext.setObjectName("TipText")
        #self.imagetext.setFixedSize(44,10)
        self.tiptext.move(299,181)

        #self.name.setFixedSize(60,17)

        self.addbutton=QPushButton("添加",self)
        self.addbutton.setObjectName("AddButton")
        self.addbutton.move(220,213)
        self.addbutton.setFixedSize(49,21)
        self.addbutton.clicked.connect(self.add)

        self.trainbutton=QPushButton("训练",self)
        self.trainbutton.setObjectName("TrainButton")
        self.trainbutton.move(285,213)
        self.trainbutton.setFixedSize(49,21) 
        self.trainbutton.clicked.connect(self.train)  

        self.fileslist=[]    

        self.setStyleSheet('''QPushButton{border-radius:3px;color:white;background:#5691d3;border:none;font-size:10px;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}#TipText{font-size:10px;color:#909090}#ImageValue{background:white}#ImageText{background:transparent;background:#909090;color:white;font-size:9px;border-bottom-left-radius:5px;border-bottom-right-radius:5px}QLineEdit{border-radius:2px;font-size:12px;border:1px solid #a6a6a6;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}#Text{margin:20 0 0 0;background:white;border:none} QLabel{font-size:11px;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;} #Prompt{background:#eef4fb;padding-left:16;}''')

    def add(self):
        print("add")
        msg="success"
        coms=""
        if(len(self.idvalue.text())==0):
            reply = QMessageBox.information(self,"Information","Invalid Input")
            return 
        out_dir="/home/whf/桌面/faceR/GUIQt/traindata/"+str(self.idvalue.text()+"/")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        for file in self.fileslist:
            fileinfo = QFileInfo(file)
            filename=fileinfo.fileName()
            com="cp -r "+file+" "+out_dir+filename
            res=os.system(com)
            print(res)
        #db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        #db.setDatabaseName('FaceEntrance.sqlite')
        #db.open()
        #print(res)
        query = QtSql.QSqlQuery()
        res=query.exec_("insert into information values("+str(self.idvalue.text())+",'"+str(self.namevalue.text())+"' , 0)")
        print(res)
        #db.close()
        reply = QMessageBox.information(self,"Information",msg)


    def select(self):
        print("##")
        fileslist=[]
        files, ok1 = QFileDialog.getOpenFileNames(self, "多文件选择", "./", "所有文件 (*);;文本文件 (*.txt)")
        for file in files:
            fileinfo = QFileInfo(file)
            if(fileinfo.suffix()=="jpg" or fileinfo.suffix()=="png" ):
                fileslist.append(file)
        self.fileslist=fileslist

    def train2(self):
        res=os.system('python /home/whf/桌面/faceR/openface/util/align-dlib.py ../traindata align outerEyesAndNose ../traindata-Aligned')
        if(res!=0):
            return
        if(os.path.exists("/home/whf/桌面/faceR/GUIQt/traindata-Aligned/cache.t7")):
            os.system('rm /home/whf/桌面/faceR/GUIQt/traindata-Aligned/cache.t7')
        res=os.system('luajit /home/whf/桌面/faceR/openface/batch-represent/main.lua -outDir ../train-features -data ../traindata-Aligned')
        if(res!=0):
            return
        res=os.system('python /home/whf/桌面/faceR/openface/demos/classifier.py train ../train-features')

    def train(self):
        res=subprocess.call('python /home/whf/桌面/faceR/openface/util/align-dlib.py ../traindata align outerEyesAndNose ../traindata-Aligned',shell=True)
        if(res!=0):
            return
        if(os.path.exists("/home/whf/桌面/faceR/GUIQt/traindata-Aligned/cache.t7")):
            os.system('rm /home/whf/桌面/faceR/GUIQt/traindata-Aligned/cache.t7')
        res=subprocess.call('luajit /home/whf/桌面/faceR/openface/batch-represent/main.lua -outDir ../train-features -data ../traindata-Aligned',shell=True)
        
        if(res!=0):
            return
        res=subprocess.call('python /home/whf/桌面/faceR/openface/demos/classifier.py train ../train-features',shell=True)
        

class myLabel(QLabel):
    clicked=pyqtSignal()
    def mouseReleaseEvent(self,QMouseEvent):
        if QMouseEvent.button()==Qt.LeftButton:
            self.clicked.emit()

class QueryFrame(QFrame):
    def __init__(self):
        super(QueryFrame,self).__init__()
        self.table_widget = QTableView()
        #self.table_widget.setFixedSize(400,300)
        self.table_widget.setObjectName("TableWidget")
        self.model = QtSql.QSqlTableModel()
        self.model.setTable('information') # 设置数据模型的数据表
        self.table_widget.setModel(self.model)
        res=self.model.select()
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange) # 允许字段更改
        #self.model.setItem("1000",'HELLO')
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #item0 = QTableWidgetItem(column1)
        #item0.setFlags( QtCore.Qt.ItemIsEnabled)
        layout=QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        print(res)
        self.setFixedSize(650,388)
        self.setObjectName("Text")
        print(self.model)
        self.table_widget.setAlternatingRowColors(1);
        self.fileslist=[]    

        self.setStyleSheet('''QTableView::item:!alternate:!selected{background-color:rgb(200, 200, 200);}#TableWidget{border:none;gridline-color:#eef4fb;alternate-background-color:rgb(220, 220, 220);selection-background-color: rgb(210,210,210);background:rgb(240,240,240)}QPushButton{border-radius:3px;color:white;background:#5691d3;border:none;font-size:10px;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}#TipText{font-size:10px;color:#909090}#ImageValue{background:white}#ImageText{background:transparent;background:#909090;color:white;font-size:9px;border-bottom-left-radius:5px;border-bottom-right-radius:5px}QLineEdit{border-radius:2px;font-size:12px;border:1px solid #a6a6a6;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}#Text{margin:20 0 0 0;background:white;border:none} QLabel{font-size:11px;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;} #Prompt{background:#eef4fb;padding-left:16;}''')

class RecordFrame(QFrame):
    def __init__(self):
        super(RecordFrame,self).__init__()
        self.table_widget = QTableView()
        #self.table_widget.setFixedSize(400,300)
        self.table_widget.setObjectName("TableWidget")
        self.model = QtSql.QSqlTableModel()
        self.model.setTable('record') # 设置数据模型的数据表
        self.table_widget.setModel(self.model)
        res=self.model.select()
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange) # 允许字段更改
        #self.model.setItem("1000",'HELLO')
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #item0 = QTableWidgetItem(column1)
        #item0.setFlags( QtCore.Qt.ItemIsEnabled)
        layout=QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        print(res)
        self.setFixedSize(650,388)
        self.setObjectName("Text")
        print(self.model)
        self.table_widget.setAlternatingRowColors(1);
        self.fileslist=[]    

        self.setStyleSheet('''QTableView::item:!alternate:!selected{background-color:rgb(200, 200, 200);}#TableWidget{border:none;gridline-color:#eef4fb;alternate-background-color:rgb(220, 220, 220);selection-background-color: rgb(210,210,210);background:rgb(240,240,240)}QPushButton{border-radius:3px;color:white;background:#5691d3;border:none;font-size:10px;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}#TipText{font-size:10px;color:#909090}#ImageValue{background:white}#ImageText{background:transparent;background:#909090;color:white;font-size:9px;border-bottom-left-radius:5px;border-bottom-right-radius:5px}QLineEdit{border-radius:2px;font-size:12px;border:1px solid #a6a6a6;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}#Text{margin:20 0 0 0;background:white;border:none} QLabel{font-size:11px;font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;} #Prompt{background:#eef4fb;padding-left:16;}''')


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=MainWindow()
    demo.show()
    sys.exit(app.exec_())
