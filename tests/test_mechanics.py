from app import create_app
from app.models import db, Mechanic
from datetime import datetime
import unittest


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name="test_user", email="test@email.com", phone='123-456-7890', salary=50000)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "123-456-7890",
            "salary": 50000
        }
 
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
    
    def test_invalid_creation(self):
        mechanic_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "salary": 50000
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

     
    def test_update_mechanic(self):
        updated_data = {
            "name": "Updated Name",
            "email": "fake@email.com",
            "phone": "123-456-3333",
            "salary": 60000
        }
        
        response = self.client.put('/mechanics/1', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Name")
    
    def test_get_all_mechanic(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_user')


    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)

    def test_most_tickets_mechanics(self):
        response = self.client.get('/mechanics/most_tickets')
        self.assertEqual(response.status_code, 200)