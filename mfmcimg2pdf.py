# Image to PDF

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw
import sys, os
import img2pdf
from PIL import Image, ImageQt

from mainwindow4 import Ui_MainWindow
from welcome3 import Ui_DialogWelcome

class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    converted = qtc.pyqtSignal()
    new_files_selected = qtc.pyqtSignal()

    def __init__(self, files, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = files
        self.current_file_n = 0
        self.current_page_n = 0
        self.total_pages = 1
        
        self.setupUi(self)
        # change image to first image
        self.split_files = self.split_filenames(self.files)
        self.PDFnames = self.defaultPDFnames(self.split_files)
        self.updateImage(self.split_files[self.current_file_n])
        self.updatePDFname(self.PDFnames[self.current_file_n])

        #connect signals to slots
        self.pushButtonExit.clicked.connect(self.exit)
        self.actionExit.triggered.connect(self.exit)
        self.actionChoose_Files.triggered.connect(self.on_new_files_selected)
        self.lineEditPDF_file.textChanged.connect(self.PDFchanged)
        self.pushButtonConvert.setDefault(True)
        self.pushButtonConvert.clicked.connect(self.convert2PDF)
        self.lineEditPDF_file.returnPressed.connect(self.convert2PDF)
        self.pushButtonSkip.clicked.connect(self.next_file)
        self.converted.connect(self.next_file)
        self.new_files_selected.connect(self.on_new_files_selected)
        self.pushButtonNewFiles.clicked.connect(self.on_new_files_selected)
        self.pushButtonAll.clicked.connect(self.convert_all)
        self.lineEdit_current_page.editingFinished.connect(self.current_page_changed)
        self.pushButton_left.clicked.connect(self.left_clicked)
        self.pushButton_right.clicked.connect(self.right_clicked)

    def split_filenames(self, files):
        #returns list splitfiles of files split into list of (complete path, directory, filename, extension)
        splitfiles = []
        for i in range(len(files)):
            fdir = os.path.dirname(files[i])
            fname,fextension = os.path.splitext(os.path.basename(files[i]))
            splitfiles.append([files[i],fdir, fname, fextension])
        return splitfiles

    def defaultPDFnames(self, split_files):
        #returns list of splifiles with extension changed to .PDF of list (complete path, directory, filename, ".PDF")
        PDFnames = []
        for i in range(len(split_files)):
            PDFnames.append([f"{split_files[i][1]}/{split_files[i][2]}.PDF", split_files[i][1], split_files[i][2], ".PDF"])
        return PDFnames
        
    def PDFchanged(self):
        #update current filename when PDF filename typed in line edit
        self.PDFnames[self.current_file_n][2] = self.lineEditPDF_file.text()
        self.PDFnames[self.current_file_n][0] = f"{self.PDFnames[self.current_file_n][1]}/{self.lineEditPDF_file.text()}.PDF"

    def updateImage(self, split_file):
        #change label_orig_img and label_orig_file
        self.img = Image.open (split_file[0])
        try:
            self.total_pages = self.img.n_frames
        except:
            self.total_pages = 1
        self.current_page_n = 1
        self.label_total_pages.setText(qtc.QCoreApplication.translate("MainWindow", f"   of {self.total_pages}"))
        self.showPage(self.img, self.current_page_n, self.total_pages)
        self.label_orig_file.setText(qtc.QCoreApplication.translate("MainWindow", f"{split_file[2]}{split_file[3]}"))

    def showPage(self, img, pg, total_pages):
        #img is PIL.Image object
        self.lineEdit_current_page.setText(qtc.QCoreApplication.translate("MainWindow", f"{self.current_page_n}"))

        if (pg>total_pages):
            pg = total_pages
        if total_pages>1:
            img.seek(pg-1)
        qtimg = ImageQt.ImageQt(img)
        self.label_orig_img.setPixmap(qtg.QPixmap.fromImage(qtimg)) 

    def current_page_changed(self):
        #lineEdit_current_page changed
        try:
            page = int(self.lineEdit_current_page.text()) 
        except ValueError:
            self.showPage(self.img, self.current_page_n, self.total_pages)
            return
        self.current_page_n = page
        if self.current_page_n <= 1:
            self.current_page_n = 1
        if self.current_page_n >= self.total_pages:
            self.current_page_n = self.total_pages
        self.showPage(self.img, self.current_page_n, self.total_pages)

    def left_clicked(self):
        if self.current_page_n > 1:
            self.current_page_n -= 1
        self.showPage(self.img, self.current_page_n, self.total_pages)

    def right_clicked(self):
        if self.current_page_n < self.total_pages:
            self.current_page_n += 1
        self.showPage(self.img, self.current_page_n, self.total_pages)
    
    def updatePDFname(self, split_file):
        #update lineEditPDF when next file is selected
        self.lineEditPDF_file.deselect()
        self.lineEditPDF_file.setText(qtc.QCoreApplication.translate("MainWindow", f"{split_file[2]}"))
        
        self.lineEditPDF_file.selectAll()
        self.lineEditPDF_file.setFocus()

    def convert2PDF(self):
        self.img.close()
        PDF_file = self.PDFnames[self.current_file_n]
        split_file = self.split_files[self.current_file_n]
        if os.path.exists(PDF_file[0]):
            msg_exists = qtw.QMessageBox()
            msg_exists.setIcon(qtw.QMessageBox.Warning)
            msg_exists.setText(f"{PDF_file[0]} exists")
            msg_exists.setInformativeText("Do you want to continue?")
            msg_exists.setWindowTitle("Img2PDF")
            msg_exists.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel)
            reply = msg_exists.exec()
            if reply == qtw.QMessageBox.No or reply == qtw.QMessageBox.Cancel:
                return

            #double check
            msg_exists = qtw.QMessageBox()
            msg_exists.setIcon(qtw.QMessageBox.Warning)
            msg_exists.setText(f"Are you sure you want to overwrite {PDF_file[0]}?")
            msg_exists.setWindowTitle("Img2PDF")
            msg_exists.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel)
            reply = msg_exists.exec()
            if reply == qtw.QMessageBox.No or reply == qtw.QMessageBox.Cancel:
                return
            os.remove(PDF_file[0])
            
        # qtw.QMessageBox.information(self, "Img2PDF", f"{PDF_file[0]} converted") 
        with open(PDF_file[0],"wb") as f1, open(split_file[0],"rb") as f2:
            f1.write(img2pdf.convert(f2))    
        if os.path.isfile(split_file[0]):
            os.remove(split_file[0])
        self.converted.emit()

    def convert_all(self):
        msg_all = qtw.QMessageBox()
        msg_all.setIcon(qtw.QMessageBox.Warning)
        msg_all.setText(f"Do you want to convert all files to default PDF names?")

        msg_all.setWindowTitle("Img2PDF")
        msg_all.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No | qtw.QMessageBox.Cancel)
        reply = msg_all.exec()
        if reply == qtw.QMessageBox.No or reply == qtw.QMessageBox.Cancel:
            return
        self.PDFnames = self.defaultPDFnames(self.split_files)
        while self.current_file_n < len(self.split_files):
            if self.current_file_n < len(self.split_files)-1:
                self.convert2PDF()
            else:
                self.convert2PDF()
                break
        

    def next_file(self):
        if self.current_file_n >= (len(self.split_files)-1):
            self.current_file_n = (len(self.split_files)-1)
            self.label_orig_img.setPixmap(qtg.QPixmap(":/mfmc logo 2015 (square).png"))
            msg_lastfile = qtw.QMessageBox()  
            msg_lastfile.setIcon(qtw.QMessageBox.Warning)
            msg_lastfile.setText(f"No more files selected")
            msg_lastfile.setWindowTitle("Img2PDF")
            msg_lastfile.setStandardButtons(qtw.QMessageBox.Cancel | qtw.QMessageBox.Close)
            msg_lastfile.addButton(qtw.QPushButton('Select new files...'), qtw.QMessageBox.YesRole)
            reply = msg_lastfile.exec()
            if reply == qtw.QMessageBox.Close:
                self.close()
            if reply == 0:
                self.new_files_selected.emit()
        else:
            self.current_file_n += 1
            
            self.updateImage(self.split_files[self.current_file_n])
            self.updatePDFname(self.split_files[self.current_file_n])

    @qtc.pyqtSlot()
    def on_new_files_selected(self):
        self.welcome = WelcomeWidget()
        self.welcome.show()
        self.close()

    def keyPressEvent(self, e):
        if e.key() == qtc.Qt.Key_Escape:
            self.close()

    def exit(self):
        self.close()
        



