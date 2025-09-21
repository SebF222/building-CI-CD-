from app import create_app
from app.models import Mechanics, db
from datetime import date
import unittest 
from app.utils.util import encode_token

class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig') #Create a testing version of the app 
        dob_date = date.fromisoformat('2004-01-01')
        self.mechanic = Mechanics(address='1122 tester street', email='tester@email.com', first_name='tester', DOB=dob_date, last_name='mechanic', password='123', salary='48000') #creating a started user to test things like get login update and delete 
        with self.app.app_context():
            db.drop_all() #removing lingering tables
            db.create_all() #create fresh for another round of testing
            db.session.add(self.mechanic) #adding user to the database
            db.session.commit()
            self.token = encode_token(1) #encoding a token for example test mechanic ^^ that person i created above
        self.client = self.app.test_client() #creates a test client tthat will send request to api

    # test creating a mechanic (needs to start with test)
    def test_create_mechanic(self):
        mechanic_payload = { 
            "address": "1122 tester street", 
            "email": "testmechanic@email.com",
            "first_name": "test_mechanic",
            "DOB": "2004-01-01",
            "last_name": "mechanic",
            "password": "123",
            "salary": "48000"
            }
        
        response = self.client.post('/mechanics', json=mechanic_payload) #sending a test post request to the api by using my test client and using the json body
        print(response.json)
        self.assertEqual(response.status_code, 201) #checking if i got a 201 resposnse stautus code
        self.assertEqual(response.json['first_name'], "test_mechanic" ) #checking to make sure the data that I sent in is apart of the response
        #not working 



    #Negative check: See what happens when we intentionally try and brerak an endpoint
    def test_invalid_create(self):
        mechanic_payload = { 
            "address": "1122 tester street", 
            "first_name": "tester",
            "DOB": "2004-01-01",
            "last_name": "mechanic",
            "password": "123",
            "salary": "48000"
            }
        
        response = self.client.post("/mechanics", json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json) #Membership check that email is in the response json

    def test_get_mechanics(self):
        response = self.client.get("/mechanics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["first_name"], "tester")

    def test_login(self):
        login_creds = {
            "email": "tester@email.com",
            "password": "123"

        }
        
        response = self.client.post('/mechanics/login', json=login_creds)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_delete(self):
        headers = {"Authorization": "Bearer " + self.token} # this is where the token would get stored when deleting

        response = self.client.delete("/mechanics/", headers=headers) #Sending delete request to /mechanics with my authorization headers. ex the one from postman and making one right here
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'mechanic id 1, successfully deleted.') # deleted response and has to be the same way as it is in routes mechanics

    def test_unauthorized_delete(self):

        response = self.client.delete("/mechanics/") #Sending delete request to /mechanics without token
        self.assertEqual(response.status_code, 401) # should get an error response

    def test_update(self): 
        headers = {"Authorization": "Bearer " + self.token}

        update_payload = { 
            "address": "1122 tester street", 
            "email": "updatedmechanic@email.com",
            "first_name": "test_mechanic",
            "DOB": "2004-01-01",
            "last_name": "mechanic",
            "password": "123",
            "salary": "48000"
            }
        
        response = self.client.put("/mechanics/", headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'updatedmechanic@email.com')
    
    def test_update_unauthorized(self):
        update_payload = { 
            "address": "1122 tester street", 
            "email": "updatedmechanic@email.com",
            "first_name": "test_mechanic",
            "DOB": "2004-01-01",
            "last_name": "mechanic",
            "password": "123",
            "salary": "48000"
            }
        
        response = self.client.put("/mechanics/", json=update_payload)
        self.assertEqual(response.status_code, 401)

    def test_update_invalid_token(self):
        headers = {"Authorization": "Bearer invalid_token"}
        
        update_payload = { 
            "address": "1122 tester street", 
            "email": "updatedmechanic@email.com",
            "first_name": "test_mechanic",
            "DOB": "2004-01-01",
            "last_name": "mechanic",
            "password": "123",
            "salary": "48000"
            }
        
        response = self.client.put("/mechanics/", headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 401)

    def test_my_tickets(self):
        headers = {"Authorization": "Bearer " + self.token}
        
        response = self.client.get("/mechanics/my-tickets", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_my_tickets_unauthorized(self):
        response = self.client.get("/mechanics/my-tickets")
        self.assertEqual(response.status_code, 401)

    def test_my_tickets_invalid_token(self):
        headers = {"Authorization": "Bearer invalid_token"}
        
        response = self.client.get("/mechanics/my-tickets", headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_by_tickets(self):
        response = self.client.get("/mechanics/by-tickets")
        self.assertEqual(response.status_code, 200)

    def test_popularity(self):
        response = self.client.get("/mechanics/popularity")
        self.assertEqual(response.status_code, 200)

    