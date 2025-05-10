from app import create_app
from app.models import db, Inventory
import unittest


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.inventory = Inventory(name="test_item", price=19.99)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.inventory)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_inventory(self):
        inventory_payload = {
        "name": "Test Item",
        "price": 49.99
    }

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Test Item")
    
    def test_invalid_creation(self):
        inventory_payload = {
            "name": "None"
        }

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])


     
    def test_update_inventory(self):
        updated_data = {
            "name": "Test Item",
            "price": 60.00
        }
        response = self.client.put('/inventory/1', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['price'], 60.00)
    
    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_item')


    def test_delete_inventory(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", response.json["message"])
