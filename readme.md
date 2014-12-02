Cook Roulette: Data-driven meals
=====================
![home page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/homepage.png)

Cook Roulette is a random meal generator that creates combinations of food so you don't have to think about what you should make for dinner.

The premise 
----- 

Let's look at meal generation from a data-driven perspective. A recipe
is really a list of ingredients with associated amounts and
instructions; however for this project I consider a recipe to simply be a list of ingredients.  Websites such as allrecipes.com and foodnetwork.com
have an incredible amount of recipe content. I scraped and cleaned
recipes from a variety of websites, and used publicly-availble data
from [Y.-Y. Ahn et
al.](http://www.scientificamerican.com/article/flavor-connection-taste-map-interactive/)
for this project. Ingredients can be associated with each other in a variety of
ways and for Cook Roulette, I examined these in three ways:
1. k-means clustering
2. Markov chains
3. Randomness


 k-means clustering
----
Machine learning (ML) is an excellent way to learn information from a
dataset and comes in two flavors: supervised and unsupervised. One of
the most common unsupervised ML algorithms is k-means clustering. 

The k-means algorithm works by taking a dataset and dividing it into k
number of clusters. There are, thus, k number of centroids that
correspond to the center of a given cluster. These centroids are
initially randomly placed throughout the data set. Each point in the
dataset is then evaluated to see which centroid it is closest to. It
is then assigned to belong to the cluster group of the closest
centroid. Once all points are evaluted, the centroids are moved to
reflect the center of their individual cluster. Ideally, this process
is iterated until the cluster membership is stabilized and movement of
the centroids has ceased.

For Cook Roulette, I implemented k-means clustering on the scraped
recipes. The distances used to determine cluster membership is the
Pearson correlation coefficient, which compares the inclusion of
ingredients (e.g., pizza and pasta both have cheese and tomatoes and
are likely to be in the same cluster which is distinct from green bean
casserole and mushroom soup which both have cream and mushrooms). The
k-means meals are created by randomly selecting a cluster and then
populating a meal skeleton (i.e., something that has a vetetable,
protein, and starch) with the ingredients of that cluster.

Markov chains 
---- 

Markov chains are constructed by the probability of
an event occurring at a given state. Given a particular state, when
event a occurs, what are the probabilities associated with that event
of what might happen next? In the case of the scraped recipe, I created a database with 

Randomness 
---- 

For random meals, the ingredients are populated by a randomly selected
ingredient that fulfills each ingredient type of the meal
skeleton. The select function from the random module is used to select
each ingredient.


Web App Features
----------------------- 
1. Log in functionality
2. Save meals
3. Select type of meal generation (k-means, Markov chain, or random)
4. Uses Yummly API to find a recipe that uses those meal ingredients


Let's cook!
-------------
Cook Roulette randomly generates meal skeletons.

The code is run with a shell script::

     ./cookroulette.scr

This script would nominally hold API keys for twilio and yummly in
order to achieve full functionality of the site. These are omitted in
this repository, but instructions for setting up both are included at
the end.





User Experience
-----------------------
Users can create an account:
![create page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/create_account.png)

And then log into the page:
![login page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/login.png)

The main part of the page:
![main page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/main_part.png)


Extras
-----------------------
1. Text to twilio for a k-means generated meal

2. Outward facing REST-ful API that provides a json object with a generated k-means meal

Technology stack
----
1. Python
2. Python Flask
3. SQLAlchemy
4. Sqlite
5. Yummly API
6. JQuery/Javascript
7. Twilio API
8. Jinja2
9. HTML/CSS/Bootstrap