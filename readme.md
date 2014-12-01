Cook Roulette: A random meal generator
=====================
![home page]
(https://raw.githubusercontent.com/jkru/cook_roulette/master/readme_img/hompage.png)

Cook Roulette is a random meal generator that creates combinations of food so you don't have to think about what you should make for dinner.

https://guides.github.com/features/mastering-markdown/


The premise
-----
Cook Roulette randomly generates meals.

The code is run with a shell script::

     ./runscript.scr

This isn't included here, but holds the keys to yummly and twilio.

Web App Features
----------------------- 
1. Log in functionality
2. Save meals
3. Select type of meal generation (k-means, Markov chain, or random)
4. Uses Yummly API to find a recipe that uses those meal ingredients

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

