from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb
from PyQt5.uic import loadUiType
import datetime
ui,_ = loadUiType('library.ui')
login,_ = loadUiType('login.ui')


class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)

    def Handel_Login(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data :
            if username == row[1] and password == row[3]:
                print('user match')
                self.window2 = MainApp()
                self.close()
                self.window2.show()

            else:
                self.label_3.setText('** Your User Name Or Password is Not Correct !!')



class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Buttons()
        self.Dark_Orange_Theme()


        self.Show_Author()
        self.Show_Category()
        self.Show_Publisher()

        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()

        self.Show_All_Clients()
        self.Show_All_Books()

        self.Show_All_Operations()




    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)



    def Handel_Buttons(self):
        self.pushButton_6.clicked.connect(self.Show_Themes)
        self.pushButton_21.clicked.connect(self.Hiding_Themes)

        self.pushButton_3.clicked.connect(self.Open_Day_To_Day_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_26.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_4.clicked.connect(self.Open_Users_Tab)
        self.pushButton_5.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_12.clicked.connect(self.Add_New_Book)
        self.pushButton_10.clicked.connect(self.Search_Books)
        self.pushButton_9.clicked.connect(self.Edit_Books)
        self.pushButton_11.clicked.connect(self.Delete_Books)

        self.pushButton_14.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_16.clicked.connect(self.Add_Publisher)

        self.pushButton_7.clicked.connect(self.Add_New_User)
        self.pushButton_8.clicked.connect(self.Login)
        self.pushButton_13.clicked.connect(self.Edit_User)

        self.pushButton_17.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_18.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_19.clicked.connect(self.Dark_Gray_Theme)
        self.pushButton_20.clicked.connect(self.Blue_Green_Theme)

        self.pushButton_22.clicked.connect(self.Add_New_Client)
        self.pushButton_24.clicked.connect(self.Search_Client)
        self.pushButton_23.clicked.connect(self.Edit_Client)
        self.pushButton_25.clicked.connect(self.Delete_Client)

        self.pushButton.clicked.connect(self.Handel_Day_Operations)

        self.pushButton_27.clicked.connect(self.Procedure)
    def Show_Themes(self):
        self.groupBox_3.show()

    def Hiding_Themes(self):
        self.groupBox_3.hide()


    ############# Opening Tabs #############

    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)

    #######################################################
    ################ Day To Day Operations ################

    def Handel_Day_Operations(self):
        book_title = self.lineEdit.text()
        client_name = self.lineEdit_29.text()
        type = self.comboBox.currentText()
        days_number = self.comboBox_2.currentIndex() + 1
        today_date = datetime.date.today()
        to_date = today_date + datetime.timedelta(days= days_number)

        print(today_date)
        print(to_date)

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO dayoperations(book_name , client , type , days , date , to_date )
            VALUES (%s , %s , %s , %s , %s , %s)
        ''' , (book_title ,client_name ,type ,days_number ,today_date ,to_date))

        self.db.commit()
        self.statusBar().showMessage('New Operation Added')

        self.Show_All_Operations()

    def Show_All_Operations(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' 
            SELECT book_name , client , type , date , to_date FROM dayoperations
        ''')

        data = self.cur.fetchall()

        print(data)

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row , form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    #######################################
    ################ Books ################

    def Show_All_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_code, book_name, book_description, book_category, book_author, book_publisher, book_price FROM book''')
        data = self.cur.fetchall()

        print(data)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row, form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget_5.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)

        self.db.close()


    def Add_New_Book(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price = self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book(book_name,book_description ,book_code,book_category,book_author,book_publisher,book_price)
            VALUES (%s , %s , %s , %s , %s , %s , %s) 
        ''' , (book_title , book_description , book_code , book_category , book_author , book_publisher, book_price))

        self.db.commit()
        self.statusBar().showMessage('New Book Added')

        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_3.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')
        self.Show_All_Books()



    def Search_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_11.text()

        sql= ''' SELECT * FROM book WHERE book_name = %s'''
        self.cur.execute(sql, [(book_title)])

        data = self.cur.fetchone()
        print(data)

        self.lineEdit_10.setText(data[1])
        self.textEdit_3.setPlainText(data[2])
        self.lineEdit_8.setText(data[3])
        self.comboBox_9.setCurrentText(data[4])
        self.comboBox_11.setCurrentText(data[5])
        self.comboBox_10.setCurrentText(data[6])
        self.lineEdit_9.setText(str(data[7]))
    def Edit_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_10.text()
        book_description = self.textEdit_3.toPlainText()
        book_code = self.lineEdit_8.text()
        book_category = self.comboBox_9.currentText()
        book_author = self.comboBox_11.currentText()
        book_publisher = self.comboBox_10.currentText()
        book_price = self.lineEdit_9.text()

        search_book_title = self.lineEdit_11.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s ,book_description=%s ,book_code=%s ,book_category=%s ,book_author=%s ,book_publisher=%s ,book_price=%s WHERE book_name = %s
        ''', (book_title,book_description,book_code,book_category,book_author,book_publisher,book_price, search_book_title))

        self.db.commit()
        self.statusBar().showMessage('book updated')
        self.Show_All_Books()
    def Delete_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()
        book_title= self.lineEdit_11.text()
        warning= QMessageBox.warning(self, 'Delete Book' , "are you sure you want to delete this book", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sql = ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql, [(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')
            self.Show_All_Books()


    #######################################

    ################ Clients ################
    def Show_All_Clients(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT client_name , client_email, client_nationalid FROM clients ''')
        data = self.cur.fetchall()

        print(data)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        for row, form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget_6.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)

        self.db.close()


    def Add_New_Client(self):
        client_name = self.lineEdit_22.text()
        client_email = self.lineEdit_23.text()
        client_nationalid = self.lineEdit_24.text()

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute ('''
            INSERT INTO clients(client_name , client_email , client_nationalid)
            VALUES (%s , %s, %s)
        ''' , (client_name , client_email , client_nationalid))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')
        self.Show_All_Clients()

    def Search_Client(self):
        client_national_id = self.lineEdit_28.text()
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        sql= ''' SELECT * FROM clients WHERE client_nationalid = %s '''
        self.cur.execute(sql , [(client_national_id)])
        data = self.cur.fetchone()
        print(data)

        self.lineEdit_26.setText(data[1])
        self.lineEdit_25.setText(data[2])
        self.lineEdit_27.setText(data[3])

    def Edit_Client(self):
        client_original_national_id = self.lineEdit_28.text()
        client_name = self.lineEdit_26.text()
        client_email = self.lineEdit_25.text()
        client_national_id = self.lineEdit_27.text()

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            UPDATE clients SET client_name = %s , client_email = %s , client_nationalid = %s WHERE client_nationalid = %s
        ''' , (client_name , client_email , client_national_id, client_original_national_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Client Data Updated')
        self.Show_All_Clients()

    def Delete_Client(self):
        client_original_national_id = self.lineEdit_28.text()

        warning_message = QMessageBox.warning(self , "Delete Client", " You are deleting this client Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if warning_message == QMessageBox.Yes :

            self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
            self.cur = self.db.cursor()

            sql =''' DELETE FROM clients WHERE client_nationalid = %s '''
            self.cur.execute(sql, [(client_original_national_id)])

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('Client Deleted Successfully')
            self.Show_All_Clients()




    #######################################

    ################ Users ################

    def Add_New_User(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_5.text()
        email = self.lineEdit_6.text()
        password = self.lineEdit_7.text()
        password2 = self.lineEdit_12.text()

        if password == password2 :
            self.cur.execute('''
                INSERT INTO users(user_name , user_email , user_password)
                VALUES (%s , %s , %s)
            ''' , (username, email , password))

            self.db.commit()
            self.statusBar().showMessage('New User Added')
        else:
            self.label_30.setText('please add a valid password twice')


    def Login(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()


        username = self.lineEdit_14.text()
        password = self.lineEdit_13.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data :
            if username == row[1] and password == row[3]:
                print('user match')
                self.statusBar().showMessage('Valid Username & Password')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_18.setText(row[1])
                self.lineEdit_16.setText(row[2])
                self.lineEdit_15.setText(row[3])



    def Edit_User(self):
        username = self.lineEdit_18.text()
        email = self.lineEdit_16.text()
        password = self.lineEdit_15.text()
        password2 = self.lineEdit_17.text()

        original_name = self.lineEdit_14.text()

        if password == password2 :
            self.db = MySQLdb.connect(host='localhost', user='root', password='toor', db='library')
            self.cur = self.db.cursor()

            self.cur.execute('''
                UPDATE users SET user_name = %s , user_email = %s , user_password = %s WHERE user_name = %s
            ''', (username , email , password , original_name))
            self.db.commit()
            self.statusBar().showMessage('User Data Updated Succesfully')

        else:
            print('Make sure that you Entered password correctly!!')

    #######################################

    ################ Users ################


    def Add_Category(self):
        category_name = self.lineEdit_19.text()
        category_id= self.lineEdit_31.text()

        try:
            self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
            self.cur = self.db.cursor()

            self.cur.execute('''
                INSERT INTO category (category_name,idcategory) VALUES (%s, %s)
            ''' , (category_name,category_id))

            self.db.commit()
            self.statusBar().showMessage ('New Category Added')
            self.lineEdit_19.setText('')
            self.Show_Category()
            self.Show_Category_Combobox()

        except MySQLdb.IntegrityError as e:
            error_message = "Error: Duplicate Category ID. Please choose a different Category ID."
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def Show_Category(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name, idcategory FROM category''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form) :
                    self.tableWidget_2.setItem(row , column , QTableWidgetItem(str(item)))
                    column +=1

                row_position= self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)


    def Add_Author(self):
        author_name = self.lineEdit_20.text()
        author_id=self.lineEdit_32.text()
        try:
            self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
            self.cur = self.db.cursor()


            self.cur.execute('''
                INSERT INTO authors (author_name, idauthor) VALUES (%s, %s)
            ''', (author_name, author_id))

            self.db.commit()
            self.lineEdit_20.setText('')
            self.statusBar().showMessage('New Author Added')
            self.Show_Author()
            self.Show_Author_Combobox()

        except MySQLdb.IntegrityError as e:
            error_message = "Error: Duplicate Author ID. Please choose a different Author ID."
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def Show_Author(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name, idauthor FROM authors''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form) :
                    self.tableWidget_3.setItem(row , column , QTableWidgetItem(str(item)))
                    column +=1

                row_position= self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)


    def Add_Publisher(self):
        publisher_name = self.lineEdit_21.text()
        publisher_id = self.lineEdit_33.text()

        try:

            self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
            self.cur = self.db.cursor()

            self.cur.execute('''
                INSERT INTO publisher (publisher_name, idpublisher) VALUES (%s, %s)
            ''', (publisher_name,publisher_id))

            self.db.commit()
            self.lineEdit_21.setText('')
            self.statusBar().showMessage('New Publisher Added')
            self.Show_Publisher()
            self.Show_Publisher_Combobox()
                except MySQLdb.IntegrityError as e:
            error_message = "Error: Duplicate Author ID. Please choose a different Publisher ID."
            QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)

    def Show_Publisher(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name, idpublisher FROM publisher''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form) :
                    self.tableWidget_4.setItem(row , column , QTableWidgetItem(str(item)))
                    column +=1

                row_position= self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)


    #######################################

    ################ show settings data in UI ################

    def Show_Category_Combobox(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute( ''' SELECT category_name FROM category''')
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        for category in data :
            self.comboBox_3.addItem(category[0])
            self.comboBox_9.addItem(category[0])

    def Show_Author_Combobox(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute (''' SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        self.comboBox_4.clear()
        for author in data :
            self.comboBox_4.addItem(author[0])
            self.comboBox_11.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute (''' SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        self.comboBox_5.clear()
        for publisher in data :
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_10.addItem(publisher[0])

    def Procedure(self,author_name):
        author_name = self.lineEdit_30.text()
        if author_name:
            self.db = MySQLdb.connect(host='localhost', user='root', password='toor', db='library')
            self.cur = self.db.cursor()

            self.cur.callproc('OtherBooksOfAuthor', (author_name,))
            data = self.cur.fetchall()

            print(data)
            self.tableWidget_7.setRowCount(len(data))
            self.tableWidget_7.setColumnCount(len(data[0]))

            for row_index, row_data in enumerate(data):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.tableWidget_7.setItem(row_index, col_index, item)
           


    #######################################

    ################  UI  Themes ################
    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Gray_Theme(self):
        style = open('themes/qdarkgray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Blue_Green_Theme(self):
        style = open('themes/maviyesil.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
def main():
    app= QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()


###(pyrcc5 icons.qrc -o icons_rc.py)###