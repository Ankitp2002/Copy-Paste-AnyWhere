
import sys
import time
import os
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication,QStackedWidget,QMessageBox,QFileDialog,QTableWidgetItem
from PyQt5.QtCore import QCoreApplication
import requests
from PyQt5.uic import loadUi
import json
from PyQt5 import uic
from login_ui import Login_ui
from profile_ui import Profile_ui
from signup_ui import Ui_signup
from home_ui import Home_ui
from fileData_ui import FileData_ui
import PyInstaller

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()

        # loadUi("Ui/login.ui",self)
        # Ui_MainWindow, QtBaseClass = uic.loadUiType("login_ui.py")
        self.ui = Login_ui()
        self.ui.setupUi(self)

        self.ui.Login.clicked.connect(self.loginfunction)
        self.ui.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.signup.clicked.connect(self.gotocreate)

    def loginfunction(self):

        msg_box = QMessageBox()
        email=self.ui.EmailId.text()
        password=self.ui.Password.text()

        url = "http://192.168.1.126:3000/login"
        # url = "http://127.0.0.1:5000/login"
        data = {"userEmail": email, "userPassword": password}

        response = requests.post(url, json=data)
        api_data = json.loads(response.text)

        if api_data['status'] == True:

            self.jwt_token_value = api_data['token']

            home = main_page(jwt_token_value = self.jwt_token_value)
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            msg_box.setText("Your login succeesful.")
        else:
            msg_box.setText("check your cradantial!")


        msg_box.setIcon(QMessageBox.Information)

        msg_box.exec_()

    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()

        # loadUi('Ui/Signup.ui', self)
        self.ui = Ui_signup()
        self.ui.setupUi(self)

        self.ui.Submit.clicked.connect(self.createaccfunction)
        self.ui.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.Conformpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.back.clicked.connect(self.back_to_login)

    def createaccfunction(self):
        email = self.ui.Email.text()
        name = self.ui.Name.text()
        msg_box = QMessageBox()
        if self.ui.Password.text()==self.ui.Conformpassword.text():
            password=self.ui.Password.text()
            url = "http://192.168.1.126:3000/signup"
            # url = "http://127.0.0.1:5000/signup"
            data = {"userName" : name ,"userEmail" : email ,"userPassword" : password }
            response = requests.post(url, json=data)
            # time.sleep(1)
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
            msg_box.setText("Your response has been recorded.")
        else:
            msg_box.setText("Your Password and Confirm Password is not same")

        msg_box.setIcon(QMessageBox.Information)

        msg_box.exec_()

    def back_to_login(self):

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class main_page(QDialog):

    def __init__(self,jwt_token_value):
        super(main_page, self ).__init__()

        # loadUi('Ui/home.ui', self)
        self.ui = Home_ui()
        self.ui.setupUi(self)

        self.jwt_token_value = jwt_token_value

        self.ui.ViewHistory.clicked.connect(self.file_Page)
        self.ui.profile.clicked.connect(self.profile_Page)
        self.ui.logout.clicked.connect(self.Logout)
        self.ui.copy.clicked.connect(self.UploadFile)
        self.ui.paste.clicked.connect(self.getFile)
        # ------------------------------file get token

    def file_Page(self):

        filePage = filed_data(jwt_token_value=self.jwt_token_value)
        widget.addWidget(filePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def profile_Page(self):
        profilePage = Profile(jwt_token_value=self.jwt_token_value)
        widget.addWidget(profilePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Logout(self):

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def UploadFile(self):

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        fname,_ = file_dialog.getOpenFileNames()

        # fname,_ = QFileDialog.getOpenFileName(self, 'Open file')
        msg_box = QMessageBox()

        if len(fname)==1:
# ---------------------------------------------------Singal File Upload ---------------------------------------------------------
            file = fname[0]

            self.ui.file.setText(f"selected files :{file}")

            files = {'file': open(file, 'rb')}

            url = 'http://192.168.1.126:3000/uploadSingleFile'
            # url = 'http://127.0.0.1:5000/uploadSingleFile'

            response = requests.post(url, files=files , headers={"token" : self.jwt_token_value})

            message = json.loads(response.text)

            if message['token']:

                msg_box.setText(f"Token : {message['token']} \n  FileName : {message['fileName']}")

                self.ui.copy_button = msg_box.addButton("Copy", QMessageBox.ActionRole)

                self.ui.copy_button.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(msg_box.text()))

            else:

                msg_box.setText(f"  Not Success : {message['responce']}  ")


        else:
# -------------------------------------------------Multiple File UPload -----------------------------------------------
            self.ui.file.setText(f"selected files :{fname}")

            files = [('file', open(file_name, 'rb')) for file_name in fname]

            url = 'http://192.168.1.126:3000/uploadMultipleFile'
            # url = 'http://127.0.0.1:5000/uploadMultipleFile'

            responce = requests.post(url,files = files ,headers={"token":self.jwt_token_value})

            message = json.loads(responce.text)

            msg_box.setText(f"Token : {message['token']}")

            self.ui.copy_button = msg_box.addButton("Copy", QMessageBox.ActionRole)

            self.ui.copy_button.clicked.connect(lambda: QtWidgets.QApplication.clipboard().setText(msg_box.text()))

        msg_box.setIcon(QMessageBox.Information)

        msg_box.exec_()

    def getFile(self):

        try:
            fileToken = self.ui.token.text()
            print(fileToken)
            file_dialog = QFileDialog()

            if fileToken == "":

                print("black")

            elif fileToken.isdigit():
                print(fileToken,"is digit")
                url = 'http://192.168.1.126:3000/get/'
                # url = ' http://127.0.0.1:5000/get/'

                response = requests.get(url+fileToken , headers={"token": self.jwt_token_value},stream=True)

                content = response.content

                if content == b'':
    # -------------------------------------------------------Multiple file get and set in file data to access using singal file name--------------------------------------------------
                    self.ui.fileList = response.headers['file']

                    QMessageBox.information(self, 'Success', 'All File In Your File Section to downloaded As Per Your Requirement.')

                else:
    # ----------------------------------------------Singal File Get------------------------------------------------------
                    text_content = content.decode('utf-8')

                    extension = response.headers['fileName'].split('.')[1]

                    # file_dialog.setNameFilter(f"{extension} files (*.{extension})")
                    file_path, _ = file_dialog.getSaveFileName(self, 'Save File', '',f'.{extension}')

                    if not file_path:
                        return QMessageBox.information(self, 'Path Not Selected', 'File downloaded Faield.')


                    # Save the file
                    with open(f'{file_path}.{extension}', 'w') as f:
                        f.write(text_content)

                    QMessageBox.information(self, 'Success', 'File downloaded successfully.')

            else:
    # ------------------------------------ --------------------------get file using file name ----------------------------
                print(fileToken,"no dwegit")
                url = 'http://192.168.1.126:3000/files/'

                response = requests.get(url + fileToken, headers={"token": self.jwt_token_value}, stream=True)

                content = response.content
                extension = str(response.headers['fileName']).split('.')[-1]

                file_path, _ = file_dialog.getSaveFileName(self, 'Save File', '', f'.{extension}')

                if not file_path:
                    return QMessageBox.information(self, 'Path Not Selected', 'File downloaded Faield.')

                if extension == "PNG" or "jpg" or "JPEG":

                    # text_content = content.decode('utf-8')

                    # Save the file
                    with open(f'{file_path}.{extension}', 'wb') as f:
                        f.write(content)

                elif extension == "mp3" or "mp4":

                    # Save the file
                    with open(f'{file_path}.{extension}', 'wb') as f:
                        f.write(content)

                else:
                    text_content = content.decode('utf-8')

                    # Save the file
                    with open(f'{file_path}.{extension}', 'w') as f:
                        f.write(text_content)

                QMessageBox.information(self, 'Success', 'File downloaded successfully.')

        except Exception:

            QMessageBox.information(self, 'Faield', f'Check Your Enter Details{Exception}')


class filed_data(QDialog):

    def __init__(self,jwt_token_value):
        super(filed_data, self).__init__()

        # loadUi('Ui/FileData.ui', self)

        self.ui = FileData_ui()
        self.ui.setupUi(self)

        self.jwt_token_value = jwt_token_value
        self.ui.home.clicked.connect(self.home_Page)
        self.ui.profile.clicked.connect(self.profile_Page)
        self.ui.logout.clicked.connect(self.Logout)
        self.ui.FileName.setColumnWidth(0,600)
        self.ui.Referes.clicked.connect(self.data)


    def home_Page(self):

        homePage = main_page(jwt_token_value=self.jwt_token_value)
        widget.addWidget(homePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def profile_Page(self):

        profilePage = Profile(jwt_token_value=self.jwt_token_value)
        widget.addWidget(profilePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Logout(self):

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def data(self):

        url = ' http://192.168.1.126:3000/UserFile'


        # url = ' http://127.0.0.1:5000/UserFile'

        responce = requests.get(url,headers={"token":self.jwt_token_value})

        data = json.loads(responce.text)

        if data['Files'] != []:

            row = self.ui.FileName.setRowCount(len(data['Files']))

            tableRow = 0

            for rowData in data['Files']:
                item = QtWidgets.QTableWidgetItem(str(rowData))

                size_item = QTableWidgetItem(str(rowData))
                size_item.setFont(QtGui.QFont("Arial", 10))  # set font size to 10
                size_item.setForeground(QtGui.QColor(0, 0, 255))  # set font color to blue

                self.ui.FileName.setItem(tableRow,0,item)

                tableRow += 1

        else:

            QMessageBox.information(self, 'Files', 'Data Not Available.')



class Profile(QDialog):

    def __init__(self,jwt_token_value):
        super(Profile, self).__init__()
        # loadUi('Ui/Profile.ui',self)

        self.ui = Profile_ui()
        self.ui.setupUi(self)

        self.jwt_token_value = jwt_token_value
        self.ui.home.clicked.connect(self.home_Page)
        self.ui.ViewHistory.clicked.connect(self.file_Page)
        self.ui.logout.clicked.connect(self.Logout)

        url = ' http://192.168.1.126:3000/profile'
        # url = 'http://127.0.0.1:5000/profile'

        header = {"token": self.jwt_token_value}

        response = requests.get(url , headers=header)

        userData = json.loads(response.text)

        self.ui.name.setText(userData['Name'])
        self.ui.email.setText(userData['Email'])

    def home_Page(self):

        homePage = main_page(jwt_token_value=self.jwt_token_value)
        widget.addWidget(homePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def file_Page(self):
        filePage = filed_data(jwt_token_value=self.jwt_token_value)
        widget.addWidget(filePage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Logout(self):

        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    mainwindow=Login()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(1000)
    widget.setFixedHeight(600)
    widget.show()
    app.exec_()
