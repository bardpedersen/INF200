import matplotlib.pyplot as plt
import numpy as np

class WindowPlot:
    def __init__(self, island_map):
        self.herb_list = []
        self.car_list = []
        self.years = []
        self.island_map = island_map


        self._fig = None
        
        
    def update_year(self, year):
        self.years.append(year)

    def update_animals(self, num_animals):
        self.herb_list.append(num_animals)
    """"
    def update_animal_carn(self, num_animals_carn):
        self.nr_car.append(num_animals_carn)
    """

    def animals_nr(self):
        plt.plot(self.years, self.herb_list)
        plt.xlabel('Years')
        plt.ylabel('Animals')
        plt.title('Herbivores in single cell')

    def color_map(self):
        colour = {'W': (0.0, 0.0, 1.0),
                  'L': (0.0, 0.6, 0.0),
                  'H': (0.5, 1.0, 0.5),
                  'D': (1.0, 1.0, 0.5)}

        colour_map = [[colour[column] for column in row]
                      for row in self.island_map.splitlines()]

        fig = plt.figure()
        image_axes = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # (start point, x), (start point y),
        image_axes.imshow(colour_map)


    def herb_map(self, map):
        list_of_nr_animals = []
        nr_rows = 0
        for key in map:
            list_of_nr_animals.append(map[key].population_sum_herb)

        for row in self.island_map.splitlines():
            nr_rows += 1
            pass

        nested_list = [list_of_nr_animals[i:i+nr_rows] for i in range(0, len(list_of_nr_animals), nr_rows)]
        array_list = np.array(np.array(i) for i in nested_list)

        ax = plt.subplot()
        im = ax.imshow(array_list)
        plt.colorbar(im)
        plt.show()

    def carn_map(self):


        pass

    def one_graph(self):
        fig = plt.figure(figsize=(10,10))
        #Plotting the map
        ax = fig.add_subplot(2, 2, 1)
        self.color_map()

        #plotting the animals
        self.animals_nr()

        #plotting the animals on map
        #self.herb_map()

        plt.show()

"""
    def update(n_steps):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, n_steps)
        ax.set_ylim(0, 1)def update_animals_age(self):
        self.age_car.append()
        line = ax.plot(np.arange(n_steps),    self.age_herb.append()
                       np.full(n_steps, np.nan), 'b-')[0]    pass

        for n in range(n_steps):def update_animals_fitness(self):
            ydata = line.get_ydata()    self.fitness_car.append()
            ydata[n] = np.random.random()    self.fitness_herb.append()
            line.set_ydata(ydata)    pass
            plt.pause(1e-6)

"""