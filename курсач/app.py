import sys
from PyQt5.uic.properties import QtWidgets
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtWidgets import QTableWidgetItem
import const
import ui
import time
import random
# import bluetooth
#
# sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# sock.connect(("SmartHome", 1))
import PyQt5.QtBluetooth as bl

class Window(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.build_handlers()
        

    def build_handlers(self):
        self.pushButton.clicked.connect(self.pushButtonClick)
        self.tempSlider.valueChanged.connect(self.sliderMove)


    def tempUpdate(self):
        #answer = getTempFromRooms()
        answer = [random.randrange(-25,25) for i in range(5)]
        print(answer)
        for i in range(len(answer)):
            item = QTableWidgetItem(str(answer[i]))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i,0,item)
        
    def sliderMove(self):
        self.tempValue.setText(str(self.tempSlider.value()))
        
    def pushButtonClick(self):
        room = const.rooms[self.roomBox.currentText()]
        t = self.tempSlider.value()
        

def getTempFromRooms(sock,tempDict:dict):
    command = "YT0\r\n"
    try:
        sock.send(command)
        response = sock.recv(88)
        answer = response.decode('utf-8')
        return answer.split('#')[1:6]
    except Exception: 
        return None

def strControl(room, power):
    if power<0:
        if power%10==0:
            return 'XC{}q\r\n'.format(room)
        else:
            return 'XC{}{}\r\n'.format(room,abs(power))
    else:
        if power%10==0:
            return 'XH{}q\r\n'.format(room)
        else:
            return 'XH{}{}\r\n'.format(room,abs(power))

def funControl(t_old, t_now, t_need, power):#return UP DOWN STOP
    neuron_h = 1 if t_now - t_old>=0.3 else 0
    neuron_c = 1 if t_now - t_old<=-0.3 else 0

    neuron_dt_h = 1 if t_need - t_now>=0.5 else 0
    neuron_dt_c = 1 if t_need - t_now<=-0.5 else 0

    neuron_up = 1 if neuron_dt_h-neuron_h>=1 else 0
    neuron_down = 1 if neuron_dt_c-neuron_c>=1 else 0
    neuron_stop = 1 if neuron_h+neuron_c-neuron_up-neuron_down>=1 else 0
    # print('{},{},{},{}'.format(neuron_h,neuron_c,neuron_dt_h,neuron_dt_c))
    if neuron_up>0:
        return power+1
    elif neuron_down>0:
        return power-1
    elif neuron_stop>0:
        return power
    # return neuron_up, neuron_down, neuron_stop           

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    timer = QTimer()
    timer.timeout.connect(window.tempUpdate)
    timer.start(2000)
    app.exec_()

if __name__ == "__main__":
    main()
