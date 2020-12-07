from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys

class QLabelClickable(QtWidgets.QLabel):
    
    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

        self.setObjectName('obj_1')
        self.clicked = False
        self.parent = parent
        # print(f'parent: {parent}')        # parent: <__main__.MyWindow object at 0x7fe8b6f7e430>

    def mousePressEvent(self, event):
        self.clicked = True
    
    def mouseReleaseEvent(self, event):
        if self.clicked:
            label_class_name = self.metaObject().className()
            self.parent.on_click(index=1, klass=label_class_name)
            self.clicked = False


class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def on_click(self, **kwargs):
        # print(f'kwargs: {kwargs}')
        if all (k in kwargs.keys() for k in ("index","klass")):
            current_obj_klass = kwargs['klass']
            current_obj_idx = kwargs['index']
            print(f'{current_obj_klass} (index {current_obj_idx}) was clicked')
        else:
            raise Exception(f"MISSING KEYS IN {kwargs}")

    def initUI(self):
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Test with pretty QPushButton")


        #
        #   LABEL
        #

        self.label=QLabelClickable(self)                    # Custom QLabel
        self.label.setText("I am a label !")
        self.label.move(50,50)
        self.label.setToolTip('This is a QLabel')  

        #
        #   BUTTON
        #

        self.base_btn = QtWidgets.QPushButton(self)
        self.base_btn.setText("I am a button !")
        self.base_btn.move(50,120)
        self.base_btn.setToolTip('This is a QPushButton')
        self.base_btn.setObjectName('obj_2')
        base_btn_class_name = self.base_btn.metaObject().className()
        self.base_btn.clicked.connect(lambda: self.on_click(index=2, klass=base_btn_class_name))


        #
        #   PRETTY BUTTON (QPushButton like QLabel)
        #

        self.pretty_btn = QtWidgets.QPushButton(self)
        self.pretty_btn.setGeometry(50, 180, 60, 60)        # QWidget.setGeometry(x, y, w, h)
        self.pretty_btn.setFlat(True)                       # https://doc.qt.io/qt-5/qpushbutton.html#flat-prop
        self.pretty_btn.setAutoFillBackground(True)
        # setting icon and icon size to the button 
        self.pretty_btn.setIcon(QIcon('refill_warning.png')) 
        self.pretty_btn.setIconSize(QSize(50,50))
        # use css to specify no border (QPushButton like QLabel when pressed)
        self.pretty_btn.setStyleSheet(
            '''
            QPushButton::pressed {
                border:  none;
            }
            ''') 
        self.pretty_btn.setToolTip('This is a QPushButton shown like a QLabel')
        self.pretty_btn.setObjectName('obj_3')
        pretty_btn_class_name = self.pretty_btn.metaObject().className()
        self.pretty_btn.clicked.connect(lambda: self.on_click(index=3, klass=pretty_btn_class_name))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
