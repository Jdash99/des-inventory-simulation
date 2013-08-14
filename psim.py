import sys
import numpy as np
from PySide.QtGui import QApplication,QWidget,\
                            QVBoxLayout, QHBoxLayout, QMainWindow, QFont
from PySide.QtCore import Slot


import psim_plot
import psim_control
import psim_summary

from psim_functions import make_distribution, make_data, Product


class MainWindow(QWidget):
    """Class that contains the main window
    Includes two panels: 
    left panel -> control
    right panel -> plot and summary
    """

    def __init__(self, parent=None):

        QWidget.__init__(self)

        # Create the QVBoxLayout that lays out the whole form
        self.main_panel = QHBoxLayout()
        self.lpanel = QHBoxLayout()
        self.rpanel = QVBoxLayout()
        self.plot_box = QHBoxLayout()
        self.summary_box = QHBoxLayout()

        # Control widget
        self.control = psim_control.ControlLayout()
        self.control.sim_button.clicked.connect(self.button_pressed)

        # Plot Widget
        self.graph = psim_plot.MatplotlibWidget()

        # Summary Widget
        self.summary = psim_summary.SummaryLayout()

        # Adding plot to left panel and control widget to right panel
        self.lpanel.addWidget(self.control)
        self.rpanel.addWidget(self.graph)
        self.rpanel.addWidget(self.summary)
        
        # Adding lpanel and rpanel widget to the main MainWindow
        self.main_panel.addLayout(self.lpanel)
        self.main_panel.addLayout(self.rpanel)
        # self.main_panel.addStretch(1)
        self.setLayout(self.main_panel)

        self.df = None

    @Slot()
    def button_pressed(self):
        """Actions when sim button is pressed"""
        policy_name = self.control.policy.currentText()

        pam1 = int(self.control.p1.text())
        pam2 = int(self.control.p2.text())
        periods = int(self.control.periods.text())

        product = Product("Product_A",
                          make_distribution(np.random.normal, 7, 3),
                          make_distribution(np.random.triangular, 1, 2, 3),
                          15,
                          100000.0)

        if policy_name == 'Qs':
            policy = {'method': 'Qs', 'arguments': {'Q': pam1, 's': pam2}}
        elif policy_name == 'Ss':
            policy = {'method': 'Ss', 'arguments': {'S': pam1, 's': pam2}}
        elif policy_name == 'RS':
            policy = {'method': 'RS', 'arguments': {'R': pam1, 'S': pam2}}
        elif policy_name == 'RSs':
            pam3 = int(self.control.p3.text())
            policy = {
                'method': 'RSs',
                'arguments': {
                    'R': pam1,
                    'S': pam2,
                    's': pam3}}

        self.df = make_data(product, policy, periods)
        
        carrying_cost = sum(self.df['avg_inv']) * product.price * (0.21) * (periods / 52.0)
        shortage_cost = sum(self.df['lost_sales']) * product.price
        total_cost = carrying_cost + shortage_cost
        service = 1 - (sum(self.df['lost_sales']) / sum(self.df['demand']))
        self.summary.inventory_cost.setText("{:,.2f}".format(total_cost))
        self.summary.service_level.setText("{:.2%}".format(service))
        self.graph.Plot(self.df, policy, periods)
        self.graph.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()

    frame.show()
    app.exec_()
