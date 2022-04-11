from fileinput import filename
from pickle import NONE
import string
import sys
import os
import shutil
from tabnanny import filename_only
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import csv

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
from datetime import datetime
import glob

G_image, saveImage, filename_with_exttention, G_username, G_admin = None, None, None, None, None
current_csv_file = None
Global_image, G_MainImage, local_beautification, Beautifed_image = None, None, None, None


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("./src/ui/welcomescreen.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("./src/ui/login.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.homeButton.clicked.connect(self.HomeButtonClicked)
        self.admin.clicked.connect(self.checkIfAdmin)

    def HomeButtonClicked(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def checkIfAdmin(self):
        passdlg = AdminLoginDialog()
        if(passdlg.exec_() == QDialog.Accepted):
            window = AdminScreen()
            # window.show()
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def loginfunction(self):
        global G_username
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")

        else:
            try:
                with open('./src/csv/user_data.csv', 'r') as readFile:
                    reader = csv.reader(readFile)
                    for row in reader:
                        if row == []:
                            continue
                        elif str(row[1]) == str(password):
                            result_pass = str(row[1])

                if result_pass == password:
                    print("Successfully logged in.")
                    self.error.setText("")
                    G_username = user
                    today = datetime.now().date()
                    time = datetime.now().time()
                    try:
                        with open('./src/csv/users_details.csv', 'a') as appendFile:
                            writer = csv.writer(appendFile)
                            list_append = [str(user), str(
                                password), str(time), str(today)]
                            writer.writerow(list_append)
                    except:
                        print("Something went wrong while data sending")

                    msg = QMessageBox()
                    msg.setWindowTitle("Successs")
                    msg.setText("Successfully Logged In ! ")
                    x = msg.exec_()

                    Uiform = ImageLoading()
                    widget.addWidget(Uiform)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            except:
                self.error.setText("Invalid username or password")


class AdminLoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AdminLoginDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(300)
        self.setFixedHeight(150)

        layout = QVBoxLayout()

        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Enter Password.")
        self.QBtn = QPushButton()
        self.QBtn.setText(" Login")
        self.setWindowTitle('Admin Login')
        self.QBtn.clicked.connect(self.login)

        title = QLabel("Admin Login")
        font = title.font()
        font.setPointSize(16)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(self.passinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def login(self):
        global G_admin
        if(self.passinput.text() == "#123"):
            G_admin = "Admin 1"
            self.accept()
        elif(self.passinput.text() == "#1234"):
            G_admin = "Admin 2"
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong Password')


class AdminScreen(QDialog):
    def __init__(self):
        super(AdminScreen, self).__init__()
        global G_admin, current_csv_file
        loadUi("./src/ui/admin.ui", self)
        # self.loaddata()
        self.homeButton.clicked.connect(self.HomeButtonClicked)
        self.clearCache.clicked.connect(self.emptyCache)
        self.login_data.clicked.connect(self.loadUserLoginData)
        self.user_data.clicked.connect(self.loadUserDetails)
        self.formatdata.clicked.connect(self.formatData)

        self.clearCache.hide()
        self.formatdata.hide()
        self.adminName.setText("Hello "+G_admin+" !")
        path = "./src/cache"
        dir = os.listdir(path)
        if len(dir) != 0:
            self.clearCache.show()
            self.clearCache.setText("Clear " + str(len(dir))+" files")
        else:
            self.clearCache.hide()

    def formatData(self):
        global current_csv_file
        print("formatting data ")
        lines = list()
        with open("./src/csv/"+current_csv_file+".csv", 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                if row == []:
                    continue
                else:
                    lines.append(row)
        with open("./src/csv/"+current_csv_file+".csv", 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        if current_csv_file == "user_data":
            self.loadUserDetails()
        elif current_csv_file == "users_details":
            self.loadUserLoginData()

    def loadUserDetails(self):
        global current_csv_file
        current_csv_file = "user_data"
        self.formatdata.show()
        self.userDetails.setAlternatingRowColors(True)
        self.userDetails.setColumnCount(2)
        self.userDetails.horizontalHeader().setCascadingSectionResizes(False)
        self.userDetails.horizontalHeader().setSortIndicatorShown(False)
        self.userDetails.horizontalHeader().setStretchLastSection(True)
        self.userDetails.verticalHeader().setVisible(False)
        self.userDetails.verticalHeader().setCascadingSectionResizes(False)
        self.userDetails.verticalHeader().setStretchLastSection(False)
        self.userDetails.setHorizontalHeaderLabels(
            ("UserName.", "Password"))

        row_number = 1
        self.userDetails.clearContents()
        with open("./src/csv/user_data.csv", "r") as readfile:
            read = csv.reader(readfile)
            for row in read:
                row_number = row_number+1
                self.userDetails.removeRow(row_number)

        self.userDetails.insertRow(row_number)
        with open("./src/csv/user_data.csv", "r") as readfile:
            read = csv.reader(readfile)
            for row_number, row_data in enumerate(read):
                self.userDetails.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if row_data == []:
                        continue
                    else:
                        self.userDetails.setItem(
                            row_number, column_number, QTableWidgetItem(str(data)))

    def emptyCache(self):
        folder = './src/cache'
        try:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Cleared the cache ")
            msg.exec_()
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
        self.clearCache.hide()

    def HomeButtonClicked(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        global G_username
        G_username = None

    def loadUserLoginData(self):
        global current_csv_file
        current_csv_file = "users_details"
        self.formatdata.show()
        self.userDetails.setAlternatingRowColors(True)
        self.userDetails.setColumnCount(5)
        self.userDetails.horizontalHeader().setCascadingSectionResizes(False)
        self.userDetails.horizontalHeader().setSortIndicatorShown(False)
        self.userDetails.horizontalHeader().setStretchLastSection(True)
        self.userDetails.verticalHeader().setVisible(False)
        self.userDetails.verticalHeader().setCascadingSectionResizes(False)
        self.userDetails.verticalHeader().setStretchLastSection(False)
        self.userDetails.setHorizontalHeaderLabels(
            ("UserName.", "Password", "Time Of Login", "Date of Login", "Total Logged in"))

        row_number = 1
        self.userDetails.clearContents()
        with open("./src/csv/users_details.csv", "r") as readfile:
            read = csv.reader(readfile)
            for row in read:
                row_number = row_number+1
                self.userDetails.removeRow(row_number)

        self.userDetails.insertRow(row_number)
        with open("./src/csv/users_details.csv", "r") as readfile:
            read = csv.reader(readfile)
            for row_number, row_data in enumerate(read):
                self.userDetails.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if row_data == []:
                        continue
                    else:
                        self.userDetails.setItem(
                            row_number, column_number, QTableWidgetItem(str(data)))


class ImageLoading(QWidget):
    def __init__(self):
        super(ImageLoading, self).__init__()
        loadUi("./src/ui/load_image.ui", self)
        self.loadimage.clicked.connect(self.openFile)
        # self.convert.clicked.connect(self.converRGB)
        self.clearvalue.clicked.connect(self.clearImage)
        self.save.clicked.connect(self.saveFile)
        self.convert.clicked.connect(self.converRGB)
        self.beautify.clicked.connect(self.BeautifyScreen)

        pixmapi = getattr(QStyle, "SP_BrowserStop")
        icon = self.style().standardIcon(pixmapi)
        self.clearvalue.setIcon(icon)

        self.clearvalue.hide()
        self.homeButton.clicked.connect(self.HomeButtonClicked)

        global G_username, Global_image, saveImage
        self.username.setText("Welcome "+G_username)
        if (Global_image is None):
            print("in IF")
        else:
            saveImage = Global_image
            image = QtGui.QImage(
                Global_image.data, Global_image.shape[1], Global_image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.imageLabel.setPixmap(QPixmap(image))
            self.clearvalue.show()
            self.loadimage.hide()

    def BeautifyScreen(self):
        window = BeautifyScreen()
        # window.show()
        widget.addWidget(window)
        widget.setCurrentIndex(widget.currentIndex()+1)
        try:
            if Global_image is None:
                print("in if")
            else:
                print("loading beautify screen ")
                window = BeautifyScreen()
                # window.show()
                widget.addWidget(window)
                widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("Please Select The Image First!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def HomeButtonClicked(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.clearImage()
        
    def clearImage(self):
        global G_image, filename_with_exttention, saveImage, Global_image
        G_image, saveImage, filename_with_exttention, Global_image = None, None, None, None
        print("function is called")
        self.imageLabel.setPixmap(QPixmap(""))
        self.loadimage.show()
        self.clearvalue.hide()
        self.imageLabel.setText("please select photo")

    def openFile(self):
        global G_image, Global_image, G_MainImage, filename_with_exttention
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            None, "QFileDialog.getOpenFileName()", "", "Images (*.png *.xpm *.jpg )", options=options)
        if fileName:

            G_image = fileName
            filename_with_exttention = os.path.basename(fileName)
            Global_image = cv2.imread(fileName)
            G_MainImage = cv2.imread(fileName)
            self.imageLabel.setPixmap(QPixmap(fileName))
            # self.imageLabel.resize(300, 200)
            self.imageLabel.setStyleSheet("border: 1px solid black;")
            # hiding the image load button
            self.loadimage.hide()
            self.clearvalue.show()
        else:
            self.imageLabel.setText("please selete image")

    def converRGB(self):
        print("converting")
        global G_image, saveImage, filename_with_exttention, Global_image
        prototxt = "./src/files/colorization_deploy_v2.prototxt"
        caffe_model = "./src/files/colorization_release_v2.caffemodel"
        pts_npy = "./src/files/pts_in_hull.npy"
        try:
            img = G_image
            test_image = img
            # print(" in convertRGB ", test_image)
            # Loading our model
            net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)
            pts = np.load(pts_npy)

            layer1 = net.getLayerId("class8_ab")
            # print(layer1)
            layer2 = net.getLayerId("conv8_313_rh")
            # print(layer2)
            pts = pts.transpose().reshape(2, 313, 1, 1)
            net.getLayer(layer1).blobs = [pts.astype("float32")]
            net.getLayer(layer2).blobs = [np.full(
                [1, 313], 2.606, dtype="float32")]

            # Converting the image into RGB and plotting it
            # Read image from the path
            test_image = cv2.imread(test_image)
            # test_image = cv2.resize(test_image, (960, 540))
            # Convert image into gray scale
            test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
            # Convert image from gray scale to RGB format
            test_image = cv2.cvtColor(test_image, cv2.COLOR_GRAY2RGB)

            normalized = test_image.astype("float32") / 255.0
            # Converting the image into LAB
            lab_image = cv2.cvtColor(normalized, cv2.COLOR_RGB2LAB)
            # Resizing the image
            resized = cv2.resize(lab_image, (224, 224))

            # Extracting the value of L for LAB image
            L = cv2.split(resized)[0]
            L -= 50   # OR we can write L = L - 50

            # print(" Debugger 1")
            net.setInput(cv2.dnn.blobFromImage(L))
            # Finding the values of 'a' and 'b'
            ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
            # Resizing
            ab = cv2.resize(ab, (test_image.shape[1], test_image.shape[0]))

            # Combining L, a, and b channels
            L = cv2.split(lab_image)[0]
            # Combining L,a,b
            LAB_colored = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

            # Converting LAB image to RGB
            RGB_colored = cv2.cvtColor(LAB_colored, cv2.COLOR_LAB2RGB)
            # Limits the values in array
            RGB_colored = np.clip(RGB_colored, 0, 1)
            # Changing the pixel intensity back to [0,255],as we did scaling during pre-processing and converted the pixel intensity to [0,1]
            RGB_colored = (255 * RGB_colored).astype("uint8")
            # print(" Debugger 2")

            RGB_BGR = cv2.cvtColor(RGB_colored, cv2.COLOR_RGB2BGR)
            saveImage, Global_image = RGB_BGR, RGB_BGR
            filename_with_exttention = os.path.basename(img)

            # fileName1 = cv2.filter2D(fileName1, -1, kernel)
            image = QtGui.QImage(
                RGB_BGR.data, RGB_BGR.shape[1], RGB_BGR.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.imageLabel.setPixmap(QPixmap(image))


            cv2.imwrite(
                "./src/cache/Colored "+filename_with_exttention, RGB_BGR)


        except:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("Please Select The Image First!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def saveFile(self):
        global G_image, filename_with_exttention, saveImage
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "colored "+filename_with_exttention, "Images (*.png *.xpm *.jpg)", options=options
            )

            if fileName:
                cv2.imwrite(fileName, saveImage)
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Saved Image ..! ")
                msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("Perform Some Action First!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()


class BeautifyScreen(QWidget):
    def __init__(self):
        super(BeautifyScreen, self).__init__()
        loadUi("./src/ui/beautifyImage.ui", self)

        self.blur.valueChanged.connect(self.sliderChanged)
        self.blur.sliderReleased.connect(self.sldReconnect)

        self.sharpen.valueChanged.connect(self.sliderChanged)
        self.sharpen.sliderReleased.connect(self.sldReconnect)

        self.emboss.valueChanged.connect(self.sliderChanged)
        self.emboss.sliderReleased.connect(self.sldReconnect)

        pixmapi = getattr(QStyle, "SP_DialogApplyButton")
        icon = self.style().standardIcon(pixmapi)
        self.pushButton_2.setIcon(icon)
        self.pushButton_3.setIcon(icon)
        self.pushButton_4.setIcon(icon)

        self.pushButton_2.clicked.connect(self.saveTempImage)
        self.pushButton_3.clicked.connect(self.saveTempImage)
        self.pushButton_4.clicked.connect(self.saveTempImage)

        pixmapi = getattr(QStyle, "SP_DialogCancelButton")
        icon = self.style().standardIcon(pixmapi)
        self.pushButton_5.setIcon(icon)
        self.pushButton_6.setIcon(icon)
        self.pushButton_7.setIcon(icon)

        self.pushButton_5.clicked.connect(self.clearSlidder)
        self.pushButton_6.clicked.connect(self.clearSlidder)
        self.pushButton_7.clicked.connect(self.clearSlidder)

        self.backBtn.clicked.connect(self.imgeLoadfunction)
        global Global_image, Beautifed_image
        Beautifed_image = Global_image
        if Beautifed_image is None:
            print("in if")
        else:
            image = QtGui.QImage(
                Beautifed_image.data, Beautifed_image.shape[1], Beautifed_image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.imageLabel.setPixmap(QPixmap(image))

    def saveTempImage(self):
        global Beautifed_image, local_beautification

        Beautifed_image = local_beautification
        image = QtGui.QImage(
            Beautifed_image.data, Beautifed_image.shape[1], Beautifed_image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap(image))
        self.blur.setValue(0)
        self.sharpen.setValue(0)
        self.emboss.setValue(0)

    def imgeLoadfunction(self):
        global Global_image, Beautifed_image
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Save The Changes ")
        msgbox.setText('Do You Want To Save The Changes ?')

        msgbox.addButton('Cancel', QMessageBox.YesRole)
        msgbox.addButton(QMessageBox.Ok)

        response = msgbox.exec_()
        if response == QMessageBox.Ok:
            print("Yes")
            Global_image = Beautifed_image
            window = ImageLoading()
            # window.show()
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex()+1)

        elif(response == QMessageBox.YesRole):
            print("Cancle Btn")
            window = ImageLoading()
            # window.show()
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            print("nothing is happening ")
            window = ImageLoading()
            # window.show()
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex()+1)


    def clearSlidder(self):
        global Beautifed_image, local_beautification
        local_beautification = Beautifed_image
        if Beautifed_image is None:
            print("in if")
        else:
            image = QtGui.QImage(
                Beautifed_image.data, Beautifed_image.shape[1], Beautifed_image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.imageLabel.setPixmap(QPixmap(image))
        self.blur.setValue(0)
        self.sharpen.setValue(0)
        self.emboss.setValue(0)

    def sldReconnect(self):
        self.sender().valueChanged.connect(self.sliderChanged)
        self.sender().valueChanged.emit(self.sender().value())
        if (self.sender().objectName() == "blur"):
            self.emboss.setValue(1)
        elif(self.sender().objectName() == "emboss"):
            self.blur.setValue(1)

    def sliderChanged(self):
        global Global_image, Beautifed_image, local_beautification
        print(self.sender().objectName() + " : " + str(self.sender().value()))
        fileName1 = Beautifed_image
        if (self.sender().objectName() == "blur"):
            self.emboss.setValue(1)
            self.sharpen.setValue(1)
            mytext = int(self.sender().value())
            self.blurLabel.setText(str(mytext))
            print("text values", mytext)
            try:
                fileName1 = cv2.GaussianBlur(
                    fileName1, (mytext, mytext), cv2.BORDER_DEFAULT)

                image = QtGui.QImage(
                    fileName1.data, fileName1.shape[1], fileName1.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()

                self.imageLabel.setPixmap(QPixmap(image))
                local_beautification = fileName1
            except:
                print("Wrong value")
        elif(self.sender().objectName() == "emboss"):
            self.blur.setValue(1)
            self.sharpen.setValue(1)
            mytext = int(self.sender().value())
            self.embossLabel.setText(str(mytext))
            print("text values", mytext)
            try:
                kernel = np.array([[0, -mytext, -mytext],
                                   [mytext, 0, -mytext],
                                   [mytext, mytext, 0]])
                fileName1 = cv2.filter2D(fileName1, -1, kernel)
                image = QtGui.QImage(
                    fileName1.data, fileName1.shape[1], fileName1.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                self.imageLabel.setPixmap(QPixmap(image))
                local_beautification = fileName1
            except:
                print("Wrong value in emboss")
        elif(self.sender().objectName() == "sharpen"):
            mytext = int(self.sender().value())
            self.sharpenLabel.setText(str(mytext))
            self.emboss.setValue(1)
            self.blur.setValue(1)
            try:
                kernel = np.array([[mytext/100, mytext/100*5, mytext/100],
                                   [mytext/100*9, mytext/10*8.6, mytext/100*16],
                                   [mytext/100*33, mytext/100*7, mytext/100*8]])
                fileName1 = cv2.filter2D(fileName1, -1, kernel)

                image = QtGui.QImage(
                    fileName1.data, fileName1.shape[1], fileName1.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                self.imageLabel.setPixmap(QPixmap(image))
                local_beautification = fileName1
            except:
                print("Wrong value in emboss")


class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("./src/ui/createacc.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.homeButton.clicked.connect(self.HomeButtonClicked)

    def HomeButtonClicked(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def signupfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            self.error.setText("Please fill in all inputs.")

        elif password != confirmpassword:
            self.error.setText("Passwords do not match.")
        else:
            user_info = [user, password]
            try:
                with open('./src/csv/user_data.csv', 'a') as appendFile:
                    writer = csv.writer(appendFile)
                    list_append = [str(user), str(password)]
                    writer.writerow(list_append)
                    # Clearing values
                    self.emailfield.setText("")
                    self.passwordfield.setText("")
                    self.confirmpasswordfield.setText("")
                    # showring msg box
                    msg = QMessageBox()
                    msg.setWindowTitle("Successs")
                    msg.setText("Successfully Logged In!")
                    msg.exec_()
            except:
                print("Error in Creating account")
                QMessageBox.information(QMessageBox(), 'Error')


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(700)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
