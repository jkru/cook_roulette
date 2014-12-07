from flask import Flask, request, render_template
from flask import redirect, url_for, flash, session, jsonify
from recipemachine import RecipeMachine
from passlib.hash import sha256_crypt
from twilio.rest import TwilioRestClient
import twilio.twiml
import os
import model
import json
import requests



app = Flask(__name__)

FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "asdf") 
app.secret_key = FLASK_SECRET_KEY

TWILIO_ACCOUNT_SID=os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN=os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER=os.environ.get('TWILIO_NUMBER')

YUMMLY_APP_ID = os.environ.get('YUMMLY_APP_ID')
YUMMLY_APP_KEY = os.environ.get('YUMMLY_APP_KEY')


@app.route("/")
def welcome_page():
    """ Renders welcome page"""
    return render_template("index.html")

@app.route("/create")
def display_create_account_page():
    """ Renders create account page"""
    return render_template("create.html")


@app.route("/create", methods =['POST'])
def actually_create_account_page():
    """Makes post requests to get user input to create an account. """

    email_in = request.form.get("email")
    password_in = request.form.get("password")
    settings_in = request.form.get("settings")    

    password_in_s_h = sha256_crypt.encrypt(password_in)
    adduser = model.create_user_account(email=email_in, password=password_in_s_h, settings=settings_in)

    flash (adduser)

    if adduser == "Successfully Added!":
        return render_template("index.html")
    else:
        return redirect(url_for("display_create_account_page"))

@app.route("/login")
def display_login_page():
    """Displays log in page. """
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def actually_login_page():
    """Makes post requests to get user input to log into account. """

    email_in = request.form.get("email")
    password_in = request.form.get("password")

    login = model.login(email_in,password_in)

    flash (login)
    if login != "Yay!":
        return redirect(url_for("display_login_page"))
    else:
        session['email'] = email_in
        session['logged_in'] = True
        session['default_setting'] = model.session.query(model.User).filter_by(email=email_in).first().settings
        return redirect(url_for("random_meal"))

@app.route("/account")
def show_account_page():
    """Renders the account page"""
    return render_template("account.html", email=session['email'])

@app.route("/changepw")
def display_change_pw():
    """Renders change password page from the account page"""
    return render_template("changepw.html", email=session['email'])

@app.route("/changepw", methods=['POST'])
def actually_change_pw():
    """Uses post requests to change the user password """

    password_check = request.form.get("oldpassword")
    password_in = request.form.get("newpassword")
    password_in2 = request.form.get("checknewpassword")

    #check old password
    login = model.login(session['email'],password_check)
    if login != "Yay!":
        flash ("Incorrect Password")
        return redirect(url_for("display_change_pw"))
    else:
        if password_in!=password_in2:
            flash ("New Password Does Not Match")
            return redirect(url_for("display_change_pw"))
        else:
            password_in_s_h = sha256_crypt.encrypt(password_in)
            updatepw = model.change_pw(session['email'],password_in_s_h)
            flash (updatepw)
            return redirect(url_for("show_account_page"))


@app.route("/displaysaved")
def display_saved_recipes():
    """Shows the saved recipes"""

    list_of_recipes = model.get_list_saved_recipes(session['email'])
    saved_recipe_list = []
    for recipe in list_of_recipes:
        saved_meal = {}
        saved_recipe = json.loads(recipe.recipe)

        saved_meal[u'vegetable'] = saved_recipe[u'vegetable']
        saved_meal[u'protein'] = saved_recipe[u'protein']
        saved_meal[u'starch'] = saved_recipe[u'starch']

        saved_recipe_list.append(saved_meal)

    print saved_recipe_list
    return render_template("saved_recipes.html", recipes=saved_recipe_list)



@app.route("/logout")
def logout():
    """logs user out. clears session """

    session.clear()
    return render_template("index.html")


