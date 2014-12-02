Cook Roulette: Data-driven meals
=====================
![home page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/homepage.png)

Cook Roulette is a random meal generator that creates combinations of food so you don't have to think about what you should make for dinner.
####Table of Contents
- [The Premise](#the-premise)
  - [k-means Clustering](#k-means-clustering)
  - [Markov Chains](#markov-chains)
  - [Randomness](#randomness)
- [Web App Features](#web-app-features)
- [Let's cook: User Experience](#lets-cook-user-experience)
  - [Running Cook Roulette](#running-cook-roulette)
  - [Landing Page](#landing-page)
  - [Log in Page](#log-in-page)
  - [Create Account Page](#create-account-page)
  - [Meal Generation](#meal-generation)
  - [Account Page](#account-page)
- [Testing](#testing)
- [Extras](#extras)
  - [Twilio Texts](#twilio-texts)
  - [Cook Roulette API](#cook-roulette-api)
- [Technology Stack](#techonology-stack)
- [Installation](#installation)

##The Premise 

Let's look at meal generation from a data-driven perspective. A recipe
is really a list of ingredients with associated amounts and
instructions; however for this project I consider a recipe to simply be a list of ingredients.  Websites such as allrecipes.com and foodnetwork.com
have an incredible amount of recipe content. I scraped and cleaned
recipes from a variety of websites, and used publicly-availble data
from [Y.-Y. Ahn et
al.](http://www.scientificamerican.com/article/flavor-connection-taste-map-interactive/)
for this project. Ingredients can be associated with each other in a variety of
ways and for Cook Roulette, I examined these in three ways:


###1. k-means clustering
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

###2. Markov Chains

Markov chains are constructed by the probability of an event occurring
at a given state. Given a particular state, when event a occurs, what
are the probabilities associated with that event of what might happen
next? For Cook Roulette, I created a dictionary that associates each
ingredient of every scraped recipe with every other ingredient that it
shares a recipe with.

The meal skeleton is then populated by randomly selecting an
ingredient and then selecting the next ingredient from the associated
ingredients. This continues until the meal skeleton is populated with
an ingredient of every type. These meals are more random than the
k-means meals.

###3. Randomness

For random meals, the ingredients are populated by a randomly selected
ingredient that fulfills each ingredient type of the meal
skeleton. The select function from the random module is used to select
each ingredient. As one would expect, these meals are the most random.

##Web App Features

1. Log in functionality
2. Save meals
3. Select type of meal generation (k-means, Markov chain, or random)
4. Uses Yummly API to find a recipe that uses those meal ingredients


##Let's Cook: User Experience
### Running Cook Roulette
The code is run with a shell script::

     ./cookroulette.scr

This script would nominally hold API keys for twilio and yummly in
order to achieve full functionality of the site. These are omitted in
this repository, but instructions for setting up both are included at
the end.

###Landing Page
The landing page for Cook Roulette allows for the user to enter the site and get a randomly generated meal or log into the website.
![landing page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/homepage.png)

###Log in Page 

The log in page allows existing users to log in with email and a
password or new users to enter the create account page. The user
information is stored in a SQLite database. Passwords are salted and
hashed for security.

![login page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/login.png)

###Create Account Page

New users can create an account here, as accessed by the log in
page. Users can choose the type of ingredient association they prefer, 

![create page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/create_account.png)


###Meal Generation
The heart of the app lives on this page, which displays the randomly generated meal. 
![main page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/main_part.png)

Users can click on the button to generate more meals. These subsequent meals are displayed via a JQuery/AJAX call. The user can also select options to choose the type of meal that is generated and to enable a call the to Yummly API, which will return an image and a recipe based on a search of the generated ingredients:

![more meals]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/select_recipe.png)

If logged in, users can also save a meal that they like. 
![saved]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/savebutton.png)

###Account Page
These saved recipes, along with account information, can be accessed through the account page:
![account page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/account_page.png)

##Testing 

Unit tests were written for functions spanning the cookroulette,
config_db, and model modules. These tests were written using the
unittest python library.

To run the set of tests, simply run the run_tests script::

   ./run_tests.scr

![unit tests]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/runtest.png)



##Extras

###Twilio Texts 

I used the Twilio API to connect Cook Roulette to mobile world via
SMS. Users can text an SMS-optimized Twilio number and get a k-means
generated meal texted back. This feature widely believed to be best
used in the wild at grocery stores.

![Mobile Screenshot]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/static/img/readme_img/twilio.png)


### Cook Roulette API

Cook Roulette provides an outward-facing, REST-ful API for developers
interested in implementing random meals into their code. The API is
available at localhost:5000/api. There are no limits on API
calls. Each call returns a JSON object that is of the form:


   {"meal": { 
        "vegetable": "tomato", 
        "protein": "bacon", 
        "starch": "macaroni" 
        } 
   } 

 where each "meal" skeleton consists of a vegetable, protein, and
 starch and the ingredients are randomly populated from k-means
 clustered ingredients.

Technology Stack
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

Installation
-------
After you download the code, installation is straightforward.

1. Create a python virtual environment::

        virtualenv env


2. Activate the virtual environment::

        source env/bin/activate


3. Install the requirements::

        pip install -r requirements.txt

And now you're ready to run!

