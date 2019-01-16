
import matplotlib.pyplot as plt


class PlotGraph:

    def __init__(self, x_list, y_list):
        self.x = x_list
        self.y = y_list

    def name_plot(self, name_x, name_y, title):
        plt.xlabel(name_x)
        plt.ylabel(name_y)
        plt.title(title)

    def plot_graph(self):
        plt.plot(self.x, self.y)
        plt.show()
