import model 
import unittest
import config_db

class ConfigDbUnitTestCase(unittest.TestCase):

    def testShouldGiveDictionaryWithRecipeCluster(self):
        """ test make dictionary in clusters"""
        cluster_test = {1: [1]}
        self.assertEqual(config_db.get_recipes_in_clusters(),cluster_test)

    def testShouldGiveDictionaryWithClusterIngredients(self):
        """test get_ingredients_in_clusters"""
        cluster_test = {1: [1]}
        cluster_ingredients={1:[u'tomato', u'steak', u'potato']}
        self.assertEqual(config_db.get_ingredients_in_clusters(cluster_test),cluster_ingredients)

    def testShouldGiveDictionaryWithTypeIngredients(self):
        """test ingredient_types"""
        test_type_ingredient = {u'vegetable': [u'tomato'], u'protein': [u'steak'], u'starch': [u'potato']}
        self.assertEqual(config_db.ingredient_types(),test_type_ingredient)

    def testShouldGiveDictionaryWithIngredientTypes(self):
        """test types_ingredients"""
        test_ingredient_types = {u'tomato': [u'vegetable'], u'steak': [u'protein'], u'potato': [u'starch']} 
        self.assertEqual(config_db.types_ingredients(),test_ingredient_types)

    def testShouldGiveDictionaryWithIngredientIngredients(self):
        """test markov_db"""
        test_ingredient_ingredients = {u'potato': [u'tomato', u'steak', u'tomato', u'steak', u'tomato', u'steak']} 
        self.assertEqual(config_db.markov_db(),test_ingredient_ingredients)

    def testShouldGiveBackListOfPotentiallyGlobalVariables(self):
        """test getter"""
        cluster_test = {1: [1]}
        cluster_ingredients={1:[u'tomato', u'steak', u'potato']}
        test_type_ingredient = {u'vegetable': [u'tomato'], u'protein': [u'steak'], u'starch': [u'potato']}
        test_ingredient_types = {u'tomato': [u'vegetable'], u'steak': [u'protein'], u'potato': [u'starch']} 
        test_ingredient_ingredients = {u'potato': [u'tomato', u'steak', u'tomato', u'steak', u'tomato', u'steak']} 
        test_getter = [cluster_test, cluster_ingredients, test_type_ingredient, test_ingredient_types,test_ingredient_ingredients]
        self.assertEqual(config_db.getter(),test_getter)

if __name__ =="__main__":
    unittest.main()

