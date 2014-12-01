import cookroulette
import unittest
import model

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app= cookroulette.app.test_client()

    def testHomePage(self):
        response = self.app.get("/")
        self.assertIn("Roulette", response.data)

    def testCreateAccount(self):
        response = self.app.get("/create")
        self.assertIn("Statistical", response.data)

    def testLogin(self):
        response = self.app.get("/login")
        self.assertIn("Statistical", response.data)



if __name__=="__main__":
    unittest.main()
