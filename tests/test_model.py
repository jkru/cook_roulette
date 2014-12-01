import model
import unittest
import random

class ModelUnitTestCase(unittest.TestCase):

    def testShouldReturnPleaseFillOutAllFields(self):
        """no email test on create_user_account"""
        self.assertEqual(model.create_user_account("","password"),"Please Fill Out All Fields")

    def testShouldReturnPleaseFillOutAllFields2(self):
        """no pw test on create_user_account"""
        self.assertEqual(model.create_user_account("email",""), "Please Fill Out All Fields")
    
    def testShouldReturnUserAlreadyExist(self):
        """tests for inserting a new user"""
        shpw = '$5$rounds=110000$Nuh.QHEOksPjQUyj$2qAPC1KZNNYwRMjUC9UHTgZi0rkEWQkurJZj.R9BzxD'
        self.assertEqual(model.create_user_account("julie@test.com",shpw),"User Already Exists.")

    def testShouldReturnSuccessfullyAdded(self):
        """adds new fake user"""
        fakeemail = "test@"+str(random.randint(0,1000))+str(random.randint(1000,4000))+".com"
        self.assertEqual(model.create_user_account(fakeemail,"testpw"),"Successfully Added!")

    def testShouldReturnFillOUtAllFieldsPw1(self):
        """ test log in where not everything is entered: email"""
        self.assertEqual(model.login("","testpw"),"Fill Out All Fields")

    def testShouldReturnFillOUtAllFieldsPw2(self):
        """ test log in where not everything is entered: PW"""
        self.assertEqual(model.login("testemail",""),"Fill Out All Fields")

    def testShouldReturnYay(self):
        """ test successful log in"""
        password = "julie"
        email = "julie@test.com"
        self.assertEqual(model.login(email,password),"Yay!")

    def testShouldReturnIncorrectPassword(self):
        """test an incorrect password """
        self.assertEqual(model.login("julie@test.com","wrongpw"),"Incorrect Password")

    def testShouldReturnEmailDoesNotExist(self):
        """test with wrong email """
        self.assertEqual(model.login("wrong@email.com","julie"),"Email does not exist")

    def testShouldReturnPasswordSuccessfullyUpdated(self):
        """test email changing function"""
        shpw = '$5$rounds=110000$Nuh.QHEOksPjQUyj$2qAPC1KZNNYwRMjUC9UHTgZi0rkEWQkurJZj.R9BzxD'
        self.assertEqual(model.change_pw("julie@test.com",shpw),"Password Successfully Updated!")
        

#how do you unit test adding entries to a database?

if __name__ =="__main__":
    unittest.main()

