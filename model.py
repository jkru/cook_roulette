from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, ForeignKey, Boolean, Table
from sqlalchemy import Column, Integer, String, DateTime, Text
from passlib.hash import sha256_crypt
import os

SQLITEDB = os.environ.get('SQLITEDB')
engine = create_engine(SQLITEDB, echo=False)
session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False,
                                      autoflush=False))
Base = declarative_base()
Base.query = session.query_property

def connect():
    """ connects to SQLite database"""

    SQLITEDB = os.environ.get('SQLITEDB')
    engine = create_engine(SQLITEDB, echo=True)
    session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit=False,
                                      autoflush=False))
    return session()

#==================User tables with saved meal information==========/
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    settings = Column(String(64), nullable=True)


def create_user_account(email, password, settings="kmeans"):
    """creates a user account.

    Takes in an email and password and checks to see that they're not
    already in the database. Returns messages if this fails. Adds in
    the username and salted+hashed password to the database and
    returns a Successfully Added message once it writes to the
    database.

    """

    if email =="" or password =="":
        return "Please Fill Out All Fields"
    try:
        #get an "all()" and then see if your list is empty
        existing = session.query(User).filter_by(email=email).first()
        if email == existing.email:
            return "User Already Exists."
    except:
        u = User()
        u.email = email
        u.password = password
        u.settings = settings

        session.add(u)
        session.commit()
        return "Successfully Added!"

def login(email_in, password_in):
    """Logs into user account.

    Takes email and password input. Checks if they're valid. Checks
    against the email/password combination in the database. It will
    always return a message to tell the user the status of the log in.

    """

    if email_in =="" or password_in =="":
        print "stops here at no password"
        return "Fill Out All Fields"
    db_return = session.query(User).filter_by(email=email_in).first()
    try:
        db_return.email
        db_pw = db_return.password
        
        if sha256_crypt.verify(password_in,db_pw):
            return "Yay!"
        else:
            return "Incorrect Password"
    except:
        return "Email does not exist"


def change_pw(email_in,newpass):
    """Changes a previously registered user's password.

    Takes in an email and a new password and updates the password in
    the database with the new salted+hashed password.

    """

    u = session.query(User).filter_by(email=email_in).first()
    u.password = newpass
    session.add(u)
    session.commit()
    return "Password Successfully Updated!"
    
class SavedRecipe(Base):

    __tablename__= "savedrecipes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    recipe = Column(String(500), nullable=False)
    rating = Column(String(10))

    user = relationship("User", backref=backref('savedrecipes', order_by=id))

def save_recipe(session_email,saved_meal):
    """Saves a meal to a user account.
    
    Takes in the saved meal, queries by user email, and writes to the
    savedrecipes table.

    """

    user_id = session.query(User).filter_by(email=session_email).first().id
    s = SavedRecipe(user_id=user_id, recipe=saved_meal)
    session.add(s)
    session.commit()


def get_list_saved_recipes(session_email):
    """Returns a list of a user's saved meals.

    Queries the database with a user's email for user_id. Searches for
    the saved meals associated with the user. Returns a list of json
    meals.

    """
    user = session.query(User).filter_by(email=session_email).first()
    all_recipes = session.query(SavedRecipe).filter_by(user_id=user.id).all()

    list_of_recipes = []
    for a_recipe in all_recipes:
        list_of_recipes.append(a_recipe)

    return list_of_recipes


#==================These are 3 tables with 2 association tables==========/

#association table between ingredients and recipes
recipes_ingredients_association = Table('recipes_ingredients', Base.metadata, Column('recipe_id', Integer, ForeignKey('recipes.id')), Column('ingredient_id', Integer, ForeignKey('ingredients.id')))

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    cluster = Column(Integer, nullable=False)

    ingredients = relationship("Ingredient", secondary=recipes_ingredients_association)

#association table between ingredients and types_
ingredients_types_association = Table('ingredients_types', Base.metadata, Column('ingredient_id', Integer, ForeignKey('ingredients.id')), Column('type_id', Integer, ForeignKey('types_.id')))

class Ingredient(Base):
    __tablename__= "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    recipes = relationship("Recipe", secondary=recipes_ingredients_association)
    types_ = relationship("Type_", secondary=ingredients_types_association)

class Type_(Base):
    __tablename__="types_"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    ingredients = relationship("Ingredient", secondary=ingredients_types_association)


def main():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
