##################################################
# Tube Cutter GUI
#
# Ezra Kainz
# 14 Jun 2023
##################################################


from PyQt5 import QtCore, QtWidgets, QtSerialPort, uic

class Cutter(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Cutter, self).__init__(parent) # Call the inherited classes __init__ method
        uic.loadUi('cutter.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.cutButton.clicked.connect(self.cut)
        self.resetButton.clicked.connect(self.reset)
        self.serial = QtSerialPort.QSerialPort(
            '/dev/ttyUSB0',
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive
        )


    def cut(self): #make this non blocking + catch no cnnection error and display in red to consoleTextbox
        self.cutButton.setEnabled(False)
        time.sleep(1) #replace with wait till end of message - allow reset button to break
        self.send(self.length.text().encode())
        self.consoleTextbox.append(self.length.text())
        time.sleep(1) #replace with wait till end of message - allow reset button to break
        self.send(self.cuts.text().encode())
        self.consoleTextbox.append(self.cuts.text())
        #wait until read "complete!"
        self.cutButton.setEnabled(True)


    def reset(self):
        self.send("\x03")

    def send(self, message):
        self.serial.write(message)

    #future: add reset cuts on blade + rest of info section

    @QtCore.pyqtSlot()
    def receive(self):
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
