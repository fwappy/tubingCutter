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
        self.length.valueChanged.connect(self.updateTotal)
        self.cuts.valueChanged.connect(self.updateTotal)
        self.setButton.clicked.connect(self.setMotorVars)
        self.serial = QtSerialPort.QSerialPort(         # open serial connection
            '/dev/ttyUSB0',
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive
        )
        self.serial.errorOccurred.connect(self.showError)     #connect errors
        self.reset()
        self.getMotorVars()

    @QtCore.pyqtSlot()
    def cut(self): #make this non blocking + catch no cnnection error and display in red to consoleTextbox
        self.cutButton.setEnabled(False)
        self.send(self.length.text())
        time.sleep(1) #replace with wait till end of message - allow reset button to break
        self.send(self.cuts.text())
        #wait until read "complete!"
        self.getMotorVars()
        self.cutButton.setChecked(False)
        self.cutButton.setEnabled(True)

    @QtCore.pyqtSlot()
    def reset(self):
        if self.serial.isOpen():
            self.serial.close()
        self.serial.open(QtCore.QIODevice.ReadWrite)
        if self.serial.isOpen():
            self.serial.write(b'\x03') #send ctrl-c

    #future: add reset cuts on blade + rest of info section

    def send(self, text):
        self.serial.write(text.encode())
        self.serial.write(b'\r') #send newline
        self.serial.waitForBytesWritten() # blocking

    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            self.consoleTextbox.append(text)

    def waitforText(self, text): #fix blocking
        while True:
            text = self.serial.readLine().data().decode()
            if text == "complete!":
                break

    def updateTotal(self): #updates the total LCDNumber
        self.total.display(self.length.value() * self.cuts.value())

    def setMotorVars(self):
        #self.send(b'figurethisout\r')
        print("setMotorVars Not Implemented")

    def getMotorVars(self):
        #self.send(b'figurethisout\r')
        print("getMotorVars not Implemented")

    def showError(self):
        if self.serial.error() != self.serial.NoError:
            self.consoleTextbox.append('<font color="red">' + self.serial.errorString() + '<\font>')


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Cutter()
    w.show()
    sys.exit(app.exec_())
