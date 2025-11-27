import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

main_window_ref = None

# BOITE DE DIALOGUE
def openFile():
    fname, _ = QFileDialog.getOpenFileName(None, "Ouvrir un fichier")
    if not fname:
        print("No file selected.")
        return
    print("File opened:", fname)
    file = QFile(fname)
    if not file.open(QFile.ReadOnly | QFile.Text):
        print("Unable to open file.")
        return
    stream = QTextStream(file)
    content = stream.readAll()
    file.close()
    main_window_ref.textEdit.setHtml(content)

def saveFile():
    fname, _ = QFileDialog.getSaveFileName(None, "Save file")
    if not fname:
        print("No file selected.")
        return
    print("File saved:", fname)
    file = QFile(fname)
    if not file.open(QFile.WriteOnly | QFile.Text):
        print("Unable to save file.")
        return
    stream = QTextStream(file)
    content = main_window_ref.textEdit.toHtml()
    stream << content
    file.close()

# QUITTER L'APP APRES CONFIRMATION
def quitApp():
    main_window_ref.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # TAILLE DE LA FENETRE
        self.resize(400,400)

        # BARRE DE MENU
        bar = self.menuBar()
        fileMenu = bar.addMenu("File")

        # NEW ACTION
        newAction = QAction(QIcon("new.png"), "New", fileMenu)
        newAction.setShortcut("Ctrl+N")
        newAction.setToolTip("Create a new file.")

        # OPEN ACTION
        openAction = QAction(QIcon("open.png"), "Open", fileMenu)
        openAction.setShortcut("Ctrl+O")
        openAction.setToolTip("Open a file.")
        openAction.triggered.connect(openFile)

        # SAVE ACTION
        saveAction = QAction(QIcon("save.png"), "Save", fileMenu)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setToolTip("Save file.")
        saveAction.triggered.connect(saveFile)

        # COPY ACTION
        copyAction = QAction(QIcon("copy.png"), "Copy", fileMenu)
        copyAction.setShortcut("Ctrl+C")
        copyAction.setToolTip("Copy selection.")

        # QUIT ACTION
        quitAction = QAction(QIcon("quit.png"), "Quit", fileMenu)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setToolTip("Quit the app.")
        quitAction.triggered.connect(quitApp)

        # AJOUT DANS LE MENU
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(copyAction)
        fileMenu.addAction(quitAction)

        # BARRE D’OUTILS
        toolbar = self.addToolBar("MainToolbar")
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        toolbar.addAction(copyAction)
        toolbar.addAction(quitAction)

        # ZONE CENTRALE
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        # BARRE DE STATUS
        self.statusBar().showMessage("Ready")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Confirmation", "Do you really want to quit ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            print("App closed.")
        else:
            event.ignore()
            print("Quit cancelled.")

def main(args):
    global main_window_ref
    app = QApplication(args)
    mw = MainWindow()
    main_window_ref = mw
    mw.show()
    app.exec()

if __name__ == "__main__":
    print("execution du programme")
    main(sys.argv)