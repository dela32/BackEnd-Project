from app import create_app
from app.models import db, Customer
import unittest


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(name="test_user", email="test@email.com", phone="555-555-5555", password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "ao@email.com",
            "phone": "123-456-6789",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
    
    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-6789",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])


    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }
        
        with self.app.app_context():
            response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    
    def test_invalid_login(self):
        credentials = {
            "email": "test@email.com",
            "password": "wrongpass"
        }

        with self.app.app_context():
            response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Invalid email or password')
        
     
    def test_update_customer(self):
    # Step 1: Create a customer
        new_customer_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "password": "secret"
        }

        create_response = self.client.post("/customers/", json=new_customer_data)
        self.assertEqual(create_response.status_code, 201)
        customer_id = create_response.get_json()["id"]

        # Step 2: Log in to get a token (adjust this function to return a valid token for that user)
        with self.app.app_context():
            token = self.test_login_customer()
            headers = {'Authorization': f"Bearer {token}"}

            # Step 3: Send PUT request with updated fields
            updated_data = {
                "name": "John Day",
                "email": "john_day@example.com",
                "phone": "987-654-3210",
                "password": "newsecret"
            }

            response = self.client.put(f"/customers/{customer_id}", json=updated_data, headers=headers)

            # Step 4: Check results
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], "John Day")
            self.assertEqual(response.json['email'], "john_day@example.com")
            self.assertEqual(response.json['phone'], "987-654-3210")


            
            
    def test_get_all_customer(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_user')


    def test_delete_customer(self):
        with self.app.app_context():
            token = self.test_login_customer()
            headers = {'Authorization': f"Bearer {token}"}
            response = self.client.delete('/customers/1', headers=headers)
            self.assertEqual(response.status_code, 200)

 