from TreeModel import TreeModel, CustomNode
from PySide6.QtWidgets import (QWidget,  QHBoxLayout, QSizePolicy, QTreeView)
from vtkmodules.vtkRenderingCore import vtkRenderer
import vtkmodules.vtkInteractionStyle
import QVTKRenderWindowInteractor as QVTK
QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Create VTK Widget
        self.VTKwidget = QVTKRenderWindowInteractor(self)
        style = vtkmodules.vtkInteractionStyle.vtkInteractorStyleTrackballCamera()
        self.VTKwidget._Iren.SetInteractorStyle(style)
        self.ren = vtkRenderer()
        self.ren.SetBackground(1,1,1)
        self.VTKwidget.GetRenderWindow().AddRenderer(self.ren)
        self.VTKwidget.Initialize()
        self.VTKwidget.Start()
        
        # Create Tree Item List
        self.treeItems = []

        # Create Tree View
        self.treeView = QTreeView()
        self.treeView.setHeaderHidden(True)
        #self.treeView.resizeColumnToContents(0)

        # Left layout
        size.setHorizontalStretch(3.5)
        self.VTKwidget.setSizePolicy(size)
        self.main_layout.addWidget(self.VTKwidget)
        
        # Right layout
        size.setHorizontalStretch(1.5)
        self.treeView.setSizePolicy(size)
        self.main_layout.addWidget(self.treeView)
        
        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def addTreeItems(self,data):
        self.treeItems.append(CustomNode(None,'MBS Model'))
        for item in data:
            if(len(item) == 1):
                for x in self.treeItems:
                    x.addChild(CustomNode(None,item))
            if(len(item) == 2):
                 for x in self.treeItems[0]._children:
                     if(x._data == [item[0]]):
                        if isinstance(item[1], list):
                            x.addChild(CustomNode(item[1][1],item[1][0]))
                        else:
                            x.addChild(CustomNode(None,item[1]))
            if(len(item) == 3):
                for x in self.treeItems[0]._children:
                    if(x._data == [item[0]]):
                        for y in x._children:
                            if(y._data == [item[1]]):
                                test = item[2][0]
                                y.addChild(CustomNode(item[2][1],item[2][0]))

        self.model = TreeModel(self.treeItems)

        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.model.selectedItemChanged)
        self.treeView.setColumnWidth(0,1000)
        self.treeView.expandAll()

    def clearTree(self):
        self.treeItems = []
        self.treeView.setModel(TreeModel(self.treeItems))