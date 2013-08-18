import sys
from PySide.QtGui import QPushButton,  QWidget, QVBoxLayout, \
                        QHBoxLayout, QFormLayout, QComboBox, \
                        QLineEdit, QLabel, QGridLayout, QIcon
from PySide.QtCore import Slot                


class SummaryLayout(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.layout = QVBoxLayout()

        self.grid = QGridLayout()
       
        self.service_title = QLabel("NIVEL DE SERVICIO")
        self.service_title.setStyleSheet("""
            QLabel {
            font: bold "Arial";
            font-size: 16px;
            } 
            """)
        
        self.service_level = QLabel("")
        self.service_level.setStyleSheet("""
            QLabel {
            font: "Arial";
            font-size: 16px;
            } 
            """)
        
        self.cost_title = QLabel("COSTO")
        self.cost_title.setStyleSheet("""
            QLabel {
            font: bold "Arial";
            font-size: 16px;
            } 
            """)
        
        self.inventory_cost = QLabel("")
        self.inventory_cost.setStyleSheet("""
            QLabel {
            font: "Arial";
            font-size: 16px;
            text-align: center;
            } 
            """)

        # img_icon = QIcon("table.png")
        # self.table_btn = QPushButton(img_icon, "",self)
        # self.table_btn.setFlat(True)
        # self.table_btn.setToolTip("Muestra resultados")

        self.grid.addWidget(self.cost_title, 0, 0)
        self.grid.addWidget(self.inventory_cost, 1, 0)
        
        self.grid.addWidget(self.service_title, 0, 1)
        self.grid.addWidget(self.service_level, 1, 1)

        #self.grid.addWidget(self.table_btn, 0, 2)
        #self.grid.addWidget(self.service_level, 1, 2)
        
        self.setLayout(self.grid)     
