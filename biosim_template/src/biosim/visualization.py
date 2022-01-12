import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

"""
Inspired by Hans Ekkehard Plessers Grapichs ile from randvis prodject
Link: https://gitlab.com/nmbu.no/emner/inf200/h2021/inf200-course-materials/-/blob/main/january_block/examples/randvis_project/src/randvis/graphics.py
"""
_DEFAULT_DIR = os.path.join(r'C:\Users\pbuka\Code\JanuarBlokk\biosim-a17-peder-bard\biosim_template','results')
_DEFAULT_NAME = 'sim'
_DEFAULT_FORMAT = 'png'

class Visualization:
    """ Visualizes the results from biosim"""
    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
        """
        :param img_dir: directory for image files to be stored
        :param img_name: start of image name
        :param img_fmt: format of image

        """

        self._fig = None
        self._map_ax = None
        self._herb_ax = None
        self._carn_ax = None
        self._pop_ax = None
        self._pop_line = None

    def _color_map(self, island_map):
        """
        makes a colour map of the string map
        """
        colour = {'W': (0.0, 0.0, 1.0),
                  'L': (0.0, 0.6, 0.0),
                  'H': (0.5, 1.0, 0.5),
                  'D': (1.0, 1.0, 0.5)}

        colour_map = [[colour[column] for column in row]
                      for row in island_map.string_map.splitlines()]
        self._img_ax = plt.imshow(colour_map)


    def setup(self, island_map, final_year):
        """
        prepares for plotting

        Has to be called before :meth: 'update_plot'

        """

        self._img_step = None

        # create new plot window
        if self._fig is None:
            self._fig = plt.figure()


        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2,2,1)
        self._color_map(island_map)

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(2,2,3)

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(2,2,4)

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(2,2,2)

        if self._pop_line is None:
            pop_plot = self._pop_ax.plot(np.arange(0,final_year), np.full(final_year,np.nan))
            self._pop_line = pop_plot[0]
        else:
            x_data, y_data = self._pop_line.get_data()
            x_new = np.arange(x_data[0], final_year+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._pop_line.set_data(np.hstack((x_data,x_new)),np.hstack((y_data,y_new)))

    def update(self, year, island_map):
        """
        updates plot with current year

        :param year: is the year the simulation currently is in
        :param island_map: is the island map object to be plotted
        """
        self._update_herb_map(island_map)
        self._update_carn_map(island_map)
        self._update_pop_graph(year, island_map)
        self._fig.canvas.flush_events()
        plt.pause(1e-6)


    def _update_herb_map(self,island_map):
        """
        plots the population on the map by color

        :param island_map: is the island_map object containg info about the simulation
        """

        nested_list = list(map(list,island_map.string_map.splitlines()))
        x = 1
        for i in range(len(nested_list)):
            y = 1
            for j in range(len(nested_list[0])):
                if island_map.map_dict[(x, y)].population_sum_herb == None:
                    nested_list[i][j] = 0
                else:
                    nested_list[i][j] = island_map.map_dict[(x, y)].population_sum_herb
                y += 1
            x += 1

        matrix = np.array(nested_list)
        self._herb_ax.imshow(matrix)



    def _update_carn_map(self, island_map):
        nested_list = list(map(list, island_map.string_map.splitlines()))
        x = 1
        for i in range(len(nested_list)):
            y = 1
            for j in range(len(nested_list[0])):
                if island_map.map_dict[(x, y)].population_sum_carn == None:
                    nested_list[i][j] = 0
                else:
                    nested_list[i][j] = island_map.map_dict[(x, y)].population_sum_carn
                y += 1
            x += 1

        matrix = np.array(nested_list)
        self._carn_ax.imshow(matrix)




    def _update_pop_graph(self, year, island_map):
        """
        plotting the animals in the cell by years|
        """

        y_data = self._pop_line.get_ydata()
        y_data[year] = island_map.island_total_herbivores + island_map.island_total_carnivores
        self._pop_line.set_ydata(y_data)


    def show_plot(self):

        plt.show()




