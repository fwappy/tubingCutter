##################################################
# Tube Cutter GUI
#
# Ezra Kainz
# 14 Jun 2023
##################################################

import time
from PyQt5 import QtCore, QtWidgets, QtSerialPort, uic

class Cutter(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Cutter, self).__init__(parent)            # Call the inherited classes __init__ method
        uic.loadUi('cutter.ui', self)                   # Load the .ui file
        self.show() # Show the GUI
        self.cutButton.clicked.connect(self.cut)        # connect buttons
        self.resetButton.clicked.connect(self.reset)
        self.serial = QtSerialPort.QSerialPort(         # open serial connection
            '/dev/ttyUSB0',
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive
        )
        self.serial.open(QtCore.QIODevice.ReadWrite)
        self.reset()

    @QtCore.pyqtSlot()
    def cut(self): #make this non blocking + catch no cnnection error and display in red to consoleTextbox
        self.cutButton.setEnabled(False)
        if self.serial.isOpen():
            self.serial.write(self.length.text().encode())
            self.serial.write(b'\r') #send newline
            self.consoleTextbox.append(self.length.text()) #update textbox
            time.sleep(5) #replace with wait till end of message - allow reset button to break
            self.serial.write(self.cuts.text().encode())
            self.serial.write(b'\r')
            self.consoleTextbox.append(self.cuts.text())
            #wait until read "complete!"
        else:
            self.conErr()
        self.cutButton.setChecked(False)
        self.cutButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def reset(self):
        if self.serial.isOpen():
            self.serial.write(b'\x03')
        else:
            self.conErr()

    def conErr(self):
        self.consoleTextbox.append("Error: No serial connection to cutter") #make red

    #future: add reset cuts on blade + rest of info section

    @QtCore.pyqtSlot()
    def receive(self): #this doesnt work
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            #text = text.rstrip('\r\n')
            self.consoleTextbox.append(text)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Cutter()
    w.show()
    sys.exit(app.exec_())
