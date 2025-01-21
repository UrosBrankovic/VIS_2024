from mainWindow import mainWindow
import QVTKRenderWindowInteractor as QVTK
QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(['QVTKRenderWindowInteractor'])

    mainWindow(app)

if __name__ == "__main__":
    main()