Cook Roulette: Data-driven meals
=====================
![home page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/readme_img/homepage.png)

Cook Roulette is a random meal generator that creates combinations of food so you don't have to think about what you should make for dinner.

The premise 
----- 

Let's look at meal generation from a data-driven perspective. Websites
such as allrecipes.com and foodnetwork.com have an incredible amount
of recipe content. A recipe is really a list of ingredients with
associated amounts and instructions. For this project, I considered a
recipe to be a set of ingredients. 

Ingredients can be associated with each other in a variety of
ways. For Cook Roulette, I examined them in three ways:

1. k-means clustering
2. Markov chains
3. Complete randomness


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
(https://raw.githubusercontent.com/jkru/cook_roulette/master/readme_img/create_account.png)

And then log into the page:
![login page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/readme_img/login.png)

The main part of the page:
![main page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/readme_img/main_part.png)


Extras
-----------------------
1. Text to twilio for a k-means generated meal

2. Outward facing REST-ful API that provides a json object with a generated k-means meal

