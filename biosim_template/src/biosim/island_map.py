]    def feeding(self):
        """
        Animals residing in a cell eat in descend- ing order of fitness.
        Each animal tries every year to eat an amount F of fodder,
        but how much feed the animal obtain depends on fodder available in the cell

        Here:
        F = 10
        f_max = 800
        """
        self.animals_in_cell.sort(reversed=True, key='fitness')
        all_herbivore = np.array(self.animals_in_cell)
        available_fodder = 800
        appetite = 10
        for herbivore in all_herbivore:
            if available_fodder == 0:
                break
            elif available_fodder >= appetite:
                # herbivore.eat(appetite)
                available_fodder = available_fodder - appetite
            elif 0 < available_fodder < appetite:
                # herbivore.eat(available_fodder)
                available_fodder = 0

    def procreation(self):
        """
        Animals can mate if there are at least two animals of the same species in a cell.
        Gender plays no role in mating.Each animal can give birth to at most one off- spring per year.
        At birth, the mother animal loses ξ times the actual birth weight of the baby.
        If the mother would lose more than her own weight,
        then no baby is born and the weight of the mother remains unchanged.
        """
        pass

    def migration(self):
        """No migration on one cell island"""
        pass

    def aging(self):
        """
        At birth, each animal has age a = 0 .
        Age increases by one year for each year that passes
        """
        for animal in self.animals_in_cell:
            # animal.grow_up()
            pass

    def weight(self):
        """
        Every year, the weight of the animal decreases.
        When an animal eats an amount of fodder, its weight increases.
        """
        for animal in self.animals_in_cell:
            # animal.lose_weight
            pass

        for animal in self.animals_in_cell:
            # animal.gain_weight
            pass

    def death(self):
        """
        Animals die when its weight is w = 0
        """
        for animal in self.animals_in_cell:
            if animal.death:
                # self.animals_in_cell.remove(animal)
                pass
