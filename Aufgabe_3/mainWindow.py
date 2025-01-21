import mbsModel
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkWindowToImageFilter
from vtkmodules.all import vtkInteractorStyleTrackballCamera
import QVTKRenderWindowInteractor as QVTK
QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor
from PySide6.QtWidgets import QMainWindow, QFileDialog, QColorDialog
from PySide6.QtGui import QAction, QKeySequence
from vtkmodules.vtkIOImage import vtkPNGWriter

class mainWindow(QMainWindow):    
    def __init__(self,app):
        super().__init__()
        # create the widget
        self.widget = QVTKRenderWindowInteractor(self)
        self.setCentralWidget(self.widget)

        # window sizing
        geometry = self.screen().availableGeometry()
        self.resize(geometry.width() * 0.8, geometry.height() * 0.7)

        # menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.options_menu = self.menu.addMenu("Options")

        # status bar
        self.status = self.statusBar()
        self.status.showMessage("")

        # load QAction
        load = QAction("Load", self)
        load.triggered.connect(self.load)
        self.file_menu.addAction(load)

        # save QAction
        save = QAction("Save", self)
        save.triggered.connect(self.save)
        self.file_menu.addAction(save)
        
        # import fdd QAction
        impFddAction = QAction("Import", self)
        impFddAction.triggered.connect(self.importFdd)
        self.file_menu.addAction(impFddAction)

        # exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # change background QAction
        change_background_color = QAction("Hintergrundfarbe ändern", self)
        change_background_color.triggered.connect(self.changeColor)
        self.options_menu.addAction(change_background_color)

        # screenshot QAction
        take_screenshot = QAction("Screenshot", self)
        take_screenshot.triggered.connect(self.screenshot)
        self.options_menu.addAction(take_screenshot)

        #if you don't want the 'q' key to exit comment this.
        self.widget.AddObserver("ExitEvent", lambda o, e, a=app: a.quit())

        self.ren = vtkRenderer()
        self.ren.SetBackground(1,1,1)
        self.widget.GetRenderWindow().AddRenderer(self.ren)
        self.widget._Iren.SetInteractorStyle(vtkInteractorStyleTrackballCamera())

        # show the widget
        self.show()

        self.widget.Initialize()
        self.widget.Start()

        # start event processing
        # Source: https://doc.qt.io/qtforpython/porting_from2.html
        # 'exec_' is deprecated and will be removed in the future.
        # Use 'exec' instead.
        try:
            app.exec()
        except AttributeError:
            app.exec_()

    def load(self):
        fileName = QFileDialog.getOpenFileName(self,str("Open json File"), "C:/", str("json File (*.json)"))
        self.__currentModel__ = mbsModel.mbsModel()
        self.__currentModel__.loadDatabase(fileName[0])
        self.__currentModel__.showModel(self.ren)
        self.ren.ResetCamera()
        self.status.showMessage("Datenbank geladen")

    def save(self):
        self.__currentModel__.saveDatabase("C:\\VIS_2024\\Aufgabe_3\\test.json")
        self.status.showMessage("Datenbank gespeichert")

    def importFdd(self):
        fileName = QFileDialog.getOpenFileName(self,str("Open fdd File"), "C:/", str("fdd File (*.fdd)"))
        self.__currentModel__ = mbsModel.mbsModel()
        self.__currentModel__.importFddFile(fileName[0])
        self.__currentModel__.showModel(self.ren)
        self.ren.ResetCamera()
        self.status.showMessage("FDD Datei importiert")

    def changeColor(self):
        # Farbauswahldialog öffnen
        color = QColorDialog.getColor()

        # Überprüfen, ob eine gültige Farbe ausgewählt wurde
        if color.isValid():
            # RGB-Werte der ausgewählten Farbe extrahieren
            r, g, b, _ = color.getRgbF()

            # Hintergrundfarbe der 3D-Ansicht setzen und neu rendern
            self.ren.SetBackground(r, g, b)
            self.widget.GetRenderWindow().Render()

    def screenshot(self):
        w2if = vtkWindowToImageFilter()
        w2if.SetInput(self.widget.GetRenderWindow())
        w2if.SetInputBufferTypeToRGB()
        w2if.ReadFrontBufferOff()
        w2if.Update()

        writer = vtkPNGWriter()
        fileName = QFileDialog.getSaveFileName(self, "C:/", str("screenshot.png"))
        writer.SetFileName(fileName[0])
        writer.SetInputConnection(w2if.GetOutputPort())
        writer.Write()
