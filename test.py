from PyQt5 import QtWidgets
import pyqtgraph as pg
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setTitle('Test')
        self.setCentralWidget(self.graphWidget)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature_1 = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        temperature_2 = [50, 35, 44, 22, 38, 32, 27, 38, 32, 44]

        # Add Background colour to white
        self.graphWidget.setBackground('w')

        # Add Axis Labels
        self.graphWidget.setLabel('left', 'Temperature (°C)', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Time (s)', color='red', size=30)

        # Add legend
        self.graphWidget.addLegend()

        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        # Set Range
        self.graphWidget.setXRange(0, 11)
        self.graphWidget.setYRange(20, 55)

        self.plot(hour, temperature_1, "Sensor1", 'r')
        self.plot(hour, temperature_2, "Sensor2", 'b')

    def plot(self, x, y, plot_name, color):
        pen = pg.mkPen(color=color, width=5)
        self.graphWidget.plot(x, y, name=plot_name, pen=pen, symbol='o', symbolSize=10, symbolBrush=color)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exit(app.exec_())


if __name__ == '__main__':
    main()


# https://www.learnpyqt.com/courses/graphics-plotting/plotting-pyqtgraph/
