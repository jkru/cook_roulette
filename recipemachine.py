import random
import config_db

class RecipeMachine(object):
    #class that creates the meals

    def generate_markov_recipe(self):
        """RM method that creates Markov chain meals.

        Uses config getter to get the Markov chain dictionary, picks a
        seed ingredient, calls a function that fills out the rest of
        the meal based on the seed ingredient, formats the meal to
        remove the underscores, and then returns the completed Markov
        meal.

        """
        self.markov_chain_dict = config_db.getter()[4]
        self.markov_seed_ingr = random.choice(self.markov_chain_dict.keys())
        self.markov_meal = self.populate_markov_meal()
        self.meal = self.markov_meal
        display_meal = self.nounder()
        return self.meal

    def populate_markov_meal(self):
        """Populates the meal skeleton for Markov meals.

        Randomly selects an ingredient from the Markov chain
        associated with random seed ingredient. Checks if the meal
        skeleton is complete. Returns meal if it is, keeps going if
        it's not. If more than 20 items have been generated, and the
        meal is still not complete, it picks a new random seed
        ingredient and uses that as the base for the Markov
        chain. Currently an bi-gram.

        """

        ingredient_by_type = config_db.getter()[3]
        
        meal = {"protein":"", "vegetable":"", "starch":""}
        needs_more = True
        my_ingredient = self.markov_seed_ingr
        counter = 0

        while needs_more:
            my_list_of_types = ingredient_by_type[my_ingredient]
            my_first_type = my_list_of_types[0]
            meal[my_first_type] = my_ingredient
            my_ingredient = random.choice(self.markov_chain_dict[self.markov_seed_ingr])
            counter +=1
            if counter == 20:
                counter = 1
                my_ingredient = random.choice(self.markov_chain_dict.keys())

            if meal['protein'] != "" and meal['vegetable']!="" and meal['starch']!="":
                needs_more = False
        return meal
        
    def generate_random_recipe(self):
        """Generates the meal for the random meals.

        Gets a list of types with every associated ingredient from the
        entire recipe database. Calls the meal skeleton-filling
        method. Checks to see if meal is completed. Passes it through
        a formatter to take out underscores. Returns completed meal.

        note: congfig_db2 => {protein: chicken, steak}
        """

        self.all_types = config_db.getter()[2]
        while True:
            self.meal = self.make_random_meal()
            complete_meal = self.check_meal()
            display_meal = self.nounder()

            if complete_meal:
                return self.meal
                break

    def make_random_meal(self):
        """Fills in the meal skeleton for the random meal.

        Randomly selects an ingredient associated with each
        type. Returns meal.

        """

        meal = {}
        for type_, ingredients in self.all_types.iteritems():
            meal[type_] = random.choice(ingredients)
        return meal


    def generate_kmeans_recipe(self):
        """Generates the k-means meals.
        
        Gets a dictionary filled with clusters and associated
        ingredients. Randomly chooses a cluster. Sorts ingredients of
        said cluster into types. Calls method that fills the meal
        skeleton. Checks to see if the meal is complete. Calls
        function to remove underscores. Returns completed meal.

        """
        while True:
            self.cluster = config_db.getter()[0].keys()
            self.seed_cluster = random.choice(self.cluster)
            self.ingr_sorted_type = self.get_ing_type()
            self.meal = self.make_kmeans_meal()
            complete_meal = self.check_meal()
            display_meal = self.nounder()

            if complete_meal:
                return self.meal
                break    

    def nounder(self):
        """takes out underscores from names.
        
        Goes through a dictionary and takes out the underscores in all
        of the ingredients (items).

        """
        for type_, item in self.meal.iteritems():
            self.meal[type_] = item.replace("_"," ")
        return self.meal
            

    def get_ing_type(self):
        """returns a dictionary of all of the ingredients in a cluster that
        are sorted based on their type.

        Looks in the dictionary where key=cluste number and value =
        each ingredient. Appends each to the correct type.

        #do something here where it makes the ingredient type based on the
        #global type_dictionary, that has the ingredients categorized by type
        #and then grabs at the ingredients that are in the particular cluster
        #dictionary.
        """

        thisclusterings = config_db.getter()[1][self.seed_cluster]
        alltypes = config_db.getter()[2]
        allingrs = config_db.getter()[3]
        ingr_sorted_type = {}

        this_cluster_types = {}
        
        for ingr in thisclusterings:
            ingr = ingr.replace(" ","_")
            for alltypes in allingrs[ingr]:
                this_cluster_types.setdefault(alltypes,[]).append(ingr)
        return this_cluster_types


    def make_kmeans_meal(self):
        """populates the k-means meal dictionary. 

        Picks a random ingredient from each ingredient type associated
        with a particular cluster.

        """

        meal = {'vegetable':"",'protein':"",'starch':""}
        for key, value in self.ingr_sorted_type.iteritems():
            if value != "":
                meal[key] = random.choice(self.ingr_sorted_type[key])
        return meal
    
    def check_meal(self):
        """checks to see if there are empty entries in the meal.
        """

        if "" not in self.meal.values():
            return True

if __name__=="__main__":
    import doctest
    doctest.testmod()