class WelcomeWidget(qtw.QDialog, Ui_DialogWelcome):
    files_selected = qtc.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.imgFiles = []

        self.setupUi(self)
        self.connectSignals()

    def connectSignals(self):
        self.pushButtonSel.clicked.connect(self.getImgFiles)
        self.pushButtonDir.clicked.connect(self.getImgDir)
        self.pushButtonExit.clicked.connect(self.exit)
        self.files_selected.connect(self.on_files_selected)


    def getImgFiles(self):
        options = qtw.QFileDialog.Options()
        fileNames, _ = qtw.QFileDialog.getOpenFileNames(self
            ,"Files to Convert", "","Image files (*.tif *.bmp *.gif *.png);; All Files (*)", options=options)
        imgfileNames = []
        for file in fileNames:
            if (os.path.splitext(file)[1].lower()) in (".tif", ".bmp", ".gif", ".png"):
                imgfileNames.append(file)
        self.imgFiles = imgfileNames
        if imgfileNames:
            self.files_selected.emit(imgfileNames)

    def getImgDir(self):
        options = qtw.QFileDialog.Options()
        fileNames = []
        dir = qtw.QFileDialog.getExistingDirectory(self, "Select Directory to Convert", options=options)
        if not dir:
            return
        all_files = os.listdir(dir)
        for file in all_files:
            if (os.path.splitext(file)[1]).lower() in (".tif", ".bmp", ".gif", ".png"):
                fileNames.append(f"{dir}/{file}")
        self.imgFiles = fileNames
        if fileNames:
            self.files_selected.emit(fileNames)
        else:
            qtw.QMessageBox.warning(self, "Img2PDF", f"No image files found in {dir}!")

    
    @qtc.pyqtSlot(list)
    def on_files_selected(self, files):
        qtw.QMessageBox.information(self, "Img2PDF", f"{len(files)} image files selected.")
        self.main = MainWindow(files)
        self.main.show()
        self.close()
                   
    def exit(self):
        self.close()



if __name__ == '__main__':
    if os.path.exists("\\\\Changlo\\incoming faxes"):
        os.chdir("\\\\Changlo\\incoming faxes")

    app = qtw.QApplication(sys.argv)

    widget = WelcomeWidget()
    widget.show()
 
    sys.exit(app.exec_())