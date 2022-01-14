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
        self._herb_plot = None
        self._carn_ax = None
        self._carn_plot = None
        self._pop_ax = None
        self._pop_plot = None
        self._herb_line = None
        self._carn_line = None
        self._fitness_ax = None
        self._weight_ax = None
        self._age_ax = None


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


    def setup(self, island_map, final_year,y_max=None,cmax=200):
        """
        prepares for plotting

        Has to be called before :meth: 'update_plot'

        """

        self._img_step = None

        # create new plot window
        if self._fig is None:
            self._fig = plt.figure()


        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 3, 4)
        self._color_map(island_map)

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(3, 3, 5)
            self._herb_plot = None

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(3, 3, 6)
            self._carn_plot = None

        if self._age_ax is None:
            self._age_ax = self._fig.add_subplot(3, 3, 7)

        if self._weight_ax is None:
            self._weight_ax = self._fig.add_subplot(3, 3, 8)

        if self._fitness_ax is None:
            self._fitness_ax = self._fig.add_subplot(3, 3, 9)

        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(3, 3, 2)
            self._pop_ax.title.set_text('Population of island')
            self._pop_ax.set(xlabel ='Years',ylabel='Num of animals')
        if y_max is not None:
            self._pop_ax.set_ylim(0,y_max)
        self._pop_ax.set_xlim(0,final_year+1)


        if self._herb_line is None:
            pop_plot = self._pop_ax.plot(np.arange(0,final_year+1),
                                           np.full(final_year+1,np.nan))
            self._herb_line = pop_plot[0]

        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1]+1,final_year+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape,np.nan)
                self._herb_line.set_data(np.hstack((x_data,x_new)),
                                        np.hstack((y_data,y_new)))

        if self._carn_line is None:
            pop_plot = self._pop_ax.plot(np.arange(0, final_year + 1),
                                         np.full(final_year + 1, np.nan))
            self._carn_line = pop_plot[0]
        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)),
                                        np.hstack((y_data, y_new)))

        self._fig.subplots_adjust(wspace=0.30,hspace=0.30)


    def update(self, year, island_map,cmax=200,hist_specs=None):
        """
        updates plot with current year

        :param year: is the year the simulation currently is in
        :param island_map: is the island map object to be plotted
        """
        plt.ion()
        self._update_herb_map(island_map,cmax)
        self._update_carn_map(island_map,cmax)
        self._update_pop_graph(year, island_map)
        self._update_age_weight_fitness(island_map,hist_specs=None)
        self._fig.canvas.flush_events()
        plt.pause(1e-6)
        self._fig.show()


    def _update_herb_map(self,island_map,cmax):
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

        if self._herb_plot is None:
            self._herb_plot = self._herb_ax.imshow(matrix,interpolation='nearest',vmin=0,vmax=200)
            plt.colorbar(self._herb_plot,ax=self._herb_ax)
        else:
            self._herb_plot.set_data(matrix)



    def _update_carn_map(self, island_map,cmax):
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
        if self._carn_plot is None:
            self._carn_plot = self._carn_ax.imshow(matrix,interpolation='nearest',vmin=0,vmax=cmax)
            plt.colorbar(self._carn_plot,ax=self._carn_ax)
        else:
            self._carn_plot.set_data(matrix)


    def _update_age_weight_fitness(self,island_map,hist_specs):
        hist_specs ={
            'weight':{'max':80,'delta':2},
            'age':{'max':40,'delta':2},
            'fitness':{'max':1,'delta':2}

        }
        """
        updates the histograms of age weight and fitness,

        :param island_map: island_map object containing all info about island
        """
        herb,carn = island_map.island_age_weight_fitness()

        self._age_ax.cla()
        self._age_ax.hist(herb['age'],histtype='step',range=(0,hist_specs['age']['max']),rwidth=hist_specs['age']['delta'])
        self._age_ax.hist(carn['age'],histtype='step',range=(0,hist_specs['age']['max']),rwidth=hist_specs['age']['delta'])

        self._weight_ax.cla()
        self._weight_ax.hist(herb['weight'],histtype='step',range=(0,hist_specs['weight']['max']),rwidth=hist_specs['weight']['delta'])
        self._weight_ax.hist(carn['weight'],histtype='step',range=(0,hist_specs['weight']['max']),rwidth=hist_specs['weight']['delta'])

        self._fitness_ax.cla()
        self._fitness_ax.hist(herb['fitness'],histtype='step',range=(0,hist_specs['fitness']['max']),rwidth=hist_specs['fitness']['delta'])
        self._fitness_ax.hist(carn['fitness'],histtype='step',range=(0,hist_specs['fitness']['max']),rwidth=hist_specs['fitness']['delta'])


    def _update_pop_graph(self, year, island_map):
        """
        plotting the animals in the cell by years|

        :param year: what year it is in used for x axis in this case
        :param island_map: island_map object containing all info about island
        """

        y_data_herb = self._herb_line.get_ydata()
        y_data_herb[year] = island_map.island_total_herbivores
        self._herb_line.set_ydata(y_data_herb)

        y_data_carn = self._carn_line.get_ydata()
        y_data_carn[year] = island_map.island_total_carnivores
        self._carn_line.set_ydata(y_data_carn)
        plt.pause(1e-6)












