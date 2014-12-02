import cookroulette
import unittest
import model

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app= cookroulette.app.test_client()

    #these test that pages are displayed
    def testHomePage(self):
        response = self.app.get("/")
        self.assertIn("Roulette", response.data)

    def testCreateAccount(self):
        response = self.app.get("/create")
        self.assertIn("Statistical", response.data)

    def testLogin(self):
        response = self.app.get("/login")
        self.assertIn("Log in", response.data)

    def testDevelopers(self):
        response = self.app.get("/developers")
        self.assertIn("JSON", response.data)


if __name__=="__main__":
    unittest.main()