@app.route("/feedme")
def random_meal():
    """Loads the feedme page and creates a random meal.

    """

    recipe_maker = RecipeMachine()
    recipe_method = session.get('default_setting', "random")

    methods = {"kmeans":recipe_maker.generate_kmeans_recipe,
               "markov":recipe_maker.generate_markov_recipe,
               "random":recipe_maker.generate_random_recipe}

    ingredients = methods[recipe_method]()

    session['meal'] = ingredients
    recipe_method = recipe_method

    return render_template("random_meal.html",vegetable=ingredients['vegetable'], 
                           protein=ingredients['protein'],starch=ingredients['starch'],
                           yummly_image_url="", end_of_url="", recipe_method=recipe_method)


@app.route("/nextmeal")
def next_random_meal():
    """ returns a dictionary for the AJAX query.

    """
    recipe_maker = RecipeMachine()
    
    recipe_method = request.args.get("settings")
    if recipe_method == "kmeans":
        ingredients = recipe_maker.generate_kmeans_recipe()
    elif recipe_method == "markov":
        ingredients = recipe_maker.generate_markov_recipe()
    elif recipe_method=="random":
        ingredients = recipe_maker.generate_random_recipe()

    session['meal'] = ingredients
    recipe_method=recipe_method
    if request.args.get("checked") == "yes":
        try:
            yummly_api_request = requests.get('http://api.yummly.com/v1/api/recipes?_app_id='
                                              +YUMMLY_APP_ID+'&_app_key='
                                              +YUMMLY_APP_KEY+'&q='+str(ingredients['vegetable'])
                                              +'%2C+'+str(ingredients['protein'])+'%2C+'
                                              +str(ingredients['starch'])+'&requirePictures=true')
            json_text = yummly_api_request.text
            json_object = json.loads(json_text)
            try:
                end_of_url = json_object['matches'][0][u'id']
                large_image =  json_object['matches'][0][u'imageUrlsBySize'][u'90'].replace('=s90-c','=s730-e365')
                yummly_rec_name = json_object['matches'][0][u'recipeName']
            except:
                end_of_url = ""
                large_image = "http://upload.wikimedia.org/wikipedia/commons/1/18/Yummly_logo.png"
                yummly_rec_name = "Why don't you try"
        except:
            end_of_url =""
            large_image = ""
            yummly_rec_name =""


    else:
        end_of_url =""
        large_image = ""
        yummly_rec_name =""

    rendering_info = {'vegetable':ingredients['vegetable'], 'protein':ingredients['protein'],
                      'starch':ingredients['starch'],'yummly_image_url':large_image,
                      'end_of_url':end_of_url,'recipe_name':yummly_rec_name,'recipe_method':recipe_method}

    return jsonify(rendering_info)


@app.route('/saveme')
def save_recipe():
    """ saves a meal to the database"""

    saved_meal =  json.dumps(session['meal'])
    model.save_recipe(session['email'],saved_meal)

    return redirect(url_for("random_meal"))

@app.route('/twilio', methods=['GET','POST'])
def hello_custom():
    """ sends kmeans meal text.
    
    Instantiates RecipeMachine class and generates a k-means meal
    that is then sent out via twilio text if the twilio number is
    texted.

    """

    recipe_maker = RecipeMachine()
    ingredients = recipe_maker.generate_kmeans_recipe()
    message = ingredients['vegetable']+" "+ingredients['protein']+" "+ingredients['starch']
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)


@app.route('/api')
def random_api():
    """ k-means meal to API
    
    Instantiates the RecipeMachine class and generates a kmeans meal
    that is rendered at localhost:5000/api
    
    """

    recipe_maker = RecipeMachine()
    ingredients = recipe_maker.generate_kmeans_recipe()

    dict_meal = {"meal":{"protein":ingredients['protein'],
                         "vegetable":ingredients['vegetable'],
                         "starch":ingredients['starch']}}

    api_meal = json.dumps(dict_meal)

    return api_meal


@app.route('/developers')
def developers():
    """Loads informational page on API for interested developers"""
    return render_template("developers.html")


if __name__ == "__main__":
    print "INIT"
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0",port=PORT)

