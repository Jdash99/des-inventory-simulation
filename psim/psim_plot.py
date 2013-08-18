import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(FigureCanvas):

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure(dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

    def Plot(self, df, policy, periods):
        self.axes.clear()
        y1 = df['initial_net_inv']
        d = df['demand']

        if policy['method'] == 'Qs':
            y2 = policy['arguments']['s'] * np.ones(periods)
            l1, = self.axes.step(
                y1, 'k', linewidth=1.2, label='Nivel Inv.', where='post', alpha=0.7)
            l2, = self.axes.plot(y2, 'r-', label='Punto de reorden', alpha=0.8)
            #l2, = self.axes.axhline(y=3)
        elif policy['method'] == 'Ss':
            y2 = policy['arguments']['s'] * np.ones(periods)
            y3 = policy['arguments']['S'] * np.ones(periods)
            l1, = self.axes.step(
                y1, 'k', linewidth=1.2, label='Nivel Inv.', where='post', alpha=0.7)
            l2, = self.axes.plot(y2, 'r-', label='Punto de reorden', alpha=0.8)
            l3, = self.axes.plot(y3, 'b-', label='Nivel Max.', alpha=0.8)
        elif policy['method'] == 'RS':
            y2 = policy['arguments']['S'] * np.ones(periods)
            l1, = self.axes.step(
                y1, 'k', linewidth=1.2, label='Nivel Inv.', where='post', alpha=0.7)
            l2, = self.axes.plot(y2, 'b:', label='Nivel Max.')
        elif policy['method'] == 'RSs':
            y2 = policy['arguments']['s'] * np.ones(periods)
            y3 = policy['arguments']['S'] * np.ones(periods)
            l1, = self.axes.step(
                y1, 'k', linewidth=1.2, label='Nivel Inv.', where='post', alpha=0.7)
            l2, = self.axes.plot(y2, 'r:', label='Punto de reorden')
            l3, = self.axes.plot(y3, 'b:', label='Nivel Max.')

        l4, = self.axes.step(d, 'g', linewidth=1.2, label='Demanda.', alpha=0.5)
        #t = self.axes.set_title(policy['method'] + ' Simulation')
        t = self.axes.set_title("Simulación {}".format(policy['method']))
        self.axes.legend(loc='best', prop={'size': 10})
        self.axes.set_xlabel("Periodos")
        self.axes.set_ylabel("Nivel de Inventario")

