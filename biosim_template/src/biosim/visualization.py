import matplotlib.pyplot as plt
import numpy as np

class Visualization:
    def __init__(self):
        self.herb_list = []
        self.carn_list = []
        self.years = []
        self._fig = None
        

    def update_year(self, year):
        self.years.append(year)

    def update_animals(self, island_map):
        self.herb_list.append(island_map.island_total_carnivores)
        self.carn_list.append(island_map.island_total_herbivores)

    def color_map(self, island_map):
        """
        makes a colour map of the string map
        """
        colour = {'W': (0.0, 0.0, 1.0),
                  'L': (0.0, 0.6, 0.0),
                  'H': (0.5, 1.0, 0.5),
                  'D': (1.0, 1.0, 0.5)}

        colour_map = [[colour[column] for column in row]
                      for row in island_map.string_map.splitlines()]


        plt.imshow(colour_map)



    def herb_map(self,island_map):
        """
        plots the population on the map by color
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
        plt.imshow(matrix)
        plt.title('Herbivore map')
        plt.colorbar()
        plt.show()


    def carn_map(self, island_map):
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
        plt.imshow(matrix)
        plt.title('Carnivore map')
        plt.colorbar()
        plt.show()



    def one_graph(self):
        """
        plotting the animals in the cell by years

        """

        plt.title('Herbivores and carnivores on the island')
        plt.plot(self.years,self.herb_list,self.years, self.carn_list)
        plt.xlabel('years')
        plt.ylabel('Num of Animals')
        plt.show()


