import sys
from PySide.QtGui import QPushButton,  QWidget, QVBoxLayout, \
                        QHBoxLayout, QFormLayout, QComboBox, \
                        QLineEdit, QLabel, QIntValidator, QIcon


class ControlLayout(QWidget):
    """Widget that stores the controls"""

    def __init__(self):
        QWidget.__init__(self)

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        # The products that we want to make available
        self.products = ['Producto A']

        # Create and fill the combo box to choose the product
        self.product = QComboBox(self)
        self.product.addItems(self.products)

        # Add it to the form layout with a label
        self.form_layout.addRow('Producto:', self.product)

        # Add policies label and combobox
        self.policies = ['Qs', 'Ss', 'RS', 'RSs']
        self.policy = QComboBox(self)
        self.policy.addItems(self.policies)
        self.form_layout.addRow('Politica', self.policy)

        # Connect policy button to hide 3rd parameter
        self.policy.activated.connect(self.changed_policy)

        # Add Parameters
        self.parameters = QLabel('', self)
        self.form_layout.addRow("&Parametros", self.parameters)

        # Parameter 1
        self.p1 = QLineEdit(self, QWidget)
        self.p1_label = QLabel("Q")

        self.pam1_box = QHBoxLayout()
        self.pam1_box.addWidget(self.p1_label)
        self.pam1_box.addStretch(1)
        self.pam1_box.addWidget(self.p1)

        self.form_layout.addRow(self.pam1_box)

        # Parameter 2
        self.p2 = QLineEdit(self, QWidget)
        self.p2_label = QLabel("s")

        self.pam2_box = QHBoxLayout()
        self.pam2_box.addWidget(self.p2_label)
        self.pam2_box.addStretch(1)
        self.pam2_box.addWidget(self.p2)

        self.form_layout.addRow(self.pam2_box)

        # Parameter 3
        self.p3 = QLineEdit(self, QWidget)
        self.p3.hide()
        self.p3_label = QLabel("")

        self.pam3_box = QHBoxLayout()
        self.pam3_box.addWidget(self.p3_label)
        self.pam3_box.addStretch(1)
        self.pam3_box.addWidget(self.p3)

        self.form_layout.addRow(self.pam3_box)

        # Add Periods
        self.periods = QLineEdit(self, QWidget)
        self.periods_label = QLabel("Periodos")

        self.periods_box = QHBoxLayout()
        self.periods_box.addWidget(self.periods_label)
        self.periods_box.addStretch(1)
        self.periods_box.addWidget(self.periods)

        self.form_layout.addRow(self.periods_box)

        # Add form layout to main layout
        self.layout.addLayout(self.form_layout)

        # Add stretch to separate the form layout from the button
        self.layout.addStretch(1)

        # Create a horizontal box layout to hold the button
        self.button_box = QHBoxLayout()

        # Add stretch to push the button to the far right
        #self.button_box.addStretch(1)

        # Create the sim button with its caption
        self.sim_button = QPushButton('Simular', self)

        # Add it to the button box
        self.button_box.addWidget(self.sim_button)

        # Add the button box to the bottom of the main VBox layout
        self.layout.addLayout(self.button_box)

        self.setLayout(self.layout)

    def changed_policy(self):
        """Changes labels if the policy is changed"""
        pol = self.policy.currentText()
        if pol in ['Qs', 'Ss', 'RS']:
            self.p3_label.setText('')
            self.p3.hide()
            if pol == 'Qs':
                self.p1_label.setText('Q')
                self.p2_label.setText('s')
            elif pol == 'Ss':
                self.p1_label.setText('S')
                self.p2_label.setText('s')
            elif pol == 'RS':
                self.p1_label.setText('R')
                self.p2_label.setText('S')
        elif pol == 'RSs':
            self.p1_label.setText('R')
            self.p2_label.setText('S')
            self.p3_label.setText('s')
            self.p3.show()
