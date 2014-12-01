import model

global CLUSTERS 
CLUSTERS = None
global CLUSTER_INGREDIENTS
CLUSTER_INGREDIENTS = None
global TYPE_DICTIONARY
TYPE_DICTIONARY = None
global INGR_TYPE
INGR_TYPE = None
global CHAINS
CHAINS = None


def get_recipes_in_clusters():
    """makes a dictionary of clusters

    Queries the recipe table and creates a dictionary with 
    key = cluster, value = recipes in the cluster.

    """
    allrecipes = model.session.query(model.Recipe).all()
    clusters = {}
    for recipe in allrecipes:
        if clusters.get(recipe.cluster,0) != 0:
            clusters[recipe.cluster] == clusters[recipe.cluster].append(recipe.id)
        else:
            recipelist = []
            recipelist.append(recipe.id)
            clusters[recipe.cluster] = recipelist
    return clusters
        
def get_ingredients_in_clusters(clusters):
    """takes {recipe:cluster} dict and figures out what ingredients belong
    to each cluster.

    """
    cluster_ingredients = {}
    for cluster, recipes in clusters.iteritems():
        cluster_recipes_ingredients = []
        for recipe in recipes:
            a_recipe =  model.session.query(model.Recipe).filter_by(id=recipe).all()
            the_ingredients = a_recipe[0].ingredients
            ingredients_list = []
            for an_ingredient in the_ingredients:
                no_under_ingred= an_ingredient.name.replace("_"," ")
                ingredients_list.append(no_under_ingred)
            cluster_recipes_ingredients.extend(ingredients_list)
        cluster_ingredients[cluster] = cluster_recipes_ingredients
    return cluster_ingredients

def ingredient_types():
    """creates a dictionary of ingredients by type.

    queries SQL database and then creates a dictionary with
    {type:[ingredients]}

    """
    all_types = model.session.query(model.Type_).all()    

    type_dictionary = {}

    for a_type in all_types:
        types_list = []
        typed_ingredients = a_type.ingredients
        for my_ingredient in typed_ingredients:
            types_list.append(my_ingredient.name)
        type_dictionary[a_type.name] = types_list
    return type_dictionary


def types_ingredients():
    """creates a dictioanry of types by ingredient

    queries SQL database and then creates a dictionary with
    {ingredient:[types]}
    """

    all_ingrs = model.session.query(model.Ingredient).all()    

    ingr_dictionary = {}

    for an_ingr in all_ingrs:
        ingr_list = []
        associated_types = an_ingr.types_
        for my_type in associated_types:
            ingr_list.append(my_type.name)
        ingr_dictionary[an_ingr.name] = ingr_list
    return ingr_dictionary


def markov_db():
    """creates a dictionary for the markov recipes.

    goes through and makes a dictionary with key = ingredient value =
    list of every other ingredient that the key ingredient is in a
    recipe with. Sorry English grammar, you lose this round.

    """
    all_recipes = model.session.query(model.Recipe).all()
    chains = {}
    for a_recipe in all_recipes:
        ingr_names = []
        for ingr in a_recipe.ingredients:
            ingr_names.append(ingr.name)

        for ingr_name in ingr_names:
            chains.setdefault(ingr.name,[]).extend(ingr_names)
 
    for ingredient, coincident_ingredients in chains.iteritems():
        de_duped=[]
        for co_ing in coincident_ingredients:
            if co_ing != ingredient:
                de_duped.append(co_ing)
        chains[ingredient]=de_duped
    return chains


def getter():
    """Getter function for the dictionaries that contain the meal
    generation dictionaries.
    
    looks for the global variables. If they don't exist, go run the
    functions that creates them. Otherwise, return the global
    variables.

    """

    global CLUSTERS
    global CLUSTER_INGREDIENTS
    global TYPE_DICTIONARY
    global INGR_TYPE
    global CHAINS
    if CLUSTERS is None:
        CLUSTERS = get_recipes_in_clusters()
        CLUSTER_INGREDIENTS = get_ingredients_in_clusters(CLUSTERS)
        TYPE_DICTIONARY = ingredient_types()
        INGR_TYPE = types_ingredients()
        CHAINS = markov_db()
    return [CLUSTERS, CLUSTER_INGREDIENTS, TYPE_DICTIONARY, INGR_TYPE, CHAINS]


#set globals = None
#if globals = None
#do the fucntions to get the dictionaries
#else return globals

#instead of returns, global blah blah = dictionary

#getters to return variables

if __name__=="__main__":
    main()
    
